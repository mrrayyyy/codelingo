---
type: infra
owner: claude
stakes: routine
priority: P1
opened: 2026-11-05
---

# Tích hợp công cụ migration schema bằng Alembic trước khi có dữ liệu trên cloud

## Ngữ cảnh
Schema cơ sở dữ liệu hiện tại được khởi tạo bằng SQLAlchemy `create_all` (README đã lưu ý: "không dùng làm chiến lược nâng cấp schema"). Giai đoạn 2 của lộ trình sẽ thêm các cột dữ liệu mới (nghĩa tiếng Việt, cụm từ vựng). Một khi lịch sử học tập đã được lưu trữ trên Neon, việc thay đổi schema mà không có công cụ migration sẽ đồng nghĩa với việc phải chạy SQL thủ công hoặc đối mặt nguy cơ mất dữ liệu. Thực hiện việc này trước lần deploy đầu tiên giúp giữ rủi ro ở mức `routine`; sau khi đã deploy, mọi migration đều thuộc diện `irreversible`.

Cập nhật 2026-11-06: làm **sau** [ticket bỏ ARQ/Redis](../hoan_thanh/20261106_bo_che_do_arq_redis.md) (Giai đoạn 0). Schema hiện đã có `user_id` trên các bảng chính; revision cơ sở phải giữ nguyên để sẵn sàng cho đa người dùng (chủ dự án chốt: chuẩn bị schema, chưa làm đăng nhập). Hiện `init_db()` (`backend/app/db.py`) gọi `create_all` rồi seed user `local-user`; test (`backend/tests/conftest.py`) dùng `Base.metadata.drop_all` + lifespan.

## Tiêu chí chấp nhận
- [x] Lệnh `alembic upgrade head` khởi tạo schema hiện tại thành công trên cả SQLite trống và PostgreSQL trống.
- [x] Bản revision cơ sở khớp chính xác với `create_all` (autogenerate không sinh ra diff sai lệch).
- [x] Quá trình khởi động API tự động chạy migrations (hoặc từ chối khởi động nếu schema lỗi thời) trên mọi chế độ job.
- [x] Toàn bộ bộ test chạy trên schema đã được migrate; CI báo xanh ([run 42159839436](https://github.com/mrrayyyy/codelingo/actions/runs/42159839436): `test` và `migrations` success).
- [x] README và kien_truc.md cập nhật hướng dẫn cách tạo và áp dụng migration mới.

## Kế hoạch
### Cài đặt ban đầu
- [x] Thêm `alembic` vào `backend/pyproject.toml`; sinh lại `backend/requirements.lock` và `backend/requirements.web` (bản web cần alembic vì API tự migrate khi khởi động)
- [x] Đặt `naming_convention` cho `Base.metadata` trong `backend/app/db.py` để tên constraint/index giống nhau trên SQLite và PostgreSQL (chưa có DB production nên đổi tên lúc này là an toàn)
- [x] (đổi vị trí, xem Sai lệch) Tạo `backend/alembic.ini` + `backend/app/migrations/env.py`: đọc `settings.database_url`, `target_metadata = Base.metadata`, `render_as_batch=True` khi dialect là SQLite (SQLite không hỗ trợ đủ `ALTER TABLE`), `compare_type=True`
- [x] Sinh revision `0001_initial` bằng autogenerate, đọc lại bằng tay (kiểu JSON, index, unique constraint, `ondelete`)
### Kết nối vào hệ thống
- [x] `backend/app/db.py`: `init_db()` gọi `alembic.command.upgrade(cfg, "head")` thay cho `create_all`, giữ phần seed `local-user`; đường dẫn `alembic.ini` tính từ package, không phụ thuộc cwd
- [x] DB cục bộ cũ tạo bằng `create_all` (có bảng nhưng không có `alembic_version`): phát hiện trường hợp này, so schema với `0001_initial`; nếu khớp thì `stamp head`, nếu lệch thì dừng và in hướng dẫn rõ ràng (không tự xóa dữ liệu)
- [x] Kiểm tra `scripts/cloud_start.py`, `scripts/dev.py`, `Dockerfile.cloud`, `backend/Dockerfile` vẫn khởi động đúng (migration chạy trong lifespan); bảo đảm file `alembic/` được copy vào image
- [x] `backend/tests/conftest.py`: fixture tạo DB bằng migration (`downgrade base` + `upgrade head` hoặc file SQLite mới mỗi test) thay cho `drop_all`
### Kiểm chứng
- [x] Test `backend/tests/test_migrations.py`: upgrade trên SQLite trống; autogenerate so với model → không có diff (`alembic check`)
- [x] CI (`.github/workflows/ci.yml`): thêm job dùng service container `postgres:17` chạy `alembic upgrade head` + `alembic check` (máy cá nhân không cần chạy Docker)
- [x] `pytest` → 61 passed, typecheck sạch, CI xanh: https://github.com/mrrayyyy/codelingo/actions/runs/42159839436
### Đồng bộ tài liệu
- [x] Tạo quy trình `docs/quy_trinh/tao_migration.md`: tạo revision, đọc lại, chạy thử trên SQLite và PostgreSQL CI, và **sau khi đã deploy**: `pg_dump` Neon trước, đánh dấu `[gate]`, áp dụng, kiểm tra, cách rollback
- [x] README mục "Chạy trực tiếp không cần Docker" (migration tự chạy; lệnh tạo revision); `docs/kien_truc.md` mục dữ liệu (bỏ ghi chú `create_all`); `docs/quy_tac/dieu_huong.md` (vị trí `backend/alembic/`)

## Nhật ký thực hiện
- 2026-11-06: chuyển sang `dang_lam`. Cài `alembic==1.20.1` (+ `Mako==1.4.3`).
- 2026-11-06: `backend/app/db.py`: `NAMING_CONVENTION` trên `Base.metadata` (unique dùng `column_0_N_name` để không trùng tên); `alembic_config()` cấu hình bằng code (không phụ thuộc cwd); `migrate()` + `init_db()` chạy `upgrade head` thay cho `create_all`, giữ seed `local-user`.
- 2026-11-06: migration đặt trong `backend/app/migrations/` (`env.py` tái dùng connection của caller, `render_as_batch` cho SQLite, `compare_type`); `backend/alembic.ini` chỉ dùng cho CLI. Sinh `0001_initial` bằng autogenerate trên SQLite trống, đọc lại: 11 bảng, đủ FK `ondelete`, unique, index `ix_review_schedule_due`; đổi `batch_alter_table` sang `op.create_index` để chạy giống nhau trên PostgreSQL.
- 2026-11-06: DB cũ tạo bằng `create_all`: so sánh bằng `compare_metadata`, khớp thì `stamp 0001_initial`, lệch thì `RuntimeError` và không sửa gì. Lần chạy đầu phát hiện SQLite không phản chiếu được `UNIQUE` không tên ở cấp cột (`attempts.submission_id`) dù index unique vẫn có; thêm `_sqlite_unique_index_exists` kiểm tra bằng `PRAGMA index_list/index_info`.
- 2026-11-06: `conftest.py` xóa cả `alembic_version` để lifespan dựng DB qua migration ở mỗi test. Thêm `backend/tests/test_migrations.py` (DB trống → head khớp model; downgrade base ↔ upgrade; DB cũ khớp được nhận và giữ dữ liệu; DB cũ lệch bị từ chối, không đổi). `pytest` → `61 passed`.
- 2026-11-06: CLI `alembic -c backend/alembic.ini upgrade head` + `check` trên SQLite → "No new upgrade operations detected". Thêm job `migrations` trong `ci.yml` (service `postgres:17-alpine`, xác thực `trust`, upgrade → check → downgrade base → upgrade → check).
- 2026-11-06: tài liệu: tạo `docs/quy_trinh/tao_migration.md`; cập nhật README (mục chạy không cần Docker, cây thư mục, bỏ "migration Alembic" khỏi phạm vi còn lại), `docs/kien_truc.md` (đoạn schema dưới ERD), `docs/quy_tac/dieu_huong.md`. Dockerfile không cần sửa vì cả hai image copy `backend/app` (gồm `migrations/`); `requirements.web` thêm `alembic`.

- 2026-11-06: push `adba75e`, `f7819de`; CI xanh, job `migrations` chạy upgrade → check → downgrade → upgrade → check trên PostgreSQL 17 thành công (https://github.com/mrrayyyy/codelingo/actions/runs/42159839436). Đóng ticket.

## Sai lệch
- Migration nằm trong `backend/app/migrations/` thay vì `backend/alembic/` như kế hoạch: thư mục này tự đi theo `COPY backend/app ./app` vào cả `Dockerfile.cloud` lẫn `backend/Dockerfile`, không phải sửa Dockerfile hay khai báo package data.
- Thêm xử lý giới hạn phản chiếu UNIQUE của SQLite (ngoài kế hoạch), cần để nhận DB cũ đúng.
- Tiếp nối ở ticket triển khai cloud: Neon khuyến nghị dùng kết nối trực tiếp cho migration, nên biến tùy chọn `MIGRATION_DATABASE_URL` được thêm ở ticket đó.
