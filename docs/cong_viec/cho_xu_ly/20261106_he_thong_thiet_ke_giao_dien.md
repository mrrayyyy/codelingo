---
type: feature
owner: claude
stakes: routine
priority: P1
opened: 2026-11-06
---

# Hệ thống thiết kế giao diện: mobile-first, dark mode, mặc định tiếng Việt

**Bị chặn bởi (Blocked by):** [Tách nhỏ giao diện workspace UI](../san_sang/20261105_tach_giao_dien_workspace.md).

## Ngữ cảnh
Chủ dự án chốt ngày 2026-11-06: đầu tư **thiết kế UI chỉn chu** (dự án có thể thành portfolio), học hằng ngày trên **cả điện thoại và Mac**, giao diện **mặc định tiếng Việt** (giữ nút chuyển sang tiếng Anh). Hiện tại `frontend/components/workspace.tsx` khởi tạo `useState<Locale>("en")`; style nằm trong một file `frontend/app/globals.css`, chưa có dark mode và chưa được thiết kế cho màn hình điện thoại. PWA và phiên học hằng ngày ([ticket](20261105_phien_hoc_pwa_hang_ngay.md)) cần nền thiết kế này trước.

## Tiêu chí chấp nhận
- [ ] Design token (màu, khoảng cách, bo góc, cỡ chữ, bóng) khai báo một lần trong `:root` của `frontend/app/globals.css`; có bộ màu cho dark mode qua `prefers-color-scheme` và nút chuyển thủ công lưu trong `localStorage`.
- [ ] Locale mặc định là `vi` khi chưa có lựa chọn đã lưu; nút chuyển ngôn ngữ vẫn hoạt động; thuộc tính `lang` của `<html>` đúng.
- [ ] Ở viewport 375×812 (iPhone) không có thanh cuộn ngang trên mọi trang; điều hướng chính chuyển thành thanh tab dưới đáy; vùng chạm ≥ 44px.
- [ ] Độ tương phản chữ đạt WCAG AA ở cả hai theme (kiểm bằng Playwright + axe hoặc công cụ tương đương).
- [ ] Playwright chụp ảnh từng trang ở 3 cấu hình: desktop sáng, desktop tối, mobile sáng; ảnh lưu làm baseline và dùng lại cho README portfolio.

## Kế hoạch
### Thiết kế
- [ ] Rà các trang sau khi tách (`frontend/components/pages/*`), liệt kê component lặp lại (card, button, tag CEFR, thanh tiến độ, toast, dialog)
- [ ] Viết bộ token và component primitive trong `frontend/components/ui/` (Button, Card, Tag, Progress, Dialog, Sheet, Tabs) dùng CSS thuần, không thêm thư viện UI lớn
- [ ] Thiết kế flashcard mobile: vuốt/bấm lật thẻ, 4 nút đánh giá FSRS ở vùng ngón cái
### Áp dụng
- [ ] Thay style rời rạc trong từng trang bằng primitive; xóa CSS không còn dùng
- [ ] Layout responsive: sidebar desktop ↔ tab bar mobile
- [ ] Dark mode + nút chuyển; lưu lựa chọn
- [ ] Đổi locale mặc định sang `vi` trong module i18n (`frontend/lib/i18n.ts` tạo ở ticket tách UI); cập nhật test e2e nếu đang giả định tiếng Anh
### Kiểm chứng
- [ ] Thêm test Playwright với viewport mobile; kiểm tra không cuộn ngang
- [ ] Kiểm tra tương phản tự động; sửa các vi phạm
- [ ] Typecheck, build, e2e, CI xanh; lưu ảnh chụp vào `docs/tam/` để chủ dự án duyệt
- [ ] `[user]` Chủ dự án mở thử trên điện thoại thật và duyệt giao diện
### Đồng bộ tài liệu
- [ ] README mục "Các tính năng đã triển khai" (giao diện mặc định tiếng Việt, dark mode, mobile)

## Nhật ký thực hiện

## Sai lệch
