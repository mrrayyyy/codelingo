# CodeLingo — Hợp đồng Agent (Agent Contract)

CodeLingo là công cụ cá nhân của chủ dự án dùng để học tiếng Anh công sở từ mã nguồn thực tế. File này là điểm vào chung cho mọi agent (Claude Code, Gemini/Antigravity). File này chỉ chứa định tuyến và các con trỏ điều hướng; toàn bộ quy tắc ràng buộc nằm trong [docs/protocol/](docs/protocol/README.md).

## Bắt đầu phiên làm việc (Start of session)
1. Đọc [docs/protocol/README.md](docs/protocol/README.md), sau đó đọc tiếp NAVIGATION, EXECUTION và SECRETS. **Kho lưu trữ này là công khai (public).**
2. Kiểm tra tiến độ công việc hiện tại: `ls docs/backlog/in_progress docs/backlog/ready`. Tiếp tục xử lý ticket đang trong `in_progress` dựa theo mục `## Implementation Log` trước khi bắt đầu việc mới.
3. Đối với mọi thao tác liên quan đến tài liệu, ticket hoặc ledger, đọc toàn bộ hướng dẫn kỹ năng [doc-manager skill](.agents/skills/codelingo-doc-manager/SKILL.md).
4. Kiểm tra các [ADR](docs/decisions/README.md) liên quan trước khi đề xuất bất kỳ thay đổi nào về triển khai (deployment), mô hình dữ liệu (data model), bảo mật riêng tư hoặc giao thức làm việc.

## Quy tắc trong quá trình làm việc (While working)
- Mọi công việc không nhỏ đều phải có ticket trên bảng theo dõi ([KANBAN.md](docs/protocol/KANBAN.md)); các phát hiện/vấn đề mới phát sinh phải ghi ngay vào sổ nhật ký (ledger) trong chính lượt tương tác phát hiện ra ([LEDGER.md](docs/protocol/LEDGER.md)).
- Commit sau mỗi bước làm việc có ý nghĩa và push lên `origin main` sau khi các bước kiểm tra (pre-push checks) vượt qua ([EXECUTION.md](docs/protocol/EXECUTION.md)). Các thao tác liên quan đến hosted-service, secret, schema database và viết lại git history đều phải được xác nhận trước (gated).
- Thay đổi hành vi hệ thống bắt buộc phải cập nhật tài liệu tương ứng trong cùng một ticket ([DOC_SYNC.md](docs/protocol/DOC_SYNC.md)).
- Tuyệt đối không trình bày ước lượng như một phép đo chính xác về trình độ tiếng Anh của người học ([VERIFICATION.md](docs/protocol/VERIFICATION.md)).

## Quy tắc Ngôn ngữ & Đặt tên (Language & Naming Rules)
- **Giao tiếp với chủ dự án**: Bắt buộc dùng **tiếng Việt**.
- **Nội dung tài liệu (Docs)**: Toàn bộ tài liệu (`docs/`, `README.md`, các ticket trong `backlog/`, các bản ghi trong `ledger/`, quyết định kiến trúc trong `decisions/`, runbooks, tài liệu hướng dẫn) bắt buộc phải viết bằng **tiếng Việt**.
- **Tên file & Thư mục**: **Bắt buộc luôn giữ bằng tiếng Anh** (ví dụ: `docs/architecture.md`, `docs/backlog/ready/`, `tools/`, v.v.), tuyệt đối không đổi tên file/thư mục sang tiếng Việt để bảo đảm tính tương thích tuyệt đối với tooling, scripts, git và CI/CD.
- **Mã nguồn, Lệnh & Thuật ngữ**: Code, comment trong code, commit message, command shell, API endpoint và các thuật ngữ kỹ thuật tiêu chuẩn giữ nguyên dạng tiếng Anh kỹ thuật khi cần.
- **Định dạng hiển thị**: Sử dụng link Markdown nhấp được và bảng Markdown chuẩn.

## Định tuyến công việc (Routing)

| Nhiệm vụ | Đọc trước tiên |
| :--- | :--- |
| Backend API, mô hình dữ liệu, plugins | [docs/architecture.md](docs/architecture.md), `backend/app/` |
| Frontend (Next.js) | `frontend/AGENTS.md` — bản Next.js này có điểm khác biệt với dữ liệu huấn luyện; đọc `frontend/node_modules/next/dist/docs/` |
| Chất lượng trích xuất, nội dung từ vựng | [docs/architecture.md](docs/architecture.md) §4, `backend/app/extraction.py`, `backend/app/lexicon.py` |
| Triển khai đám mây (Cloud deployment) | [docs/cloud-deployment.vi.md](docs/cloud-deployment.vi.md), [ADR 0001](docs/decisions/0001-cloud-first-free-tier.md) |
| Định hướng sản phẩm, mức độ ưu tiên | [docs/product/roadmap.md](docs/product/roadmap.md) |
| Quản lý tickets, ledger, ADRs, housekeeping | [doc-manager skill](.agents/skills/codelingo-doc-manager/SKILL.md) |

## Hoàn thành công việc (Finish)
Chạy các kiểm tra liên quan đến phần thay đổi, xem lại diff, đánh dấu hoàn thành checklist trong plan của ticket, cập nhật nhật ký thực hiện (`## Implementation Log`), commit, push. Báo cáo kết quả, danh sách lệnh kiểm tra đã chạy và output, cùng các giới hạn (nếu có) — bằng tiếng Việt, kèm link đến các file liên quan.
