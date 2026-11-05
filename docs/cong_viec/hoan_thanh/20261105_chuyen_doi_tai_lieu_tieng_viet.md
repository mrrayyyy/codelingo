---
type: docs
owner: claude
stakes: routine
priority: P1
opened: 2026-11-05
---

# Chuyển đổi toàn bộ tài liệu sang tiếng Việt và thiết lập quy tắc ngôn ngữ

## Ngữ cảnh
Yêu cầu trực tiếp từ chủ dự án:
1. Chuyển đổi toàn bộ nội dung tài liệu trong dự án (`docs/`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `frontend/AGENTS.md`, các file kỹ năng và tài liệu hướng dẫn) sang tiếng Việt để phục vụ tốt nhất việc theo dõi và học tập.
2. Thiết lập quy tắc cốt lõi về ngôn ngữ và đặt tên:
   - **Tên file và thư mục**: Bắt buộc giữ nguyên bằng tiếng Anh để đảm bảo tương thích đường dẫn, tooling, git history và scripts (`tools/docs/check_doc_links.py`, `tools/docs/housekeeping.py`).
   - **Nội dung tài liệu**: Bắt buộc viết bằng tiếng Việt.
   - **Giao tiếp**: Trao đổi với chủ dự án bằng tiếng Việt.
   - **Mã nguồn & Kỹ thuật**: Tên biến, hàm, mã nguồn, lệnh shell, endpoint API và thuật ngữ kỹ thuật giữ nguyên dạng chuẩn tiếng Anh.

## Tiêu chí chấp nhận
- [x] Bổ sung quy tắc ngôn ngữ và đặt tên vào `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `frontend/AGENTS.md`, `docs/quy_tac/README.md`, `docs/quy_tac/dong_bo_tai_lieu.md`, `docs/quy_tac/dieu_huong.md`, `.agents/skills/codelingo-doc-manager/SKILL.md`.
- [x] Chuyển đổi `README.md` sang tiếng Việt.
- [x] Chuyển đổi toàn bộ tài liệu trong `docs/quy_tac/` sang tiếng Việt.
- [x] Chuyển đổi toàn bộ tài liệu trong `docs/quyet_dinh/` (ADR) sang tiếng Việt.
- [x] Chuyển đổi các tài liệu kiến trúc, triển khai, hướng dẫn (`docs/kien_truc.md`, `docs/trien_khai_cloud.md`, `docs/xac_minh.md`, `docs/quy_trinh/don_dep_dinh_ky.md`, `docs/san_pham/lo_trinh.md`, `docs/tam/README.md`).
- [x] Chuyển đổi các template và ticket trong `docs/cong_viec/` và `docs/nhat_ky/` sang tiếng Việt, giữ nguyên header và field cần thiết cho tooling.
- [x] Chuyển đổi file kỹ năng `.agents/skills/codelingo-doc-manager/SKILL.md`.
- [x] Chạy kiểm tra: `python3 tools/docs/check_doc_links.py`, `python3 tools/docs/housekeeping.py`, `python3 tools/docs/scan_secrets.py`, test backend và typecheck frontend đều vượt qua (100% pass, 0 dead links).

## Kế hoạch

### Nhóm 1: Mở ticket & Cập nhật quy tắc cốt lõi
- [x] Tạo ticket và chuyển sang `dang_lam/`.
- [x] Cập nhật quy tắc vào `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `frontend/AGENTS.md`.
- [x] Cập nhật kỹ năng `.agents/skills/codelingo-doc-manager/SKILL.md`.

### Nhóm 2: Chuyển đổi bộ quy tắc & README chính
- [x] Cập nhật `README.md`.
- [x] Cập nhật `docs/quy_tac/README.md`, `dieu_huong.md`, `thuc_thi.md`, `bang_cong_viec.md`, `so_nhat_ky.md`, `dong_bo_tai_lieu.md`, `xac_minh.md`, `bao_mat.md`.

### Nhóm 3: Chuyển đổi Kiến trúc, Sản phẩm, Quy trình & Quyết định (ADR)
- [x] Cập nhật `docs/kien_truc.md`, `docs/san_pham/lo_trinh.md`, `docs/xac_minh.md`, `docs/trien_khai_cloud.md`, `docs/quy_trinh/don_dep_dinh_ky.md`, `docs/tam/README.md`.
- [x] Cập nhật `docs/quyet_dinh/README.md`, `0000_mau.md`, `0001_uu_tien_cloud_mien_phi.md`, `0002_quy_trinh_docs_as_code.md`, `0003_repo_cong_khai_tu_dong_commit_push.md`.

### Nhóm 4: Chuyển đổi Công việc & Nhật ký
- [x] Cập nhật `docs/cong_viec/_mau.md` và các ticket trong `san_sang/`, `cho_xu_ly/`, `hoan_thanh/`.
- [x] Cập nhật `docs/nhat_ky/_mau.md` và các mục trong `dang_mo/`.

### Nhóm 5: Kiểm tra toàn diện & Hoàn tất
- [x] Chạy `check_doc_links.py` và `housekeeping.py`.
- [x] Chạy tests và kiểm tra bảo mật `scan_secrets.py`.
- [x] Chuyển ticket sang `hoan_thanh/`, commit và push `origin main`.

## Nhật ký thực hiện
- 2026-11-05: Khởi tạo ticket chuyển đổi toàn bộ tài liệu sang tiếng Việt và thiết lập quy tắc ngôn ngữ.
- 2026-11-05: Hoàn thành Nhóm 1: Cập nhật hợp đồng agent (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `frontend/AGENTS.md`) và kỹ năng quản lý tài liệu `SKILL.md` sang tiếng Việt cùng quy tắc giữ nguyên tên file/thư mục tiếng Anh.
- 2026-11-05: Hoàn thành Nhóm 2: Chuyển đổi toàn bộ `README.md` và 8 tài liệu quy tắc trong `docs/quy_tac/` sang tiếng Việt.
- 2026-11-05: Hoàn thành Nhóm 3: Chuyển đổi toàn bộ tài liệu kiến trúc, lộ trình roadmap, bản ghi xác minh, runbooks và toàn bộ các ADR trong `docs/quyet_dinh/` sang tiếng Việt.
- 2026-11-05: Hoàn thành Nhóm 4: Chuyển đổi toàn bộ templates, tickets (`san_sang/`, `cho_xu_ly/`, `hoan_thanh/`) trong `docs/cong_viec/` và các mục trong `docs/nhat_ky/` sang tiếng Việt, bảo toàn các header và trường metadata phục vụ tooling.
- 2026-11-05: Hoàn thành Nhóm 5: Chạy toàn bộ bộ kiểm tra gồm `check_doc_links.py` (0 dead links trong 39 files), `housekeeping.py` (sạch lỗi), `scan_secrets.py` (không có secret), pytest (53 passed), và typecheck (exit 0). Chuyển ticket sang `hoan_thanh/` và chuẩn bị push.

## Sai lệch
Không có
