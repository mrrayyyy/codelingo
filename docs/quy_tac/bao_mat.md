# Bí mật và quyền riêng tư

**Kho lưu trữ này là công khai (public)** (`mrrayyyy/codelingo`, quyết định của chủ dự án ngày 2026-11-05). Mọi thứ được commit — mã nguồn, ticket, các mục nhật ký, commit message — đều có thể được đọc bởi bất kỳ ai, vĩnh viễn, ngay cả sau khi đã bị xóa trong commit sau.

## Những điều tuyệt đối không bao giờ được commit

- API keys, tokens, mật khẩu, chuỗi kết nối chứa thông tin xác thực (`.env` đã được đưa vào git-ignore; luôn duy trì trạng thái này);
- URL ứng dụng đã triển khai đi kèm với bất kỳ thông tin nào dùng để xác thực truy cập vào ứng dụng đó;
- Từ vựng thực tế, các câu ngữ cảnh hoặc đoạn trích mã nguồn được bóc tách từ repository riêng tư (không công khai);
- Tên host máy chủ, địa chỉ nội bộ hoặc thông tin cá nhân của người khác — áp dụng cho cả ticket và các mục nhật ký. Luôn mô tả khái quát.

Các khóa secret được lưu trong file `.env` ở môi trường cục bộ và trong phần cài đặt Secret của Render / GitHub Actions khi triển khai trên cloud. Việc thay đổi secret trên môi trường đám mây bắt buộc phải được phê duyệt trước ([thuc_thi.md](thuc_thi.md)). Tuyệt đối không bao giờ in giá trị secret ra màn hình chat, file log hay bất kỳ file nào.

## Trước mỗi lần commit

```sh
python3 tools/docs/scan_secrets.py                       # kiểm tra các thay đổi đã stage
git diff origin/main..HEAD | python3 tools/docs/scan_secrets.py -   # kiểm tra các commit chưa push
```

Lệnh quét sẽ in ra các kết quả khớp và trả về mã thoát exit 1 nếu phát hiện vi phạm. Các test fixture cố tình chứa mã khóa giả lập phải gắn kèm đánh dấu `fake-secret-fixture` trên cùng dòng hoặc dòng ngay phía trên để công cụ quét bỏ qua; tuyệt đối không gắn đánh dấu này cho các giá trị bí mật thực tế.

Nếu một bí mật thực tế vô tình bị push lên kho lưu trữ: trước tiên phải thu hồi/xoay vòng (rotate) khóa đó ngay lập tức (giá trị cũ đã bị lộ ngay khoảnh khắc nó xuất hiện công khai), sau đó làm sạch lịch sử git dưới dạng một hành động cần phê duyệt.

## Nguồn mã nguồn được import

CodeLingo là dự án cá nhân (chủ dự án xác nhận ngày 2026-11-06). Nguồn import là repo GitHub **công khai** (repo nổi tiếng và repo của chính chủ dự án) cùng file ZIP do chủ dự án tự tải lên. Cấu hình cloud gửi repo được import tới runner GitHub Actions, lưu câu ngữ cảnh vào Neon và có thể gửi văn bản bài tập tới Groq, nên chỉ import nội dung được phép công khai. Agent chỉ tự import repo công khai hoặc bộ mẫu đi kèm dự án; import repo mà chủ dự án không sở hữu vẫn là thao tác cần phê duyệt ([thuc_thi.md](thuc_thi.md)).
