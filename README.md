# Sharder [![Build Status](https://travis-ci.org/msempere/sharder.svg?branch=master)] (http://travis-ci.org/msempere/sharder)

Tiny sharding for Redis

## Setup:
```
pip install -r requirements.txt
```
```
python setup.py install
```
## Supported hash methods:
 * CRC32
 * MD5
 * SHA1

## Usage:
```python
>>> from sharder import Sharder, HashMethod
>>> servers = [
                {'name': 'local-server-1', 'host': '127.0.0.1', 'port': 6379, 'db': 0},
                {'name': 'local-server-2', 'host': '127.0.0.1', 'port': 6380, 'db': 0}
              ]
>>> sharder = Sharder(servers, hash_method=CRC32)
>>> sharder.set('a_key','a_value')
>>> sharder.keys()
{'local-server-2': ['a_key'], 'local-server-1': []} 

>>> sharder.keys(numeriq=True)
{'local-server-2': 1, 'local-server-1': 0}

>>> sharder.get('a_key')
'a_value'
```
