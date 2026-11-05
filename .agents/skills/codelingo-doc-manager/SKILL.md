---
name: codelingo-doc-manager
description: Tạo, di chuyển và đóng ticket trong danh sách công việc của CodeLingo, ghi và giải quyết các mục trong nhật ký, viết ADR, đồng bộ tài liệu với code, chạy housekeeping và commit/push các thay đổi tài liệu theo docs/quy_tac/. Sử dụng khi bắt đầu hoặc kết thúc công việc không nhỏ, phát hiện lỗi/nợ kỹ thuật/sai lệch/ý tưởng, ghi lại quyết định hoặc khi được hỏi về trạng thái dự án.
---

# Quản lý tài liệu CodeLingo

Quy trình chuẩn hóa cho bộ quy tắc tại [docs/quy_tac/](../../../docs/quy_tac/README.md).
Quy tắc luôn có quyền ưu tiên cao nhất nếu file này và quy tắc có điểm không đồng nhất — và sự không đồng nhất đó sẽ được ghi nhận thành một mục nhật ký `protocol-friction`.

## Quy tắc ngôn ngữ và đặt tên cốt lõi
- **Nội dung tài liệu**: Toàn bộ tài liệu (`docs/`, `README.md`, ticket, nhật ký, ADRs, quy trình) **bắt buộc viết bằng tiếng Việt**.
- **Tên thư mục**: **Bắt buộc dùng tiếng Việt không dấu snake_case** (`docs/quy_tac/`, `docs/cong_viec/`, `docs/quyet_dinh/`, `docs/nhat_ky/`, `docs/san_pham/`, `docs/quy_trinh/`, `docs/tam/`).
- **Tên file**: **Bắt buộc đặt bằng tiếng Việt không dấu snake_case** (`YYYYMMDD_<slug>.md`, `kien_truc.md`, `lo_trinh.md`, v.v.). Các file entrypoint hệ thống (`README.md`, `AGENTS.md`) giữ nguyên để tương thích.
- **Từ khóa học thuật và lệnh kỹ thuật**: Chỉ giữ nguyên tiếng Anh đối với các thuật ngữ chuyên ngành (Docker, Next.js, FastAPI, Redis, FSRS, Git, token, OAuth, PR, CI/CD...) và các trường metadata (`type`, `status`, `owner`, `next_review`, v.v.).

## 1. Nơi lưu trữ thông tin

| Loại thông tin / Dữ kiện | Nơi lưu trữ | Quy cách đặt tên |
| :--- | :--- | :--- |
| Công việc đã quyết định làm | `docs/cong_viec/<trang_thai>/` | `YYYYMMDD_<slug>.md` tạo từ `docs/cong_viec/_mau.md` |
| Vấn đề phát hiện, chưa quyết định | `docs/nhat_ky/dang_mo/` | `<loai>_YYYYMMDD_<slug>.md` tạo từ `docs/nhat_ky/_mau.md` |
| Lý do chọn giải pháp kiến trúc | `docs/quyet_dinh/` | `NNNN_<slug>.md` tạo từ `0000_mau.md`; cập nhật bảng chỉ mục trong README |
| Hiện trạng hệ thống đang có gì | `docs/kien_truc.md`, `README.md`, `docs/trien_khai_cloud.md` | Cập nhật trực tiếp tại chỗ |
| Định hướng phát triển sản phẩm | `docs/san_pham/lo_trinh.md` | Cập nhật trạng thái các giai đoạn khi đóng ticket |
| Quy trình lặp lại định kỳ | `docs/quy_trinh/<ten_quy_trinh>.md` | Không gắn ngày tháng, không phân kỳ giai đoạn |
| Bản nháp, ghi chú tạm thời | `docs/tam/<YYYYMMDD>_<task>/` | Đã đưa vào git-ignore |

Các trạng thái: công việc `cho_xu_ly → san_sang → dang_lam → hoan_thanh` (hoặc `da_huy`); nhật ký `dang_mo → da_giai_quyet | da_huy`. Trạng thái chính là thư mục chứa file.

## 2. Quy trình A — Bắt đầu công việc

1. Kiểm tra: `ls docs/cong_viec/dang_lam docs/cong_viec/san_sang`. Tiếp tục xử lý ticket đang dang dở trong `dang_lam` trước khi bắt đầu việc khác; duy trì tối đa hai ticket cùng lúc trong `dang_lam`.
2. Nếu chưa có ticket cho công việc quan trọng? Tạo một file mới từ template (`owner: claude` trừ khi chủ dự án chỉ định khác), commit file đó:
   `git add docs/cong_viec/san_sang/<file> && git commit -m "docs(cong_viec): open <slug>"`.
3. Di chuyển ticket: `git mv docs/cong_viec/san_sang/<file> docs/cong_viec/dang_lam/<file>`.
4. Viết mục `## Kế hoạch` thành một checklist chi tiết; đánh dấu các mục `[gate]` và `[user]`.
   Nếu `stakes: irreversible` → bắt buộc viết `## Bán kính ảnh hưởng` trước khi thực thi bất kỳ thao tác nào.
5. Commit: `docs(cong_viec): start <slug>`.

## 3. Quy trình B — Trong quá trình thực hiện

- Sau mỗi bước có ý nghĩa: đánh dấu hoàn thành `[x]` kèm bằng chứng (commit, output lệnh test), thêm một dòng ghi chú có gắn ngày tháng vào `## Nhật ký thực hiện`, commit ticket cùng lúc với code mà nó mô tả.
- Phát hiện vấn đề ngoài phạm vi đang làm? Ghi nhận ngay vào sổ nhật ký (Quy trình D) và tiếp tục công việc hiện tại.
- Phát hiện thêm công việc cần thiết bắt buộc phải làm? Thêm mục vào kế hoạch; không bao giờ âm thầm thực hiện ngoài kế hoạch.

## 4. Quy trình C — Hoàn thành công việc

1. Chạy các bài kiểm tra liên quan đến phần thay đổi (thuc_thi.md § Các bước kiểm tra trước khi push).
2. Đồng bộ tài liệu: cập nhật mọi tài liệu bị ảnh hưởng bởi thay đổi này (bảng trong dong_bo_tai_lieu.md).
   Nếu hoàn thành một tính năng người dùng nhìn thấy được → cập nhật mục "Các tính năng đã triển khai" trong README và lộ trình.
3. Viết mục `## Sai lệch` (hoặc ghi rõ "None").
4. Ghi nhận nợ kỹ thuật tồn đọng vào `docs/nhat_ky/dang_mo/`, ghi rõ `source:` từ ticket này.
5. Di chuyển ticket: `git mv docs/cong_viec/dang_lam/<file> docs/cong_viec/hoan_thanh/<file>`.
6. Tự động sửa liên kết di chuyển: `python3 tools/docs/check_doc_links.py --fix-moves`.
7. Nếu có ticket `cho_xu_ly/` nào đang bị chặn chờ ticket này, hãy chuyển nó sang `san_sang/`.
8. Commit `docs(cong_viec): close <slug>` và push lên remote (Quy trình F).

## 5. Quy trình D — Sổ nhật ký ghi nhận

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
## Ngữ cảnh và bằng chứng
(lệnh, kết quả đầu ra, ngày phát hiện)
## Hành động khuyến nghị
```

Chuyển đổi thành ticket: tạo ticket mới, sau đó dùng lệnh `git mv` chuyển mục nhật ký sang `docs/nhat_ky/da_giai_quyet/`, đổi `status: resolved`, thêm mục `## Giải quyết` dẫn link đến ticket. Nếu hủy bỏ, di chuyển tương tự sang `da_huy/` kèm theo lý do.

## 6. Quy trình E — Quyết định kiến trúc (ADR)

Viết ADR khi một quyết định không hiển nhiên hoặc từng có tranh luận cần được chốt lại rõ ràng để không phải bàn đi bàn lại. Đặt số thứ tự tiếp theo còn trống, đặt trạng thái `proposed` cho đến khi chủ dự án đồng ý, sau đó đổi thành `accepted`. Thêm một dòng vào bảng tra cứu trong `docs/quyet_dinh/README.md`.

## 7. Quy trình F — Commit và push

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

Nội dung commit tuân thủ quy chuẩn Conventional Commits. Các hành động cần xác nhận dù việc push là tự động: force push, viết lại lịch sử git, cài đặt/secret của repository, cấu hình hạ tầng dịch vụ cloud, thay đổi dữ liệu hoặc schema database trên môi trường triển khai (xem thuc_thi.md).

## 8. Quy trình G — Trả lời trạng thái và dọn dẹp hệ thống

- "Tiếp theo làm gì?" → Liệt kê các ticket trong `dang_lam/` và `san_sang/` kèm theo `priority` và `skill`, khuyến nghị ticket phù hợp nhất với giai đoạn hiện tại của roadmap.
- "Dọn dẹp kiểm tra" → Chạy `python3 tools/docs/housekeeping.py`, báo cáo theo nhóm vấn đề, để chủ dự án tự quyết định từng mục. Tuyệt đối không tự động đánh dấu đã giải quyết hoặc tự đổi lại ngày xem xét.

## 9. Vệ sinh kho lưu trữ công khai

Ticket, các mục nhật ký và commit message đều ở chế độ công khai trên GitHub. Tuyệt đối không lưu trữ khóa bảo mật, URL kèm thông tin xác thực, tên hệ thống nội bộ của công ty/doanh nghiệp, tên đồng nghiệp, hoặc từ vựng/đoạn code lấy từ các dự án riêng tư của công ty. Luôn mô tả các nội dung đó dưới dạng ẩn danh và tổng quát.
