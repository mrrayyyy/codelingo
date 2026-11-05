# Điều hướng dự án (Navigation)

Nơi lưu trữ của từng loại thông tin và dữ kiện. Hãy tra cứu tài liệu này trước khi phỏng đoán một endpoint API, một biến cấu hình, hay cách kết nối giữa các module.

## Tài liệu (Docs)

| Loại thông tin / Dữ kiện | Nơi lưu trữ |
| :--- | :--- |
| Cách khởi chạy, tính năng đã làm, cấu trúc thư mục | [README.md](../../README.md) |
| Thiết kế hệ thống, mô hình dữ liệu (ERD), hợp đồng plugin, chính sách trích xuất | [docs/architecture.md](../architecture.md) |
| Triển khai đám mây (Render + Neon + GitHub Actions + Groq) | [docs/cloud-deployment.vi.md](../cloud-deployment.vi.md) |
| Bằng chứng kiểm thử và build có gắn ngày tháng cho các mốc release | [docs/verification.md](../verification.md) |
| Định hướng sản phẩm, đánh giá năng lực, lộ trình phân kỳ | [docs/product/roadmap.md](../product/roadmap.md) |
| Lý do đưa ra các quyết định kiến trúc quan trọng | [docs/decisions/](../decisions/README.md) |
| Quy trình vận hành lặp lại (không gắn ngày tháng, không phân kỳ) | `docs/runbooks/` |
| Công việc đã quyết định làm và nhật ký thực hiện | `docs/backlog/<status>/` — xem [KANBAN.md](KANBAN.md) |
| Vấn đề phát hiện, chưa quyết định xử lý | `docs/ledger/<status>/` — xem [LEDGER.md](LEDGER.md) |
| File nháp tạm thời, không bao giờ commit | `docs/tmp/<YYYYMMDD>_<task>/` |

## Mã nguồn (Code)

| Vấn đề / Thành phần | Vị trí trong mã nguồn |
| :--- | :--- |
| HTTP API (toàn bộ các route) | `backend/app/main.py` |
| Cấu hình và biến môi trường | `backend/app/config.py`, `.env.example`, `.env.cloud.example` |
| Mô hình dữ liệu database | `backend/app/db.py` |
| Đường ống trích xuất từ vựng (tree-sitter → spaCy → xếp hạng) | `backend/app/extraction.py`, `backend/app/lexicon.py` |
| Quản lý tác vụ import, an toàn file nén, worker ARQ | `backend/app/imports.py` |
| Trích xuất từ xa trên GitHub Actions | `backend/app/cloud_jobs.py`, `scripts/cloud_extract.py`, `.github/workflows/extract.yml` |
| Thuật toán lặp lại ngắt quãng (FSRS) | `backend/app/srs.py` |
| Các plugin luyện tập | `backend/app/plugins.py`; hợp đồng tại `backend/app/contracts.py` và `shared/plugins.ts` |
| Bộ điều hợp TTS / STT / LLM / từ điển | `backend/app/adapters.py` |
| Giao diện người dùng Web UI | `frontend/components/workspace.tsx`, `frontend/lib/api.ts` |
| Server-side API proxy và Basic Auth | `frontend/app/api/[...path]/route.ts`, `frontend/proxy.ts` |
| Kiểm thử tự động (Tests) | `backend/tests/`, `frontend/tests/` |
| Tích hợp liên tục (CI) | `.github/workflows/ci.yml` |

`frontend/AGENTS.md` được sinh bởi `next dev` và cảnh báo rằng phiên bản Next.js này có điểm khác biệt so với dữ liệu huấn luyện: hãy đọc `frontend/node_modules/next/dist/docs/` trước khi viết code Next.js.

## Các lệnh thường dùng (Commands)

| Mục đích | Lệnh thực thi (chạy từ thư mục gốc của repository) |
| :--- | :--- |
| Kiểm thử Backend | `.venv/bin/python -m pytest backend/tests -q` |
| Kiểm tra kiểu TypeScript | `npm --prefix frontend run typecheck` |
| Build bản Production | `npm --prefix frontend run build` |
| Khởi chạy Dev cục bộ (cả API + Web) | `.venv/bin/python scripts/dev.py` |
| Kiểm thử trình duyệt (khi app đang chạy) | `cd frontend && npm run test:e2e` |
| Kiểm tra liên kết tài liệu | `python3 tools/docs/check_doc_links.py` (thêm `--fix-moves` sau khi di chuyển file) |
| Kiểm tra tình trạng tài liệu (Housekeeping audit) | `python3 tools/docs/housekeeping.py` |
