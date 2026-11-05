---
type: docs
owner: claude
stakes: routine
opened: 2026-11-05
---

# Áp dụng quy trình quản lý tác vụ và tài liệu theo mô hình docs-as-code

## Context
CodeLingo trước đây chưa có hệ thống theo dõi tác vụ, không có bản ghi quyết định và chưa có lịch sử git. Workspace AIOps của chủ dự án đang vận hành hiệu quả một bộ giao thức độc lập với nền tảng (trạng thái tính theo thư mục cho ticket, sổ nhật ký ledger cho các phát hiện, các bản ghi ADR, quy tắc đồng bộ tài liệu và kỹ năng doc-manager). Ticket này chuyển thể mô hình đó cho một repository ứng dụng của một lập trình viên duy nhất được phát triển bởi Claude Code và Gemini/Antigravity, loại bỏ các phần hạ tầng chuyên sâu (Vault, Kubernetes, SSH, logging lệnh shell), và khởi tạo backlog từ đánh giá sản phẩm.

Các quyết định đã chốt với chủ dự án vào ngày 2026-11-05:
- Mục đích: công cụ học tập cá nhân.
- Các AI agent: Claude Code và Gemini/Antigravity.
- Mức độ chuyên sâu: "vừa đủ" — giao thức, backlog, ledger, ADRs, skill, kiểm tra liên kết và dọn dẹp housekeeping; không dùng git hook hay trình ghi log lệnh.
- Repository: công khai `mrrayyyy/codelingo` trên GitHub; các agent tự động commit và push.
- Ưu tiên trong 1–2 tháng tới: sử dụng cloud hàng ngày, luyện tập tiếng Anh công sở thực chiến, nâng cao chất lượng nội dung/từ vựng. Kỹ năng trọng tâm: nói, nghe, đọc/từ vựng.

## Acceptance Criteria
- [x] `docs/protocol/` chứa mọi quy tắc ràng buộc; các file điểm vào của agent chỉ chứa con trỏ điều hướng.
- [x] Cấu trúc thư mục backlog và ledger kèm các file mẫu; khởi tạo các ticket từ đánh giá sản phẩm.
- [x] Các ADR ghi nhận quyết định ưu tiên cloud, quy trình làm việc và tự động push vào repo công khai.
- [x] Script kiểm tra liên kết và housekeeping chạy sạch lỗi; CI tự động chạy kiểm tra liên kết tài liệu.
- [x] Repository được đưa lên GitHub kèm lịch sử commit rõ ràng.

## Plan

### Kho lưu trữ (Repository)
- [x] `git init -b main`; quét kiểm tra secret các file; tạo commit cơ sở `e5d8c8e`
- [x] `.gitignore`: `docs/tmp/*`, `.claude/settings.local.json`

### Giao thức và các file điểm vào (Protocol and entry files)
- [x] `docs/protocol/{README,NAVIGATION,EXECUTION,KANBAN,LEDGER,DOC_SYNC,VERIFICATION,SECRETS}.md`
- [x] `AGENTS.md` (hợp đồng chia sẻ chung), `CLAUDE.md`, `GEMINI.md` (con trỏ điều hướng)
- [x] `.agents/skills/codelingo-doc-manager/SKILL.md`, liên kết vào `.claude/skills/`

### Cấu trúc theo dõi (Tracking structure)
- [x] `docs/backlog/` 5 thư mục trạng thái + `_TEMPLATE.md`
- [x] `docs/ledger/` 3 thư mục trạng thái + `_TEMPLATE.md`
- [x] `docs/decisions/` README, file mẫu, ADR 0001–0003
- [x] `docs/runbooks/housekeeping.md`, `tools/docs/check_doc_links.py`, `tools/docs/housekeeping.py`

### Đánh giá sản phẩm và khởi tạo (Review and seeding)
- [x] `docs/product/roadmap.md` — đánh giá và lộ trình phân kỳ
- [x] Khởi tạo các ticket trong `ready/` và `open/`; các phát hiện chưa quyết định trong `ledger/open/`

### Xác minh và xuất bản (Verification and publish)
- [x] Kiểm tra liên kết và housekeeping trả về mã thoát exit 0; backend tests và typecheck đều vượt qua
- [x] Thêm bước kiểm tra liên kết trong CI tại `.github/workflows/ci.yml`
- [x] `gh repo create mrrayyyy/codelingo --public --source . --push`

## Implementation Log
- 2026-11-05 — Đọc giao thức AIOps (`aiops/docs/protocol/*`), các template và kỹ năng `aiops-doc-manager`. Trao đổi 8 câu hỏi định hướng phạm vi với chủ dự án.
- 2026-11-05 — Bằng chứng cơ sở: `pytest backend/tests` → 53 bài test passed, 1 cảnh báo deprecation; `npm run typecheck` → exit 0.
- 2026-11-05 — Quét secret trên 62 file git chuẩn bị thêm: chỉ có placeholder trong `.env*.example` và key giả lập có chủ đích trong `backend/tests/test_extraction.py`. Commit cơ sở `e5d8c8e`.
- 2026-11-05 — Soạn thảo giao thức, file điểm vào, kỹ năng, file mẫu, các ADR, bộ công cụ tools, roadmap, các ticket và ledger ban đầu.
- 2026-11-05 — Kiểm tra: `check_doc_links.py` → 0 link hỏng trong 38 file; `housekeeping.py` cảnh báo chính xác ticket này chưa được commit; công cụ quét secret phát hiện key Groq giả lập và bỏ qua các fixture đã đánh dấu; pytest 53 passed; typecheck sạch lỗi.
- 2026-11-05 — `scan_secrets.py` bị treo trong chuỗi commit: script tự động chọn stdin khi `isatty()` trả về false (luôn xảy ra trong shell của agent). Đã sửa để script chỉ đọc stdin khi có cờ tường minh `-`; cập nhật ví dụ trong giao thức.
- 2026-11-05 — Tạo commit `e6e49ba` (protocol) và `e71221e` (roadmap, backlog).
- 2026-11-05 — `gh repo create ray-dd1510/codelingo` → HTTP 404: `gh auth status` hiển thị nhãn keyring cũ; `gh api user` → username là `mrrayyyy`. Đổi tên chủ sở hữu trong tài liệu (`4a4798f`), tạo repo https://github.com/mrrayyyy/codelingo (công khai) và push nhánh `main`.

## Deviations
- Các file hiện có `docs/architecture.md`, `docs/cloud-deployment.vi.md` và `docs/verification.md` được giữ nguyên vị trí (README trỏ tới các file này); file NAVIGATION ánh xạ chúng thay vì di chuyển vị trí.
- Chủ sở hữu repo là `mrrayyyy`, thay vì `ray-dd1510` như trao đổi ban đầu — cùng một tài khoản, đây là username hiện tại. Không cần xử lý thêm.
- Lỗi đọc stdin của script quét secret đã được sửa trực tiếp trong ticket này (xem nhật ký). Không cần xử lý thêm.
