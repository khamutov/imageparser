import requests
import urllib.request

def __get(url:str):
    return requests.get(url=url).json().get("data")

def image_parser():
    counter = 0
    import os
    f = open("url")
    for lines in f.readlines():
        line = lines.split(" ")
        os.makedirs(line[1])
        for images in __get(line[0]):
            for image in images.get("images"):
                urllib.request.urlretrieve(image,
                                           line[1] +"\\" + str(counter) + ".jpg")
                counter+=1