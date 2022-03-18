#!/usr/bin/env python
from setuptools import setup, find_packages
from imp import load_source
from os import path as op
import io

__version__ = load_source("version", "version.py").__version__

here = op.abspath(op.dirname(__file__))


with open(op.join(here, "README.md")) as fp:
    long_description = fp.read()

# get the dependencies and installs
with io.open(op.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [x.strip().replace("git+", "") for x in all_reqs if "git+" not in x]

setup(
    name="spherical2images",
    author="Rub21",
    author_email="ruben@developmentseed.org",
    version=__version__,
    description="Script to convert spherical images into flat splitted images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/developmentseed/spherical2images",
    keywords="",
    entry_points={
        "console_scripts": [
            "get_mapillary_points = spherical2images.get_mapillary_points:main",
            "clip_mapillary_pano = spherical2images.clip_mapillary_pano:main",
        ]
    },
    packages=find_packages(exclude=["docs", "tests*"]),
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
)
