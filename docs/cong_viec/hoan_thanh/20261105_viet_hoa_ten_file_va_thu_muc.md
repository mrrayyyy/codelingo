---
type: docs
owner: claude
stakes: routine
priority: P1
opened: 2026-11-05
---

# Đổi tên thư mục và file docs sang tiếng Việt và chuẩn hóa nội dung tiếng Việt

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
2. Đổi tên toàn bộ các file tài liệu trong `docs/` sang tiếng Việt không dấu dạng snake_case:
   - `docs/architecture.md` → `docs/kien_truc.md`
   - `docs/cloud-deployment.vi.md` → `docs/trien_khai_cloud.md`
   - `docs/verification.md` → `docs/xac_minh.md`
   - `docs/san_pham/roadmap.md` → `docs/san_pham/lo_trinh.md`
   - `docs/quy_trinh/housekeeping.md` → `docs/quy_trinh/don_dep_dinh_ky.md`
   - Toàn bộ các file trong `docs/quy_tac/`, `docs/quyet_dinh/`, `docs/cong_viec/`, `docs/nhat_ky/`.
   - Giữ nguyên tên file tiếng Anh chỉ cho các file entrypoint của hệ thống/tooling ngoài root (`README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `frontend/AGENTS.md`).
3. Làm sạch hoàn toàn nội dung tài liệu: chuyển toàn bộ các tiêu đề (`Ngữ cảnh`, `Tiêu chí chấp nhận`, `Kế hoạch`, `Nhật ký thực hiện`, `Sai lệch`, `Ngữ cảnh và bằng chứng`, `Hành động khuyến nghị`, v.v.) và loại bỏ các phần mở ngoặc tiếng Anh thừa, CHỈ GIỮ LẠI các từ khóa học thuật/kỹ thuật tiếng Anh (Docker, API, FSRS, Next.js, Redis, Tree-sitter, spaCy, FastAPI, SQLite, PostgreSQL, ARQ, Git, commit, push, CI/CD, JSON, PR, token, OAuth, Basic Auth, LLM, TTS, STT, Groq, Neon, Render).
4. Cập nhật các script công cụ `check_doc_links.py`, `housekeeping.py`, `.gitignore` và các file hợp đồng agent.

## Tiêu chí chấp nhận
- [x] Di chuyển toàn bộ các thư mục con của `docs/` sang cấu trúc tiếng Việt snake_case bằng `git mv`.
- [x] Đổi tên toàn bộ các file trong `docs/` sang tiếng Việt snake_case bằng `git mv`.
- [x] Cập nhật `tools/docs/housekeeping.py`, `tools/docs/check_doc_links.py` và `.gitignore`.
- [x] Dịch sạch toàn bộ các tiêu đề và nội dung sang tiếng Việt thuần, chỉ giữ từ khóa học thuật tiếng Anh.
- [x] Kiểm tra và sửa 100% link tương đối, đạt 0 dead links (`0 dead link(s) in 40 file(s)`).
- [x] Chạy `housekeeping.py` báo cáo hợp lệ.
- [x] Toàn bộ test backend (53 passed) và frontend typecheck (0 errors) vượt qua.

## Kế hoạch

### Bước 1: Mở ticket & Di chuyển thư mục, đổi tên file
- [x] Tạo ticket và chuyển sang `dang_lam/`.
- [x] Di chuyển các thư mục bằng `git mv`.
- [x] Đổi tên các file tài liệu trong `docs/` sang tiếng Việt bằng `git mv`.
- [x] Cập nhật `.gitignore`.

### Bước 2: Cập nhật công cụ tooling
- [x] Cập nhật `tools/docs/check_doc_links.py` hỗ trợ thư mục tiếng Việt.
- [x] Cập nhật `tools/docs/housekeeping.py` hỗ trợ regex và thư mục tiếng Việt.

### Bước 3: Làm sạch nội dung tiếng Việt & Tiêu đề
- [x] Cập nhật các tiêu đề và nội dung trong `docs/quy_tac/`.
- [x] Cập nhật các tiêu đề và nội dung trong `docs/quyet_dinh/`.
- [x] Cập nhật các tiêu đề và nội dung trong `docs/nhat_ky/`.
- [x] Cập nhật các tiêu đề và nội dung trong `docs/cong_viec/`.
- [x] Cập nhật các tiêu đề và nội dung trong `docs/quy_trinh/`, `docs/san_pham/`, `docs/kien_truc.md`, `docs/trien_khai_cloud.md`, `docs/xac_minh.md`, `README.md`.
- [x] Cập nhật `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `frontend/AGENTS.md`, `.agents/skills/codelingo-doc-manager/SKILL.md`.

### Bước 4: Sửa liên kết và kiểm tra xác minh
- [x] Chạy `check_doc_links.py` và sửa sạch dead links (đạt 0 dead links).
- [x] Chạy `housekeeping.py` kiểm tra phân loại và tính hợp lệ.
- [x] Chạy pytest (53 passed) và frontend typecheck (sạch lỗi).
- [x] Chuyển ticket sang `hoan_thanh/`, commit và push lên `origin main`.

## Nhật ký thực hiện
- 2026-11-05 — Khởi tạo ticket và di chuyển toàn bộ thư mục trong `docs/` sang tiếng Việt không dấu snake_case (`docs/quy_tac/`, `docs/quyet_dinh/`, `docs/cong_viec/`, `docs/nhat_ky/`, `docs/san_pham/`, `docs/quy_trinh/`, `docs/tam/`).
- 2026-11-05 — Đổi tên toàn bộ các file tài liệu trong `docs/` sang tiếng Việt không dấu snake_case theo yêu cầu mới nhất của chủ dự án.
- 2026-11-05 — Cập nhật `tools/docs/check_doc_links.py` và `tools/docs/housekeeping.py` để hỗ trợ quét cấu trúc thư mục tiếng Việt mới và regex cho các tiêu đề tiếng Việt (`## Nhật ký thực hiện`, `## Sai lệch`).
- 2026-11-05 — Cập nhật toàn bộ link markdown tương đối trên 40 file tài liệu trong dự án, đảm bảo `check_doc_links.py` báo cáo 0 dead links.
- 2026-11-05 — Làm sạch toàn bộ các tiêu đề tiếng Anh còn sót lại trong các file tài liệu, backlog, ledger, template; chỉ giữ các thuật ngữ kỹ thuật tiếng Anh chuẩn.
- 2026-11-05 — Chạy kiểm tra: `scan_secrets.py` (0 secrets), `pytest` (53 passed), `npm run typecheck` (0 errors), `check_doc_links.py` (0 dead links).

## Sai lệch
Không có
