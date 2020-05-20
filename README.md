# koco

`koco` is a library to easily access [`kocohub`](https://github.com/kocohub) datasets. <br>
`kocohub` contains **KO**rean **CO**rpus for natural language processing.

## Installation
> NOTE: The code is tested on `Python 3.6.9`

#### from pypi
```
pip install koco
```

#### from source
```
git clone https://github.com/inmoonlight/koco
cd koco
pip install .
```

## Usage
Using `koco` is similar to [`nlp`](https://github.com/huggingface/nlp). The main methods are:
- `koco.list_datasets()`: list all available datasets and their modes in [`kocohub`](https://github.com/kocohub)
- `koco.load_dataset(dataset_name, mode)`: load dataset in [`kocohub`](https://github.com/kocohub) with data-specific mode

#### example
```python
>>> import koco

>>> koco.list_datasets()
{'korean-hate-speech': ['train_dev', 'unlabeled', 'test'],
 'sae4k': ['train_dev', 'test']}

>>> train_dev = koco.load_dataset('korean-hate-speech', mode='train_dev')
>>> type(train_dev)
dict
>>> train_dev.keys()
dict_keys(['train', 'dev'])
>>> train_dev['train'][33]
{'comments': '2,30대 골빈여자들은 이 기사에 다 모이는건가ㅋㅋㅋㅋ 이래서 여자는 투표권 주면 안된다. 엠넷사전투표나 하고 살아야지 계집들은',
 'contain_gender_bias': True,
 'bias': 'gender',
 'hate': 'hate',
 'news_title': '"“8년째 연애 중”…‘인생술집’ 블락비 유권♥전선혜, 4살차 연상연하 커플"'}
 
 >>> test = koco.load_dataset('korean-hate-speech', mode='test')
 >>> type(test)
 list
 >>> test[33]
 {'comments': '끝낼때도 됐지 요즘같은 분위기엔 성드립 잘못쳤다가 난리. 그동안 잘봤습니다',
 'news_title': '[단독] ‘SNL 코리아’ 공식적인 폐지 확정…아름다운 종료'}
```
