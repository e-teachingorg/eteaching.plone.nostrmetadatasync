# -*- coding: utf-8 -*-

from setuptools import find_namespace_packages
from setuptools import setup
from pathlib import Path
import re

init_py = Path(
    "src/eteaching/plone/nostrmetadatasync/__init__.py"
).read_text(encoding="utf-8")

match = re.search(
    r'^__version__ = ["\']([^"\']+)["\']',
    init_py,
    re.MULTILINE,
)

version = match.group(1)

long_description = open("README.md").read()

setup(
    name="eteaching.plone.nostrmetadatasync",
    version="1.0.0b5",
    description="Nostr integration for Plone 6.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: 6.2",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="CMS Plone Python",
    author="Markus Schmidt",
    author_email="m.schmidt@iwm-tuebingen.de",
    url="https://github.com/e-teachingorg/eteaching.plone.nostrmetadatasync",
    project_urls={
        "Homepage": "https://github.com/e-teachingorg/eteaching.plone.nostrmetadatasync",
        "PyPI": "https://pypi.org/project/eteaching.plone.nostrmetadatasync",
        "Source": "https://github.com/e-teachingorg/eteaching.plone.nostrmetadatasync",
        "Tracker": "https://github.com/e-teachingorg/eteaching.plone.nostrmetadatasync/issues",
    },
    license="GPL-2.0-only",
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "Products.CMFPlone",
        "plone.api",
        "pynostr",
        "z3c.jbot",
    ],
    extras_require={
        "test": [
            "horse-with-no-namespace",
            "plone.app.testing",
            "plone.classicui",
            "plone.restapi[test]",
            "pytest",
            "pytest-cov",
            "pytest-plone>=1.0.0a2",
        ],
        "release": [
            "zest.releaser[recommended]",
            "zestreleaser.towncrier",
            "zest.pocompile",
        ],
    },
    entry_points="""
    [plone.autoinclude.plugin]
    target = plone
    """,
)
