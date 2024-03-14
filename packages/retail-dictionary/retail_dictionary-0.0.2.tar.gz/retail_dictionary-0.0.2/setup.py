from setuptools import setup, find_packages
import codecs
import os
import re
import pandas
import string
import warnings
import spacy
from pkg_resources import resource_filename
filepath = resource_filename('retail_dictionary', 'rd.xlsx')
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
VERSION = '0.0.2'
DESCRIPTION = 'Retail Dictionary where you can find meaning of Retail terms'
LONG_DESCRIPTION = 'Retail Dictionary where you can find meaning of Retail terms'


setup(
    name="retail_dictionary",
    version=VERSION,
    author="Marcel Tino",
    author_email="<marceltino92@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    package_data={'':[filepath]},
    include_package_data=True,
    install_requires=['pandas','spacy'],
    keywords=['retail','retailterms','retaildictionary'])
