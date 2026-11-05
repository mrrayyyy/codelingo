# Thực thi công việc (Execution)

Quy chuẩn tiến hành công việc trong kho lưu trữ này và đối với các dịch vụ đám mây được kết nối (Render, Neon, GitHub, Groq).

## Bốn bước thực thi (Four steps)

1. **Khảo sát (Investigate)** — đọc kỹ mã nguồn và tài liệu, chạy thử các bài test, tái hiện vấn đề. Tự động thực hiện (Autonomous).
2. **Xác định nguyên nhân gốc rễ (Root-cause)** — chỉ rõ cơ chế gây lỗi chính xác trước khi chỉnh sửa code.
3. **Sửa đổi và kiểm chứng cục bộ (Change and verify locally)** — chỉnh sửa, sau đó chạy các [kiểm tra trước khi push](#cac-buoc-kiem-tra-truoc-khi-push-pre-push-checks). Một thay đổi chưa thể coi là hoàn thành chỉ vì nó biên dịch thành công; xem [VERIFICATION.md](VERIFICATION.md).
4. **Commit và push** — tuân thủ chính sách bên dưới.

## Tự động hóa vs Cần phê duyệt (Autonomous vs gated)

**Tự động hóa (Autonomous - không cần xác nhận trước)**: đọc file, chỉnh sửa cục bộ, chạy tests và builds, khởi chạy server dev nội bộ, tạo hoặc di chuyển tickets và ledger, **tạo commit trên nhánh `main`, và push lên `origin main` khi đã vượt qua các kiểm tra trước khi push** ([ADR 0003](../decisions/0003-public-repo-auto-commit-push.md), chủ dự án phê duyệt, 2026-11-05).

**Cần phê duyệt (Gated - bắt buộc dừng lại, nêu rõ *hành động, mục tiêu, tác động, cách phục hồi* và chờ lệnh xác nhận rõ ràng từ chủ dự án)**:

- `git push --force`, viết lại lịch sử git, xóa nhánh hoặc xóa thẻ tag;
- Thay đổi cài đặt kho lưu trữ GitHub, chế độ hiển thị (visibility), secrets hoặc biến GitHub Actions;
- Tạo, thay đổi hoặc xóa các dịch vụ trên Render, biến môi trường hoặc các project/branch trên Neon;
- Bất kỳ thao tác migration schema nào hoặc xóa dữ liệu trực tiếp trên database đã triển khai;
- Xóa dữ liệu học tập cục bộ (`.data/`, `docker compose down -v`);
- Thêm dịch vụ trả phí hoặc bất kỳ hành động nào có thể phát sinh chi phí;
- Import một repository mà chủ dự án không sở hữu (xem [SECRETS.md](SECRETS.md)).

Sự đồng ý của chủ dự án chỉ có hiệu lực cho hành động cụ thể được hỏi, không áp dụng cho hành động tương tự kế tiếp.

## Chính sách commit và push (Commit and push policy)

- **Commit sau mỗi bước có ý nghĩa**, trong chính lượt tương tác đó, không đợi phải nhắc:
  khi một ticket được mở hoặc di chuyển, một mục ledger được ghi nhận, một tài liệu được cập nhật, hoặc một thay đổi mã nguồn đã vượt qua kiểm tra. Nhiều commit nhỏ luôn tốt hơn một commit gom quá lớn.
- **Chỉ định đường dẫn rõ ràng khi stage (`git add <path>`)** — tuyệt đối không dùng `git add -A` hay `git add .` khi repo đã có lịch sử. Công việc của phiên làm việc khác trong cây thư mục không thuộc quyền tự ý commit của bạn.
- **Mỗi commit chỉ phục vụ một chủ đề duy nhất**, tuân thủ chuẩn Conventional Commits
  (`feat(practice): …`, `fix(api): …`, `docs(backlog): …`, `chore: …`).
- **Push lên `origin main` ngay sau khi các kiểm tra trước khi push vượt qua.** Trước khi push, kiểm tra `git log origin/main..HEAD` để nắm chắc các commit sẽ được đẩy lên.
- Khi Render đã bật chế độ tự động deploy từ nhánh `main`, **mỗi lần push chính là một lần deploy**. Một commit chứa thay đổi schema database, dịch chuyển dữ liệu hoặc thay đổi cấu hình môi trường thuộc diện `stakes: irreversible` và bắt buộc phải được phê duyệt trước (gated), mặc dù việc push thông thường là tự động.

Lý do: Workspace AIOps từng mất nhiều ngày công sức thiết kế chỉ vì nằm trong working tree chưa được commit. Trong một kho lưu trữ công khai, quy tắc này đồng thời giúp mọi thay đổi đều có thể xem lại minh bạch trên GitHub.

### Các bước kiểm tra trước khi push (Pre-push checks)

Chạy các bài kiểm tra liên quan đến phần thay đổi; chạy toàn bộ nếu không chắc chắn:

```sh
.venv/bin/python -m pytest backend/tests -q      # kiểm tra backend
npm --prefix frontend run typecheck              # kiểm tra kiểu dữ liệu frontend
python3 tools/docs/check_doc_links.py            # kiểm tra liên kết tài liệu
python3 tools/docs/scan_secrets.py               # bảo đảm không có bí mật/secret nào bị stage
```

Các bài kiểm tra trình duyệt và build production sẽ tự động chạy trong CI ở mỗi lượt push. Nếu CI trên nhánh `main` bị báo đỏ (thất bại), lỗi đó phải được ưu tiên sửa chữa trước khi bắt đầu bất kỳ tính năng mới nào.

## Bán kính ảnh hưởng phải được ghi thành văn bản (Blast radius is written, not discussed)

Đối với các ticket có mức độ `stakes: irreversible`, hậu quả tiềm tàng phải được viết rõ trong mục `## Blast Radius` của ticket **trước khi** thực thi: điều gì không thể phục hồi, thay đổi chạm tới những thành phần nào khác, và khi xảy ra sự cố tồi tệ thì hậu quả ra sao. Chỉ hỏi xác nhận miệng là chưa đủ — việc viết thành văn bản buộc người thực hiện phải dự liệu đầy đủ mọi hệ quả.

## Không tự ý thay đổi quyết định đã chốt (Do not re-own a decision)

Khi chủ dự án đã chốt quyết định về một vấn đề, agent không được tự ý hoãn lại, thay đổi hoặc biến tấu một phần quyết định đó theo nhận định cá nhân rồi âm thầm ghi vào commit message. Nếu có ý kiến khác, hãy nêu rõ ràng và để chủ dự án lựa chọn.
