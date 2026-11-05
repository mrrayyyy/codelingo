@AGENTS.md

# Bộ điều hợp Claude Code (Claude Code adapter)
- File này không chứa quy tắc riêng. Mọi quy tắc ràng buộc nằm trong [docs/protocol/](docs/protocol/README.md).
- Thư mục `.agents/` là nguồn chuẩn (canonical). Kỹ năng doc-manager được liên kết vào `.claude/skills/codelingo-doc-manager`; kích hoạt kỹ năng này cho bất kỳ thao tác nào với ticket, ledger, ADR hoặc dọn dẹp (housekeeping).
- File `.claude/settings.local.json` là cá nhân và đã được đưa vào git-ignore.
- Toàn bộ nội dung tài liệu viết bằng tiếng Việt; tên file và thư mục luôn giữ bằng tiếng Anh.
- Nếu một quy tắc gây tốn thời gian hoặc cản trở công việc chính đáng, hãy tạo một mục `type: protocol-friction` trong `docs/ledger/open/` thay vì âm thầm lách luật.
