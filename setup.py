#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")


requirements = [
    "RelevanceAI[notebook]",
    "vectorhub[sentence-transformers]>=1.8.3",
    "jupyter",
    "typing_extensions",
]

notebook_test_requirements = [
    "matplotlib",   ## Needed for Vectorhub Clip2Vec in non-Colab env
    "seaborn",      ## Needed for running ClusterVizOps in non-Colab env
    "nbconvert>=1.3.5",
    "nbformat>=3.0.9",
]

dev_requirements = [
    "ipykernel",
    # "autopep8",
    # "pylint",
    # "flake8",
    "pre-commit",
]

setuptools.setup(
    name="workflows",
    version="0.0.1",
    description="RelevanceAI Workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="dev@relevance.ai",
    install_requires=requirements,
    extras_require={
        "tests": notebook_test_requirements,
        "dev": dev_requirements + notebook_test_requirements,
    },
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
