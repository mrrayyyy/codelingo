---
type: refactor
owner: claude
stakes: routine
priority: P1
opened: 2026-11-06
---

# Bỏ chế độ job ARQ/Redis, rút gọn Compose và xử lý cảnh báo Starlette TestClient

## Ngữ cảnh
Chủ dự án chốt ngày 2026-11-06: bỏ ARQ/Redis, chỉ giữ `inline` + `github_actions` ([ADR 0004](../../quyet_dinh/0004_bo_che_do_arq_redis.md)). Đây là ticket đầu tiên của Giai đoạn 0; làm trước Alembic để migration đầu tiên và tài liệu không còn nhắc tới Redis.

Gộp luôn cảnh báo `StarletteDeprecationWarning` của test client vì cùng sửa `backend/pyproject.toml` và sinh lại `backend/requirements.lock` ([mục nhật ký](../../nhat_ky/da_giai_quyet/no_ky_thuat_20261105_canh_bao_starlette_testclient.md)).

## Tiêu chí chấp nhận
- [ ] `grep -rni "arq\|redis" backend/app scripts compose.yaml Dockerfile.cloud backend/Dockerfile .github` không còn kết quả (trừ comment giải thích lịch sử nếu có).
- [ ] `job_mode` chỉ chấp nhận `inline | github_actions`; giá trị `arq` trong `.env` cũ gây lỗi cấu hình rõ ràng khi khởi động.
- [ ] `cleanup_spool` vẫn chạy định kỳ ở cả hai chế độ (đã có trong lifespan) và có test.
- [ ] `docker compose config` hợp lệ với 3 dịch vụ `db`, `api`, `web`.
- [ ] `pytest backend/tests -q` xanh, **không còn** `StarletteDeprecationWarning`; CI trên `main` xanh.
- [ ] README, `docs/kien_truc.md`, `docs/quy_tac/dieu_huong.md`, ADR 0001 (phần hệ quả) không còn mô tả ARQ/Redis như thành phần đang chạy.

## Kế hoạch
### Mã nguồn backend
- [ ] `backend/app/config.py`: bỏ `redis_url`; `job_mode: Literal["inline", "github_actions"]`
- [ ] `backend/app/main.py`: xóa import `arq`, xóa nhánh `elif settings.job_mode == "arq"` trong `dispatch`; nhánh mặc định là `inline` (`background.add_task(process_import, {}, job.id)`)
- [ ] `backend/app/imports.py`: xóa `WorkerSettings`, `worker_startup`; đổi chữ ký `process_import(ctx, job_id)` → `process_import(job_id)` và cập nhật mọi nơi gọi (`main.py`, `scripts/cloud_extract.py` nếu có, tests); sửa comment "Match the single ARQ worker…"
- [ ] `backend/pyproject.toml`: bỏ `arq`
### Cảnh báo Starlette TestClient
- [ ] Đọc release notes của Starlette/FastAPI phiên bản đang khóa trong `backend/requirements.lock` để tìm cách thay thế chuẩn (gói được cảnh báo đề xuất là `httpx2`); ghi lại nguồn và ngày đọc trong nhật ký thực hiện
- [ ] Áp dụng cách sửa (thêm/ghim gói test hoặc nâng phiên bản) vào `backend/pyproject.toml` (`[project.optional-dependencies].test` nếu chỉ dùng cho test)
- [ ] Sinh lại `backend/requirements.lock` và `backend/requirements.web` bằng đúng cách đang dùng (xem header của file lock); xác nhận `arq`, `redis`, `hiredis` biến mất
### Hạ tầng chạy
- [ ] `compose.yaml`: xóa dịch vụ `redis`, `worker`, volume `redis-data`; `api` dùng `JOB_MODE: inline`, bỏ `REDIS_URL`, bỏ `depends_on.redis`
- [ ] `.env.example`, `.env.cloud.example`: bỏ `REDIS_URL` nếu có
- [ ] Kiểm tra `Dockerfile.cloud`, `backend/Dockerfile`, `scripts/cloud_start.py`, `scripts/dev.py` không còn tham chiếu Redis/ARQ
### Kiểm chứng
- [ ] Thêm test: cấu hình `JOB_MODE=arq` bị từ chối (`pydantic.ValidationError`)
- [ ] Thêm test: `cleanup_spool` xóa file spool quá 1 giờ và đánh dấu job treo là `failed`
- [ ] `.venv/bin/python -m pytest backend/tests -q` → xanh, 0 warning Starlette (dán output)
- [ ] `npm --prefix frontend run typecheck`; `docker compose config -q` (không cần chạy container)
- [ ] Push; CI trên `main` xanh (dẫn link run)
### Đồng bộ tài liệu
- [ ] README: mục Docker Compose (bỏ Redis, `logs -f api worker` → `logs -f api`), cây thư mục (`imports.py`, `compose.yaml`)
- [ ] `docs/kien_truc.md`: câu ngăn xếp công nghệ dòng 7, sơ đồ Mermaid (bỏ nút `Redis / ARQ` và `Python worker`, thay bằng background task/GitHub Actions), bảng cột mốc
- [ ] `docs/quy_tac/dieu_huong.md`: dòng `worker ARQ`
- [ ] ADR 0001: thêm ghi chú ở mục Hệ quả "một phần được thay thế bởi ADR 0004"

## Nhật ký thực hiện

## Sai lệch
