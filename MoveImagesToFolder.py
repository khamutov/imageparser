# coding=utf-8
import shutil
from pathlib import Path

from tqdm import tqdm

valid_pct=0.2
train_pct=0.2

dir_name= ["train","test","validation"]

class MoveImages:
    def __init__(self,array_images:[],array_dirs : [] = dir_name):
        self.__array_images = array_images
        self.__array_dirs = array_dirs

    def __move_images_to_folder(self,path_src: Path, path_dist: Path, dir_name: str, images: []):
        for image in tqdm(images, desc="move images to {} len {}".format(dir_name, len(images))):
            if not path_dist.joinpath(image).is_file():
                shutil.copyfile(src=path_src.joinpath(image), dst=path_dist.joinpath(image))

    def move_images(self, path: Path):
        validation_idx = round(len(self.__array_images, ) * valid_pct)
        test_idx = round(validation_idx + len(self.__array_images) * train_pct)
        for dir in tqdm(self.__array_dirs,desc="Move files"):
            self.__move_images_to_folder(path, path.joinpath(dir), dir, self.__array_images[:validation_idx])
            self.__move_images_to_folder(path, path.joinpath(dir), dir, self.__array_images[validation_idx: test_idx])
            self.__move_images_to_folder(path, path.joinpath(dir), dir, self.__array_images[test_idx:])