#!/usr/bin/env python3
"""Refuse to let a secret into this public repository.

    python3 tools/docs/scan_secrets.py                      # scans `git diff --cached`
    git diff origin/main..HEAD | python3 tools/docs/scan_secrets.py -   # scans a diff on stdin

Stdin is read only with the explicit `-` argument: agent shells have no TTY, so
guessing from isatty() blocks forever waiting for input.

Checks added lines only. A line is skipped when it, or one of the three lines
before it, contains the marker `fake-secret-fixture` (for deliberate test data).
Exit 1 and print file:line on a match. A backstop, not a guarantee.
"""
import re
import subprocess
import sys

PATTERNS = {
    "GitHub token": r"\b(gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})",
    "Groq key": r"\bgsk_[A-Za-z0-9]{30,}",
    "OpenAI-style key": r"\bsk-(proj-)?[A-Za-z0-9_-]{20,}",
    "AWS access key": r"\bAKIA[0-9A-Z]{16}\b",
    "Private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "Slack token": r"\bxox[baprs]-[A-Za-z0-9-]{10,}",
    "URL with password": r"[a-z+]+://[^\s:/@$]+:[^\s@${}<>]{6,}@[^\s]+",
    "Assigned secret": r"(?i)\b(api_key|secret|password|token)\s*[=:]\s*['\"]?[A-Za-z0-9_\-]{24,}",
}
PLACEHOLDER = re.compile(r"(?i)(USER:PASSWORD@|replace-this|your-|example|changeme|generate-a|choose-a)")
MARKER = "fake-secret-fixture"


def main() -> int:
    text = sys.stdin.read() if sys.argv[1:] == ["-"] else subprocess.run(
        ["git", "diff", "--cached", "--no-color", "-U3"], capture_output=True, text=True, check=True).stdout
    path, line_no, recent, hits = "?", 0, [], []
    for raw in text.splitlines():
        if raw.startswith("+++ "):
            path = raw[6:] if raw.startswith("+++ b/") else raw[4:]
            continue
        if raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            line_no = int(m.group(1)) - 1 if m else 0
            recent = []
            continue
        if raw.startswith("-"):
            continue
        line_no += 1
        content = raw[1:]
        if raw.startswith("+") and MARKER not in content and not any(MARKER in r for r in recent):
            for name, pattern in PATTERNS.items():
                m = re.search(pattern, content)
                if m and not PLACEHOLDER.search(m.group(0)):
                    hits.append(f"{path}:{line_no}: {name}")
        recent = (recent + [content])[-3:]
    for hit in hits:
        print(hit)
    print(f"{len(hits)} possible secret(s)" if hits else "No secrets found in added lines.")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
