# coding=utf-8
import os
import shutil
from pathlib import Path

from tqdm import tqdm

valid_pct = 0.2
train_pct = 0.2

dir_name = ["train", "test", "validation"]


class MoveImages:

    def __collect_files(self, path_from: Path):
        files = {}

        # r=root, d=directories, f = files
        for r, d, f in os.walk(path_from):
            tempF = []
            for file in f:
                tempF.append(os.path.join(r, file))
            files[r] = tempF
        return files

    def __move_images_to_folder(self,path_from: Path, path_dist: Path, dir_name: str, images: []):
        for image in tqdm(images, desc="move images to {} len {}".format(dir_name, len(images))):
            path = Path(path_dist)
            if not path.is_file():
                if not path_dist.is_dir():
                    os.mkdir(path_dist)
                shutil.copyfile(src=image,
                                dst=path_dist.joinpath("".join(f for f in image.split("\\")[1:])))

    def move_images(self, path_from: Path, path_to: Path):
        image_dict = self.__array_images = self.__collect_files(path_from)
        for i in tqdm(image_dict,desc="Copy files"):
            self.__array_images = image_dict[i]
            if len(self.__array_images) == 0:
                continue
            validation_idx = round(len(self.__array_images, ) * valid_pct)
            test_idx = round(validation_idx + len(self.__array_images) * train_pct)
            self.__move_images_to_folder(path_from, path_to.joinpath("validation"), "validation", self.__array_images[:validation_idx])
            self.__move_images_to_folder(path_from, path_to.joinpath("test"), "test", self.__array_images[validation_idx: test_idx])
            self.__move_images_to_folder(path_from, path_to.joinpath("train"), "train", self.__array_images[test_idx:])
