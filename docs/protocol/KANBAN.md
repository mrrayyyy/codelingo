# Kanban (`docs/backlog/`)

Bảng theo dõi tác vụ (task board). Trạng thái công việc chính là **thư mục chứa file**; thay đổi trạng thái đồng nghĩa với việc di chuyển file (`git mv`), nhờ đó lệnh `git log --follow` sẽ hiển thị lịch sử chính xác của từng lần chuyển đổi trạng thái.

```text
open/         tác vụ đã có nhưng đang bị chặn (blocked) — nguyên nhân chặn được nêu rõ trong ticket
ready/        không bị chặn, đã sẵn sàng để thực hiện
in_progress/  đang được tiến hành xử lý
done/         đã hoàn thành; ticket đóng vai trò như một bản ghi lịch sử
cancel/       đã hủy bỏ, kèm theo lý do cụ thể ngay trong file
```

Luồng chuyển đổi: `open/` → `ready/` → `in_progress/` → `done/`. Một ticket không bao giờ nhảy cóc trực tiếp từ `open/` sang `in_progress/`: người giải quyết nguyên nhân chặn phải chuyển ticket sang `ready/` trước tiên, giúp việc trả lời câu hỏi "hiện tại có thể làm gì" chỉ cần một lệnh `ls`.

## Quy tắc Ngôn ngữ & Đặt tên
- **Tên file & Thư mục**: Bắt buộc giữ **100% bằng tiếng Anh** theo mẫu `YYYYMMDD_<slug>.md`. Thư mục trạng thái (`open/`, `ready/`, `in_progress/`, `done/`, `cancel/`) giữ nguyên tiếng Anh.
- **Nội dung ticket**: Bắt buộc viết bằng **tiếng Việt**.
- **Frontmatter & Tiêu đề chuẩn**: Các khóa metadata (`type:`, `owner:`, `stakes:`, `priority:`, `skill:`, `opened:`) và các tiêu đề chuẩn (`## Context`, `## Acceptance Criteria`, `## Plan`, `## Blast Radius`, `## Implementation Log`, `## Deviations`) giữ nguyên định dạng tiếng Anh để bảo đảm công cụ script phân tích (`tools/docs/housekeeping.py`) hoạt động chuẩn xác.

## Khi nào cần tạo ticket

Hãy mở một ticket cho bất kỳ công việc nào làm thay đổi hành vi hiển thị với người dùng, tác động tới nhiều hơn một module, hoặc dự kiến mất hơn 30 phút thực hiện. Các lỗi chính tả nhỏ, sửa một dòng code đơn giản hoặc sửa liên kết tài liệu chỉ cần một commit message rõ ràng là đủ.

## Các trường thông tin (Fields)

Tên file đặt theo định dạng `YYYYMMDD_slug.md`. Tạo từ mẫu [`_TEMPLATE.md`](../backlog/_TEMPLATE.md).

- `type: feature | content | refactor | infra | docs | investigation`
- `owner: claude | user` — mặc định cho ticket mới là `claude`. Chỉ gán `user` khi chủ dự án xác nhận sẽ tự thực hiện (tài khoản, thanh toán, việc yêu cầu đăng nhập trình duyệt cá nhân). Claude/agent không tự ý nhận hoặc đổi quyền sở hữu một ticket thuộc về `user`.
- `stakes: routine | irreversible` — mức độ rủi ro: `irreversible` (không thể hoàn tác) dành cho thay đổi schema/dữ liệu database trên cloud, cấu hình triển khai, khóa secret, hoặc việc xóa dữ liệu học tập. Tự động nâng cấp mức này nếu công việc phát sinh phức tạp hơn dự tính.
- `priority: P1 | P2 | P3` — P1 là giai đoạn hiện tại trong lộ trình phát triển [docs/product/roadmap.md](../product/roadmap.md).
- `skill:` tùy chọn — `speaking | listening | reading | writing | vocabulary` dành cho các ticket sản phẩm, giúp theo dõi trực quan tiến độ của từng kỹ năng ngôn ngữ.

## Vòng đời xử lý ticket (Lifecycle)

1. **Sẵn sàng thực hiện (Becoming pickable)** — nguyên nhân chặn được giải quyết; chuyển file sang `ready/`.
2. **Bắt đầu thực hiện (Starting)** — chuyển file sang `in_progress/`. Viết mục `## Plan` trước nếu chưa có, dưới dạng một [checklist chi tiết](#ke-hoach-la-mot-checklist-chi-tiet).
3. **Theo dõi tiến độ (Tracking)** — ghi thêm nội dung vào `## Implementation Log` sau mỗi bước làm việc có ý nghĩa. Một ticket nằm trong `in_progress/` với log trống hoặc cũ kỹ là vi phạm quy chuẩn: các phiên làm việc có thể hết ngữ cảnh giữa chừng, và việc dồn tóm tắt để viết vào cuối cùng thường dẫn đến mất mát thông tin.
4. **Đóng ticket (Closing)** — ghi rõ mục `## Deviations` (hoặc ghi "None"); ghi nhận các tồn đọng chưa xử lý vào `docs/ledger/open/` kèm dẫn chứng từ ticket này; cập nhật các tài liệu bị ảnh hưởng ([DOC_SYNC.md](DOC_SYNC.md)); chuyển file sang `done/`.

Luôn duy trì tối đa **hai** ticket trong `in_progress/` cùng một lúc. Các dự án cá nhân thường bị đình trệ vì mở quá nhiều việc cùng lúc, chứ không phải vì làm quá ít.

## Kế hoạch là một checklist chi tiết

Mỗi mục trong kế hoạch là một hành động cụ thể với một kết quả có thể kiểm tra độc lập, nêu rõ vị trí thực hiện (file, module, dịch vụ), được đánh dấu **`[gate]`** khi cần sự phê duyệt theo [EXECUTION.md](EXECUTION.md) và **`[user]`** khi chỉ có chủ dự án mới có thể làm, đồng thời được đánh dấu `[x]` ngay trong lượt hoàn thành kèm theo bằng chứng cụ thể (commit hash, output của test). Những công việc phát sinh ngoài dự kiến phải được bổ sung thành mục mới trong checklist, không được âm thầm làm.

## Commit tại thời điểm tạo và thời điểm hoàn tất

Commit ticket ngay khoảnh khắc nó được tạo và một lần nữa khi nó chuyển sang `done/` hoặc `cancel/` — chỉ định rõ ràng đường dẫn file của ticket đó (kèm theo các mục ledger tương ứng). Trạng thái công việc chính là thư mục, và lịch sử git là bản ghi duy nhất lưu lại mốc thời gian chuyển trạng thái; một ticket chưa được commit sẽ không có cả hai điều trên.

## Mối liên hệ với Sổ nhật ký (Ledger)

[Sổ nhật ký (Ledger)](LEDGER.md) lưu trữ những thứ *được phát hiện*; backlog lưu trữ những việc *đã quyết định làm*. Một mục trong ledger sẽ được "tốt nghiệp" khi có người quyết định bắt tay vào làm, và chuyển sang `ledger/resolved/` ngay tại thời điểm ticket tương ứng được tạo ra.
