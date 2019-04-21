# coding=utf-8
from pathlib import Path

def make_dirs(path: Path):
    path.joinpath("train").mkdir(parents=True, exist_ok=True)
    path.joinpath("validation").mkdir(parents=True, exist_ok=True)
    path.joinpath("test").mkdir(parents=True, exist_ok=True)