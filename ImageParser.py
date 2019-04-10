import csv
import json
import urllib.request
from pathlib import Path
from tqdm import tqdm


def __make_dir(path: Path):
    if not path.is_dir():
        path.mkdir()


def __save_images(url: str, path: Path):
    resp = __get_response(url)
    for images_count in tqdm(range(len(resp)), desc='load categories      '):
        for count_image in tqdm(range(len(resp[images_count].get("images"))), desc='load images     '):
            last_segment = __get_last_segment(resp[images_count].get("images")[count_image])
            if path.joinpath(last_segment).is_file():
                continue
            urllib.request.urlretrieve(resp[images_count].get("images")[count_image],
                                       path.joinpath(last_segment))


def __get_response(url: str) -> json:
    return json.load(urllib.request.urlopen(url=url)).get("data")


def __get_last_segment(url: str) -> str:
    return str(Path(url).name.split("?")[0])


def image_parser(file_name: str = "url.csv"):
    file = Path(file_name)
    if not file.is_file():
        raise Exception("file not found")

    with open(file, "r") as f:
        reader = csv.DictReader(f, ["url", "dir_name"], delimiter=";")
        for row in reader:
            path = Path(row["dir_name"])
            __make_dir(path)
            __save_images(row["url"], path)


if __name__ == "__main__":
    image_parser()
