# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geqco']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'geqco',
    'version': '0.1.0',
    'description': 'A brief description of your package',
    'long_description': 'None',
    'author': 'Aron Jansen',
    'author_email': 'aronpjansen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
