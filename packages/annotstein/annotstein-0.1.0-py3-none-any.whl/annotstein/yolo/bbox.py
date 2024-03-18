import csv
from io import TextIOWrapper
from itertools import chain
import pathlib
import typing as t
from typing_extensions import Annotated, Self
from pydantic import AnyHttpUrl, BaseModel, Field, ValidationInfo, field_validator
import yaml

from PIL import Image
from annotstein.coco import ops as coco
from annotstein.common import IMAGE_SUFFIXES
from annotstein.yolo.common import xcycwh_to_xywh, xywh_to_xcycwh

SplitSet = t.Union[pathlib.Path, t.List[pathlib.Path]]


class Annotation(BaseModel):
    # Category identifier
    category_id: int

    # Bbox with format [x_center, y_center, width, height]
    bbox: Annotated[t.List[float], Field(min_length=4, max_length=4)]


class AnnotationGroup(BaseModel):
    # Image file concerned by these annotations
    file_name: str

    # Collection of annotations
    annotations: t.List[Annotation]

    @classmethod
    def parse_annotation_file(cls, path: pathlib.Path) -> Self:
        with open(path) as fp:
            reader = csv.reader(fp, delimiter=" ")
            annotations = []
            for row in reader:
                try:
                    annotations.append(
                        Annotation(
                            category_id=int(row[0]),
                            bbox=list(map(float, row[1:])),
                        )
                    )
                except Exception:
                    pass

        return cls(file_name=str(path.resolve()), annotations=annotations)

    def dump(self, fp: TextIOWrapper):
        writer = csv.writer(fp, delimiter=" ")
        for annotation in self.annotations:
            writer.writerow([annotation.category_id, *annotation.bbox])

    def dumps(self):
        res = ""
        for annotation in self.annotations:
            res += " ".join(map(str, [annotation.category_id, *annotation.bbox]))

        return res


class Dataset(BaseModel):
    annotations: t.List[AnnotationGroup]
    names: t.Optional[t.Dict[int, str]]

    @classmethod
    def from_coco(cls, coco_dataset: coco.Dataset) -> Self:
        images_index = {i.id: i for i in coco_dataset.images}
        grouped_by_image: t.Dict[str, t.List[coco.Annotation]] = {i.file_name: [] for i in coco_dataset.images}
        for annotation in coco_dataset.annotations:
            file_name = images_index[annotation.image_id].file_name
            grouped_by_image[file_name].append(annotation)

        yolo_annotations = []
        for file_name, annotation_group in grouped_by_image.items():
            annotations = [Annotation(category_id=a.category_id, bbox=list(xywh_to_xcycwh(a.bbox))) for a in annotation_group]
            yolo_annotations.append(AnnotationGroup(file_name=file_name, annotations=annotations))

        names = {c.id: c.name for c in coco_dataset.categories}

        return cls(annotations=yolo_annotations, names=names)

    def to_coco(self):
        images: t.List[coco.Image] = []
        annotations: t.List[coco.Annotation] = []
        found_categories = set()

        for i, annotation_group in enumerate(self.annotations):
            images.append(coco.Image(
                id=i,
                file_name=annotation_group.file_name,
                height=None,
                width=None,
            ))
            
            for j, annotation in enumerate(annotation_group.annotations):
                annotations.append(coco.Annotation(
                    id=j,
                    image_id=i,
                    category_id=annotation.category_id,
                    bbox=xcycwh_to_xywh(annotation.bbox),
                    segmentation=[[]],
                ))
                found_categories.add(annotation.category_id)

        if self.names is not None:
            categories = [coco.Category(id=i, name=name, supercategory=name) for i, name in self.names.items()]
        else:
            categories = [coco.Category(id=i, name=str(i), supercategory=str(i)) for i in found_categories]

        return coco.Dataset(
            categories=categories,
            images=images,
            annotations=annotations
        )


class TrainTask(BaseModel):
    path: pathlib.Path
    train: SplitSet
    val: SplitSet
    test: t.Optional[SplitSet] = None

    nc: t.Annotated[t.Optional[int], Field(validate_default=True)] = None
    classes: t.Dict[int, str]

    download: t.Optional[AnyHttpUrl] = None

    @field_validator("nc", mode="after")
    @classmethod
    def compute_nc(cls, v: t.Optional[int], info: ValidationInfo) -> int:
        if v is None:
            nc = len(info.data["classes"])
        else:
            assert v == len(info.data["classes"])
            nc = v

        return nc

    @classmethod
    def parse_yaml(cls, path: pathlib.Path) -> "TrainTask":
        with open(path) as fp:
            d = yaml.safe_load(fp)
        return cls.model_validate(d)

    def to_coco(self) -> t.Tuple[coco.Dataset, coco.Dataset, t.Optional[coco.Dataset]]:
        if isinstance(self.train, list):
            train_dss = [parse_split_to_coco(self.path / pt) for pt in self.train]
            train_ds = coco.merge_datasets(*train_dss)
        else:
            train_ds = parse_split_to_coco(self.path / self.train)
        if isinstance(self.val, list):
            val_dss = [parse_split_to_coco(self.path / vt) for vt in self.val]
            val_ds = coco.merge_datasets(*val_dss)
        else:
            val_ds = parse_split_to_coco(self.path / self.val)

        test_ds = None
        if self.test is not None:
            if isinstance(self.test, list):
                test_dss = [parse_split_to_coco(self.path / tt) for tt in self.test]
                test_ds = coco.merge_datasets(*test_dss)
            else:
                test_ds = parse_split_to_coco(self.path / self.test)

        return train_ds, val_ds, test_ds



def parse_split_to_coco(
    path: pathlib.Path,
    names: t.Optional[t.Dict[int, str]] = None,
):

    images_path = path / "images"
    labels_path = path / "labels"
    if not (images_path.exists() and labels_path.exists()):
        images_path = labels_path = path

    images: t.List[coco.Image] = []
    image_index: t.Dict[str, coco.Image] = dict()
    annotations: t.List[coco.Annotation] = []
    found_categories = set()
    for file in chain(*[images_path.glob(f"*{s}") for s in IMAGE_SUFFIXES]):
        image = None
        try:
            width, height = Image.open(file).size
        except Exception:
            continue

        image = coco.Image(
            id=1 + len(images),
            file_name=str(file.resolve()),
            height=height,
            width=width,
        )

        images.append(image)
        image_index[file.stem] = image

    for file in labels_path.glob("*.txt"):
        if file.stem not in image_index:
            continue

        image = image_index[file.stem]
        try:
            yolo_annotations = AnnotationGroup.parse_annotation_file(file)
        except Exception:
            continue

        coco_annotations = []
        try:
            for annotation in yolo_annotations.annotations:
                bbox = xywh_to_xcycwh(annotation.bbox)
                coco_annotations.append(
                    coco.Annotation(
                        id=len(annotations),
                        image_id=image.id,
                        category_id=annotation.category_id,
                        area=bbox[2] * bbox[3],
                        iscrowd=0,
                        bbox=list(bbox),
                        segmentation=[],
                        attributes=dict(),
                    )
                )

                found_categories.add(annotation.category_id)
        except Exception:
            pass

        annotations.extend(coco_annotations)

    if names is not None:
        categories = [coco.Category(id=i, supercategory=name, name=name) for i, name in names.items()]
    else:
        categories = [coco.Category(id=i, supercategory=str(i), name=str(i)) for i in found_categories]

    return coco.Dataset(
        images=images,
        annotations=annotations,
        categories=categories,
    )


class SplitsDataset(BaseModel):
    train_annotations: t.List[AnnotationGroup]
    val_annotations: t.List[AnnotationGroup]
    test_annotations: t.Optional[AnnotationGroup] = None

    def to_coco(self):
        datasets: t.List[coco.Dataset] = []
        return datasets
