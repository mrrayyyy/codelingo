"""Start a small web/API pair in one managed service; NLP runs remotely."""
import os
import signal
import subprocess
import sys
import time

required = ["DATABASE_URL", "API_KEY", "WORKSPACE_PASSWORD", "GITHUB_ACTIONS_TOKEN", "GITHUB_ACTIONS_REPO"]
missing = [name for name in required if not os.environ.get(name)]
if missing:
    raise SystemExit("Missing required cloud settings: " + ", ".join(missing))
if not os.environ["DATABASE_URL"].startswith("postgresql+psycopg://"):
    raise SystemExit("Use a persistent PostgreSQL URL with the postgresql+psycopg:// scheme")
if len(os.environ["WORKSPACE_PASSWORD"]) < 16:
    raise SystemExit("WORKSPACE_PASSWORD must contain at least 16 characters")
if len(os.environ["API_KEY"]) < 32 or os.environ["API_KEY"] == os.environ["WORKSPACE_PASSWORD"]:
    raise SystemExit("API_KEY must be a separate secret of at least 32 characters")

os.environ["JOB_MODE"] = "github_actions"
os.environ.setdefault("SPOOL_DIR", "/spool")
os.environ.setdefault("API_URL", "http://127.0.0.1:8000")
os.environ.setdefault("HOSTNAME", "0.0.0.0")
os.environ.setdefault("PORT", "10000")
os.environ.setdefault("NODE_OPTIONS", "--max-old-space-size=192")
processes = []


def stop(*_):
    raise KeyboardInterrupt


signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
try:
    processes = [
        subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]),
        subprocess.Popen(["node", "server.js"], cwd="/app/web"),
    ]
    while all(process.poll() is None for process in processes):
        time.sleep(.5)
except KeyboardInterrupt:
    pass
finally:
    for process in processes:
        if process.poll() is None:
            process.terminate()
    for process in processes:
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
    sys.exit(1 if any(p.returncode and p.returncode > 0 for p in processes) else 0)
