# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="j2yaml",
    version="0.1.0",
    description="Jinja2-templates inside YAML-files.",
    license="GPLv3",
    author="tombayo",
    author_email="pypi@tombayo.com",
    url="https://github.com/tombayo/j2yaml",
    package_dir={"": "j2yaml"},
    packages=find_packages(where="j2yaml"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=['Jinja2==3.1.3','MarkupSafe==2.1.5','PyYAML==6.0.1'],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"]
    },
    python_requires=">=3.8"
)
