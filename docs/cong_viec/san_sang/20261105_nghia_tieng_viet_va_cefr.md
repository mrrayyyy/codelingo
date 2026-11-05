---
type: content
owner: claude
stakes: routine
priority: P1
skill: vocabulary
opened: 2026-11-05
---

# Bổ sung nghĩa tiếng Việt, câu ví dụ và cải thiện ước lượng cấp độ CEFR

## Ngữ cảnh
Từ điển tích hợp sẵn hiện chỉ có 33 định nghĩa (`backend/app/lexicon.py`, đếm ngày 2026-11-05) và bảng `vocab_items` chưa có trường tiếng Việt nào, dẫn đến hầu hết flashcard đều hiển thị "chưa có định nghĩa" (definition unavailable). Đối với người học Việt Nam, vòng lặp ôn tập rất cần một giải nghĩa tiếng Việt ngắn gọn, một định nghĩa tiếng Anh dễ hiểu và một câu ví dụ mộc mạc. Các từ chưa rõ cấp độ CEFR hiện mặc định gán mức B2.

Ràng buộc từ [xac_minh.md](../../quy_tac/xac_minh.md): nội dung do AI sinh ra phải được dán nhãn rõ ràng là do AI sinh, tuyệt đối không bao giờ được trình bày như dữ kiện từ điển chính thống.

## Tiêu chí chấp nhận
- [ ] Schema database (thực hiện qua Alembic): bổ sung các cột `meaning_vi`, `definition_en`, `example`, `content_source` (`lexicon | dictionary | ai`), `content_checked` cho từng mục từ vựng.
- [ ] Làm giàu dữ liệu theo yêu cầu đơn lẻ và theo lô thông qua adapter LLM được cấu hình, kèm JSON schema nghiêm ngặt; chỉ gửi từ vựng và câu ngữ cảnh ngắn đã lưu — tuyệt đối không gửi cả file mã nguồn.
- [ ] Giao diện dán nhãn rõ ràng cho nội dung do AI sinh và cho phép chủ dự án chỉnh sửa / duyệt nội dung (`content_checked`).
- [ ] Ước lượng CEFR sử dụng phân dải tần suất Zipf của thư viện `wordfreq` cho các từ nằm ngoài từ điển biên soạn sẵn; đánh dấu rõ là giá trị ước lượng.
- [ ] Chế độ offline/không có LLM giữ nguyên cách hoạt động: hiển thị "chưa có thông tin", không tự bịa đặt câu chữ.
- [ ] Kiểm thử tự động với adapter LLM giả lập bao gồm các trường hợp phản hồi hợp lệ, không hợp lệ và dịch vụ ngoại tuyến.

## Kế hoạch
Viết chi tiết khi bắt tay vào làm. Phụ thuộc vào ticket Alembic để thực hiện thay đổi schema.

## Nhật ký thực hiện

## Sai lệch
