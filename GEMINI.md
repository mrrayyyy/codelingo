# Gemini / Antigravity — Điểm vào (Entry point)

File này **không chứa quy tắc riêng**. Hãy đọc [AGENTS.md](AGENTS.md) — hợp đồng chia sẻ chung — và sau đó là [docs/protocol/](docs/protocol/README.md), nơi lưu trữ mọi quy tắc ràng buộc, để mọi agent đều tuân thủ các quy tắc thống nhất.

Trước khi thực hiện bất kỳ thao tác nào với ticket, ledger, ADR hoặc dọn dẹp hệ thống, hãy đọc kỹ toàn bộ hướng dẫn tại [.agents/skills/codelingo-doc-manager/SKILL.md](.agents/skills/codelingo-doc-manager/SKILL.md) và làm theo.

Quy định tối thiểu trước khi thực hiện bất cứ thao tác nào:

- [NAVIGATION.md](docs/protocol/NAVIGATION.md) — nơi lưu trữ từng nhóm thông tin/dữ kiện.
- [EXECUTION.md](docs/protocol/EXECUTION.md) — các hành động tự động hóa vs cần phê duyệt (gated), chính sách commit và push.
- [SECRETS.md](docs/protocol/SECRETS.md) — kho lưu trữ này là công khai (public).
- [KANBAN.md](docs/protocol/KANBAN.md) và [LEDGER.md](docs/protocol/LEDGER.md) — ghi nhận các phát hiện ngay trong lượt nhận ra chúng.
- **Quy tắc ngôn ngữ & Đặt tên**: Nội dung tài liệu (`docs/`, `README.md`, tickets...) viết bằng tiếng Việt; tên file và thư mục luôn giữ nguyên bằng tiếng Anh.

Nếu một quy tắc làm tốn thời gian hoặc cản trở công việc chính đáng, hãy tạo một mục `type: protocol-friction` trong `docs/ledger/open/` thay vì âm thầm lách quy tắc.
