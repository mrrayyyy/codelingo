---
type: feature
owner: claude
stakes: routine
priority: P1
skill: reading
opened: 2026-11-06
---

# Import được repo GitHub public lớn (repo nổi tiếng) và chỉ một thư mục con

**Bị chặn bởi (Blocked by):** [Triển khai cloud](../san_sang/20261105_trien_khai_cloud_render_neon_groq.md) (cần số đo thực tế của runner GitHub Actions).

## Ngữ cảnh
Ngày 2026-11-06 chủ dự án chọn nguồn học chính là **repo GitHub public nổi tiếng** và repo của chính mình. Hiện tại `download_github` (`backend/app/imports.py`) tải `codeload.github.com/<owner>/<repo>/zip/HEAD` và dừng khi vượt `max_upload_bytes` = 20 MiB; `unpack_archive` giới hạn 5.000 file và 50 MiB sau giải nén (`backend/app/config.py`); callback `/cloud/jobs/{id}/complete` nhận tối đa 500 mục. Các repo nổi tiếng thường lớn hơn nhiều mức này, nên hôm nay hầu như không import được. Ở chế độ `github_actions`, việc tải và trích xuất chạy trên runner (`scripts/cloud_extract.py`), không chạy trên Render, nên có thể nới giới hạn riêng cho runner mà không làm nặng web service miễn phí.

## Tiêu chí chấp nhận
- [ ] Import được URL dạng `https://github.com/<owner>/<repo>/tree/<ref>/<path>`: chỉ trích xuất thư mục con đó (ví dụ `docs/` hoặc một package).
- [ ] Ở chế độ `github_actions`, giới hạn tải/giải nén/số file cấu hình riêng cho runner qua biến môi trường trong `.github/workflows/extract.yml`; web service (chế độ `inline`/upload ZIP) giữ giới hạn hiện tại.
- [ ] Bỏ qua thư mục/file không có giá trị học: `node_modules`, `vendor`, `dist`, `build`, file minified, lockfile, file sinh tự động, fixture nhị phân — áp dụng cả khi đếm giới hạn.
- [ ] Import thành công ít nhất 2 repo public nổi tiếng cỡ lớn (chọn khi làm, ghi tên, kích thước, thời gian runner, số từ) và không vượt hạn mức GitHub Actions.
- [ ] Vẫn giữ mọi bảo vệ an toàn hiện có (không `extractall`, chặn path traversal/symlink, không thực thi code, lọc secret).

## Kế hoạch
### Khảo sát
- [ ] Đo kích thước archive và số file của 3–5 repo nổi tiếng ứng viên; ghi kết quả có ngày
- [ ] So sánh cách tải trên runner: zip codeload hiện tại + lọc khi giải nén, hoặc `git clone --depth 1 --filter=blob:none --sparse` cho thư mục con (git không thực thi hook khi clone; vẫn cần kiểm tra an toàn). Ghi lựa chọn và lý do vào nhật ký thực hiện
### Triển khai
- [ ] `github_repository()` chấp nhận thêm `/tree/<ref>/<path>`; validate `ref` và `path` (không `..`, độ dài giới hạn); lưu `ref`/`path` vào `repos` (cột mới qua Alembic nếu cần → nâng `stakes` lên `irreversible` và làm theo `docs/quy_trinh/tao_migration.md`)
- [ ] Bộ lọc thư mục/file bỏ qua trong `unpack_archive`/`extraction.py`, có danh sách cấu hình
- [ ] Giới hạn theo môi trường: `MAX_UPLOAD_BYTES`, `MAX_EXPANDED_BYTES`, `MAX_FILES` lớn hơn trong `extract.yml`; giữ mặc định nhỏ cho web
- [ ] Xem lại giới hạn 500 mục ở callback: giữ top N theo điểm xếp hạng, có thông báo trong UI ("đã giữ N từ giá trị nhất")
- [ ] UI hộp thoại import: gợi ý dán link thư mục con cho repo lớn; thông báo lỗi giới hạn dễ hiểu bằng tiếng Việt
### Kiểm chứng
- [ ] Test: phân tích URL `/tree/`, chặn path độc hại, bộ lọc bỏ qua, giới hạn khác nhau theo chế độ
- [ ] Import thật 2 repo lớn qua Actions; ghi số liệu vào `docs/xac_minh.md`
### Đồng bộ tài liệu
- [ ] README (giới hạn import, link thư mục con), `docs/trien_khai_cloud.md` (biến môi trường của runner), `docs/kien_truc.md` §4

## Nhật ký thực hiện

## Sai lệch
