import zipfile

import pytest

from app.config import settings
from app.imports import unpack_archive


def test_expanded_archive_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "max_expanded_bytes", 8)
    archive = tmp_path / "too-large.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
        zipped.writestr("readme.md", "A" * 1000)
    root = tmp_path / "out"
    root.mkdir()
    with pytest.raises(ValueError, match="Expanded archive"):
        unpack_archive(archive, root)


def test_archive_entry_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "max_files", 1)
    archive = tmp_path / "too-many.zip"
    with zipfile.ZipFile(archive, "w") as zipped:
        zipped.writestr("one.md", "English documentation")
        zipped.writestr("two.md", "More English documentation")
    root = tmp_path / "out"
    root.mkdir()
    with pytest.raises(ValueError, match="entry limit"):
        unpack_archive(archive, root)


def test_zip_upload_byte_limit(client, monkeypatch):
    monkeypatch.setattr(settings, "max_upload_bytes", 8)
    response = client.post("/imports/zip", files={"file": ("large.zip", b"0" * 100)})
    assert response.status_code == 413
    assert not list(settings.spool_dir.glob("*.part"))
