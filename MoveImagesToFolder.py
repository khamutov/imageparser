# coding=utf-8
import os
import shutil
from pathlib import Path

from tqdm import tqdm

valid_pct = 0.2
train_pct = 0.2

dir_name = ["train", "test", "validation"]


class MoveImages:
    @classmethod
    def __collect_files(cls, path_from: Path):
        files = {}

        # r=root, d=directories, f = files
        for r, d, f in os.walk(path_from):
            tempF = []
            for file in f:
                tempF.append(os.path.join(r, file))
            files[r] = tempF
        return files

    @classmethod
    def __move_images_to_folder(cls, path_dist: Path, dir_name: str, images: []):
        for image in tqdm(images, desc="move images to {} len {}".format(dir_name, len(images))):
            image_parts = list(Path(image).parts)
            label = image_parts[1:-1]
            image_name = image_parts[-1]
            path = Path(path_dist) / Path("/".join(label))
            if not path.is_file():
                if not path.is_dir():
                    path.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src=image,
                                dst=path.joinpath(image_name))

    @classmethod
    def move_images(cls, path_from: Path, path_to: Path):
        image_dict = cls.__array_images = cls.__collect_files(path_from)
        for i in tqdm(image_dict, desc="Copy files"):
            cls.__array_images = image_dict[i]
            if len(cls.__array_images) == 0:
                continue
            validation_idx = round(len(cls.__array_images, ) * valid_pct)
            test_idx = round(validation_idx + len(cls.__array_images) * train_pct)
            cls.__move_images_to_folder(path_to.joinpath("validation"), "validation", cls.__array_images[:validation_idx])
            cls.__move_images_to_folder(path_to.joinpath("test"), "test", cls.__array_images[validation_idx: test_idx])
            cls.__move_images_to_folder(path_to.joinpath("train"), "train", cls.__array_images[test_idx:])
