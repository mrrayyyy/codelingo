---
type: feature
owner: claude
stakes: routine
priority: P1
opened: 2026-11-05
---

# PWA có thể cài đặt và phiên học 10 phút mỗi ngày

**Bị chặn bởi (Blocked by):** [Triển khai cloud](../san_sang/20261105_trien_khai_cloud_render_neon_groq.md) (cần có URL đã triển khai và đo lường thời gian khởi động nguội thực tế) và [Tách nhỏ giao diện workspace UI](../san_sang/20261105_tach_giao_dien_workspace.md).

## Ngữ cảnh
Các bài luyện tập hiện đang nằm rải rác ở các trang riêng biệt; để hình thành thói quen học hàng ngày cần có một nút bấm duy nhất. Gói miễn phí của Render sẽ tự động ngủ khi nhàn rỗi, khiến lần mở app đầu tiên trong ngày có thể bị chậm. Một ứng dụng PWA có thể cài đặt lên màn hình chính với vỏ tĩnh (static shell) được cache sẵn sẽ hiển thị màn hình học tập ngay lập tức kèm thông báo trạng thái "đang đánh thức server" rõ ràng thay vì một trang trắng đơ.

## Tiêu chí chấp nhận
- [ ] Có thể cài đặt lên màn hình chính iOS/Android (manifest, icons, service worker chỉ cache vỏ tĩnh giao diện — không cache dữ liệu học tập trong trình duyệt).
- [ ] Màn hình "Hôm nay" (Today): ôn tập các thẻ đến hạn (giới hạn tối đa 15 thẻ) → 1 bài tập nghe → 1 bài tập nói → màn hình tổng kết phiên học, kéo dài khoảng 10 phút.
- [ ] Trạng thái khởi động nguội (cold start) hiển thị văn bản tiến trình rõ ràng, không báo lỗi; tự động retry cho đến khi API phản hồi.
- [ ] Bảng điều khiển (dashboard) hiển thị số phút luyện tập và số lượt làm bài theo từng kỹ năng trong 7 ngày gần nhất.

## Kế hoạch

## Nhật ký thực hiện

## Sai lệch
