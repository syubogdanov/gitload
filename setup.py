from os import PathLike
from typing import List

from setuptools import setup


def read(path: str | PathLike) -> str:
    with open(path) as file:
        return file.read()


def requirements(path: str | PathLike) -> List[str]:
    return read(path).splitlines()


if __name__ == "__main__":
    setup(
        name="gitload",
        version="1.0",
        description="Python API for downloading web-repositories",
        long_description=read("README.md"),
        long_description_content_type="text/markdown",
        author="Sergei Bogdanov",
        author_email="syubogdanov@outlook.com",
        url="https://github.com/syubogdanov/gitload",
        packages=[
            "gitload.bitbucket",
            "gitload.github",
        ],
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
        ],
        license="MIT",
        install_requires=requirements("requirements.txt"),
    )
