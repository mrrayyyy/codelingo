# 0004. Bỏ chế độ job ARQ/Redis, chỉ giữ `inline` và `github_actions`

- Trạng thái: accepted
- Ngày: 2026-11-06
- Người quyết định: chủ dự án

## Ngữ cảnh
`backend/app/config.py` định nghĩa `job_mode: Literal["inline", "arq", "github_actions"]`. Chế độ `arq` cần Redis, một tiến trình worker riêng (`app.imports.WorkerSettings`) và các dịch vụ `redis` + `worker` trong `compose.yaml`. [ADR 0001](0001_uu_tien_cloud_mien_phi.md) đã chọn cloud làm mô hình chính, trong đó import chạy trên GitHub Actions (`github_actions`), còn dev và CI chạy `inline` (`scripts/dev.py`, `.github/workflows/ci.yml`). Như vậy `arq` không còn được môi trường nào dùng thật, nhưng vẫn kéo theo dependency (`arq`, Redis), nhánh điều phối riêng trong `dispatch` (`backend/app/main.py`) và tài liệu vận hành riêng ([mục nhật ký gốc](../nhat_ky/da_giai_quyet/y_tuong_20261105_don_gian_hoa_che_do_job.md)).

Ứng dụng hiện chỉ có một người dùng; kế hoạch đa người dùng (2026-11-06) chỉ dừng ở mức chuẩn bị schema, chưa cần hàng đợi job phân tán.

## Quyết định
- `job_mode` chỉ còn hai giá trị `inline` (dev, CI, Compose) và `github_actions` (cloud).
- Xóa `arq` khỏi dependency, bỏ `redis_url`, `WorkerSettings`, `worker_startup` và nhánh `arq` trong `dispatch`.
- Việc dọn file tạm định kỳ (`cleanup_spool`) chạy trong vòng lặp bảo trì của lifespan API, như chế độ `inline` hiện tại.
- `compose.yaml` được giữ ở dạng rút gọn: `db` (PostgreSQL) + `api` (`JOB_MODE=inline`) + `web`, để có môi trường PostgreSQL cục bộ giống Neon khi cần kiểm thử migration.

## Các phương án thay thế đã xem xét
- **Giữ nguyên cả 3 chế độ** — tốn công bảo trì cho một đường chạy không môi trường nào dùng.
- **Bỏ luôn Compose** — mất cách chạy PostgreSQL cục bộ để thử migration Alembic trước khi áp lên Neon.

## Hệ quả
- Ít code, ít dependency và ít tài liệu phải đồng bộ hơn; `dispatch` chỉ còn hai nhánh.
- Import ở chế độ `inline` chạy trong tiến trình API và được tuần tự hóa bằng `_import_lock`. Đủ cho một người dùng; nếu sau này mở cho nhiều người dùng mà import trên Actions không đáp ứng được thì cần ADR mới.
- Ticket thực hiện: [20261106_bo_che_do_arq_redis](../cong_viec/dang_lam/20261106_bo_che_do_arq_redis.md).
