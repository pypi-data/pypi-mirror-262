# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tabulate_django']

package_data = \
{'': ['*']}

install_requires = \
['Django', 'tabulate']

setup_kwargs = {
    'name': 'tabulate-django',
    'version': '0.1.0',
    'description': 'An application to pretty print Django QuerySets and Model instances in the shell',
    'long_description': None,
    'author': 'James Hardy',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>2.7',
}


setup(**setup_kwargs)
