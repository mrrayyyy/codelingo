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
- [x] `grep -rni "arq\|redis" backend/app scripts compose.yaml Dockerfile.cloud backend/Dockerfile .github` không còn kết quả (trừ comment giải thích lịch sử nếu có).
- [x] `job_mode` chỉ chấp nhận `inline | github_actions`; giá trị `arq` trong `.env` cũ gây lỗi cấu hình rõ ràng khi khởi động.
- [x] `cleanup_spool` vẫn chạy định kỳ ở cả hai chế độ (đã có trong lifespan) và có test.
- [x] `docker compose config` hợp lệ với 3 dịch vụ `db`, `api`, `web`.
- [x] `pytest backend/tests -q` xanh, **không còn** `StarletteDeprecationWarning` (57 passed, 0 warning); CI trên `main` xanh ([run 42159360424](https://github.com/mrrayyyy/codelingo/actions/runs/42159360424)).
- [x] README, `docs/kien_truc.md`, `docs/quy_tac/dieu_huong.md`, ADR 0001 (phần hệ quả) không còn mô tả ARQ/Redis như thành phần đang chạy.

## Kế hoạch
### Mã nguồn backend
- [x] `backend/app/config.py`: bỏ `redis_url`; `job_mode: Literal["inline", "github_actions"]`
- [x] `backend/app/main.py`: xóa import `arq`, xóa nhánh `elif settings.job_mode == "arq"` trong `dispatch`; nhánh mặc định là `inline` (`background.add_task(process_import, {}, job.id)`)
- [x] `backend/app/imports.py`: xóa `WorkerSettings`, `worker_startup`; đổi chữ ký `process_import(ctx, job_id)` → `process_import(job_id)` và cập nhật mọi nơi gọi (`main.py`, `scripts/cloud_extract.py` nếu có, tests); sửa comment "Match the single ARQ worker…"
- [x] `backend/pyproject.toml`: bỏ `arq`
### Cảnh báo Starlette TestClient
- [x] Đọc release notes của Starlette/FastAPI phiên bản đang khóa trong `backend/requirements.lock` để tìm cách thay thế chuẩn (gói được cảnh báo đề xuất là `httpx2`); ghi lại nguồn và ngày đọc trong nhật ký thực hiện
- [x] Áp dụng cách sửa (thêm/ghim gói test hoặc nâng phiên bản) vào `backend/pyproject.toml` (`[project.optional-dependencies].test` nếu chỉ dùng cho test)
- [x] Sinh lại `backend/requirements.lock` và `backend/requirements.web` bằng đúng cách đang dùng (xem header của file lock); xác nhận `arq`, `redis`, `hiredis` biến mất
### Hạ tầng chạy
- [x] `compose.yaml`: xóa dịch vụ `redis`, `worker`, volume `redis-data`; `api` dùng `JOB_MODE: inline`, bỏ `REDIS_URL`, bỏ `depends_on.redis`
- [x] `.env.example`, `.env.cloud.example`: bỏ `REDIS_URL` nếu có
- [x] Kiểm tra `Dockerfile.cloud`, `backend/Dockerfile`, `scripts/cloud_start.py`, `scripts/dev.py` không còn tham chiếu Redis/ARQ
### Kiểm chứng
- [x] Thêm test: cấu hình `JOB_MODE=arq` bị từ chối (`pydantic.ValidationError`)
- [x] Thêm test: `cleanup_spool` xóa file spool quá 1 giờ và đánh dấu job treo là `failed`
- [x] `.venv/bin/python -m pytest backend/tests -q` → `57 passed in 2.24s`, 0 warning (trước đó: `53 passed, 1 warning`)
- [x] `npm --prefix frontend run typecheck` sạch; `docker compose config -q` → exit 0; services `api, db, web`
- [x] Push; CI trên `main` xanh: https://github.com/mrrayyyy/codelingo/actions/runs/42159360424 (commit `79b4a5d`, job `test`: success)
### Đồng bộ tài liệu
- [x] README: mục Docker Compose (bỏ Redis, `logs -f api worker` → `logs -f api`), cây thư mục (`imports.py`, `compose.yaml`)
- [x] `docs/kien_truc.md`: câu ngăn xếp công nghệ dòng 7, sơ đồ Mermaid (bỏ nút `Redis / ARQ` và `Python worker`, thay bằng background task/GitHub Actions), bảng cột mốc
- [x] `docs/quy_tac/dieu_huong.md`: dòng `worker ARQ`
- [x] ADR 0001: thêm ghi chú ở mục Hệ quả "một phần được thay thế bởi ADR 0004"

## Nhật ký thực hiện
- 2026-11-06: chuyển sang `dang_lam`. Mốc ban đầu: `pytest` → `53 passed, 1 warning` (`StarletteDeprecationWarning`).
- 2026-11-06: gỡ ARQ khỏi `config.py` (`job_mode: Literal["inline", "github_actions"]`, bỏ `redis_url`), `main.py` (bỏ import và nhánh `arq` trong `dispatch`), `imports.py` (bỏ `WorkerSettings`, `worker_startup`; `process_import(job_id)`, `cleanup_spool()` không còn tham số `ctx`). Không có test hay script nào khác gọi hai hàm này.
- 2026-11-06: cảnh báo Starlette: đọc `starlette/testclient.py` bản 1.10.0 đang khóa. Module này `import httpx2` trước, chỉ fallback sang `httpx` kèm cảnh báo. Đã kiểm tra metadata wheel `httpx2==2.16.0` (tác giả Tom Christie, repo `github.com/pydantic/httpx2`, BSD-3-Clause) trước khi cài. Thêm `httpx2>=2.16,<3` vào extra `test`; code app vẫn dùng `httpx`.
- 2026-11-06: gỡ `arq`, `redis`, `hiredis`, `PyJWT` (chỉ `redis` cần) khỏi venv, cài `httpx2` (+ `httpcore2`, `truststore`), cài lại editable để `pip check` sạch. Sinh lại `requirements.lock` bằng `pip freeze --exclude-editable` giữ thứ tự gốc (lockfile cũ đúng bằng output freeze). Bỏ `arq` khỏi `requirements.web`.
- 2026-11-06: `compose.yaml` còn `db`, `api` (`JOB_MODE: inline`), `web`; bỏ volume `redis-data`. `.env.example`, `.env.cloud.example`, Dockerfile, `scripts/` không có tham chiếu Redis/ARQ. `.env` cục bộ không đặt `JOB_MODE` (đã kiểm tra theo tên biến, không đọc giá trị).
- 2026-11-06: thêm `backend/tests/test_jobs.py` (2 chế độ hợp lệ, `JOB_MODE=arq` bị `ValidationError`, `cleanup_spool` xóa file/thư mục quá 1 giờ, giữ file mới, chuyển job treo quá 1 giờ sang `failed`, giữ job đang chạy). `pytest` → `57 passed`, 0 warning.
- 2026-11-06: đồng bộ README (Compose, tính năng, cây thư mục), `docs/kien_truc.md` (§1, sơ đồ, bảng cột mốc), `docs/quy_tac/dieu_huong.md`, ADR 0001 (ghi chú thay thế một phần bởi ADR 0004).
- 2026-11-06: push `c449c18`, `79b4a5d`; CI xanh (run 42159360424). Đóng ticket.

## Sai lệch
Không có thay đổi phạm vi. Thêm việc nhỏ ngoài kế hoạch gốc: gỡ cả `PyJWT` (chỉ `redis` cần) và cài lại gói editable để `pip check` sạch; ghi trong nhật ký thực hiện. Không còn tồn đọng nào cần ghi vào sổ nhật ký.
