# 0001. Ưu tiên Cloud trên các dịch vụ managed miễn phí

- Trạng thái: accepted
- Ngày: 2026-10-27 (ghi nhận ngày 2026-11-05)
- Người quyết định: chủ dự án

## Ngữ cảnh
Bản MVP ban đầu được thiết kế chạy tự host bằng Docker Compose (PostgreSQL, Redis, worker ARQ, mô hình cục bộ Piper/Whisper/Ollama). Tuy nhiên, chủ dự án không muốn chạy các tác vụ nặng hay các model AI cục bộ trên máy tính cá nhân, và muốn sử dụng ứng dụng hàng ngày mà không cần phải khởi chạy bất cứ tiến trình nào trên máy tính.

## Quyết định
Mô hình triển khai ưu tiên là cấu hình đám mây được mô tả trong [trien_khai_cloud.md](../trien_khai_cloud.md):

- Render (gói web service miễn phí) chạy cả ứng dụng Next.js và FastAPI trong cùng một container (`Dockerfile.cloud`);
- Neon (gói miễn phí) lưu trữ dữ liệu học tập lâu dài;
- GitHub Actions thực thi trích xuất từ vựng qua Tree-sitter + spaCy theo nhu cầu (`extract.yml`, `JOB_MODE=github_actions`), chỉ nhận job ID và gọi callback trả về kết quả;
- Groq cung cấp các API tùy chọn cho TTS, STT và LLM.

Cấu hình Compose và chế độ job `inline` vẫn được duy trì phục vụ việc phát triển và chạy test cục bộ. Tất cả các cấu hình đều dùng chung database schema, hợp đồng plugin, logic bóc tách và thuật toán FSRS.

## Các phương án thay thế đã xem xét
- Chạy Compose trên VPS — phát sinh chi phí hàng tháng và tốn công bảo trì server.
- Database PostgreSQL miễn phí của Render — tự động xóa sau 30 ngày, không phù hợp để lưu dữ liệu học tập lâu dài.
- Dùng Vercel cho toàn bộ ứng dụng — giới hạn kích thước payload của serverless function gây lỗi khi tải lên các file ZIP lớn.

## Hệ quả
- Quá trình import repo diễn ra chậm hơn một chút (do thời gian khởi động runner GitHub Actions) nhưng hoàn toàn miễn phí và không gây tải máy cá nhân.
- Các đặc tính của gói miễn phí (tự ngủ khi không dùng, hạn ngạch tài nguyên) sẽ định hình trải nghiệm giao diện người dùng; xem chi tiết tại lộ trình roadmap.
- Phải duy trì tương thích cả 3 chế độ job (`inline`, `arq`, `github_actions`) — **một phần được thay thế bởi [ADR 0004](0004_bo_che_do_arq_redis.md) (2026-11-06): chỉ còn `inline` và `github_actions`**; xem [bản ghi nhật ký về việc đơn giản hóa các chế độ này](../nhat_ky/da_giai_quyet/y_tuong_20261105_don_gian_hoa_che_do_job.md).
- Tính đến ngày 2026-11-05 cấu hình cloud này **chưa** được kích hoạt triển khai thực tế ([xac_minh.md](../xac_minh.md)).
