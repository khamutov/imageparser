import requests
import urllib.request
from tqdm import tqdm

def __get(url:str):
    return requests.get(url=url).json().get("data")

def image_parser():
    counter = 0
    import os
    f = open("url")
    for lines in f.readlines():
        line = lines.split(" ")
        if not os.path.isdir(line[1]):
            os.makedirs(line[1])
        for images in __get(line[0]):
            for count in tqdm(range(len(images.get("images")))):
                if os.path.isfile(line[1] +"\\" + str(counter) + ".jpg"):
                    counter += 1
                    continue
                urllib.request.urlretrieve(images.get("images")[count],
                                            line[1] +"\\" + str(counter) + ".jpg")
                counter += 1

image_parser()