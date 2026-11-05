---
type: infra
owner: claude
stakes: irreversible
priority: P1
opened: 2026-11-05
---

# Triển khai cấu hình đám mây (Render + Neon + GitHub Actions + Groq)

## Ngữ cảnh
Cấu hình triển khai trên đám mây ([ADR 0001](../../quyet_dinh/0001_uu_tien_cloud_mien_phi.md), [hướng dẫn](../../trien_khai_cloud.md)) chưa từng được triển khai thực tế. Chủ dự án muốn sử dụng CodeLingo hàng ngày mà không cần chạy bất cứ thứ gì trên máy tính cá nhân. Việc tạo tài khoản dịch vụ và nhập các khóa bí mật cần thực hiện trên trình duyệt của chủ dự án; Claude/agent sẽ chuẩn bị mã nguồn, kiểm tra xác minh và hoàn thiện tài liệu.

Nên thực hiện sau ticket Alembic để schema đầu tiên trên cloud đã được quản lý bằng migration.

## Tiêu chí chấp nhận
- [ ] Ứng dụng đã triển khai tải tốt sau lớp bảo vệ Basic Auth trên cả điện thoại và máy tính.
- [ ] Quy trình import repo mẫu hoàn tất thông qua GitHub Actions; tính năng xem từ vựng và ôn tập flashcard hoạt động chuẩn xác.
- [ ] Lịch sử ôn tập vẫn tồn tại nguyên vẹn sau khi Render khởi động lại (dữ liệu lưu trên Neon).
- [ ] Các tính năng Groq TTS/STT/LLM hoạt động tốt hoặc hiển thị trạng thái "chưa được cấu hình" rõ ràng.
- [ ] File `docs/xac_minh.md` ghi nhận bằng chứng có gắn ngày tháng; các thông tin hạn mức gói miễn phí trong tài liệu hướng dẫn được tái xác minh và gắn ngày.

## Kế hoạch
### Chuẩn bị
- [ ] Tái xác minh các dữ kiện về gói miễn phí trong `docs/trien_khai_cloud.md` đối chiếu với tài liệu mới nhất của Render, Neon, GitHub, Groq; ghi rõ ngày tháng
- [ ] Xác nhận các tên model Groq trong `.env.cloud.example` còn hoạt động; cập nhật lại nếu cần
- [ ] Cấu hình build `Dockerfile.cloud` trong CI (thêm job kiểm tra) thay vì build cục bộ
### Tài khoản và khóa bí mật
- [ ] `[user]` Tạo project trên Neon; giữ kín chuỗi kết nối
- [ ] `[user]` Tạo fine-grained GitHub token giới hạn quyền cho repo `mrrayyyy/codelingo`, quyền Actions: write
- [ ] `[user]` Tạo dịch vụ trên Render từ blueprint `render.yaml`; nhập các biến môi trường secret trên bảng điều khiển Render
- [ ] `[user]` Thêm secret `CODELINGO_URL` và `CODELINGO_API_KEY` vào phần GitHub Actions secrets của repo
- [ ] `[user]` Tùy chọn: Nhập Groq API key trên Render nếu muốn dùng AI giọng nói/viết
### Kiểm chứng
- [ ] `[gate]` Thực hiện lần deploy đầu tiên; kiểm tra endpoint `/api/health`
- [ ] Import repo mẫu từ đầu đến cuối; ôn tập thử một thẻ flashcard; restart dịch vụ; kiểm tra dữ liệu ôn tập vẫn còn
- [ ] Đo lường thời gian khởi động nguội sau khi app ở trạng thái ngủ; ghi lại số liệu phục vụ ticket PWA
- [ ] Đồng bộ tài liệu: xac_minh.md, hướng dẫn cloud; chuyển ticket `20261105_phien_hoc_pwa_hang_ngay.md` sang `san_sang/`

## Bán kính ảnh hưởng
- Tạo tài khoản dịch vụ cloud và các secret thực tế; nếu làm lộ `API_KEY`, `WORKSPACE_PASSWORD` hoặc GitHub token sẽ dẫn đến nguy cơ lộ dữ liệu học tập cá nhân hoặc người ngoài có thể kích hoạt runner Actions. Cách phục hồi: xoay vòng thu hồi key trên Render/GitHub, tiến hành deploy lại.
- Sau mốc này, **mỗi lần push lên `main` chính là một lần deploy** (cơ chế auto-deploy của Render). Một commit lỗi sẽ làm sập ứng dụng cho đến khi được sửa; cách phục hồi là tạo commit revert.
- Database Neon nắm giữ bản sao duy nhất của lịch sử ôn tập. Các thay đổi schema sau thời điểm này đều là ticket có mức `irreversible`, bắt buộc phải có bước sao lưu dự phòng (`pg_dump`) trước tiên.
- Các kho mã nguồn được import tại đây sẽ chạy qua các runner Actions của repo công khai; log chỉ in số lượng thống kê, nhưng chỉ import repo công khai hoặc mã nguồn thuộc quyền sở hữu (bao_mat.md).

## Nhật ký thực hiện

## Sai lệch
