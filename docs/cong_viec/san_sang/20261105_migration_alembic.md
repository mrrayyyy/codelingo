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

## Tiêu chí chấp nhận
- [ ] Lệnh `alembic upgrade head` khởi tạo schema hiện tại thành công trên cả SQLite trống và PostgreSQL trống.
- [ ] Bản revision cơ sở khớp chính xác với `create_all` (autogenerate không sinh ra diff sai lệch).
- [ ] Quá trình khởi động API tự động chạy migrations (hoặc từ chối khởi động nếu schema lỗi thời) trên mọi chế độ job.
- [ ] Toàn bộ bộ test chạy trên schema đã được migrate; CI báo xanh.
- [ ] README và kien_truc.md cập nhật hướng dẫn cách tạo và áp dụng migration mới.

## Kế hoạch
### Cài đặt ban đầu
- [ ] Thêm `alembic` vào `backend/pyproject.toml` và sinh lại `backend/requirements.lock`
- [ ] Khởi tạo thư mục `backend/alembic/` với `env.py` đọc `settings.database_url` và `db.Base.metadata`
- [ ] Tạo revision cơ sở `0001_initial` từ các model hiện tại trong `backend/app/db.py`
### Kết nối vào hệ thống
- [ ] Thay thế lệnh `create_all` trong vòng đời API (`backend/app/main.py`) bằng lệnh nâng cấp lên head
- [ ] Cập nhật tương tự cho `scripts/cloud_start.py` và dịch vụ `api` trong Compose
- [ ] Cấu hình `backend/tests/conftest.py` khởi tạo DB test thông qua migration
### Kiểm chứng và cập nhật tài liệu
- [ ] Chạy autogenerate so với bản cơ sở → diff rỗng
- [ ] Chạy pytest, typecheck; bảo đảm CI báo xanh (dẫn link run)
- [ ] Đồng bộ tài liệu: mục "Chạy trực tiếp không cần Docker" trong README, ghi chú về migration trong kien_truc.md

## Nhật ký thực hiện

## Sai lệch
