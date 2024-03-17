# dict-toolkit

## reference data
https://github.com/skywind3000/ECDICT

## install and use
```shell
pip install dict-toolkit
```

```python
from dict_toolkit.extensions.query_agent import auto_query
auto_query('hello')
```

## development
#### venv
create venv
```shell
python -m venv venv
```

source venv
```shell
source venv/bin/activate
```

deactivate venv
```shell
deactivate
```

#### package
```shell
python setup.py sdist bdist_wheel
```



