---
type: idea
status: open
discovered: 2026-11-05
next_review: 2026-11-19
source: product review in 20261105_agent_docs_workflow_bootstrap
severity: normal
owner: user
---

# Cân nhắc loại bỏ chế độ job ARQ/Redis và cấu hình Compose

## Ngữ cảnh & Bằng chứng (Context & Evidence)
File `backend/app/config.py` định nghĩa `job_mode: Literal["inline", "arq", "github_actions"]`; `compose.yaml` khởi chạy PostgreSQL, Redis, API và worker; `Dockerfile.cloud` + `render.yaml` phục vụ cấu hình triển khai trên cloud. Mỗi chế độ có luồng điều phối riêng trong hàm `dispatch` của `backend/app/main.py` và các tài liệu vận hành tương ứng. Chủ dự án đã chọn ưu tiên triển khai cloud (ADR 0001) và là người dùng duy nhất của hệ thống. Đọc và ghi nhận ngày 2026-11-05.

## Hành động khuyến nghị (Recommended Action)
Chủ dự án xem xét quyết định có nên tiếp tục duy trì chế độ `arq` + Compose hay không.
- Nếu bỏ: giữ `inline` cho môi trường dev/CI và `github_actions` cho môi trường cloud; xóa mã nguồn liên quan đến Redis/ARQ, worker trong `compose.yaml` và các phần tài liệu liên quan; ghi nhận thành ADR 0004 thay thế một phần kiến trúc ban đầu.
- Nếu giữ: không cần hành động gì, chuyển mục này sang cancelled kèm theo lý do.
