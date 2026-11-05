# Bảng quản lý công việc (`docs/cong_viec/`)

Bảng theo dõi tác vụ. Trạng thái công việc chính là **thư mục chứa file**; thay đổi trạng thái đồng nghĩa với việc di chuyển file (`git mv`), nhờ đó lệnh `git log --follow` sẽ hiển thị lịch sử chính xác của từng lần chuyển đổi trạng thái.

```text
cho_xu_ly/    tác vụ đã có nhưng đang bị chặn — nguyên nhân chặn được nêu rõ trong ticket
san_sang/     không bị chặn, đã sẵn sàng để thực hiện
dang_lam/     đang được tiến hành xử lý
hoan_thanh/   đã hoàn thành; ticket đóng vai trò như một bản ghi lịch sử
da_huy/       đã hủy bỏ, kèm theo lý do cụ thể ngay trong file
```

Luồng chuyển đổi: `cho_xu_ly/` → `san_sang/` → `dang_lam/` → `hoan_thanh/`. Một ticket không bao giờ nhảy cóc trực tiếp từ `cho_xu_ly/` sang `dang_lam/`: người giải quyết nguyên nhân chặn phải chuyển ticket sang `san_sang/` trước tiên, giúp việc trả lời câu hỏi "hiện tại có thể làm gì" chỉ cần một lệnh `ls`.

## Quy tắc ngôn ngữ và đặt tên
- **Tên thư mục**: Bắt buộc dùng **tiếng Việt không dấu snake_case** (`cho_xu_ly/`, `san_sang/`, `dang_lam/`, `hoan_thanh/`, `da_huy/`).
- **Tên file**: Bắt buộc dùng **tiếng Việt không dấu snake_case** theo mẫu `YYYYMMDD_<slug>.md`.
- **Nội dung ticket**: Bắt buộc viết bằng **tiếng Việt**.
- **Tiêu đề chuẩn**: Sử dụng các tiêu đề thuần Việt (`## Ngữ cảnh`, `## Tiêu chí chấp nhận`, `## Kế hoạch`, `## Bán kính ảnh hưởng`, `## Nhật ký thực hiện`, `## Sai lệch`). Các trường metadata (`type:`, `owner:`, `stakes:`, `priority:`, `skill:`, `opened:`) giữ nguyên định dạng tiếng Anh để tương thích với script kiểm tra.

## Khi nào cần tạo ticket

Hãy mở một ticket cho bất kỳ công việc nào làm thay đổi hành vi hiển thị với người dùng, tác động tới nhiều hơn một module, hoặc dự kiến mất hơn 30 phút thực hiện. Các lỗi chính tả nhỏ, sửa một dòng code đơn giản hoặc sửa liên kết tài liệu chỉ cần một commit message rõ ràng là đủ.

## Các trường thông tin

Tên file đặt theo định dạng `YYYYMMDD_slug.md`. Tạo từ mẫu [`_mau.md`](../cong_viec/_mau.md).

- `type: feature | content | refactor | infra | docs | investigation`
- `owner: claude | user` — mặc định cho ticket mới là `claude`. Chỉ gán `user` khi chủ dự án xác nhận sẽ tự thực hiện (tài khoản, thanh toán, việc yêu cầu đăng nhập trình duyệt cá nhân). Agent không tự ý nhận hoặc đổi quyền sở hữu một ticket thuộc về `user`.
- `stakes: routine | irreversible` — mức độ rủi ro: `irreversible` (không thể hoàn tác) dành cho thay đổi schema/dữ liệu database trên cloud, cấu hình triển khai, khóa secret, hoặc việc xóa dữ liệu học tập. Tự động nâng cấp mức này nếu công việc phát sinh phức tạp hơn dự tính.
- `priority: P1 | P2 | P3` — P1 là giai đoạn hiện tại trong lộ trình phát triển [docs/san_pham/lo_trinh.md](../san_pham/lo_trinh.md).
- `skill:` tùy chọn — `speaking | listening | reading | writing | vocabulary` dành cho các ticket sản phẩm, giúp theo dõi trực quan tiến độ của từng kỹ năng ngôn ngữ.

## Vòng đời xử lý ticket

1. **Sẵn sàng thực hiện** — nguyên nhân chặn được giải quyết; chuyển file sang `san_sang/`.
2. **Bắt đầu thực hiện** — chuyển file sang `dang_lam/`. Viết mục `## Kế hoạch` trước nếu chưa có, dưới dạng một [checklist chi tiết](#ke-hoach-la-mot-checklist-chi-tiet).
3. **Theo dõi tiến độ** — ghi thêm nội dung vào `## Nhật ký thực hiện` sau mỗi bước làm việc có ý nghĩa. Một ticket nằm trong `dang_lam/` với log trống hoặc cũ kỹ là vi phạm quy chuẩn: các phiên làm việc có thể hết ngữ cảnh giữa chừng, và việc dồn tóm tắt để viết vào cuối cùng thường dẫn đến mất mát thông tin.
4. **Đóng ticket** — ghi rõ mục `## Sai lệch` (hoặc ghi "None"); ghi nhận các tồn đọng chưa xử lý vào `docs/nhat_ky/dang_mo/` kèm dẫn chứng từ ticket này; cập nhật các tài liệu bị ảnh hưởng ([dong_bo_tai_lieu.md](dong_bo_tai_lieu.md)); chuyển file sang `hoan_thanh/`.

Luôn duy trì tối đa **hai** ticket trong `dang_lam/` cùng một lúc. Các dự án cá nhân thường bị đình trệ vì mở quá nhiều việc cùng lúc, chứ không phải vì làm quá ít.

## Kế hoạch là một checklist chi tiết

Mỗi mục trong kế hoạch là một hành động cụ thể với một kết quả có thể kiểm tra độc lập, nêu rõ vị trí thực hiện (file, module, dịch vụ), được đánh dấu **`[gate]`** khi cần sự phê duyệt theo [thuc_thi.md](thuc_thi.md) và **`[user]`** khi chỉ có chủ dự án mới có thể làm, đồng thời được đánh dấu `[x]` ngay trong lượt hoàn thành kèm theo bằng chứng cụ thể (commit hash, output của test). Những công việc phát sinh ngoài dự kiến phải được bổ sung thành mục mới trong checklist, không được âm thầm làm.

## Commit tại thời điểm tạo và thời điểm hoàn tất

Commit ticket ngay khoảnh khắc nó được tạo và một lần nữa khi nó chuyển sang `hoan_thanh/` hoặc `da_huy/` — chỉ định rõ ràng đường dẫn file của ticket đó (kèm theo các mục nhật ký tương ứng). Trạng thái công việc chính là thư mục, và lịch sử git là bản ghi duy nhất lưu lại mốc thời gian chuyển trạng thái; một ticket chưa được commit sẽ không có cả hai điều trên.

## Mối liên hệ với sổ nhật ký

[Sổ nhật ký](so_nhat_ky.md) lưu trữ những thứ *được phát hiện*; danh sách công việc lưu trữ những việc *đã quyết định làm*. Một mục trong nhật ký sẽ được "tốt nghiệp" khi có người quyết định bắt tay vào làm, và chuyển sang `nhat_ky/da_giai_quyet/` ngay tại thời điểm ticket tương ứng được tạo ra.
