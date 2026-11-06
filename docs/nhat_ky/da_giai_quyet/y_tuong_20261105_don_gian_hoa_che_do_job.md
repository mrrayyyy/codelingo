---
type: idea
status: resolved
discovered: 2026-11-05
source: product review in 20261105_khoi_tao_quy_trinh_tai_lieu_agent
severity: normal
owner: user
---

# Cân nhắc loại bỏ chế độ job ARQ/Redis và cấu hình Compose

## Ngữ cảnh và bằng chứng
File `backend/app/config.py` định nghĩa `job_mode: Literal["inline", "arq", "github_actions"]`; `compose.yaml` khởi chạy PostgreSQL, Redis, API và worker; `Dockerfile.cloud` + `render.yaml` phục vụ cấu hình triển khai trên cloud. Mỗi chế độ có luồng điều phối riêng trong hàm `dispatch` của `backend/app/main.py` và các tài liệu vận hành tương ứng. Chủ dự án đã chọn ưu tiên triển khai cloud ([ADR 0001](../../quyet_dinh/0001_uu_tien_cloud_mien_phi.md)) và là người dùng duy nhất của hệ thống. Đọc và ghi nhận ngày 2026-11-05.

## Hành động khuyến nghị
Chủ dự án xem xét quyết định có nên tiếp tục duy trì chế độ `arq` + Compose hay không.
- Nếu bỏ: giữ `inline` cho môi trường dev/CI và `github_actions` cho môi trường cloud; xóa mã nguồn liên quan đến Redis/ARQ, worker trong `compose.yaml` và các phần tài liệu liên quan; ghi nhận thành ADR 0004 thay thế một phần kiến trúc ban đầu.
- Nếu giữ: không cần hành động gì, chuyển mục này sang `da_huy` kèm theo lý do.

## Giải quyết
2026-11-06: chủ dự án chọn bỏ ARQ/Redis, giữ `inline` + `github_actions`, Compose rút gọn còn `db` + `api` + `web`. Ghi thành [ADR 0004](../../quyet_dinh/0004_bo_che_do_arq_redis.md); thực hiện trong ticket [20261106_bo_che_do_arq_redis](../../cong_viec/hoan_thanh/20261106_bo_che_do_arq_redis.md).
