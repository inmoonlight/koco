"""Load kocohub/sae4k (Structured Argument Extraction for Korean) dataset

The dataset contains
    - 50,837 utterances of input, output, and label
    - total number of labels is 6

For more information, see https://github.com/kocohub/sae4k
"""

import pandas as pd
import random

from ..utils import DOWNLOAD_DIR

dataset = 'sae4k'
datadir = f'{DOWNLOAD_DIR}/{dataset}-master'


def _load_and_split(split='9:1', seed=42):
    """Load entire dataset (total: 50,837)

    Args:
        split (str): ${train}:${dev}
        seed (int): random seed

    Returns:
        trainset (DataFrame[label, input, output]):
            2   이번 주에 기온변화가 가장 큰 요일을 알려줘  이번 주 기온변화 가장 큰 요일
        devset (DataFrame[label, input, output]):
            0   공기청정기 켜져있니 공기청정기 켜졌는지
        testset (DataFrame[label, input, output]):
            4   이번주 목요일 할머니 칠순잔치 일정 추가해줘 이번주 목요일 할머니 칠순잔치 일정 추가하기
    """
    d = pd.read_csv(f'{datadir}/{dataset}_v2.txt', sep='\t', header=None)
    d.columns = ['label', 'input', 'output']

    # testset fixed to the last 10%
    total = d.shape[0]
    test = d.iloc[-(total // 10):]
    # split train, dev
    train_dev = d.iloc[:-(total // 10)]
    shuffled_idx = list(train_dev.index)
    random.seed(seed)
    random.shuffle(shuffled_idx)
    t_ratio, d_ratio = split.split(':')
    split_at = len(shuffled_idx) // (int(t_ratio) + int(d_ratio)) * int(t_ratio)
    train = train_dev.iloc[:split_at]
    dev = train_dev.iloc[split_at:]

    return train, dev, test


def _load_train_dev(split='9:1', seed=42):
    """Load train, dev set

    Args:
        split (str): ${train}:${dev}
        seed (int): random seed

    Returns:
        dataset (dict):
            {
                'train': [
                             {
                                'input': str,
                                'output': str,
                                'label': int
                             },
                             ...

                         ],
                'dev': [
                            {
                                'input': str,
                                'output': str,
                                'label': int
                            },
                                              ...
                       ]
            }
    """
    train, dev, _ = _load_and_split(split, seed)
    dataset = dict()
    dataset['train'] = train.to_dict('records')
    dataset['dev'] = dev.to_dict('records')
    return dataset


def _load_test():
    """Load testset

    Returns:
        testset (list of dict):
            [
                {
                    'input': str,
                    'output': str,
                    'label': int
                },
                ...
            ]
    """
    _, _, test = _load_and_split()
    return test.to_dict('records')


AVAILABLE_MODE = {
    'train_dev': _load_train_dev,
    'test': _load_test
}


def load(mode, split='9:1', seed=42):
    """Load sae4k dataset

    Args:
        mode (str): Either train_dev or test
        split (str): ${train}:${dev}
        seed (int): random seed
    """
    if mode not in AVAILABLE_MODE:
        raise ValueError(f'Invalid mode. Try one of {AVAILABLE_MODE.keys()}')
    return AVAILABLE_MODE[mode]()  # TODO: levarge split and seed
