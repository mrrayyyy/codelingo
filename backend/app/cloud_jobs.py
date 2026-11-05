"""On-demand remote NLP jobs, using GitHub-hosted runners instead of local models."""
import re

import httpx

from .config import settings
from .imports import update_job


async def dispatch_remote(job_id: str) -> None:
    repo = settings.github_actions_repo
    workflow = settings.github_actions_workflow
    if not settings.github_actions_token or not re.fullmatch(r"[\w.-]+/[\w.-]+", repo) or not re.fullmatch(r"[\w.-]+\.ya?ml", workflow):
        raise RuntimeError("Configure GITHUB_ACTIONS_TOKEN and GITHUB_ACTIONS_REPO to enable remote imports")
    async with httpx.AsyncClient(timeout=20, trust_env=False, follow_redirects=False) as client:
        response = await client.post(f"https://api.github.com/repos/{repo}/actions/workflows/{workflow}/dispatches",
            headers={"Authorization": f"Bearer {settings.github_actions_token}", "Accept": "application/vnd.github+json",
                     "X-GitHub-Api-Version": "2022-11-28"},
            json={"ref": settings.github_actions_ref, "inputs": {"job_id": job_id}})
        response.raise_for_status()
    update_job(job_id, 2, "Waiting for the cloud extractor · your computer can stay idle", "queued")
