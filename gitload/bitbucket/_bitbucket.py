# MIT License
#
# Copyright (c) 2023 Sergei Bogdanov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import pathlib
import tempfile
import urllib.error
import urllib.request
import zipfile


def download(user: str, repo: str) -> pathlib.Path:
    """
    Download the repository from BitBucket

    Args:
        user: User on BitBucket
        repo: Repository on BitBucket

    Returns:
        The path to the directory where the repository was downloaded

    Raises:
        TypeError: The arguments do not match the signature
        ValueError: The arguments (archive) are empty (broken)
        RuntimeError: Error when downloading the repository (archive)

    See Also:
        urllib.request.urlretrieve(...)
    """
    if not isinstance(user, str):
        raise TypeError("The argument 'user' must be 'str'")

    if not isinstance(repo, str):
        raise TypeError("The argument 'repo' must be 'str'")

    if not user:
        raise ValueError("The argument 'user' must be non-empty")

    if not repo:
        raise ValueError("The argument 'repo' must be non-empty")

    try:
        url = f"https://bitbucket.org/{user}/{repo}/get/HEAD.zip"
        archive_path, _ = urllib.request.urlretrieve(url)

    except urllib.error.HTTPError:
        raise RuntimeError("Failed to access the repository")

    except Exception as exception:
        raise RuntimeError(f"An unexpected exception occurred: {exception}")

    if not zipfile.is_zipfile(archive_path):
        raise ValueError("The downloaded file is not a zip archive")

    extract_path = pathlib.Path(tempfile.mkdtemp())
    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(extract_path)

    os.remove(archive_path)
    return extract_path
