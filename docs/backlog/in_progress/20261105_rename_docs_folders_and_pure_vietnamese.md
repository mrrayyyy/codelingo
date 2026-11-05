---
type: docs
owner: claude
stakes: routine
priority: P1
opened: 2026-11-05
---

# Đổi tên thư mục docs sang tiếng Việt và làm sạch hoàn toàn nội dung tiếng Việt

## Ngữ cảnh
Yêu cầu trực tiếp từ chủ dự án:
1. Đổi tên toàn bộ thư mục bên trong `docs/` sang tiếng Việt không dấu dạng snake_case:
   - `docs/protocol/` → `docs/quy_tac/`
   - `docs/backlog/` → `docs/cong_viec/` (và các thư mục con: `cho_xu_ly`, `san_sang`, `dang_lam`, `hoan_thanh`, `da_huy`)
   - `docs/decisions/` → `docs/quyet_dinh/`
   - `docs/ledger/` → `docs/nhat_ky/` (và các thư mục con: `dang_mo`, `da_giai_quyet`, `da_huy`)
   - `docs/product/` → `docs/san_pham/`
   - `docs/runbooks/` → `docs/quy_trinh/`
   - `docs/tmp/` → `docs/tam/`
2. Làm sạch hoàn toàn nội dung tài liệu: chuyển toàn bộ các tiêu đề (`Context`, `Acceptance Criteria`, `Plan`, `Implementation Log`, `Deviations`, `Context & Evidence`, `Recommended Action`, v.v.) và các phần mở ngoặc tiếng Anh thừa sang tiếng Việt chuẩn, CHỈ GIỮ LẠI các từ khóa học thuật/kỹ thuật tiếng Anh (Docker, API, FSRS, Next.js, Redis, Tree-sitter, spaCy, FastAPI, SQLite, PostgreSQL, ARQ, Git, commit, push, CI/CD, JSON, PR, token, OAuth, Basic Auth, LLM, TTS, STT, Groq, Neon, Render).
3. Cập nhật các script công cụ `check_doc_links.py`, `housekeeping.py`, `.gitignore` và các file hợp đồng agent.

## Tiêu chí chấp nhận
- [ ] Di chuyển toàn bộ các thư mục con của `docs/` sang cấu trúc tiếng Việt snake_case bằng `git mv`.
- [ ] Cập nhật `tools/docs/housekeeping.py`, `tools/docs/check_doc_links.py` và `.gitignore`.
- [ ] Dịch sạch toàn bộ các tiêu đề và nội dung sang tiếng Việt, chỉ giữ từ khóa học thuật tiếng Anh.
- [ ] Chạy `check_doc_links.py --fix-moves` để sửa tự động và kiểm tra 100% link tương đối, 0 dead links.
- [ ] Chạy `housekeeping.py` báo cáo sạch lỗi.
- [ ] Toàn bộ test backend và frontend typecheck vượt qua.

## Kế hoạch

### Bước 1: Mở ticket & Di chuyển thư mục
- [ ] Tạo ticket và chuyển sang `in_progress/`.
- [ ] Di chuyển các thư mục bằng `git mv`.
- [ ] Cập nhật `.gitignore`.

### Bước 2: Cập nhật công cụ tooling
- [ ] Cập nhật `tools/docs/check_doc_links.py`.
- [ ] Cập nhật `tools/docs/housekeeping.py`.

### Bước 3: Làm sạch nội dung tiếng Việt & Tiêu đề
- [ ] Cập nhật các tiêu đề và nội dung trong `docs/quy_tac/`.
- [ ] Cập nhật các tiêu đề và nội dung trong `docs/quyet_dinh/`.
- [ ] Cập nhật các tiêu đề và nội dung trong `docs/nhat_ky/`.
- [ ] Cập nhật các tiêu đề và nội dung trong `docs/cong_viec/`.
- [ ] Cập nhật các tiêu đề và nội dung trong `docs/quy_trinh/`, `docs/san_pham/`, `docs/architecture.md`, `docs/verification.md`, `README.md`.
- [ ] Cập nhật `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `frontend/AGENTS.md`, `.agents/skills/codelingo-doc-manager/SKILL.md`.

### Bước 4: Sửa liên kết và kiểm tra xác minh
- [ ] Chạy `check_doc_links.py --fix-moves` và sửa sạch dead links.
- [ ] Chạy `housekeeping.py` bảo đảm exit 0.
- [ ] Chạy pytest và frontend typecheck.
- [ ] Chuyển ticket sang `hoan_thanh/`, commit và push lên `origin main`.

## Nhật ký thực hiện
- 2026-11-05: Khởi tạo ticket thực hiện theo yêu cầu chuẩn hóa cấu trúc thư mục tiếng Việt và nội dung thuần Việt.

## Sai lệch
None
