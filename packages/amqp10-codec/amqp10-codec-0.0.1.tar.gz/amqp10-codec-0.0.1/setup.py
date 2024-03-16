# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amqp10_codec']

package_data = \
{'': ['*']}

install_requires = \
['cython>=3.0.8,<4.0.0']

setup_kwargs = {
    'name': 'amqp10-codec',
    'version': '0.0.1',
    'description': '',
    'long_description': '# AMQP 1.0 Message Format\n\n![testing](https://github.com/effedib/ParserAMQP/actions/workflows/test.yml/badge.svg)\n\nThe library is for encode and decode AMQP 1.0 message format. \n\n### Use Poetry\n- create your virtual environment with `python -m venv venv`\n- activate your virtual environment with `source venv/bin/activate`\n- install poetry with `pip install poetry isort black pytest`\n- install dependencies with `poetry install`\n- run tests with `poetry run pytest`\n\n### Contributing to the project\nFormat and sort the code with \n- `poetry run black amqp10_codec tests`  \n- `poetry run isort amqp10_codec tests`.\n\n\n',
    'author': 'Gabriele Santomaggio',
    'author_email': 'G.santomaggio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
