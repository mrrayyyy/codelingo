# Bản ghi quyết định kiến trúc (ADR)

Nơi ghi lại câu trả lời cho câu hỏi *tại sao* — những quyết định đằng sau hình thái và cấu trúc hiện tại của CodeLingo, tách biệt với [kien_truc.md](../kien_truc.md) (nơi ghi nhận *hệ thống hiện có những gì*).

Tham khảo các ADR liên quan trước khi đề xuất thay đổi về triển khai, mô hình dữ liệu, ranh giới quyền riêng tư hoặc quy tắc làm việc. Mục tiêu là không bao giờ phải bàn cãi lại một quyết định đã chốt và không âm thầm vi phạm quyết định đó.

## Khi nào cần viết một ADR

Khi một quyết định không hiển nhiên, từng có tranh luận, hoặc có thể gây bất ngờ cho người đọc mới — ví dụ: "tại sao GitHub Actions lại đảm nhận NLP thay vì worker thường trực", "tại sao repository này lại để chế độ công khai". Các thay đổi thông thường thuộc về ticket và commit message.

## Quy tắc ngôn ngữ và đặt tên
- **Tên thư mục**: Bắt buộc dùng **tiếng Việt không dấu snake_case** (`docs/quyet_dinh/`).
- **Tên file**: Bắt buộc dùng **tiếng Việt không dấu snake_case** theo mẫu `NNNN_<slug>.md` (ví dụ: `0001_uu_tien_cloud_mien_phi.md`).
- **Nội dung ADR**: Bắt buộc viết bằng **tiếng Việt**.

## Định dạng

Mỗi quyết định là một file riêng, đặt tên `NNNN_<slug>.md`, đánh số thứ tự liên tiếp. Sao chép từ mẫu [0000_mau.md](0000_mau.md).

## Các trạng thái

- `proposed` — đang được xem xét, thảo luận
- `accepted` — đã được thông qua và áp dụng vào mã nguồn
- `superseded by NNNN` — đã bị thay thế bởi quyết định số NNNN; vẫn giữ lại file cũ để lưu vết lịch sử

## Bảng chỉ mục

| ADR | Trạng thái | Quyết định |
| :--- | :--- | :--- |
| [0001](0001_uu_tien_cloud_mien_phi.md) | accepted | Ưu tiên Cloud trên các dịch vụ managed miễn phí; giữ cấu hình self-hosted phục vụ phát triển |
| [0002](0002_quy_trinh_docs_as_code.md) | accepted | Áp dụng quy trình quản lý tác vụ và tài liệu theo mô hình docs-as-code chuyển thể từ AIOps |
| [0003](0003_repo_cong_khai_tu_dong_commit_push.md) | accepted | Kho lưu trữ công khai; các agent tự động commit và push lên nhánh `main` |
| [0004](0004_bo_che_do_arq_redis.md) | accepted | Bỏ chế độ job ARQ/Redis; chỉ giữ `inline` (dev/CI/Compose) và `github_actions` (cloud) |
