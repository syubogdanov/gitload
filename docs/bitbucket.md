# gitload.bitbucket - interaction with BitBucket

## gitload.bitbucket.download

### Signature

```python
def download(user: str, repo: str) -> pathlib.Path:
    ...
```

### Description

Download the repository from `BitBucket`. The downloaded repository will be
placed in the directory for temporary files.

### Examples

```python
>>> from gitload.bitbucket import download
>>> download(user='microsoft', repo='azure-cli-run')
PosixPath('/tmp/tmpl6zs0352')
```

```python
>>> from gitload.bitbucket import download
>>> download(user='reviewdog', repo='reviewdog')
WindowsPath('C:/Users/GitLoad/AppData/Local/Temp/tmpm8g1yn9x')
```

```python
>>> from gitload.bitbucket import download
>>> download(user='missing', repo='repository')
Traceback (most recent call last):
    ...
RuntimeError: Failed to access the repository
```
