#!/usr/bin/env python
# from setuptools import setup  # Using distutils, seems to be more flexible with build
from distutils.core import setup
import weatherca

LONG_DESCRIPTION = open('README.md').read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

KEYWORDS = 'Python Weather Clients'


requires = [
    'requests>=2.25.0,<3.0.0',
    'xmltodict>=0.12.0,<1.0.0',
]


setup(
    name='weatherca',
    include_package_data=True,
    version=weatherca.__version__,
    description=KEYWORDS,
    long_description=LONG_DESCRIPTION,
    author='radzhome',
    author_email='radek@radtek.ca',
    download_url='https://github.com/Postmedia-Digital/python-weather-canada',
    url='https://github.com/Postmedia-Digital/python-weather-canada',
    packages=['weatherca', 'weatherca.images', 'weatherca.data', ],

    package_dir={'weatherca': 'weatherca'},
    platforms=['Platform Independent'],
    license='BSD',
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    install_requires=requires,
)
