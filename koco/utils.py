import os

DOWNLOAD_DIR = f'{os.path.expanduser("~")}/.kocohub'


def exist_dataset(dataset):
    return os.path.exists(f'{DOWNLOAD_DIR}/{dataset}-master')


def exist_dir(dirpath):
    return os.path.exists(dirpath)


def make_dirs(dirpath):
    if not exist_dir(dirpath):
        os.makedirs(dirpath)


def read_lines(path):
    return [line.rstrip('\n') for line in open(path)]
