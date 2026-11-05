"""Run both local services with shared settings; Ctrl-C stops both."""
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

root = Path(__file__).resolve().parent.parent
load_dotenv(root / ".env")
os.environ.setdefault("JOB_MODE", "inline")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{root}/.data/codelingo.db")
os.environ.setdefault("SPOOL_DIR", str(root / ".data/uploads"))
os.environ["PYTHONPATH"] = str(root / "backend")
processes = [
    subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"], cwd=root, start_new_session=True),
    subprocess.Popen(["npm", "run", "dev"], cwd=root / "frontend", start_new_session=True),
]
try:
    while all(p.poll() is None for p in processes):
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    for process in processes:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
    for process in processes:
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
