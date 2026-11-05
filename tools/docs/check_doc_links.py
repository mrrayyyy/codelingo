#!/usr/bin/env python3
"""Dead relative Markdown links in the docs and agent entry files.

Run from anywhere after moving or deleting a ticket, ledger entry or document:
    python3 tools/docs/check_doc_links.py              # exit 1 when a dead link remains
    python3 tools/docs/check_doc_links.py --fix-moves  # repair links whose target moved to exactly one other place

Scanned: docs/**/*.md (docs/tmp excluded), the root *.md files, and .agents/**/*.md.
Ignored: fenced and inline code, http(s)/mailto links, anchors-only links.
Adapted from the AIOps workspace's checker (2026-11-05).
"""
import glob
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
TMP = os.path.join(ROOT, "docs", "tmp") + os.sep
LINK = re.compile(r"\]\(([^)#\s]+)(#[^)]*)?\)")


def files():
    found = set(glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True))
    found |= set(glob.glob(os.path.join(ROOT, "*.md")))
    found |= set(glob.glob(os.path.join(ROOT, ".agents", "**", "*.md"), recursive=True))
    return sorted(f for f in found if not f.startswith(TMP))


def prose(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def scan():
    dead = []
    for f in files():
        with open(f, encoding="utf-8") as handle:
            src = handle.read()
        for m in LINK.finditer(prose(src)):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path = os.path.normpath(os.path.join(os.path.dirname(f), target))
            if not os.path.exists(path):
                dead.append((os.path.relpath(f, ROOT), target))
    return dead


def fix_moves(dead):
    by_name = {}
    for f in files():
        by_name.setdefault(os.path.basename(f), []).append(f)
    for rel, target in dead:
        candidates = by_name.get(os.path.basename(target), [])
        if len(candidates) != 1:
            continue
        f = os.path.join(ROOT, rel)
        new = os.path.relpath(candidates[0], os.path.dirname(f)).replace(os.sep, "/")
        with open(f, encoding="utf-8") as handle:
            src = handle.read()
        out = src.replace(f"]({target})", f"]({new})").replace(f"]({target}#", f"]({new}#")
        if out != src:
            with open(f, "w", encoding="utf-8") as handle:
                handle.write(out)
            print(f"fixed  {rel}: {target} -> {new}")


if __name__ == "__main__":
    dead = scan()
    if "--fix-moves" in sys.argv and dead:
        fix_moves(dead)
        dead = scan()
    for rel, target in dead:
        print(f"DEAD  {rel} -> {target}")
    print(f"{len(dead)} dead link(s) in {len(files())} file(s)")
    sys.exit(1 if dead else 0)
