---
type: feature
owner: claude
stakes: irreversible
priority: P1
opened: 2026-11-05
---

# PWA có thể cài đặt và phiên học 10 phút mỗi ngày

**Bị chặn bởi (Blocked by):** [Triển khai cloud](../san_sang/20261105_trien_khai_cloud_render_neon_groq.md) (cần có URL đã triển khai và đo lường thời gian khởi động nguội thực tế) và [Tách nhỏ giao diện workspace UI](../san_sang/20261105_tach_giao_dien_workspace.md), [Hệ thống thiết kế giao diện](20261106_he_thong_thiet_ke_giao_dien.md).

## Ngữ cảnh
Các bài luyện tập hiện đang nằm rải rác ở các trang riêng biệt; để hình thành thói quen học hàng ngày cần có một nút bấm duy nhất. Gói miễn phí của Render sẽ tự động ngủ khi nhàn rỗi, khiến lần mở app đầu tiên trong ngày có thể bị chậm. Một ứng dụng PWA có thể cài đặt lên màn hình chính với vỏ tĩnh (static shell) được cache sẵn sẽ hiển thị màn hình học tập ngay lập tức kèm thông báo trạng thái "đang đánh thức server" rõ ràng thay vì một trang trắng đơ.

Cập nhật 2026-11-06: chủ dự án chốt phiên học **khoảng 10 phút**, dùng trên **điện thoại và Mac**. Khi chưa có plugin nói/nghe mới, phiên học dùng tạm `dictation` (nghe) và `read_aloud` (nói) hiện có; khi các plugin `speaking.roleplay` và `listening.meeting` hoàn thành thì đổi sang chúng qua cấu hình, không phải sửa luồng phiên học.

## Tiêu chí chấp nhận
- [ ] Có thể cài đặt lên màn hình chính iOS/Android (manifest, icons, service worker chỉ cache vỏ tĩnh giao diện — không cache dữ liệu học tập trong trình duyệt).
- [ ] Màn hình "Hôm nay" (Today): ôn tập các thẻ đến hạn (giới hạn tối đa 15 thẻ) → 1 bài tập nghe → 1 bài tập nói → màn hình tổng kết phiên học, kéo dài khoảng 10 phút.
- [ ] Trạng thái khởi động nguội (cold start) hiển thị văn bản tiến trình rõ ràng, không báo lỗi; tự động retry cho đến khi API phản hồi.
- [ ] Bảng điều khiển (dashboard) hiển thị số phút luyện tập và số lượt làm bài theo từng kỹ năng trong 7 ngày gần nhất.

## Kế hoạch
### Chuẩn bị
- [ ] Đọc tài liệu manifest/PWA và metadata của bản Next.js đang dùng trong `frontend/node_modules/next/dist/docs/` (bản này khác dữ liệu huấn luyện, xem `frontend/AGENTS.md`)
- [ ] Lấy số đo khởi động nguội từ nhật ký của ticket triển khai cloud
### Backend
- [ ] Endpoint `GET /session/today` (router `backend/app/routes/session.py`): trả về tối đa 15 thẻ đến hạn, 1 bài nghe, 1 bài nói theo danh sách plugin cấu hình được (`session_listening_plugin`, `session_speaking_plugin` trong `config.py`, mặc định `dictation` / `read_aloud`)
- [ ] Ghi nhận thời lượng: thêm cột `duration_ms` vào `attempts` (migration Alembic) và gửi kèm từ frontend; thẻ ôn tập dùng thời gian giữa lúc lật và lúc đánh giá
- [ ] Endpoint thống kê 7 ngày: số phút và số lượt theo kỹ năng (`speaking | listening | reading | writing | vocabulary`) theo múi giờ `settings.timezone`
### Frontend
- [ ] Manifest (tên, icon 192/512 + maskable, `theme_color` theo design token, `display: standalone`), icon Apple touch
- [ ] Service worker chỉ cache shell tĩnh (HTML khung, JS/CSS, font, icon); **không** cache response `/api/*`
- [ ] Trang "Hôm nay": ôn thẻ → bài nghe → bài nói → tổng kết (số thẻ, điểm, thời gian, chuỗi ngày); chọn hoàn thành từng phần, có thể dừng giữa chừng
- [ ] Trạng thái khởi động nguội: gọi `/api/health` với backoff, hiển thị "Đang đánh thức máy chủ… (lần đầu trong ngày có thể mất khoảng N giây)" theo số đo thực tế; không hiển thị lỗi đỏ khi đang chờ
- [ ] Dashboard: biểu đồ cột 7 ngày theo kỹ năng (CSS/SVG nhẹ, không thêm thư viện biểu đồ lớn)
### Kiểm chứng
- [ ] Test API cho `/session/today` (giới hạn 15 thẻ, fallback plugin) và thống kê 7 ngày (ranh giới múi giờ)
- [ ] Playwright: luồng phiên học trên viewport mobile; kiểm tra manifest hợp lệ và service worker đăng ký được
- [ ] `[gate]` Push commit chứa migration `duration_ms` theo `docs/quy_trinh/tao_migration.md` (`pg_dump` trước)
- [ ] `[user]` Cài PWA lên màn hình chính điện thoại; học thử 3 ngày liên tiếp và phản hồi
### Đồng bộ tài liệu
- [ ] README "Các tính năng đã triển khai", `docs/kien_truc.md` (route mới, cột `duration_ms`), lộ trình

## Bán kính ảnh hưởng
- Ticket này thêm migration schema. Sau khi đã deploy, mỗi lần push lên `main` là một lần deploy và migration chạy thẳng trên Neon, nơi giữ bản sao duy nhất của lịch sử học tập. Migration lỗi có thể làm app không khởi động được hoặc làm hỏng dữ liệu.
- Giảm thiểu: làm theo `docs/quy_trinh/tao_migration.md`. Migration chỉ **thêm** cột/bảng (cột mới nullable hoặc có default), không xóa hay đổi tên trong cùng đợt; chạy thử trên SQLite và PostgreSQL trong CI; `pg_dump` Neon ngay trước khi push commit chứa migration.
- Phục hồi: revert commit để app chạy lại; nếu dữ liệu đã hỏng thì khôi phục từ bản dump vừa tạo (thao tác `[gate]`).

## Nhật ký thực hiện

## Sai lệch
