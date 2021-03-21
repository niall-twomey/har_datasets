import zipfile
from os import makedirs
from os.path import basename
from os.path import exists
from os.path import join
from os.path import split
from os.path import splitext

import requests
from loguru import logger
from tqdm import tqdm

from src.meta import DatasetMeta
from src.utils.loaders import iter_dataset_paths


def unzip_data(zip_path, in_name, out_name):
    if exists(join(zip_path, out_name)):
        return
    with zipfile.ZipFile(join(zip_path, in_name), "r") as fil:
        fil.extractall(zip_path)


def download_and_save(url, path, force=False, chunk_size=2 ** 12):
    response = requests.get(url, stream=True)
    fname = join(path, split(url)[1])
    desc = f"Downloading {fname}..."
    if exists(fname):
        if not force:
            return
    chunks = tqdm(response.iter_content(chunk_size=chunk_size), desc=basename(desc))
    with open(fname, "wb") as fil:
        for chunk in chunks:
            fil.write(chunk)


def download_dataset(dataset_meta_path):
    dataset = DatasetMeta(dataset_meta_path)
    if not exists(dataset.zip_path):
        makedirs(dataset.zip_path)
    for ii, url in enumerate(dataset.meta["download_urls"]):
        logger.info("\t{}/{} {}".format(ii + 1, len(dataset.meta["download_urls"]), url))
        download_and_save(url=url, path=dataset.zip_path)
        zip_name = basename(dataset.meta["download_urls"][0])
        unzip_path = join(dataset.zip_path, splitext(zip_name)[0])
        unzip_data(zip_path=dataset.zip_path, in_name=zip_name, out_name=unzip_path)


def main():
    for dataset_meta_path in iter_dataset_paths():
        logger.info(f"Downloading {dataset_meta_path}")
        download_dataset(dataset_meta_path)


if __name__ == "__main__":
    main()
