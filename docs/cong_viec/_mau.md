---
type: feature | content | refactor | infra | docs | investigation
owner: claude | user
stakes: routine | irreversible
priority: P1 | P2 | P3
skill: speaking | listening | reading | writing | vocabulary   # tùy chọn, chỉ dùng cho ticket sản phẩm
opened: YYYY-MM-DD
---

# Tiêu đề Ticket

## Ngữ cảnh
Hiện trạng hôm nay có những gì, thay đổi này sẽ biến nó thành cái gì, và tại sao điều này lại có ý nghĩa thiết thực đối với việc học tập hàng ngày. Đây là phần duy nhất bắt buộc phải có khi mở một ticket mới.

## Tiêu chí chấp nhận
- [ ] Phác thảo khi tạo ticket; tinh chỉnh chi tiết khi bắt tay vào làm. Ưu tiên các tiêu chí có thể kiểm tra được bằng một bài test tự động hoặc ảnh chụp màn hình UI.

## Kế hoạch
Được viết bởi người nhận xử lý ticket này, trước khi bắt đầu thực thi code. Là một checklist chi tiết, phân nhóm theo các tiêu đề ngắn, mỗi mục là một hành động cụ thể, đánh dấu hoàn thành khi xong ([bang_cong_viec.md](../quy_tac/bang_cong_viec.md#ke-hoach-la-mot-checklist-chi-tiet)):

### Nhóm việc
- [ ] Một hành động cụ thể, nêu rõ vị trí thực hiện (file/module/service), và kết quả có thể kiểm tra được
- [ ] `[gate]` Một hành động thao tác cloud hoặc không thể hoàn tác: bắt buộc dừng lại xin phép phê duyệt
- [ ] `[user]` Công việc chỉ có chủ dự án mới có thể làm (đăng ký tài khoản, đăng nhập trình duyệt cá nhân)

## Bán kính ảnh hưởng
BẮT BUỘC khi `stakes: irreversible`: những gì không thể phục hồi, thay đổi chạm tới những thành phần nào khác, hậu quả xấu nhất ra sao, và phương án khắc phục phục hồi.

## Nhật ký thực hiện
Appended after each meaningful step — a timeline an interrupted session can resume from.

## Sai lệch
Ghi nhận khi đóng ticket: các quyết định phát sinh ngoài phạm vi dự tính ban đầu và lý do. Bất kỳ tồn đọng nào chưa giải quyết xong phải tạo một bản ghi trong `docs/nhat_ky/dang_mo/` trích dẫn ticket này.
