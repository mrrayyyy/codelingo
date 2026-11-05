#!/usr/bin/env python3
"""Audit the ledger and backlog for things that have gone quiet.

    python3 tools/docs/housekeeping.py           # report; exit 1 if anything needs a decision
    python3 tools/docs/housekeeping.py --stale-days 5

It only reports. It never resolves, re-dates, moves or deletes anything: the value
is that a person looks at what has gone quiet. See docs/runbooks/housekeeping.md.
Python rather than shell on purpose: the AIOps shell version silently passed while
three of its checks were broken by zsh glob and `\\<` quirks.
"""
import argparse
import datetime as dt
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DOCS = os.path.join(ROOT, "docs")


def md(pattern):
    return sorted(f for f in glob.glob(os.path.join(DOCS, pattern)) if not f.endswith("_TEMPLATE.md"))


def rel(path):
    return os.path.relpath(path, ROOT)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def field(text, name):
    m = re.search(rf"^{name}:\s*([^\s#]+)", text, re.M)
    return m.group(1) if m else None


def last_commit_date(path):
    try:
        out = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%cs", "--", path],
                             capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return dt.date.fromisoformat(out) if out else None


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stale-days", type=int, default=7)
    args = parser.parse_args()
    today = dt.date.today()
    findings = {}

    def add(group, line):
        findings.setdefault(group, []).append(line)

    # 1. Ledger items past review, or missing the field.
    for f in md("ledger/open/*.md"):
        text = read(f)
        value = field(text, "next_review")
        if not value:
            add("Ledger: missing next_review", rel(f))
            continue
        try:
            due = dt.date.fromisoformat(value)
        except ValueError:
            add("Ledger: unparseable next_review", f"{value}  {rel(f)}")
            continue
        if due < today:
            add("Ledger: past next_review", f"{value}  {rel(f)}")

    # 2. Tickets gone quiet; in-progress tickets with an empty log; WIP limit.
    in_progress = md("backlog/in_progress/*.md")
    if len(in_progress) > 2:
        add("Backlog: more than two tickets in progress", f"{len(in_progress)} tickets")
    for f in in_progress:
        log = section(read(f), "Implementation Log")
        if not log or log.startswith("Appended after"):
            add("Backlog: in_progress with empty Implementation Log", rel(f))
        last = last_commit_date(f)
        if last is None:
            add("Backlog: in_progress ticket never committed", rel(f))
        elif (today - last).days > args.stale_days:
            add(f"Backlog: in_progress untouched > {args.stale_days} days", f"{last}  {rel(f)}")
    for f in md("backlog/open/*.md"):
        if "block" not in read(f).lower():
            add("Backlog: open ticket without a named blocker", rel(f))

    # 3. Closed tickets whose Deviations no ledger entry cites.
    ledger_text = "\n".join(read(f) for f in md("ledger/*/*.md"))
    for f in md("backlog/done/*.md"):
        deviations = section(read(f), "Deviations")
        if deviations and not deviations.lower().startswith(("none", "appended when")):
            slug = os.path.splitext(os.path.basename(f))[0]
            if slug not in ledger_text:
                add("Backlog: done ticket with Deviations no ledger entry cites (check if any need one)", rel(f))

    # 4. Open protocol friction needs a decision, not a new date.
    for f in md("ledger/open/protocol-friction_*.md"):
        add("Ledger: open protocol friction", rel(f))

    # 5. Protocol docs nothing links to.
    corpus = "\n".join(read(f) for f in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True)
                       if "node_modules" not in f and "/docs/tmp/" not in f)
    for f in md("protocol/*.md"):
        name = os.path.basename(f)
        if name != "README.md" and corpus.count(name) <= read(f).count(name):
            add("Protocol: unreferenced", rel(f))

    # 6. Dead links.
    result = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "docs", "check_doc_links.py")],
                            capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith("DEAD"):
            add("Links: dead", line[6:])

    counts = {d: len(md(f"backlog/{d}/*.md")) for d in ("open", "ready", "in_progress", "done", "cancel")}
    print("Backlog  " + "  ".join(f"{k}={v}" for k, v in counts.items()))
    print(f"Ledger   open={len(md('ledger/open/*.md'))}  resolved={len(md('ledger/resolved/*.md'))}")
    if not findings:
        print("Nothing needs a decision.")
        return 0
    for group, lines in findings.items():
        print(f"\n{group}:")
        for line in lines:
            print(f"  - {line}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
