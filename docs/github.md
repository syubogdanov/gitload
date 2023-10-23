# gitload.github - interaction with GitHub

## gitload.github.download

### Signature

```python
def download(user: str, repo: str) -> pathlib.Path:
    ...
```

### Description

Download the repository from `GitHub`. The downloaded repository will be placed
in the directory for temporary files.

### Examples

```python
>>> from gitload.github import download
>>> download(user='pandas-dev', repo='pandas')
PosixPath('/tmp/tmprjw_e5bf')
```

```python
>>> from gitload.github import download
>>> download(user='numpy', repo='numpy')
WindowsPath('C:/Users/GitLoad/AppData/Local/Temp/tmp17gdig4b')
```

```python
>>> from gitload.github import download
>>> download(user='missing', repo='repository')
Traceback (most recent call last):
    ...
RuntimeError: Failed to access the repository
```
