<h2 align="center">
    <img src="branding/logo/gitload.png" height="128px" width="128px">
</h2>

<p align="center">
    <img src="https://img.shields.io/badge/python-3.7+-green">
    <img src="https://img.shields.io/badge/license-MIT-green">
</p>

**GitLoad** is a simple Python API for downloading web-repositories using
only the standard library.

Supported Platforms:

- **BitBucket**: https://bitbucket.org/
- **GitHub**: https://github.com/

## Quick Start

```python
>>> from gitload.github import download
>>> download(user='numpy', repo='numpy')
WindowsPath('C:/Users/GitLoad/AppData/Local/Temp/tmp17gdig4b')
```

## Installation

- Installation using `pip` (a Python package manager):

```console
gitload@dev~$ pip install gitload
```

## License

MIT License, Copyright (c) 2023 Sergei Bogdanov. See [LICENSE](LICENSE) file.
