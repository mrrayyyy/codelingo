# 0002. Áp dụng quy trình quản lý tác vụ và tài liệu theo mô hình docs-as-code

- Trạng thái: accepted
- Ngày: 2026-11-05
- Người quyết định: chủ dự án cùng Claude

## Ngữ cảnh (Context)
Việc phát triển CodeLingo được thực hiện bởi chủ dự án cùng Claude Code và Gemini/Antigravity qua nhiều phiên làm việc khác nhau. Nếu không có một hệ thống ghi nhận chung, các kế hoạch, phát hiện và quyết định sẽ chỉ nằm lại trong lịch sử chat và biến mất khi phiên làm việc kết thúc. Chủ dự án đã và đang vận hành hiệu quả một bộ giao thức cho việc này trong workspace AIOps cá nhân.

## Quyết định (Decision)
Áp dụng một phiên bản rút gọn từ giao thức AIOps:

- Mọi quy tắc ràng buộc nằm trong [docs/protocol/](../protocol/README.md); các file `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` chỉ đóng vai trò con trỏ điều hướng;
- Quản lý ticket trong `docs/backlog/{open,ready,in_progress,done,cancel}/`, trạng thái công việc tính theo thư mục chứa file;
- Ghi nhận các phát hiện/nợ kỹ thuật trong `docs/ledger/{open,resolved,cancelled}/` bắt buộc phải có bằng chứng cụ thể và trường `next_review`;
- Các bản ghi quyết định kiến trúc (ADR) lưu trong `docs/decisions/`;
- Một kỹ năng điều phối duy nhất `.agents/skills/codelingo-doc-manager/`, được symlink vào `.claude/skills/`;
- Các script trong `tools/docs/` phục vụ kiểm tra liên kết tài liệu, dọn dẹp housekeeping và quét secret; bước kiểm tra liên kết được chạy tự động trong CI;
- **Quy tắc ngôn ngữ**: Toàn bộ nội dung tài liệu viết bằng tiếng Việt; tên file và thư mục luôn giữ bằng tiếng Anh.

Những phần đã loại bỏ so với bản AIOps gốc: các quy tắc về Vault / Kubernetes / SSH, cơ chế ghi log lệnh shell, các git hooks chặn an toàn và thư mục memory.

## Các phương án thay thế đã xem xét (Alternatives considered)
- Sử dụng GitHub Issues / Projects — agent không thể đọc ngoại tuyến nếu không gọi API qua mạng, và làm phân mảnh ngữ cảnh khỏi kho mã nguồn.
- Giữ nguyên toàn bộ cấu hình đồ sộ của AIOps kèm hooks — quá cồng kềnh so với một ứng dụng của một lập trình viên duy nhất.
- Không dùng gì cả — duy trì hiện trạng khiến ngữ cảnh và lịch sử quyết định liên tục bị thất lạc.

## Hệ quả (Consequences)
- Mọi thay đổi không nhỏ đều có một ticket đi kèm kế hoạch và nhật ký thực hiện chi tiết, giúp các phiên làm việc sau dễ dàng tiếp tục ngay cả khi phiên trước bị ngắt quãng.
- Các ticket và mục ledger đều ở chế độ công khai (xem ADR 0003), do đó tuyệt đối không được đưa thông tin bảo mật hay dữ liệu nội bộ công ty vào.
