---
type: process-gap
status: open
discovered: 2026-11-05
next_review: 2026-11-19
source: product review in 20261105_khoi_tao_quy_trinh_tai_lieu_agent
severity: high
owner: user
---

# Import mã nguồn công ty vào cấu hình cloud có thể vi phạm chính sách bảo mật

## Ngữ cảnh và bằng chứng
Mục đích của CodeLingo là học tiếng Anh từ chính mã nguồn mà chủ dự án làm việc hàng ngày, phần lớn thuộc quyền sở hữu của công ty nơi làm việc. Trong cấu hình đám mây ([ADR 0001](../../quyet_dinh/0001_uu_tien_cloud_mien_phi.md)), một repository được import sẽ được tải xuống bởi runner GitHub Actions của một repository **công khai** (`.github/workflows/extract.yml`), các câu ngữ cảnh (comment, docstring, chuỗi string kèm theo đường dẫn file và số dòng) sẽ được lưu trữ trong database Neon (`context_sentences` trong `docs/kien_truc.md`), và nội dung luyện tập có thể được gửi tới API Groq (`backend/app/adapters.py`). Script `scripts/cloud_extract.py` chỉ in log số lượng thống kê nên không làm lộ nội dung qua log Actions công khai — nhưng dữ liệu vẫn bị đưa ra khỏi phạm vi kiểm soát của doanh nghiệp. Xác định khi đọc các file trên ngày 2026-11-05.

## Hành động khuyến nghị
Chủ dự án xem xét và lựa chọn một trong các phương án:
1. Chỉ import các kho mã nguồn công khai hoặc do cá nhân sở hữu trên cấu hình cloud; sử dụng cấu hình cục bộ (chế độ inline, không dùng LLM) cho mã nguồn công ty.
2. Kiểm tra chính sách bảo mật của doanh nghiệp và nếu được phép, ghi chú rõ những repository nào được phép import.
3. Bổ sung tính năng import "chỉ dán văn bản xuôi" (chỉ nhập commit message, nội dung PR do chính chủ dự án viết) mà không bao giờ tải lên toàn bộ mã nguồn.

Cho đến khi có quyết định chính thức, quy định tại [bao_mat.md](../../quy_tac/bao_mat.md) giới hạn các agent chỉ được import các repository công khai hoặc bộ mẫu đi kèm.
