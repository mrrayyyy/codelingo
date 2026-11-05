# CodeLingo — Hợp đồng Agent

CodeLingo là công cụ cá nhân của chủ dự án dùng để học tiếng Anh công sở từ mã nguồn thực tế. File này là điểm vào chung cho mọi agent (Claude Code, Gemini/Antigravity). File này chỉ chứa định tuyến và các con trỏ điều hướng; toàn bộ quy tắc ràng buộc nằm trong [docs/quy_tac/](docs/quy_tac/README.md).

## Bắt đầu phiên làm việc
1. Đọc [docs/quy_tac/README.md](docs/quy_tac/README.md), sau đó đọc tiếp điều hướng (`dieu_huong.md`), thực thi (`thuc_thi.md`) và bảo mật (`bao_mat.md`). **Kho lưu trữ này là công khai (public).**
2. Kiểm tra tiến độ công việc hiện tại: `ls docs/cong_viec/dang_lam docs/cong_viec/san_sang`. Tiếp tục xử lý ticket đang trong `dang_lam` dựa theo mục `## Nhật ký thực hiện` trước khi bắt đầu việc mới.
3. Đối với mọi thao tác liên quan đến tài liệu, ticket hoặc sổ nhật ký, đọc toàn bộ hướng dẫn kỹ năng [doc-manager skill](.agents/skills/codelingo-doc-manager/SKILL.md).
4. Kiểm tra các [ADR](docs/quyet_dinh/README.md) liên quan trước khi đề xuất bất kỳ thay đổi nào về triển khai, mô hình dữ liệu, bảo mật riêng tư hoặc quy tắc làm việc.

## Quy tắc trong quá trình làm việc
- Mọi công việc không nhỏ đều phải có ticket trên bảng theo dõi ([bang_cong_viec.md](docs/quy_tac/bang_cong_viec.md)); các phát hiện/vấn đề mới phát sinh phải ghi ngay vào sổ nhật ký trong chính lượt tương tác phát hiện ra ([so_nhat_ky.md](docs/quy_tac/so_nhat_ky.md)).
- Commit sau mỗi bước làm việc có ý nghĩa và push lên `origin main` sau khi các bước kiểm tra (pre-push checks) vượt qua ([thuc_thi.md](docs/quy_tac/thuc_thi.md)). Các thao tác liên quan đến hosted-service, secret, schema database và viết lại git history đều phải được xác nhận trước (gated).
- Thay đổi hành vi hệ thống bắt buộc phải cập nhật tài liệu tương ứng trong cùng một ticket ([dong_bo_tai_lieu.md](docs/quy_tac/dong_bo_tai_lieu.md)).
- Tuyệt đối không trình bày ước lượng như một phép đo chính xác về trình độ tiếng Anh của người học ([xac_minh.md](docs/quy_tac/xac_minh.md)).

## Quy tắc ngôn ngữ và đặt tên
- **Giao tiếp với chủ dự án**: Bắt buộc dùng **tiếng Việt**.
- **Nội dung tài liệu**: Toàn bộ tài liệu (`docs/`, `README.md`, các ticket trong `cong_viec/`, các bản ghi trong `nhat_ky/`, quyết định kiến trúc trong `quyet_dinh/`, quy trình trong `quy_trinh/`, tài liệu hướng dẫn) bắt buộc phải viết bằng **tiếng Việt**.
- **Tên thư mục**: Bắt buộc đặt bằng **tiếng Việt không dấu snake_case** (`docs/quy_tac/`, `docs/cong_viec/`, `docs/quyet_dinh/`, `docs/nhat_ky/`, `docs/san_pham/`, `docs/quy_trinh/`, `docs/tam/`).
- **Tên file tài liệu**: Bắt buộc đặt bằng **tiếng Việt không dấu snake_case** (`docs/kien_truc.md`, `docs/xac_minh.md`, `docs/trien_khai_cloud.md`, `YYYYMMDD_<slug>.md`, v.v.). Các file entrypoint chuẩn hệ thống (`README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) giữ nguyên để tương thích với tooling và harness của IDE/agent.
- **Mã nguồn, lệnh và từ khóa học thuật/kỹ thuật**: Code, comment trong code, commit message, command shell, API endpoint và các thuật ngữ chuyên ngành (Docker, Next.js, FastAPI, Redis, FSRS, Git, token, OAuth, PR, CI/CD...) giữ nguyên dạng tiếng Anh kỹ thuật chuẩn.
- **Định dạng hiển thị**: Sử dụng link Markdown nhấp được và bảng Markdown chuẩn.

## Định tuyến công việc

| Nhiệm vụ | Đọc trước tiên |
| :--- | :--- |
| Backend API, mô hình dữ liệu, plugins | [docs/kien_truc.md](docs/kien_truc.md), `backend/app/` |
| Frontend (Next.js) | `frontend/AGENTS.md` — bản Next.js này có điểm khác biệt với dữ liệu huấn luyện; đọc `frontend/node_modules/next/dist/docs/` |
| Chất lượng trích xuất, nội dung từ vựng | [docs/kien_truc.md](docs/kien_truc.md) §4, `backend/app/extraction.py`, `backend/app/lexicon.py` |
| Triển khai đám mây | [docs/trien_khai_cloud.md](docs/trien_khai_cloud.md), [ADR 0001](docs/quyet_dinh/0001_uu_tien_cloud_mien_phi.md) |
| Định hướng sản phẩm, mức độ ưu tiên | [docs/san_pham/lo_trinh.md](docs/san_pham/lo_trinh.md) |
| Quản lý tickets, nhật ký, ADRs, housekeeping | [doc-manager skill](.agents/skills/codelingo-doc-manager/SKILL.md) |

## Hoàn thành công việc
Chạy các kiểm tra liên quan đến phần thay đổi, xem lại diff, đánh dấu hoàn thành checklist trong kế hoạch của ticket, cập nhật nhật ký thực hiện (`## Nhật ký thực hiện`), commit, push. Báo cáo kết quả, danh sách lệnh kiểm tra đã chạy và output, cùng các giới hạn (nếu có) — bằng tiếng Việt, kèm link đến các file liên quan.
