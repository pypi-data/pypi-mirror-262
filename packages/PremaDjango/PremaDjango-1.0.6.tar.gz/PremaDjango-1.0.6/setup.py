"""PremaDjango setup.py."""

import setuptools

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PremaDjango",
    version="1.0.6",
    packages=setuptools.find_packages(),
    install_requires=["Django", "setuptools_scm", "requests"],
    author="Premanath",
    author_email="talamarlapremanath143@gmail.com",
    description="configurations and settings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prema1432/premadjango/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ],
    license="MIT",
)
