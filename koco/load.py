import logging
import requests

from .patch import download_dataset
from .utils import DOWNLOAD_DIR, exist_dataset
from .korean_hate_speech import load as khs_loader


KOCOHUB = 'https://api.github.com/orgs/kocohub/repos'

logger = logging.getLogger(__name__)


def list_datasets():
    """List datasets in kocohub
    """
    success = False
    while not success:
        r = requests.get(KOCOHUB, params={'per_page': '500'})
        success = r.ok
    return [info['name'] for info in r.json()]


def is_valid_dataset(dataset):
    all_datasets = list_datasets()
    if dataset in all_datasets:
        return True
    else:
        return False


def patch_dataset(dataset, verbose=True):
    """Download and unzip dataset from kocohub

    Args:
        dataset (str): dataset name (e.g., korean-hate-speech)
        verbose (bool): whether to show dataset installation path
    """
    if exist_dataset(dataset):
        if verbose:
            logger.info(f'{dataset} is already installed in {DOWNLOAD_DIR}.')
    else:
        if not is_valid_dataset(dataset):
            raise ValueError(f'{dataset} is not in {list_datasets()}')
        download_dataset(dataset, verbose=verbose)


def load_dataset(dataset, mode, verbose=True):
    patch_dataset(dataset, verbose)

    if dataset == 'korean-hate-speech':
        return khs_loader(mode)
