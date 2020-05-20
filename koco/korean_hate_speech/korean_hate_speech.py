"""Load kocohub/korean-hate-speech dataset

The dataset contains
    - labeled train, dev set
    - label-removed test set
    - unlabeled data
    - news title for each train, dev, test, and unlabeled corpus

For more information, see https://github.com/kocohub/korean-hate-speech
"""

import pandas as pd

from ..utils import DOWNLOAD_DIR, read_lines

dataset = 'korean-hate-speech'
datadir = f'{DOWNLOAD_DIR}/{dataset}-master'


def _load_labeled():
    """Load labeled train, dev set

    Returns:
        labeled_dataset (dict):
            {
                'train': [
                             {
                                  'comments': str,
                                  'contain_gender_bias: bool,
                                  'bias': str,
                                  'hate': str,
                                  'news_title': str,
                             },
                             ...
                         ]

                'dev': [
                           {
                                'comments': str,
                                'contain_gender_bias: bool,
                                'bias': str,
                                'hate': str,
                                'news_title': str,
                           },
                           ...
                       ]
            }
    """
    train = pd.read_csv(f'{datadir}/labeled/train.tsv', sep='\t')
    dev = pd.read_csv(f'{datadir}/labeled/dev.tsv', sep='\t')
    train_news_title = read_lines(f'{datadir}/news_title/train.news_title.txt')
    dev_news_title = read_lines(f'{datadir}/news_title/dev.news_title.txt')
    assert train.shape[0] == len(train_news_title)
    assert dev.shape[0] == len(dev_news_title)

    train['news_title'] = train_news_title
    dev['news_title'] = dev_news_title

    labeled_dataset = dict()
    labeled_dataset['train'] = train.to_dict('records')
    labeled_dataset['dev'] = dev.to_dict('records')
    return labeled_dataset


def _load_unlabeled():
    """Load unlabeled corpus

    Returns:
        unlabeled_dataset (list of dict):
            [
                {
                    'comments': str,
                    'news_title': str,
                }, ...
            ]
    """
    unlabeled_comments = []
    unlabeled_news_titles = []
    for i in range(5):
        unlabeled_comments_tmp = read_lines(f'{datadir}/unlabeled/unlabeled_comments_{i}.txt')
        unlabeled_comments.extend(unlabeled_comments_tmp)
        unlabeled_news_title_tmp = read_lines(f'{datadir}/news_title/unlabeled_comments.news_title_{i}.txt')
        unlabeled_news_titles.extend(unlabeled_news_title_tmp)
    assert len(unlabeled_comments) == len(unlabeled_news_titles)

    # TODO: multi-processing
    unlabeled_dataset = []
    for c, nt in zip(unlabeled_comments, unlabeled_news_titles):
        d = {'comments': c, 'news_title': nt}
        unlabeled_dataset.append(d)
    return unlabeled_dataset


def _load_testset():
    """Load testset

    Note that testset doesn't contain any labels

    Returns:
        testset (list of dict):
            [
                {
                    'comments': str,
                    'news_title': str,
                }, ...
            ]
    """
    test = pd.read_csv(f'{datadir}/test.no_label.tsv', sep='\t')
    test_news_title = read_lines(f'{datadir}/news_title/test.news_title.txt')
    assert test.shape[0] == len(test_news_title)

    test['news_title'] = test_news_title
    return test.to_dict('records')


AVAILABLE_MODE = {
    'labeled': _load_labeled,
    'unlabeled': _load_unlabeled,
    'testset': _load_testset
}


def load(mode):
    """Load korean-hate-speech dataset

    Args:
        mode (str): Either labeled, unlabeld, or testset
    """
    if mode not in AVAILABLE_MODE:
        raise ValueError(f'Invalid mode. Try one of {AVAILABLE_MODE.keys()}')
    return AVAILABLE_MODE[mode]()
