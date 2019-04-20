# coding=utf-8
import os
import shutil
from pathlib import Path

from tqdm import tqdm

valid_pct = 0.2
train_pct = 0.2

dir_name = ["train", "test", "validation"]


class MoveImages:

    def __collect_files(self, path_dist: Path):
        return [f for f in os.listdir(path_dist) if os.path.isfile(os.path.join(path_dist, f))]

    def __move_images_to_folder(self, path_dist: Path, dir_name: str, images: []):
        for image in tqdm(images, desc="move images to {} len {}".format(dir_name, len(images))):
            path = Path(image)
            if not path.is_file():
                if not path_dist.is_dir():
                    os.mkdir(path_dist)
                shutil.copyfile(src=image,
                                dst=path_dist.joinpath(image))

    def move_images(self, path_from: Path, path_to: Path):
        files = []

        # r=root, d=directories, f = files
        for r, d, f in os.walk(path_from):
            for file in f:
                files.append(os.path.join(r, file))

        self.__array_images = self.__collect_files(path_from)
        validation_idx = round(len(self.__array_images, ) * valid_pct)
        test_idx = round(validation_idx + len(self.__array_images) * train_pct)
        self.__move_images_to_folder(path_to.joinpath("validation"), "validation", files[:validation_idx])
        self.__move_images_to_folder(path_to.joinpath("test"), "test", files[validation_idx: test_idx])
        self.__move_images_to_folder(path_to.joinpath("train"), "train", files[test_idx:])
