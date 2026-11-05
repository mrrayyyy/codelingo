import stat
import zipfile

import pytest

from app.imports import github_repository, unpack_archive


@pytest.mark.parametrize("url", ["http://github.com/a/b", "https://evil.test/a/b", "https://github.com/a/b/tree/main", "https://github.com/../b", "https://github.com/a/b?token=secret", "https://user:pass@github.com/a/b"])
def test_github_url_allowlist(url):
    with pytest.raises(ValueError):
        github_repository(url)


def test_github_git_suffix():
    assert github_repository("https://github.com/example/atlas.git") == ("example", "atlas")


@pytest.mark.parametrize("path", ["../escape.ts", "/absolute.ts", "dir\\escape.ts", "C:/file.ts"])
def test_archive_traversal_rejected(tmp_path, path):
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as zipped:
        zipped.writestr(path, "unsafe")
    root = tmp_path / "out"
    root.mkdir()
    with pytest.raises(ValueError, match="unsafe"):
        unpack_archive(archive, root)


def test_archive_symlink_rejected(tmp_path):
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as zipped:
        info = zipfile.ZipInfo("linked.py")
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        zipped.writestr(info, "/etc/passwd")
    root = tmp_path / "out"
    root.mkdir()
    with pytest.raises(ValueError, match="link"):
        unpack_archive(archive, root)
