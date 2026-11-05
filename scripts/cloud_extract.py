"""One short-lived GitHub Actions extraction job. Never logs or uploads raw source.

Only CODELINGO_URL, CODELINGO_API_KEY, and CODELINGO_JOB_ID are needed. The runner
fetches input from the trusted configured app, extracts in a temporary directory,
and returns vocabulary. It never receives database credentials.
"""
import asyncio
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID
from urllib.parse import urlparse

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
from app.config import settings
from app.extraction import extract_repository
from app.imports import download_github, unpack_archive


async def main() -> None:
    base = os.environ["CODELINGO_URL"].rstrip("/")
    parsed = urlparse(base)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("CODELINGO_URL must be the trusted HTTPS application URL")
    job_id = str(UUID(os.environ["CODELINGO_JOB_ID"]))
    key = os.environ["CODELINGO_API_KEY"]
    prefix = f"{base}/api/cloud/jobs/{job_id}"
    async with httpx.AsyncClient(timeout=120, trust_env=False, follow_redirects=False, headers={"X-API-Key": key}) as client:
        async def send(method: str, url: str, **kwargs):
            # Retry cold starts and interrupted callbacks; writes are idempotent.
            for attempt in range(4):
                try:
                    response = await client.request(method, url, **kwargs)
                    if response.status_code >= 500 and attempt < 3:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    response.raise_for_status()
                    return response
                except httpx.TransportError:
                    if attempt == 3:
                        raise
                    await asyncio.sleep(2 ** attempt)

        try:
            info = (await send("GET", prefix)).json()
            if info["status"] in {"completed", "failed"}:
                print("Import already finished; no work required.")
                return
            await send("POST", f"{prefix}/progress", json={"progress": 5})
            with TemporaryDirectory(prefix="codelingo-cloud-") as temporary:
                directory = Path(temporary)
                archive = directory / "source.zip"
                if info["source_url"]:
                    await download_github(info["source_url"], archive)
                else:
                    # Never retry one-time archive retrieval after a partial transfer.
                    async with client.stream("GET", f"{prefix}/archive") as response:
                        response.raise_for_status()
                        size = 0
                        with archive.open("wb") as output:
                            async for chunk in response.aiter_bytes():
                                size += len(chunk)
                                if size > settings.max_upload_bytes:
                                    raise ValueError("Archive exceeds the configured limit")
                                output.write(chunk)
                await send("POST", f"{prefix}/progress", json={"progress": 20})
                root = directory / "repository"
                root.mkdir()
                root = unpack_archive(archive, root)
                items = await asyncio.to_thread(extract_repository, root)
                await send("POST", f"{prefix}/progress", json={"progress": 85})
                await send("POST", f"{prefix}/complete", json={"items": [item.model_dump() for item in items]})
                print(f"Import complete: {len(items)} vocabulary items. Temporary source removed on exit.")
        except Exception as exc:
            try:
                await send("POST", f"{prefix}/progress", json={"progress": 0, "failed": True})
            except Exception:
                pass
            # Exception strings and tracebacks can include credentials or snippets.
            print(f"Extraction failed ({type(exc).__name__}). Check service configuration; no source logged.", file=sys.stderr)
            raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
