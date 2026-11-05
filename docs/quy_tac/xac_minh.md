# Xác minh và kiểm chứng

## Không phỏng đoán

- Không phỏng đoán API thư viện hay các trường cấu hình. Hãy đọc tài liệu hoặc mã nguồn của chính phiên bản đang được cài đặt (`frontend/node_modules/next/dist/docs/`, `.venv/lib/...`), cờ trợ giúp `--help`, hoặc thông báo lỗi cụ thể. Phiên bản Next.js trong dự án này mới hơn hầu hết dữ liệu huấn luyện.
- Không phỏng đoán các thông tin về dịch vụ đám mây (hạn mức gói miễn phí, tên model AI, biểu phí). Luôn kiểm tra tài liệu mới nhất của nhà cung cấp dịch vụ và ghi rõ ngày kiểm tra.
- Khi hành vi của một đoạn mã chưa chắc chắn, hãy viết test để kiểm chứng thực tế thay vì chỉ suy luận trên lý thuyết.

## Dữ kiện phải có ngày tháng

Bất kỳ tuyên bố nào có thể dẫn đến hành động thực thi — hạn mức miễn phí, tên model, hạn ngạch quota, hoặc trạng thái triển khai của ứng dụng — đều phải ghi nhận thời điểm kiểm chứng gần nhất, ví dụ: *"đã xác minh 2026-11-05"*. Một khẳng định do chính bạn viết ra không được coi là bằng chứng; nó cần có ngày kiểm chứng cụ thể như mọi nguồn dữ liệu khác.

## Phải dán nhãn rõ ràng cho các nhận định học tập

Ứng dụng này đánh giá khả năng tiếng Anh của người học. Tuyệt đối không bao giờ trình bày một ước lượng như một phép đo lường chính xác:

- Độ trùng khớp văn bản bóc tách từ giọng nói không phải là chấm điểm phát âm;
- Nhận xét đánh giá từ LLM phải được dán nhãn rõ là ước lượng AI;
- Một từ không rõ định nghĩa phải hiển thị là "chưa có thông tin", tuyệt đối không tự bịa ra;
- Cấp độ CEFR ước tính phải được ghi rõ là giá trị ước lượng.

Một tính năng làm lu mờ hoặc đánh đồng các khái niệm trên bị coi là một lỗi `bug`, kể cả khi giao diện trông có vẻ đẹp hơn.

## Xác minh sửa lỗi

Một thay đổi chưa thể coi là đã được kiểm chứng chỉ vì lần chạy sau cho kết quả xanh. Hãy tự hỏi điều gì khác có thể khiến bài test báo xanh: bài test có thực sự chạy qua đoạn mã vừa thay đổi không, dữ liệu mẫu fixture có chứa sẵn đáp án từ trước hay không, bài kiểm tra đó có chỉ là một chỉ số gián tiếp (status code 200, danh sách không rỗng) thay vì kiểm tra đúng bản chất vấn đề? Luôn ưu tiên bài kiểm tra trực diện, và nêu rõ ràng những gì mà kết quả kiểm tra *chưa* khẳng định được.

Đối với thay đổi trên giao diện UI, lệnh kiểm tra kiểu `typecheck` không được coi là đã xác minh: hãy chạy ứng dụng thực tế hoặc quy trình Playwright và quan sát trực tiếp màn hình vừa được thay đổi.
