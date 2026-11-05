---
type: docs
owner: claude
stakes: routine
priority: P1
opened: 2026-11-05
---

# Chuyển đổi toàn bộ tài liệu sang tiếng Việt và thiết lập quy tắc ngôn ngữ

## Context
Yêu cầu trực tiếp từ chủ dự án:
1. Chuyển đổi toàn bộ nội dung tài liệu trong dự án (`docs/`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `frontend/AGENTS.md`, các file kỹ năng và tài liệu hướng dẫn) sang tiếng Việt để phục vụ tốt nhất việc theo dõi và học tập.
2. Thiết lập quy tắc cốt lõi (Language & Naming Rules):
   - **Tên file và thư mục**: Bắt buộc giữ nguyên 100% bằng tiếng Anh để đảm bảo tương thích đường dẫn, tooling, git history và scripts (`tools/docs/check_doc_links.py`, `tools/docs/housekeeping.py`).
   - **Nội dung tài liệu**: Bắt buộc viết bằng tiếng Việt.
   - **Giao tiếp**: Trao đổi với chủ dự án bằng tiếng Việt.
   - **Mã nguồn & Kỹ thuật**: Tên biến, hàm, mã nguồn, lệnh shell, endpoint API và thuật ngữ kỹ thuật giữ nguyên dạng chuẩn tiếng Anh.

## Acceptance Criteria
- [ ] Bổ sung quy tắc ngôn ngữ và đặt tên vào `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `frontend/AGENTS.md`, `docs/protocol/README.md`, `docs/protocol/DOC_SYNC.md`, `docs/protocol/NAVIGATION.md`, `.agents/skills/codelingo-doc-manager/SKILL.md`.
- [ ] Chuyển đổi `README.md` sang tiếng Việt.
- [ ] Chuyển đổi toàn bộ tài liệu trong `docs/protocol/` sang tiếng Việt.
- [ ] Chuyển đổi toàn bộ tài liệu trong `docs/decisions/` (ADR) sang tiếng Việt.
- [ ] Chuyển đổi các tài liệu kiến trúc, triển khai, hướng dẫn (`docs/architecture.md`, `docs/cloud-deployment.vi.md`, `docs/verification.md`, `docs/runbooks/housekeeping.md`, `docs/product/roadmap.md`, `docs/tmp/README.md`).
- [ ] Chuyển đổi các template và ticket trong `docs/backlog/` và `docs/ledger/` sang tiếng Việt, giữ nguyên header và field cần thiết cho tooling.
- [ ] Chuyển đổi file kỹ năng `.agents/skills/codelingo-doc-manager/SKILL.md`.
- [ ] Chạy kiểm tra: `python3 tools/docs/check_doc_links.py`, `python3 tools/docs/housekeeping.py`, `python3 tools/docs/scan_secrets.py`, test backend và typecheck frontend đều vượt qua (100% pass, 0 dead links).

## Plan

### Nhóm 1: Mở ticket & Cập nhật quy tắc cốt lõi (Rules & Entrypoints)
- [x] Tạo ticket và chuyển sang `in_progress/`.
- [x] Cập nhật quy tắc vào `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `frontend/AGENTS.md`.
- [x] Cập nhật kỹ năng `.agents/skills/codelingo-doc-manager/SKILL.md`.

### Nhóm 2: Chuyển đổi bộ giao thức (Protocol) & README chính
- [ ] Cập nhật `README.md`.
- [ ] Cập nhật `docs/protocol/README.md`, `NAVIGATION.md`, `EXECUTION.md`, `KANBAN.md`, `LEDGER.md`, `DOC_SYNC.md`, `VERIFICATION.md`, `SECRETS.md`.

### Nhóm 3: Chuyển đổi Kiến trúc, Sản phẩm, Runbooks & Quyết định (ADR)
- [ ] Cập nhật `docs/architecture.md`, `docs/product/roadmap.md`, `docs/verification.md`, `docs/cloud-deployment.vi.md`, `docs/runbooks/housekeeping.md`, `docs/tmp/README.md`.
- [ ] Cập nhật `docs/decisions/README.md`, `0000-template.md`, `0001-cloud-first-free-tier.md`, `0002-docs-as-code-workflow.md`, `0003-public-repo-auto-commit-push.md`.

### Nhóm 4: Chuyển đổi Backlog & Ledger
- [ ] Cập nhật `docs/backlog/_TEMPLATE.md` và các ticket trong `ready/`, `open/`, `done/`.
- [ ] Cập nhật `docs/ledger/_TEMPLATE.md` và các mục ledger trong `open/`.

### Nhóm 5: Kiểm tra toàn diện & Hoàn tất
- [ ] Chạy `check_doc_links.py` và `housekeeping.py`.
- [ ] Chạy tests và kiểm tra bảo mật `scan_secrets.py`.
- [ ] Chuyển ticket sang `done/`, commit và push `origin main`.

## Implementation Log
- 2026-11-05: Khởi tạo ticket chuyển đổi toàn bộ tài liệu sang tiếng Việt và thiết lập quy tắc ngôn ngữ.
- 2026-11-05: Hoàn thành Nhóm 1: Cập nhật hợp đồng agent (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `frontend/AGENTS.md`) và kỹ năng quản lý tài liệu `SKILL.md` sang tiếng Việt cùng quy tắc giữ nguyên tên file/thư mục tiếng Anh.

## Deviations
None
