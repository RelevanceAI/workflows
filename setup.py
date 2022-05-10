#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import setuptools
from pathlib import Path
import yaml

pwd = Path(__file__).parent
long_description = (pwd / "README.md").read_text(encoding="utf-8")
package_versions = yaml.safe_load(open(pwd / "package_versions.yaml"))

requirements = [
    f"RelevanceAI[notebook]=={package_versions['RelevanceAI']}",
    f"sentence-transformers=={package_versions['sentence-transformers']}",
    f"transformers=={package_versions['transformers']}",
    f"vectorhub[sentence-transformers]=={package_versions['vectorhub']}",
    f"vectorhub[encoders-text-tfhub]=={package_versions['vectorhub']}",
    f"vectorhub[clip]=={package_versions['vectorhub']}",
    "jupyter",
    "typing_extensions",  ## <3.8
]

notebook_test_requirements = [
    "matplotlib",  ## Needed for Vectorhub in non-Colab env
    "seaborn",  ## Needed for running ClusterVizOps in non-Colab env
    "pandas",  ## Needed for running in non-Colab env
    "nbconvert>=1.3.5",
    "nbformat>=3.0.9",
    "umap-learn>=0.5.3",  ## For DR
    "pyyaml",
]

dev_requirements = [
    "wheel",
    "ipykernel",
    "black==22.3.0",
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
    package_dir={"": "workflows"},
    packages=setuptools.find_packages(where="workflows"),
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
