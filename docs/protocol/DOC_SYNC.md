# Đồng bộ tài liệu (Documentation Sync)

Công việc làm thay đổi hành vi của hệ thống bắt buộc phải cập nhật tài liệu mô tả hành vi đó trong chính ticket đang thực hiện — không để lại cho một đầu việc phụ sau này mà thường không bao giờ được làm.

1. Bất kỳ thay đổi nào đối với route API, mô hình dữ liệu (data model), biến môi trường, chính sách trích xuất từ vựng, plugin, hoặc cách thức khởi chạy/triển khai ứng dụng đều phải cập nhật tài liệu tương ứng **ngay trong cùng một ticket**.
2. Tuyệt đối không chuyển ticket sang `done/` khi chưa kiểm tra lại xem tài liệu liên quan có còn khớp với mã nguồn hay không. Bước kiểm tra này là một phần của quy trình đóng ticket, song song với việc viết mục `## Deviations`.
3. Nợ kỹ thuật, các giải pháp tạm và các thiếu sót được nhận biết trong quá trình làm việc phải được ghi nhận vào `docs/ledger/open/` trước khi đóng ticket.
4. Một quyết định mà các công việc sau này không nên lật lại để bàn cãi sẽ được đúc kết thành một bản ghi quyết định kiến trúc (ADR) trong `docs/decisions/`.

## Quy tắc Ngôn ngữ & Đặt tên khi cập nhật tài liệu
- **Nội dung cập nhật**: Toàn bộ tài liệu cập nhật mới hoặc sửa đổi **bắt buộc viết bằng tiếng Việt**.
- **Tên file & Thư mục**: **Bắt buộc giữ 100% bằng tiếng Anh**. Nếu tạo tài liệu mới, runbook mới, ticket mới, tuyệt đối không đặt tên file hay thư mục bằng tiếng Việt.

## Tài liệu nào cần cập nhật

| Thay đổi thực tế | Tài liệu cần cập nhật |
| :--- | :--- |
| Thêm/sửa route API, bảng dữ liệu, cột, hợp đồng plugin | [docs/architecture.md](../architecture.md) (sơ đồ ERD, các phần hợp đồng) |
| Thêm/sửa biến môi trường hoặc thiết lập cấu hình | `.env.example` / `.env.cloud.example`, và [README.md](../../README.md) hoặc [docs/cloud-deployment.vi.md](../cloud-deployment.vi.md) |
| Cách khởi chạy, build hoặc triển khai hệ thống | [README.md](../../README.md), [docs/cloud-deployment.vi.md](../cloud-deployment.vi.md), hoặc tài liệu runbook liên quan |
| Bàn giao tính năng hiển thị trực tiếp với người dùng | Mục "Các tính năng đã triển khai" trong [README.md](../../README.md); trạng thái lộ trình trong [docs/product/roadmap.md](../product/roadmap.md) |
| Lý do lựa chọn giải pháp kiến trúc | Thư mục `docs/decisions/` (ADR) |
| Tiến trình diễn ra trong quá trình thực hiện | Mục `## Implementation Log` của chính ticket đó |

Một tài liệu chứa tiêu đề các giai đoạn (phase), dấu tích hoàn thành `[x]` hoặc ngày tháng trong cấu trúc của nó là một bản ghi công việc (work record), không phải là runbook. Những nội dung đó thuộc về một ticket trong backlog.
