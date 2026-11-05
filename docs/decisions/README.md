# Bản ghi Quyết định Kiến trúc (ADRs)

Nơi ghi lại câu trả lời cho câu hỏi *tại sao* — những quyết định đằng sau hình thái và cấu trúc hiện tại của CodeLingo, tách biệt với [architecture.md](../architecture.md) (nơi ghi nhận *hệ thống hiện có những gì*).

Tham khảo các ADR liên quan trước khi đề xuất thay đổi về triển khai, mô hình dữ liệu, ranh giới quyền riêng tư hoặc giao thức làm việc. Mục tiêu là không bao giờ phải bàn cãi lại một quyết định đã chốt và không âm thầm vi phạm quyết định đó.

## Khi nào cần viết một ADR

Khi một quyết định không hiển nhiên, từng có tranh luận, hoặc có thể gây bất ngờ cho người đọc mới — ví dụ: "tại sao GitHub Actions lại đảm nhận NLP thay vì worker thường trực", "tại sao repository này lại để chế độ công khai (public)". Các thay đổi thông thường thuộc về ticket và commit message.

## Quy tắc Ngôn ngữ & Đặt tên
- **Tên file & Thư mục**: Bắt buộc giữ **100% bằng tiếng Anh** theo mẫu `NNNN-short-title.md` (ví dụ: `0001-cloud-first-free-tier.md`).
- **Nội dung ADR**: Bắt buộc viết bằng **tiếng Việt**.

## Định dạng (Format)

Mỗi quyết định là một file riêng, đặt tên `NNNN-short-title.md`, đánh số thứ tự liên tiếp. Sao chép từ mẫu [0000-template.md](0000-template.md).

## Các trạng thái (Status values)

- `proposed` — đang được xem xét, thảo luận
- `accepted` — đã được thông qua và áp dụng vào mã nguồn
- `superseded by NNNN` — đã bị thay thế bởi quyết định số NNNN; vẫn giữ lại file cũ để lưu vết lịch sử

## Bảng chỉ mục (Index)

| ADR | Trạng thái | Quyết định |
| :--- | :--- | :--- |
| [0001](0001-cloud-first-free-tier.md) | accepted | Ưu tiên Cloud trên các dịch vụ managed miễn phí; giữ cấu hình self-hosted phục vụ phát triển |
| [0002](0002-docs-as-code-workflow.md) | accepted | Áp dụng quy trình quản lý tác vụ và tài liệu theo mô hình docs-as-code chuyển thể từ AIOps |
| [0003](0003-public-repo-auto-commit-push.md) | accepted | Kho lưu trữ công khai; các agent tự động commit và push lên nhánh `main` |
