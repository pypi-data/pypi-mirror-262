# Django DF Documents

Module for serving markdown documents

## Installation:

- Install the package

```
pip install django-df-documents
```


- Include default `INSTALLED_APPS` from `df_documents.defaults` to your `settings.py`

```python
from df_documents.defaults import DF_DOCUMENTS_INSTALLED_APPS

INSTALLED_APPS = [
    ...
    *DF_DOCUMENTS_INSTALLED_APPS,
    ...
]

```


## Development

Installing dev requirements:

```
pip install -e .[test]
```

Installing pre-commit hook:

```
pre-commit install
```

Running tests:

```
pytest
```
