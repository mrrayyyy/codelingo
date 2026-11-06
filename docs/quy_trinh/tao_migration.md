# Tạo và áp dụng migration schema

Quy trình dùng mỗi lần thay đổi mô hình dữ liệu trong `backend/app/db.py`. Schema được quản lý bằng Alembic; các revision nằm trong `backend/app/migrations/versions/`. API tự chạy `upgrade head` khi khởi động (`init_db()` trong `backend/app/db.py`), nên **mỗi lần deploy là mỗi lần migration chạy trên database thật**.

## 1. Viết revision

```sh
# Sửa model trong backend/app/db.py trước, rồi từ thư mục gốc của repo:
DATABASE_URL=sqlite:////tmp/codelingo-rev.db .venv/bin/alembic -c backend/alembic.ini upgrade head
DATABASE_URL=sqlite:////tmp/codelingo-rev.db .venv/bin/alembic -c backend/alembic.ini \
  revision --autogenerate -m "<mô tả ngắn>" --rev-id NNNN_<slug>
```

- Đặt `--rev-id` theo số thứ tự kế tiếp (`0002_...`, `0003_...`) để thứ tự đọc được bằng mắt.
- **Đọc lại file sinh ra bằng tay.** Autogenerate không nhận ra đổi tên cột/bảng (nó sinh lệnh xóa rồi tạo mới, làm mất dữ liệu), không sinh dữ liệu mặc định cho bản ghi cũ và có thể bỏ sót kiểu dữ liệu.
- Ưu tiên migration chỉ **thêm**: cột mới phải `nullable=True` hoặc có `server_default`, để các dòng đã có trên Neon vẫn hợp lệ. Xóa hoặc đổi tên thì tách ra một đợt riêng, sau khi code đã ngừng dùng cột cũ.
- Tên constraint được sinh tự động theo `NAMING_CONVENTION` trong `db.py`; không đặt tên tay.
- SQLite chạy ở chế độ batch (`render_as_batch`) nên các lệnh `ALTER` phức tạp vẫn chạy được ở dev/test.
- Viết `downgrade()` đầy đủ trừ khi không thể; nếu không thể thì ghi rõ lý do trong docstring của revision.

## 2. Kiểm chứng trước khi push

```sh
.venv/bin/python -m pytest backend/tests -q        # test dựng DB qua migration; test_migrations.py so schema với model
DATABASE_URL=sqlite:////tmp/codelingo-rev.db .venv/bin/alembic -c backend/alembic.ini check   # phải in "No new upgrade operations detected"
```

Job `migrations` trong CI chạy `upgrade head → check → downgrade base → upgrade head → check` trên PostgreSQL 17, giống Neon. Không cần chạy PostgreSQL trên máy cá nhân.

## 3. Áp dụng lên môi trường đã deploy (thao tác `[gate]`)

Sau lần deploy đầu tiên, commit chứa migration thuộc diện `stakes: irreversible` ([thuc_thi.md](../quy_tac/thuc_thi.md)):

1. Ticket phải có mục `## Bán kính ảnh hưởng` mô tả migration.
2. Xin phê duyệt của chủ dự án trước khi push commit đó: nêu hành động, bảng/cột bị ảnh hưởng và cách phục hồi.
3. Sao lưu ngay trước khi push: `pg_dump "$NEON_DATABASE_URL" --format=custom --file codelingo-YYYYMMDD.dump`, chạy từ máy chủ dự án; lưu file ngoài repo. **Không** đưa bản dump lên artifact của GitHub Actions (repo công khai).
4. Push → Render build và khởi động → kiểm tra `/api/health` cùng một luồng đọc/ghi (ôn một thẻ).
5. Ghi bằng chứng có ngày vào nhật ký thực hiện của ticket.

## 4. Phục hồi

- App không khởi động sau migration: revert commit và push lại. Nếu migration đã chạy một phần, kiểm tra bảng `alembic_version` và trạng thái schema trước khi chạy lại.
- Dữ liệu hỏng: khôi phục từ bản dump vừa tạo bằng `pg_restore` (thao tác `[gate]`), sau đó revert code về revision tương ứng.

## Database tạo trước khi có Alembic

Database cục bộ tạo bằng `create_all()` cũ (có bảng nhưng không có `alembic_version`) được tự nhận khi khởi động nếu schema khớp `0001_initial` (Alembic `stamp`, dữ liệu giữ nguyên). Nếu lệch, API từ chối khởi động với thông báo hướng dẫn và không sửa gì: sao lưu file/dump, sau đó xóa database đó hoặc tự migrate bằng tay.
