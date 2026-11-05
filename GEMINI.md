# Gemini / Antigravity — Điểm vào

File này **không chứa quy tắc riêng**. Hãy đọc [AGENTS.md](AGENTS.md) — hợp đồng chia sẻ chung — và sau đó là [docs/quy_tac/](docs/quy_tac/README.md), nơi lưu trữ mọi quy tắc ràng buộc, để mọi agent đều tuân thủ các quy tắc thống nhất.

Trước khi thực hiện bất kỳ thao tác nào với ticket, nhật ký (ledger), ADR hoặc dọn dẹp hệ thống, hãy đọc kỹ toàn bộ hướng dẫn tại [.agents/skills/codelingo-doc-manager/SKILL.md](.agents/skills/codelingo-doc-manager/SKILL.md) và làm theo.

Quy định tối thiểu trước khi thực hiện bất cứ thao tác nào:

- [dieu_huong.md](docs/quy_tac/dieu_huong.md) — nơi lưu trữ từng nhóm thông tin/dữ kiện.
- [thuc_thi.md](docs/quy_tac/thuc_thi.md) — các hành động tự động hóa vs cần phê duyệt (gated), chính sách commit và push.
- [bao_mat.md](docs/quy_tac/bao_mat.md) — kho lưu trữ này là công khai (public).
- [bang_cong_viec.md](docs/quy_tac/bang_cong_viec.md) và [so_nhat_ky.md](docs/quy_tac/so_nhat_ky.md) — ghi nhận các phát hiện ngay trong lượt nhận ra chúng.
- **Quy tắc ngôn ngữ và đặt tên**: Nội dung tài liệu viết bằng tiếng Việt; tên thư mục và tên file tài liệu dùng tiếng Việt không dấu snake_case (`docs/quy_tac/`, `docs/cong_viec/`...); chỉ các từ khóa học thuật/kỹ thuật và file entrypoint hệ thống giữ nguyên tiếng Anh.

Nếu một quy tắc làm tốn thời gian hoặc cản trở công việc chính đáng, hãy tạo một mục `type: protocol-friction` trong `docs/nhat_ky/dang_mo/` thay vì âm thầm lách quy tắc.
