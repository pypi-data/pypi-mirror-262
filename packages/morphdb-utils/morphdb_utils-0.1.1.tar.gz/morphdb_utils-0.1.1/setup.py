# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['morphdb_utils']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3,<2.0.0',
 'requests>=2.31.0,<3.0.0',
 'urllib3==2.1.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'morphdb-utils',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Morphdb Utils\n\nMorph enables everyone to process data with SQL and Python using AI assist and auto-scale database powered by PostgreSQL.\n',
    'author': 'shibatanaoto',
    'author_email': 'naoto.shibata510@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
