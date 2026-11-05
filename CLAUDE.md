@AGENTS.md

# Bộ điều hợp Claude Code
- File này không chứa quy tắc riêng. Mọi quy tắc ràng buộc nằm trong [docs/quy_tac/](docs/quy_tac/README.md).
- Thư mục `.agents/` là nguồn chuẩn. Kỹ năng doc-manager được liên kết vào `.claude/skills/codelingo-doc-manager`; kích hoạt kỹ năng này cho bất kỳ thao tác nào với ticket, nhật ký (ledger), ADR hoặc dọn dẹp hệ thống.
- File `.claude/settings.local.json` là cá nhân và đã được đưa vào git-ignore.
- Toàn bộ nội dung tài liệu viết bằng tiếng Việt; tên thư mục và file tài liệu dùng tiếng Việt không dấu snake_case; chỉ các từ khóa học thuật/kỹ thuật và file entrypoint hệ thống giữ nguyên tiếng Anh.
- Nếu một quy tắc gây tốn thời gian hoặc cản trở công việc chính đáng, hãy tạo một mục `type: protocol-friction` trong `docs/nhat_ky/dang_mo/` thay vì âm thầm lách luật.
