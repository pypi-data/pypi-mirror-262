# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['morphdb_utils']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'betterproto[compiler]>=2.0.0b5,<3.0.0',
 'boto3>=1.26.80,<2.0.0',
 'grpcio-tools>=1.54.2,<2.0.0',
 'grpcio>=1.54.2,<2.0.0',
 'line-profiler>=4.1.2,<5.0.0',
 'openpyxl>=3.1.1,<4.0.0',
 'pandas>=2.1.3,<3.0.0',
 'plotly>=5.18.0,<6.0.0',
 'psycopg2-binary>=2.9.6,<3.0.0',
 'pydantic>=2.5.3,<3.0.0',
 'pypika>=0.48.9,<0.49.0',
 'requests>=2.28.2,<3.0.0',
 'seaborn>=0.13.2,<0.14.0',
 'sqlparse>=0.4.4,<0.5.0',
 'twine>=5.0.0,<6.0.0',
 'urllib3==1.26.18',
 'wheel>=0.43.0,<0.44.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'morphdb-utils',
    'version': '0.1.0',
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
