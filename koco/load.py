import logging
import importlib
import requests

from .patch import download_dataset
from .utils import dataset_to_module_name, DOWNLOAD_DIR, exist_dataset

KOCOHUB = 'https://api.github.com/orgs/kocohub/repos'

logger = logging.getLogger(__name__)


def list_datasets():
    """List datasets in kocohub

    Returns:
        dataset (dict): dataset name and its available mode
            {
                'korean-hate-speech': ['labeled', 'unlabeled', 'testset'],
                ...
            }
    """
    success = False
    while not success:
        r = requests.get(KOCOHUB, params={'per_page': '500'})  # TODO: if dataset > 500, then fix
        success = r.ok
    dataset_names = [info['name'] for info in r.json()]

    dataset = dict()
    for d_name in dataset_names:
        module_name = dataset_to_module_name(d_name)
        modes = importlib.import_module(f'koco.{module_name}').AVAILABLE_MODE
        dataset[d_name] = list(modes.keys())
    return dataset


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

    # NOTE: module name should be same with dataset name
    module_name = dataset_to_module_name(dataset)
    loader = importlib.import_module(f'koco.{module_name}').load
    return loader(mode)
