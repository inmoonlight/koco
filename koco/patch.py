import logging
import zipfile

import wget

from .utils import DOWNLOAD_DIR, make_dirs

baseurl = 'https://codeload.github.com/kocohub/{}/zip/master'

logger = logging.getLogger(__name__)


def download_dataset(dataset, verbose=True):
    make_dirs(DOWNLOAD_DIR)
    url = baseurl.format(dataset)
    wget.download(url, f'{DOWNLOAD_DIR}/{dataset}.zip')
    unzip(f'{DOWNLOAD_DIR}/{dataset}.zip')
    if verbose:
        logger.info(f'Dataset {dataset} downloaded to {DOWNLOAD_DIR}.')


def unzip(zippath):
    with zipfile.ZipFile(zippath) as z:
        z.extractall(DOWNLOAD_DIR)
