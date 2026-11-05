#!/usr/bin/env python3
"""Audit the nhat_ky and cong_viec for things that have gone quiet.

    python3 tools/docs/housekeeping.py           # report; exit 1 if anything needs a decision
    python3 tools/docs/housekeeping.py --stale-days 5

It only reports. It never resolves, re-dates, moves or deletes anything.
See docs/quy_trinh/don_dep_dinh_ky.md.
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
    return sorted(f for f in glob.glob(os.path.join(DOCS, pattern)) if not f.endswith(("_TEMPLATE.md", "_mau.md")))


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

    # 1. Nhật ký: quá hạn review hoặc thiếu trường.
    for f in md("nhat_ky/dang_mo/*.md"):
        text = read(f)
        value = field(text, "next_review")
        if not value:
            add("Nhật ký: thiếu trường next_review", rel(f))
            continue
        try:
            due = dt.date.fromisoformat(value)
        except ValueError:
            add("Nhật ký: không thể parse next_review", f"{value}  {rel(f)}")
            continue
        if due < today:
            add("Nhật ký: đã quá hạn next_review", f"{value}  {rel(f)}")

    # 2. Công việc: đình trệ; ticket đang làm có log trống; giới hạn WIP.
    in_progress = md("cong_viec/dang_lam/*.md")
    if len(in_progress) > 2:
        add("Công việc: có nhiều hơn 2 ticket đang làm cùng lúc", f"{len(in_progress)} tickets")
    for f in in_progress:
        log = section(read(f), "Nhật ký thực hiện") or section(read(f), "Implementation Log")
        if not log or log.startswith(("Thêm sau mỗi", "Appended after")):
            add("Công việc: ticket đang làm có Nhật ký thực hiện trống", rel(f))
        last = last_commit_date(f)
        if last is None:
            add("Công việc: ticket đang làm chưa từng được commit", rel(f))
        elif (today - last).days > args.stale_days:
            add(f"Công việc: ticket đang làm không chạm tới > {args.stale_days} ngày", f"{last}  {rel(f)}")
    for f in md("cong_viec/cho_xu_ly/*.md"):
        content_lower = read(f).lower()
        if "block" not in content_lower and "chặn" not in content_lower and "bị chặn" not in content_lower:
            add("Công việc: ticket chờ xử lý không nêu rõ nguyên nhân bị chặn", rel(f))

    # 3. Closed tickets whose Sai lệch no ledger entry cites.
    ledger_text = "\n".join(read(f) for f in md("nhat_ky/*/*.md"))
    for f in md("cong_viec/hoan_thanh/*.md"):
        deviations = section(read(f), "Sai lệch") or section(read(f), "Deviations")
        if deviations and not deviations.lower().startswith(("none", "không", "appended when", "ghi nhận khi")):
            slug = os.path.splitext(os.path.basename(f))[0]
            if slug not in ledger_text:
                add("Công việc: ticket hoàn thành có Sai lệch mà chưa có mục nhật ký nào trích dẫn", rel(f))

    # 4. Open protocol friction needs a decision.
    for f in md("nhat_ky/dang_mo/*friction_*.md"):
        add("Nhật ký: vướng mắc quy tắc (protocol friction) đang mở", rel(f))

    # 5. Quy tắc docs nothing links to.
    corpus = "\n".join(read(f) for f in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True)
                       if "node_modules" not in f and "/docs/tam/" not in f and "/docs/tmp/" not in f)
    for f in md("quy_tac/*.md"):
        name = os.path.basename(f)
        if name != "README.md" and corpus.count(name) <= read(f).count(name):
            add("Quy tắc: tài liệu không được liên kết tham chiếu", rel(f))

    # 6. Dead links.
    result = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "docs", "check_doc_links.py")],
                            capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith("DEAD"):
            add("Links: liên kết hỏng", line[6:])

    counts_cv = {d: len(md(f"cong_viec/{d}/*.md")) for d in ("cho_xu_ly", "san_sang", "dang_lam", "hoan_thanh", "da_huy")}
    print("Công việc  " + "  ".join(f"{k}={v}" for k, v in counts_cv.items()))
    print(f"Nhật ký    dang_mo={len(md('nhat_ky/dang_mo/*.md'))}  da_giai_quyet={len(md('nhat_ky/da_giai_quyet/*.md'))}")
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
