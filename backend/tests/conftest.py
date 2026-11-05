import os
import tempfile
from pathlib import Path

import pytest

_temporary = tempfile.TemporaryDirectory(prefix="codelingo-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{_temporary.name}/test.db"
os.environ["JOB_MODE"] = "inline"
os.environ["API_KEY"] = "local-development-key"
os.environ["SPOOL_DIR"] = f"{_temporary.name}/spool"

from app.db import Base, engine
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    Base.metadata.drop_all(engine)
    with TestClient(app, headers={"X-API-Key": "local-development-key"}) as client:
        yield client


@pytest.fixture
def sample():
    return Path(__file__).parent / "fixtures/sample_repo"
