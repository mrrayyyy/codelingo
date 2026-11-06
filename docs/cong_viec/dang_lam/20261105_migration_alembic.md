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
- [ ] Lệnh `alembic upgrade head` khởi tạo schema hiện tại thành công trên cả SQLite trống và PostgreSQL trống.
- [ ] Bản revision cơ sở khớp chính xác với `create_all` (autogenerate không sinh ra diff sai lệch).
- [ ] Quá trình khởi động API tự động chạy migrations (hoặc từ chối khởi động nếu schema lỗi thời) trên mọi chế độ job.
- [ ] Toàn bộ bộ test chạy trên schema đã được migrate; CI báo xanh.
- [ ] README và kien_truc.md cập nhật hướng dẫn cách tạo và áp dụng migration mới.

## Kế hoạch
### Cài đặt ban đầu
- [ ] Thêm `alembic` vào `backend/pyproject.toml`; sinh lại `backend/requirements.lock` và `backend/requirements.web` (bản web cần alembic vì API tự migrate khi khởi động)
- [ ] Đặt `naming_convention` cho `Base.metadata` trong `backend/app/db.py` để tên constraint/index giống nhau trên SQLite và PostgreSQL (chưa có DB production nên đổi tên lúc này là an toàn)
- [ ] Tạo `backend/alembic.ini` + `backend/alembic/env.py`: đọc `settings.database_url`, `target_metadata = Base.metadata`, `render_as_batch=True` khi dialect là SQLite (SQLite không hỗ trợ đủ `ALTER TABLE`), `compare_type=True`
- [ ] Sinh revision `0001_initial` bằng autogenerate, đọc lại bằng tay (kiểu JSON, index, unique constraint, `ondelete`)
### Kết nối vào hệ thống
- [ ] `backend/app/db.py`: `init_db()` gọi `alembic.command.upgrade(cfg, "head")` thay cho `create_all`, giữ phần seed `local-user`; đường dẫn `alembic.ini` tính từ package, không phụ thuộc cwd
- [ ] DB cục bộ cũ tạo bằng `create_all` (có bảng nhưng không có `alembic_version`): phát hiện trường hợp này, so schema với `0001_initial`; nếu khớp thì `stamp head`, nếu lệch thì dừng và in hướng dẫn rõ ràng (không tự xóa dữ liệu)
- [ ] Kiểm tra `scripts/cloud_start.py`, `scripts/dev.py`, `Dockerfile.cloud`, `backend/Dockerfile` vẫn khởi động đúng (migration chạy trong lifespan); bảo đảm file `alembic/` được copy vào image
- [ ] `backend/tests/conftest.py`: fixture tạo DB bằng migration (`downgrade base` + `upgrade head` hoặc file SQLite mới mỗi test) thay cho `drop_all`
### Kiểm chứng
- [ ] Test `backend/tests/test_migrations.py`: upgrade trên SQLite trống; autogenerate so với model → không có diff (`alembic check`)
- [ ] CI (`.github/workflows/ci.yml`): thêm job dùng service container `postgres:17` chạy `alembic upgrade head` + `alembic check` (máy cá nhân không cần chạy Docker)
- [ ] `pytest`, typecheck, CI xanh (dẫn link run)
### Đồng bộ tài liệu
- [ ] Tạo quy trình `docs/quy_trinh/tao_migration.md`: tạo revision, đọc lại, chạy thử trên SQLite và PostgreSQL CI, và **sau khi đã deploy**: `pg_dump` Neon trước, đánh dấu `[gate]`, áp dụng, kiểm tra, cách rollback
- [ ] README mục "Chạy trực tiếp không cần Docker" (migration tự chạy; lệnh tạo revision); `docs/kien_truc.md` mục dữ liệu (bỏ ghi chú `create_all`); `docs/quy_tac/dieu_huong.md` (vị trí `backend/alembic/`)

## Nhật ký thực hiện

## Sai lệch
