# Sổ nhật ký ghi nhận (`docs/ledger/`)

Nơi ghi nhận mọi vấn đề được phát hiện cần chú ý trong tương lai nhưng chưa được chốt quyết định đưa vào kế hoạch thực hiện. Mỗi vấn đề là một file riêng biệt, trạng thái tính theo thư mục chứa file: `open/`, `resolved/`, `cancelled/`. Khởi tạo từ file mẫu [`_TEMPLATE.md`](../ledger/_TEMPLATE.md); tên file tuân thủ quy tắc `<type>_YYYYMMDD_<slug>.md`.

Nếu không có sổ nhật ký này, các phát hiện sẽ chỉ nằm lại trong lịch sử chat và biến mất khi phiên làm việc kết thúc.

## Quy tắc Ngôn ngữ & Đặt tên
- **Tên file & Thư mục**: Bắt buộc giữ **100% bằng tiếng Anh** theo mẫu `<type>_YYYYMMDD_<slug>.md` (ví dụ: `tech-debt_20261105_main_py_single_module.md`). Thư mục trạng thái (`open/`, `resolved/`, `cancelled/`) giữ nguyên tiếng Anh.
- **Nội dung bản ghi**: Bắt buộc viết bằng **tiếng Việt**.
- **Frontmatter & Tiêu đề chuẩn**: Các khóa metadata (`type:`, `status:`, `discovered:`, `next_review:`, `source:`, `severity:`, `owner:`) và các tiêu đề chuẩn (`## Ngữ cảnh & Bằng chứng`, `## Hành động khuyến nghị`, `## Giải quyết`) được duy trì chuẩn xác để tương thích với script kiểm tra (`tools/docs/housekeeping.py`).

## Các loại phát hiện (Types)

`bug` (lỗi hệ thống), `tech-debt` (nợ kỹ thuật), `drift` (tài liệu không còn khớp với mã nguồn hoặc dịch vụ đám mây thực tế), `process-gap` (lỗ hổng quy trình), `protocol-friction` (quy tắc gây vướng víu), `idea` (ý tưởng sản phẩm đáng lưu lại nhưng chưa xếp lịch).

## Thời điểm ghi nhận (Filing triggers)

Ghi nhận **ngay trong chính lượt hội thoại phát hiện ra vấn đề**, không chờ đến cuối phiên làm việc:

- **Tài liệu không còn khớp với mã nguồn hoặc dịch vụ cloud** → `drift`. Sửa tài liệu ngay nếu tốn ít công sức; dù sửa hay chưa vẫn phải ghi nhận vào ledger để lưu vết sự sai lệch.
- **Một kiểm tra báo xanh (passed) nhưng kết quả thực tế lại sai** → ghi nhận ngay, giải thích rõ vì sao kết quả kiểm tra màu xanh lại gây hiểu nhầm.
- **Khi tạo ra một giải pháp tạm bợ (workaround) hoặc mã nguồn thừa** → ghi nhận `tech-debt` ngay khoảnh khắc tạo ra nó.
- **Một quy tắc làm tốn thời gian hoặc cản trở công việc chính đáng** → `protocol-friction`.
- **Nảy sinh một ý tưởng sản phẩm mới trong khi đang làm việc khác** → ghi nhận `idea` thay vì bỏ dở việc hiện tại để làm ngay.

## Bắt buộc phải có bằng chứng (Evidence is mandatory)

Mỗi bản ghi phải nêu rõ cách thức xác định vấn đề: câu lệnh thực thi, kết quả trả về, ngày tháng, file và số dòng cụ thể. Một bản ghi không có bằng chứng sẽ không thể kiểm chứng lại được nhưng lại dễ bị ngộ nhận là đúng.

Quy định cách trích dẫn: commit ghi rõ `codelingo <sha>`, CI run ghi đầy đủ URL, issue hoặc PR ghi dạng `mrrayyyy/codelingo#12`.

## Phòng ngừa lãng quên (Anti-staleness)

Trường `next_review` là bắt buộc trên mọi mục đang mở (`open/`) (mặc định là sau 2 tuần).
Quy trình [docs/runbooks/housekeeping.md](../runbooks/housekeeping.md) sẽ tự động rà soát các mục quá hạn; quy trình này không bao giờ tự ý đánh dấu hoàn thành, đổi ngày hay xóa bỏ — chủ dự án sẽ là người quyết định.

## Giải quyết một mục (Resolving)

Chuyển file sang `resolved/` (hoặc `cancelled/`) bằng lệnh `git mv`, cập nhật trường `status`, và thêm một đoạn ngắn nêu rõ điều gì đã giải quyết mục này (commit, ticket) hoặc lý do hủy bỏ. Luôn chạy `python3 tools/docs/check_doc_links.py --fix-moves` sau mỗi lần di chuyển file.
