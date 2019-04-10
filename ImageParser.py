import csv
import json
import urllib.request
from pathlib import Path
from tqdm import tqdm


def __make_dir(path: Path):
    if not path.is_dir():
        path.mkdir()


def __save_images(url: str, path: Path):
    for images in __get_response(url):
        for count in tqdm(range(len(images.get("images")))):
            last_segment = __get_last_segment(images.get("images")[count])
            if path.joinpath(last_segment).is_file():
                continue
            urllib.request.urlretrieve(images.get("images")[count],
                                       path.joinpath(last_segment))


def __get_response(url: str) -> json:
    return json.load(urllib.request.urlopen(url=url)).get("data")


def __get_last_segment(url: str) -> str:
    return str(Path(url).name.split("?")[0])


def __csv_reader(file_name: str):
    file = Path(file_name)
    if not file.is_file():
        raise Exception("file not found")

    with open(file, "r") as f:
        reader = csv.reader(f, delimiter=';')
        for line in reader:
            path = Path(line[1])
            __make_dir(path)
            __save_images(line[0], path)


def image_parser(file_name: str = "url.csv"):
    file = Path(file_name)
    if not file.is_file():
        raise Exception("file not found")

    with open(file, "r") as f:
        reader = csv.reader(f, delimiter=';')
        for line in reader:
            path = Path(line[1])
            __make_dir(path)
            __save_images(line[0], path)


if __name__ == "__main__":
    image_parser()
