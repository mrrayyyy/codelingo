# Bản ghi kiểm chứng và xác minh (Verification record)

## Bản MVP cơ sở (Base MVP)

- Bộ test API cho chu trình đầu tiên import → trích xuất → flashcard/FSRS: 32 bài test vượt qua (passed).
- Bộ test mở rộng cho trích xuất/plugin/API: 44 bài test vượt qua trước khi hỗ trợ triển khai managed cloud.
- Bản build Next.js production và cả hai bản build Docker image tự host đều thành công.
- Hai bài test trình duyệt Chromium đã vượt qua: import dữ liệu mẫu → tìm kiếm từ vựng → Monaco Editor tô sáng từ vựng → ôn tập FSRS → chấm điểm bài đọc hiểu → lưu cài đặt → chuyển đổi giao diện tiếng Việt; kiểm tra responsive trên mobile/xác thực file import/thoát modal bằng phím Escape.
- Báo cáo kiểm toán phụ thuộc (dependency audit) ghi nhận 0 lỗ hổng bảo mật sau khi build lại Monaco Editor từ ESM với bản vá DOMPurify ghi đè.

## Cấu hình Managed Cloud (Managed cloud profile)

- Bộ test Python/API bao gồm cơ chế điều phối cloud, callbacks, các bộ điều hợp provider, giới hạn kích thước, và khởi chạy web không cần model NLP: 53 bài test vượt qua.
- Kiểm tra kiểu dữ liệu TypeScript (typecheck) vượt qua thành công.
- Bài test truy cập Cloud vượt qua: Basic Auth, bảo vệ các endpoint dữ liệu nhạy cảm, phân quyền route bằng machine-key, và endpoint health check công khai.
- Các bộ điều hợp dịch vụ speech/LLM trên cloud sử dụng phản hồi giả lập (mocked responses) trong bộ kiểm thử; các cuộc gọi Groq thực tế yêu cầu có API key tài khoản và quyền truy cập model.
- Việc triển khai managed cloud thực tế chưa được thực thi: các kết nối Render/Neon và các secret trên cloud chưa được cấu hình. Chưa có URL production nào được ghi nhận. Dockerfile cloud chưa được build thử nghiệm ở máy local theo yêu cầu của người dùng nhằm tránh tải nặng máy cá nhân; việc build Dockerfile này được thiết kế để chạy trực tiếp trên hệ thống Render.
- Các tiến trình preview cục bộ và dịch vụ Docker Compose đã được dừng lại sau khi chuyển đổi định hướng ưu tiên triển khai. Workflow GitHub Actions CI đã được tích hợp để thực hiện các bước kiểm chứng tiếp theo trên runner đám mây.
