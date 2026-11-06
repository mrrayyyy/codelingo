---
type: refactor
owner: claude
stakes: routine
priority: P1
opened: 2026-11-06
---

# Tách `main.py` thành các APIRouter và chuẩn hóa cách lấy người dùng hiện tại

## Ngữ cảnh
`backend/app/main.py` dồn 26 route vào 549 dòng ([mục nhật ký](../../nhat_ky/da_giai_quyet/no_ky_thuat_20261105_main_py_mot_module.md)). Các plugin luyện nói/nghe và phiên học hằng ngày sẽ thêm nhiều route nữa. Ngoài ra, ngày 2026-11-06 chủ dự án chốt hướng "chuẩn bị schema cho đa người dùng, chưa làm đăng nhập" (dự án có thể thành portfolio hoặc mở cho người dùng khác). Schema đã có `user_id` trên `repos`, `vocab_items`, `attempts`, `review_schedule` (`backend/app/db.py`), nên phần còn thiếu là bảo đảm **mọi truy vấn** đều đi qua một dependency `current_user` duy nhất và có test chứng minh dữ liệu không lẫn giữa các user. Trang demo công khai sau này ([ticket](../cho_xu_ly/20261106_trang_demo_cong_khai.md)) cũng dựa vào dependency này.

Không thay đổi hành vi người dùng.

## Tiêu chí chấp nhận
- [ ] `backend/app/main.py` chỉ còn tạo app, lifespan, middleware và `include_router`; dưới 120 dòng.
- [ ] Các module `backend/app/routes/{profile,dashboard,imports,vocab,review,export,practice,speech,cloud}.py` dùng `APIRouter`, giữ nguyên path, method, status code và schema response.
- [ ] Một dependency `get_current_user` (trong `backend/app/deps.py`) là nguồn duy nhất cung cấp user cho mọi route dữ liệu; `grep` không còn chỗ nào tự lấy user mặc định.
- [ ] Test cách ly: tạo 2 user, import dữ liệu cho user A, mọi route đọc/ghi của user B không thấy hoặc không sửa được dữ liệu của A.
- [ ] Toàn bộ test hiện có pass mà không sửa assertion; snapshot OpenAPI (`app.openapi()`) trước và sau giống nhau về path/method.

## Kế hoạch
### Chuẩn bị
- [ ] Lưu snapshot OpenAPI hiện tại vào `docs/tam/20261106_tach_router/openapi_truoc.json` (git-ignored) để so sánh
- [ ] Liệt kê cách mỗi route hiện lấy user (đọc `main.py`, `db.py`) và ghi vào nhật ký thực hiện
### Tách module
- [ ] Tạo `backend/app/deps.py`: `get_db` (session), `get_current_user` (hiện trả về user đơn mặc định, sẵn chỗ cho auth/demo sau này), `require_key`, `require_machine_key` cho route cloud
- [ ] Tạo `backend/app/routes/` và chuyển từng nhóm route, mỗi nhóm một commit: profile+dashboard → imports+jobs+repos → vocab+dictionary → review → export → practice+speech → cloud callbacks
- [ ] Chuyển các helper dùng chung (serialize vocab, tính streak…) sang `backend/app/services/` nếu được dùng bởi hơn một router
### Kiểm chứng
- [ ] Thêm `backend/tests/test_isolation.py` theo tiêu chí cách ly ở trên
- [ ] So sánh OpenAPI sau khi tách với snapshot → chỉ khác thứ tự/tags
- [ ] `pytest`, typecheck, CI xanh; chạy `scripts/dev.py` và bấm thử import mẫu → ôn tập
### Đồng bộ tài liệu
- [ ] README cây thư mục backend; `docs/kien_truc.md` mục cấu trúc backend và nguyên tắc "mọi route dữ liệu dùng `get_current_user`"; `docs/quy_tac/dieu_huong.md` bảng tra cứu file

## Nhật ký thực hiện

## Sai lệch
