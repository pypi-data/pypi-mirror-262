# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['simpleaiosqlite']
setup_kwargs = {
    'name': 'simpleaiosqlite',
    'version': '0.0.2',
    'description': 'асинхронная версия',
    'long_description': '',
    'author': 'yayaya',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
