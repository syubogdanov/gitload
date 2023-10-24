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
import os.path
import pathlib
import tempfile
import unittest
import unittest.mock
import urllib.error
import zipfile

from gitload import bitbucket


URLRETRIEVE: str = "gitload.bitbucket._bitbucket.urllib.request.urlretrieve"


class TestUserType(unittest.TestCase):
    def test_int(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user=42, repo="gitload")

    def test_set(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user={"42"}, repo="gitload")

    def test_list(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user=["42"], repo="gitload")

    def test_bytes(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user=b"42", repo="gitload")

    def test_bool(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user=True, repo="gitload")

    def test_none(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user=None, repo="gitload")


class TestRepoType(unittest.TestCase):
    def test_int(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user="syubogdanov", repo=42)

    def test_set(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user="syubogdanov", repo={"42"})

    def test_list(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user="syubogdanov", repo=["42"])

    def test_bytes(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user="syubogdanov", repo=b"42")

    def test_bool(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user="syubogdanov", repo=True)

    def test_none(self):
        with self.assertRaises(TypeError):
            bitbucket.download(user="syubogdanov", repo=None)


class TestEmpty(unittest.TestCase):
    def test_user(self):
        with self.assertRaises(ValueError):
            bitbucket.download(user="", repo="gitload")

    def test_repo(self):
        with self.assertRaises(ValueError):
            bitbucket.download(user="syubogdanov", repo="")


class TestSuccessRequest(unittest.TestCase):
    @unittest.mock.patch(URLRETRIEVE)
    def test(self, urlretrieve: unittest.mock.MagicMock):
        filename: str = "hello.world"
        text: str = "Hello, world!"

        with open(filename, mode="w") as file:
            bytesno: int = file.write(text)
            self.assertEqual(bytesno, len(text))

        archive_path: str = tempfile.mktemp()
        with zipfile.ZipFile(archive_path, mode="w") as archive:
            archive.write(filename)

        os.remove(filename)
        urlretrieve.return_value = (archive_path, None)

        repo_path: pathlib.Path = bitbucket.download(
            user="syubogdanov",
            repo="gitload",
        )
        file_path = repo_path.joinpath(filename)

        self.assertEqual(len(os.listdir(repo_path)), 1)
        self.assertTrue(file_path.exists())
        self.assertTrue(file_path.is_file())
        self.assertEqual(file_path.read_text(), text)


class TestFailureRequest(unittest.TestCase):
    @unittest.mock.patch(
        URLRETRIEVE,
        side_effect=urllib.error.HTTPError(
            url="https://bitbucket.org/syubogdanov/gitload",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=None,
        ),
    )
    def test(self, urlretrieve: unittest.mock.MagicMock):
        with self.assertRaises(RuntimeError):
            bitbucket.download(user="syubogdanov", repo="gitload")


class TestExceptionRequest(unittest.TestCase):
    @unittest.mock.patch(
        URLRETRIEVE,
        side_effect=NotImplementedError("Test Exception"),
    )
    def test(self, urlretrieve: unittest.mock.MagicMock):
        with self.assertRaises(RuntimeError):
            bitbucket.download(user="syubogdanov", repo="gitload")


class TestInvalidZip(unittest.TestCase):
    @unittest.mock.patch(URLRETRIEVE)
    def test(self, urlretrieve: unittest.mock.MagicMock):
        path: str = tempfile.mktemp()
        text: str = "Hello, world!"

        with open(path, mode="w") as file:
            bytesno: int = file.write(text)
            self.assertEqual(bytesno, len(text))

        urlretrieve.return_value = (path, None)
        with self.assertRaises(ValueError):
            bitbucket.download(user="syubogdanov", repo="gitload")


class TestRemoveZip(unittest.TestCase):
    @unittest.mock.patch(URLRETRIEVE)
    def test_valid_zip(self, urlretrieve: unittest.mock.MagicMock):
        file_path: str = tempfile.mktemp()
        text: str = "Hello, world!"

        with open(file_path, mode="w") as file:
            bytesno: int = file.write(text)
            self.assertEqual(bytesno, len(text))

        archive_path: str = tempfile.mktemp()
        with zipfile.ZipFile(archive_path, mode="w") as archive:
            archive.write(file_path)

        urlretrieve.return_value = (archive_path, None)
        bitbucket.download(user="syubogdanov", repo="gitload")

        self.assertFalse(os.path.exists(archive_path))

    @unittest.mock.patch(URLRETRIEVE)
    def test_invalid_zip(self, urlretrieve: unittest.mock.MagicMock):
        path: str = tempfile.mktemp()
        text: str = "Hello, world!"

        with open(path, mode="w") as file:
            bytesno: int = file.write(text)
            self.assertEqual(bytesno, len(text))

        urlretrieve.return_value = (path, None)
        with self.assertRaises(ValueError):
            bitbucket.download(user="syubogdanov", repo="gitload")

        self.assertFalse(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
