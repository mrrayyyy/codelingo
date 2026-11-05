---
name: codelingo-doc-manager
description: Tạo, di chuyển và đóng ticket trong backlog của CodeLingo, ghi và giải quyết các mục trong ledger, viết ADR, đồng bộ tài liệu với code, chạy housekeeping và commit/push các thay đổi tài liệu theo docs/protocol/. Sử dụng khi bắt đầu hoặc kết thúc công việc không nhỏ, phát hiện lỗi/nợ kỹ thuật/sai lệch/ý tưởng, ghi lại quyết định hoặc khi được hỏi về trạng thái dự án.
---

# CodeLingo Documentation Manager (Quản lý Tài liệu CodeLingo)

Quy trình chuẩn hóa cho bộ giao thức tại [docs/protocol/](../../../docs/protocol/README.md).
Giao thức luôn có quyền ưu tiên cao nhất nếu file này và giao thức có điểm không đồng nhất — và sự không đồng nhất đó sẽ được ghi nhận thành một mục ledger `protocol-friction`.

## Quy tắc Ngôn ngữ & Đặt tên cốt lõi
- **Nội dung tài liệu**: Toàn bộ tài liệu (`docs/`, `README.md`, ticket, ledger, ADRs, runbooks) **bắt buộc viết bằng tiếng Việt**.
- **Tên file & Thư mục**: **Bắt buộc giữ 100% bằng tiếng Anh** (`YYYYMMDD_<slug>.md`, `docs/backlog/ready/`, `docs/decisions/`, v.v.), không bao giờ đổi tên file/thư mục sang tiếng Việt để bảo đảm tính tương thích với script và hệ thống.
- **Thuật ngữ & Lệnh kỹ thuật**: Giữ nguyên tiếng Anh tiêu chuẩn đối với code, tên lệnh, biến môi trường, commit types và frontmatter keys (`type`, `status`, `owner`, `next_review`, v.v.).

## 1. Nơi lưu trữ thông tin (Where things go)

| Loại thông tin / Dữ kiện | Nơi lưu trữ | Quy cách đặt tên |
| :--- | :--- | :--- |
| Công việc đã quyết định làm | `docs/backlog/<status>/` | `YYYYMMDD_<slug>.md` tạo từ `docs/backlog/_TEMPLATE.md` |
| Vấn đề phát hiện, chưa quyết định | `docs/ledger/open/` | `<type>_YYYYMMDD_<slug>.md` tạo từ `docs/ledger/_TEMPLATE.md` |
| Lý do chọn giải pháp kiến trúc | `docs/decisions/` | `NNNN-<slug>.md` tạo từ `0000-template.md`; cập nhật bảng chỉ mục trong README |
| Hiện trạng hệ thống đang có gì | `docs/architecture.md`, `README.md`, `docs/cloud-deployment.vi.md` | Cập nhật trực tiếp tại chỗ |
| Định hướng phát triển sản phẩm | `docs/product/roadmap.md` | Cập nhật trạng thái các giai đoạn (phase) khi đóng ticket |
| Quy trình lặp lại định kỳ | `docs/runbooks/<procedure>.md` | Không gắn ngày tháng, không phân kỳ giai đoạn |
| Bản nháp, ghi chú tạm thời | `docs/tmp/<YYYYMMDD>_<task>/` | Đã đưa vào git-ignore |

Các trạng thái: backlog `open → ready → in_progress → done` (hoặc `cancel`); ledger `open → resolved | cancelled`. Trạng thái chính là thư mục chứa file.

## 2. SOP A — Bắt đầu công việc (Start work)

1. Kiểm tra: `ls docs/backlog/in_progress docs/backlog/ready`. Tiếp tục xử lý ticket đang dang dở trong `in_progress` trước khi bắt đầu việc khác; duy trì tối đa hai ticket cùng lúc trong `in_progress`.
2. Nếu chưa có ticket cho công việc quan trọng? Tạo một file mới từ template (`owner: claude` trừ khi chủ dự án chỉ định khác), commit file đó:
   `git add docs/backlog/ready/<file> && git commit -m "docs(backlog): open <slug>"`.
3. Di chuyển ticket: `git mv docs/backlog/ready/<file> docs/backlog/in_progress/<file>`.
4. Viết mục `## Plan` thành một checklist chi tiết; đánh dấu các mục `[gate]` và `[user]`.
   Nếu `stakes: irreversible` → bắt buộc viết `## Blast Radius` trước khi thực thi bất kỳ thao tác nào.
5. Commit: `docs(backlog): start <slug>`.

## 3. SOP B — Trong quá trình thực hiện (During work)

- Sau mỗi bước có ý nghĩa: đánh dấu hoàn thành `[x]` kèm bằng chứng (commit, output lệnh test), thêm một dòng ghi chú có gắn ngày tháng vào `## Implementation Log`, commit ticket cùng lúc với code mà nó mô tả.
- Phát hiện vấn đề ngoài phạm vi đang làm? Ghi nhận ngay vào sổ nhật ký ledger (SOP D) và tiếp tục công việc hiện tại.
- Phát hiện thêm công việc cần thiết bắt buộc phải làm? Thêm mục vào plan; không bao giờ âm thầm thực hiện ngoài kế hoạch.

## 4. SOP C — Hoàn thành công việc (Finish work)

1. Chạy các bài kiểm tra liên quan đến phần thay đổi (EXECUTION.md § Pre-push checks).
2. Đồng bộ tài liệu (Doc sync): cập nhật mọi tài liệu bị ảnh hưởng bởi thay đổi này (bảng trong DOC_SYNC.md).
   Nếu hoàn thành một tính năng người dùng nhìn thấy được → cập nhật mục "Đã triển khai" trong README và roadmap.
3. Viết mục `## Deviations` (hoặc ghi rõ "None").
4. Ghi nhận nợ kỹ thuật tồn đọng vào `docs/ledger/open/`, ghi rõ `source:` từ ticket này.
5. Di chuyển ticket: `git mv docs/backlog/in_progress/<file> docs/backlog/done/<file>`.
6. Tự động sửa liên kết di chuyển (nếu có): `python3 tools/docs/check_doc_links.py --fix-moves`.
7. Nếu có ticket `open/` nào đang bị chặn (blocked) chờ ticket này, hãy chuyển nó sang `ready/`.
8. Commit `docs(backlog): close <slug>` và push lên remote (SOP F).

## 5. SOP D — Sổ nhật ký ghi nhận (Ledger)

Ghi nhận ngay trong chính lượt hội thoại phát hiện ra vấn đề:

```markdown
---
type: bug | tech-debt | drift | process-gap | protocol-friction | idea
status: open
discovered: YYYY-MM-DD
next_review: YYYY-MM-DD   # mặc định +14 ngày
source: <ticket | file:line | CI run URL | conversation>
severity: blocker | high | normal | low
owner: claude | user | either
---
# Tiêu đề tóm tắt một dòng
## Ngữ cảnh & Bằng chứng (Context & Evidence)
(lệnh, kết quả đầu ra, ngày phát hiện)
## Hành động khuyến nghị (Recommended Action)
```

Chuyển đổi thành ticket: tạo ticket mới, sau đó dùng lệnh `git mv` chuyển mục ledger sang `docs/ledger/resolved/`, đổi `status: resolved`, thêm mục `## Resolution` dẫn link đến ticket. Nếu hủy bỏ, di chuyển tương tự sang `cancelled/` kèm theo lý do.

## 6. SOP E — Bản ghi quyết định kiến trúc (ADR)

Viết ADR khi một quyết định không hiển nhiên hoặc từng có tranh luận cần được chốt lại rõ ràng để không phải bàn đi bàn lại. Đặt số thứ tự tiếp theo còn trống, đặt trạng thái `proposed` cho đến khi chủ dự án đồng ý, sau đó đổi thành `accepted`. Thêm một dòng vào bảng tra cứu trong `docs/decisions/README.md`.

## 7. SOP F — Commit và push

```sh
git add <đường_dẫn_cụ_thể>                     # tuyệt đối không dùng git add -A hoặc git add .
python3 tools/docs/scan_secrets.py             # bắt buộc phải xuất "No secrets found"
python3 tools/docs/check_doc_links.py          # kiểm tra tài liệu
.venv/bin/python -m pytest backend/tests -q    # kiểm tra backend nếu có chạm vào
npm --prefix frontend run typecheck            # kiểm tra frontend nếu có chạm vào
git commit -m "<type>(<scope>): <nội dung và lý do>"
git log --oneline origin/main..HEAD            # kiểm tra các commit sẽ được đẩy lên
git push origin main
```

Nội dung commit tuân thủ quy chuẩn Conventional Commits. Các hành động cần xác nhận (Gated) dù việc push là tự động: force push, viết lại lịch sử git, cài đặt/secret của repository, cấu hình hạ tầng dịch vụ cloud, thay đổi dữ liệu hoặc schema database trên môi trường triển khai (xem EXECUTION.md).

## 8. SOP G — Trả lời trạng thái và dọn dẹp hệ thống (Housekeeping)

- "What's next?" (Tiếp theo làm gì?) → Liệt kê các ticket trong `in_progress/` và `ready/` kèm theo `priority` và `skill`, khuyến nghị ticket phù hợp nhất với giai đoạn hiện tại của roadmap.
- "Housekeeping" (Dọn dẹp kiểm tra) → Chạy `python3 tools/docs/housekeeping.py`, báo cáo theo nhóm vấn đề, để chủ dự án tự quyết định từng mục. Tuyệt đối không tự động đánh dấu đã giải quyết hoặc tự đổi lại ngày xem xét.

## 9. Vệ sinh kho lưu trữ công khai (Public-repo hygiene)

Ticket, các mục ledger và commit message đều ở chế độ công khai trên GitHub. Tuyệt đối không lưu trữ khóa bảo mật, URL kèm thông tin xác thực, tên hệ thống nội bộ của công ty/doanh nghiệp, tên đồng nghiệp, hoặc từ vựng/đoạn code lấy từ các dự án riêng tư của công ty. Luôn mô tả các nội dung đó dưới dạng ẩn danh và tổng quát.
