# 0003. Kho lưu trữ công khai; các agent tự động commit và push

- Trạng thái: accepted
- Ngày: 2026-11-05
- Người quyết định: chủ dự án

## Ngữ cảnh (Context)
Trước đây dự án chưa có lịch sử git. Cấu hình triển khai trên cloud yêu cầu mã nguồn phải nằm trên GitHub (workflow bóc tách từ vựng bắt buộc phải nằm trên nhánh mặc định). Chủ dự án đã chọn mô hình repository công khai (public) và muốn các agent tự động commit và push mà không cần phải hỏi xin phép ở các thao tác định kỳ.

## Quyết định (Decision)
- Kho lưu trữ là `mrrayyyy/codelingo`, chế độ công khai (public), nhánh mặc định là `main`.
- Các agent tự động commit sau mỗi bước làm việc có ý nghĩa và tự động push lên `origin main` khi các bài kiểm tra trước khi push trong [EXECUTION.md](../protocol/EXECUTION.md#cac-buoc-kiem-tra-truoc-khi-push-pre-push-checks) đã vượt qua thành công.
- Các thao tác vẫn bắt buộc phải xin phép xác nhận trước (gated): force push và viết lại lịch sử git, cài đặt kho lưu trữ và các khóa bí mật (secrets), cấu hình dịch vụ trên đám mây, các thay đổi dữ liệu hoặc migration schema database trên môi trường production.

## Các phương án thay thế đã xem xét (Alternatives considered)
- Kho lưu trữ riêng tư (private) — số phút chạy GitHub Actions bị giới hạn nghiêm ngặt đối với repo private; chủ dự án ưu tiên dùng repo công khai để tận dụng tối đa runner miễn phí.
- Tự động commit nhưng chỉ push khi được yêu cầu (quy tắc của AIOps) — an toàn hơn, nhưng chủ dự án mong muốn giảm bớt lực cản thao tác đối với một dự án cá nhân.

## Hệ quả (Consequences)
- Mọi ticket, mục ledger và commit message đều ở chế độ công khai cho toàn thế giới đọc được: quy định tại [SECRETS.md](../protocol/SECRETS.md) áp dụng cho tài liệu nghiêm ngặt như đối với mã nguồn.
- Khi Render đã bật tính năng tự động deploy từ nhánh `main`, mỗi lần push chính là một lần deploy. Các bước kiểm tra pre-push checks và CI là chốt chặn duy nhất cho các thay đổi thông thường; các thay đổi schema database vẫn phải được phê duyệt trước.
- Sai sót sẽ hiển thị ngay lập tức, nhưng tiến độ công việc cũng sẽ rõ ràng và minh bạch tương ứng.
