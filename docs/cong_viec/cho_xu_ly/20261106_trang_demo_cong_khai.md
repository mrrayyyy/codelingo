---
type: feature
owner: claude
stakes: irreversible
priority: P2
opened: 2026-11-06
---

# Trang demo công khai với dữ liệu mẫu cho portfolio

**Bị chặn bởi (Blocked by):** [Triển khai cloud](../san_sang/20261105_trien_khai_cloud_render_neon_groq.md), [Tách router API và `get_current_user`](../san_sang/20261106_tach_router_api.md), [Hệ thống thiết kế giao diện](20261106_he_thong_thiet_ke_giao_dien.md).

## Ngữ cảnh
Chủ dự án chốt ngày 2026-11-06: CodeLingo có thể thành portfolio khi ứng tuyển, nên cần một link demo mà nhà tuyển dụng bấm thử được **không cần mật khẩu**, chạy trên dữ liệu mẫu. Bản thật của chủ dự án nằm sau Basic Auth (`WORKSPACE_PASSWORD`) và chứa lịch sử học cá nhân, nên demo tuyệt đối không được đọc hay ghi vào dữ liệu đó.

## Tiêu chí chấp nhận
- [ ] Có ADR mới (số thứ tự kế tiếp) ghi lại cách cô lập demo (tách dịch vụ/DB riêng hay dùng chung với user demo) cùng lý do; kiểm tra lại hạn mức free tier của Render/Neon trước khi chọn, có ghi ngày.
- [ ] Demo mở được bằng một URL công khai, không hỏi mật khẩu, có banner "Bản demo — dữ liệu được đặt lại định kỳ".
- [ ] Dữ liệu demo được seed từ repo mẫu Atlas API + một repo public nổi tiếng (đã có nghĩa tiếng Việt, cụm từ, bài luyện); tự đặt lại theo lịch (GitHub Actions cron) hoặc khi khởi động.
- [ ] Ở chế độ demo: tắt import repo tùy ý, tắt xuất dữ liệu, giới hạn số lượt gọi LLM/TTS/STT theo IP/ngày (hoặc dùng phản hồi dựng sẵn) để không cạn hạn mức Groq.
- [ ] Test chứng minh không route nào ở chế độ demo truy cập được dữ liệu của user thật.

## Kế hoạch
### Quyết định
- [ ] So sánh 2 phương án: (a) dịch vụ Render thứ hai + Neon branch/database riêng, `DEMO_MODE=true`; (b) cùng dịch vụ, route `/demo` gắn user demo qua `get_current_user`. Tiêu chí: mức độ cô lập dữ liệu thật, hạn mức free tier, công bảo trì
- [ ] Viết `docs/quyet_dinh/NNNN_trang_demo_cong_khai.md` (proposed, số kế tiếp) → `[user]` chủ dự án chọn → accepted
### Triển khai
- [ ] Thêm cấu hình `demo_mode` vào `backend/app/config.py`; middleware/dependency chặn các route bị tắt (import, export, xóa)
- [ ] Script seed `scripts/seed_demo.py` (idempotent) tạo user demo và dữ liệu mẫu
- [ ] Giới hạn lượt gọi AI ở chế độ demo (bộ đếm trong DB theo ngày)
- [ ] Banner demo + nút "Xem mã nguồn trên GitHub" trên frontend
- [ ] Workflow `.github/workflows/demo_reset.yml` chạy theo cron gọi endpoint reset có machine key
### Triển khai cloud
- [ ] `[gate]` Tạo dịch vụ/DB demo hoặc biến môi trường mới trên Render/Neon theo ADR trang demo
- [ ] `[user]` Thêm secret cần thiết cho workflow reset vào GitHub Actions
### Kiểm chứng
- [ ] Test cô lập demo ↔ user thật; test các route bị tắt trả 403
- [ ] Mở demo bằng cửa sổ ẩn danh trên điện thoại và máy tính; ghi bằng chứng có ngày vào `docs/xac_minh.md`
### Đồng bộ tài liệu
- [ ] `docs/trien_khai_cloud.md` (dịch vụ demo, biến môi trường), `.env.cloud.example`, README (link demo)

## Bán kính ảnh hưởng
- Một URL công khai không có mật khẩu: nếu cô lập sai, người lạ có thể đọc hoặc xóa lịch sử học thật trên Neon. Giảm thiểu bằng test cô lập bắt buộc pass trước khi deploy, `pg_dump` trước lần deploy đầu, và ưu tiên phương án tách DB nếu free tier cho phép.
- Lạm dụng API AI làm cạn hạn mức Groq của chủ dự án, khiến bản thật không dùng được AI. Giảm thiểu bằng giới hạn lượt theo IP/ngày; khi bị lạm dụng thì tắt AI ở demo bằng biến môi trường.
- Tạo thêm dịch vụ cloud là thao tác `[gate]`; phục hồi bằng cách xóa dịch vụ demo trên Render, không ảnh hưởng tới bản thật.

## Nhật ký thực hiện

## Sai lệch
