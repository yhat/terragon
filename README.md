# terragon
"Sub-fork" of the [`cloud`](https://pypi.python.org/pypi/cloud/2.3.1) package's 
cloudpickle.

## Install
```bash
$ pip install terragon
```

## Use
Same-ish as pickle
```python
>>> import terragon
>>> terragon.dumps({ "x": range(10) })
'\x80\x02}q\x00U\x01xq\x01]q\x02(K\x00K\x01K\x02K\x03K\x04K\x05K\x06K\x07K\x08K\tes.'
```
