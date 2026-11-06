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

Cập nhật 2026-11-06: chủ dự án xác nhận dùng Render + Neon + Groq gói miễn phí; thứ tự là [bỏ ARQ/Redis](../dang_lam/20261106_bo_che_do_arq_redis.md) → [Alembic](../dang_lam/20261105_migration_alembic.md) → ticket này. Nguồn import là repo GitHub công khai (repo nổi tiếng và repo của chính chủ dự án) cùng file ZIP; không cần token cho repo private.

## Tiêu chí chấp nhận
- [ ] Ứng dụng đã triển khai tải tốt sau lớp bảo vệ Basic Auth trên cả điện thoại và máy tính.
- [ ] Quy trình import repo mẫu hoàn tất thông qua GitHub Actions; tính năng xem từ vựng và ôn tập flashcard hoạt động chuẩn xác.
- [ ] Lịch sử ôn tập vẫn tồn tại nguyên vẹn sau khi Render khởi động lại (dữ liệu lưu trên Neon).
- [ ] Các tính năng Groq TTS/STT/LLM hoạt động tốt hoặc hiển thị trạng thái "chưa được cấu hình" rõ ràng.
- [ ] File `docs/xac_minh.md` ghi nhận bằng chứng có gắn ngày tháng; các thông tin hạn mức gói miễn phí trong tài liệu hướng dẫn được tái xác minh và gắn ngày.

## Kế hoạch
### Chuẩn bị (agent tự làm)
- [ ] Tái xác minh các dữ kiện gói miễn phí trong `docs/trien_khai_cloud.md` (Render: thời gian ngủ, giờ chạy/tháng, RAM; Neon: dung lượng, compute, cơ chế sao lưu/khôi phục; GitHub Actions: phút chạy cho repo public; Groq: model, giới hạn request/token) theo tài liệu chính thức, ghi ngày tra cứu
- [ ] Xác nhận các tên model Groq trong `backend/app/config.py` và `.env.cloud.example` còn hoạt động; cập nhật nếu cần
- [ ] Thêm job CI build `Dockerfile.cloud` (chỉ build, không push) để phát hiện lỗi image trước khi Render build
- [ ] Viết checklist từng bước có ảnh/tên nút cho phần `[user]` vào `docs/trien_khai_cloud.md` để chủ dự án làm theo nhanh
- [ ] Chọn cách sao lưu: cơ chế khôi phục có sẵn của Neon theo gói free (nếu có) và/hoặc `pg_dump` thủ công trước mỗi migration. **Không** đưa bản dump lên artifact của GitHub Actions vì repo công khai
### Tài khoản và khóa bí mật
- [ ] `[user]` Tạo project trên Neon (region gần Singapore); giữ kín chuỗi kết nối
- [ ] `[user]` Tạo fine-grained GitHub token chỉ cho repo `mrrayyyy/codelingo`, quyền Actions: write
- [ ] `[user]` Tạo dịch vụ trên Render từ blueprint `render.yaml`; nhập các biến môi trường secret (`DATABASE_URL`, `WORKSPACE_PASSWORD`, `GITHUB_ACTIONS_TOKEN`, `GITHUB_ACTIONS_REPO`)
- [ ] `[user]` Thêm secret `CODELINGO_URL` và `CODELINGO_API_KEY` vào GitHub Actions secrets của repo
- [ ] `[user]` Tạo Groq API key và nhập `GROQ_API_KEY` trên Render
### Deploy và kiểm chứng
- [ ] `[gate]` Lần deploy đầu tiên (migration `0001_initial` tự chạy trên Neon trống); kiểm tra `/api/health`
- [ ] Import repo mẫu Atlas từ đầu tới cuối qua GitHub Actions; ôn thử một thẻ; restart dịch vụ; dữ liệu ôn tập vẫn còn
- [ ] Import thử một repo public nổi tiếng cỡ vừa; ghi lại thời gian Actions và số từ trích xuất (phục vụ đánh giá giới hạn)
- [ ] Thử Groq TTS/STT/LLM qua các bài đọc to, chép chính tả, viết; ghi độ trễ
- [ ] Đo thời gian khởi động nguội sau khi app ngủ (3 lần); ghi số liệu cho ticket PWA
- [ ] `[user]` Mở app trên điện thoại và Mac qua HTTPS + Basic Auth
### Đồng bộ tài liệu
- [ ] `docs/xac_minh.md` (bằng chứng có ngày, không ghi URL kèm mật khẩu), `docs/trien_khai_cloud.md`; cập nhật lộ trình
- [ ] Chuyển các ticket đang chờ triển khai cloud sang `san_sang/` nếu không còn bị chặn bởi gì khác

## Bán kính ảnh hưởng
- Tạo tài khoản dịch vụ cloud và các secret thực tế; nếu làm lộ `API_KEY`, `WORKSPACE_PASSWORD` hoặc GitHub token sẽ dẫn đến nguy cơ lộ dữ liệu học tập cá nhân hoặc người ngoài có thể kích hoạt runner Actions. Cách phục hồi: xoay vòng thu hồi key trên Render/GitHub, tiến hành deploy lại.
- Sau mốc này, **mỗi lần push lên `main` chính là một lần deploy** (cơ chế auto-deploy của Render). Một commit lỗi sẽ làm sập ứng dụng cho đến khi được sửa; cách phục hồi là tạo commit revert.
- Database Neon nắm giữ bản sao duy nhất của lịch sử ôn tập. Các thay đổi schema sau thời điểm này đều là ticket có mức `irreversible`, bắt buộc phải có bước sao lưu dự phòng (`pg_dump`) trước tiên.
- Các kho mã nguồn được import tại đây sẽ chạy qua các runner Actions của repo công khai; log chỉ in số lượng thống kê, nhưng chỉ import repo công khai hoặc mã nguồn thuộc quyền sở hữu (bao_mat.md).

## Nhật ký thực hiện

## Sai lệch
