# Đồng bộ tài liệu

Công việc làm thay đổi hành vi của hệ thống bắt buộc phải cập nhật tài liệu mô tả hành vi đó trong chính ticket đang thực hiện — không để lại cho một đầu việc phụ sau này mà thường không bao giờ được làm.

1. Bất kỳ thay đổi nào đối với route API, mô hình dữ liệu (data model), biến môi trường, chính sách trích xuất từ vựng, plugin, hoặc cách thức khởi chạy/triển khai ứng dụng đều phải cập nhật tài liệu tương ứng **ngay trong cùng một ticket**.
2. Tuyệt đối không chuyển ticket sang `hoan_thanh/` khi chưa kiểm tra lại xem tài liệu liên quan có còn khớp với mã nguồn hay không. Bước kiểm tra này là một phần của quy trình đóng ticket, song song với việc viết mục `## Sai lệch`.
3. Nợ kỹ thuật, các giải pháp tạm và các thiếu sót được nhận biết trong quá trình làm việc phải được ghi nhận vào `docs/nhat_ky/dang_mo/` trước khi đóng ticket.
4. Một quyết định mà các công việc sau này không nên lật lại để bàn cãi sẽ được đúc kết thành một bản ghi quyết định kiến trúc (ADR) trong `docs/quyet_dinh/`.

## Quy tắc ngôn ngữ và đặt tên khi cập nhật tài liệu
- **Nội dung cập nhật**: Toàn bộ tài liệu cập nhật mới hoặc sửa đổi **bắt buộc viết bằng tiếng Việt**.
- **Tên thư mục**: **Bắt buộc dùng tiếng Việt không dấu snake_case**.
- **Tên file tài liệu**: **Bắt buộc dùng tiếng Việt không dấu snake_case**.

## Tài liệu nào cần cập nhật

| Thay đổi thực tế | Tài liệu cần cập nhật |
| :--- | :--- |
| Thêm/sửa route API, bảng dữ liệu, cột, hợp đồng plugin | [docs/kien_truc.md](../kien_truc.md) (sơ đồ ERD, các phần hợp đồng) |
| Thêm/sửa biến môi trường hoặc thiết lập cấu hình | `.env.example` / `.env.cloud.example`, và [README.md](../../README.md) hoặc [docs/trien_khai_cloud.md](../trien_khai_cloud.md) |
| Cách khởi chạy, build hoặc triển khai hệ thống | [README.md](../../README.md), [docs/trien_khai_cloud.md](../trien_khai_cloud.md), hoặc tài liệu quy trình liên quan |
| Bàn giao tính năng hiển thị trực tiếp với người dùng | Mục "Các tính năng đã triển khai" trong [README.md](../../README.md); trạng thái lộ trình trong [docs/san_pham/lo_trinh.md](../san_pham/lo_trinh.md) |
| Lý do lựa chọn giải pháp kiến trúc | Thư mục `docs/quyet_dinh/` (ADR) |
| Tiến trình diễn ra trong quá trình thực hiện | Mục `## Nhật ký thực hiện` của chính ticket đó |

Một tài liệu chứa tiêu đề các giai đoạn, dấu tích hoàn thành `[x]` hoặc ngày tháng trong cấu trúc của nó là một bản ghi công việc, không phải là quy trình vận hành. Những nội dung đó thuộc về một ticket trong danh sách công việc.
