import csv
import json
import shutil
import urllib.request
import os
from pathlib import Path
from tqdm import tqdm


class ImageParser:
    def __get_images_array(self, url: str) -> []:
        array = []
        for item in self.__get_response(url):
            for image in item.get("images"):
                array.append(image)
        return array

    def __move_images_to_folder(self, path: Path, arr: [], file="categories.csv"):
        with open(file, "r") as f:
            reader = csv.DictReader(f, ["section", "percent"], delimiter=";")
            self.last = int(0)
            for row in reader:
                for image in tqdm(arr[self.last:
                                      round(self.last + round(len(arr) * int(row.get("percent")))/100)], desc= "move images:"):
                    shutil.move(src=path.joinpath(image),
                                dst=path.joinpath(row.get("section")).joinpath(image))
                self.last = round(self.last + round(len(arr) * int(row.get("percent")))/100)

    def __save_images(self, url: str, dir_name: str, path: Path):
        for image in tqdm(self.__get_images_array(url), desc=dir_name + ": Download images"):
            last_segment = self.__get_last_segment(image)
            if not path.joinpath(last_segment).is_file():
                urllib.request.urlretrieve(image,
                                           str(path.joinpath(last_segment)))

        self.__move_images_to_folder(path, [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])


    def __get_response(self, url: str) -> str:
        return json.load(urllib.request.urlopen(url=url)).get("data")

    def __get_last_segment(self, url: str) -> str:
        return str(Path(url).name.split("?")[0])

    def image_parser(self, file_name: str = "url.csv"):
        file = Path(file_name)
        if not file.is_file():
            raise Exception("file not found")

        with open(file, "r") as f:
            reader = csv.DictReader(f, ["url", "dir_name"], delimiter=";")
            for row in tqdm(reader, desc="Done: "):
                path = Path(row["dir_name"])
                path.mkdir(parents=True, exist_ok=True)
                path.joinpath("train").mkdir(parents=True, exist_ok=True)
                path.joinpath("validation").mkdir(parents=True, exist_ok=True)
                path.joinpath("test").mkdir(parents=True, exist_ok=True)
                self.__save_images(row["url"], row["dir_name"], path)


if __name__ == "__main__":
    ImageParser().image_parser()
