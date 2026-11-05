# Bí mật và quyền riêng tư

**Kho lưu trữ này là công khai (public)** (`mrrayyyy/codelingo`, quyết định của chủ dự án ngày 2026-11-05). Mọi thứ được commit — mã nguồn, ticket, các mục nhật ký, commit message — đều có thể được đọc bởi bất kỳ ai, vĩnh viễn, ngay cả sau khi đã bị xóa trong commit sau.

## Những điều tuyệt đối không bao giờ được commit

- API keys, tokens, mật khẩu, chuỗi kết nối chứa thông tin xác thực (`.env` đã được đưa vào git-ignore; luôn duy trì trạng thái này);
- URL ứng dụng đã triển khai đi kèm với bất kỳ thông tin nào dùng để xác thực truy cập vào ứng dụng đó;
- Từ vựng thực tế, các câu ngữ cảnh hoặc đoạn trích mã nguồn được bóc tách từ repository riêng tư hoặc kho mã nguồn của công ty nơi chủ dự án làm việc;
- Tên các hệ thống nội bộ, tên host máy chủ, khách hàng hoặc tên đồng nghiệp tại nơi làm việc của chủ dự án — áp dụng cho cả ticket và các mục nhật ký. Luôn mô tả khái quát (ví dụ: "một repository công việc").

Các khóa secret được lưu trong file `.env` ở môi trường cục bộ và trong phần cài đặt Secret của Render / GitHub Actions khi triển khai trên cloud. Việc thay đổi secret trên môi trường đám mây bắt buộc phải được phê duyệt trước ([thuc_thi.md](thuc_thi.md)). Tuyệt đối không bao giờ in giá trị secret ra màn hình chat, file log hay bất kỳ file nào.

## Trước mỗi lần commit

```sh
python3 tools/docs/scan_secrets.py                       # kiểm tra các thay đổi đã stage
git diff origin/main..HEAD | python3 tools/docs/scan_secrets.py -   # kiểm tra các commit chưa push
```

Lệnh quét sẽ in ra các kết quả khớp và trả về mã thoát exit 1 nếu phát hiện vi phạm. Các test fixture cố tình chứa mã khóa giả lập phải gắn kèm đánh dấu `fake-secret-fixture` trên cùng dòng hoặc dòng ngay phía trên để công cụ quét bỏ qua; tuyệt đối không gắn đánh dấu này cho các giá trị bí mật thực tế.

Nếu một bí mật thực tế vô tình bị push lên kho lưu trữ: trước tiên phải thu hồi/xoay vòng (rotate) khóa đó ngay lập tức (giá trị cũ đã bị lộ ngay khoảnh khắc nó xuất hiện công khai), sau đó làm sạch lịch sử git dưới dạng một hành động cần phê duyệt.

## Mã nguồn công ty và nơi làm việc

Cấu hình triển khai trên cloud gửi repository được import tới các runner của GitHub Actions, lưu các câu ngữ cảnh vào Neon, và có thể gửi văn bản bài tập tới Groq. Việc import mã nguồn mà chủ dự án không sở hữu bản quyền có thể vi phạm chính sách bảo mật của doanh nghiệp. Cho đến khi chủ dự án có quyết định khác ([bản ghi nhật ký](../nhat_ky/dang_mo/lo_hong_quy_trinh_20261105_bao_mat_ma_nguon_cong_ty.md)), các agent chỉ được phép import các kho mã nguồn công khai hoặc bộ mẫu đi kèm dự án.
