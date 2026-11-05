# Dọn dẹp và Kiểm tra hệ thống (Housekeeping)

Quy trình kiểm toán lặp lại định kỳ dành cho sổ nhật ký (ledger) và bảng tác vụ (backlog). **Chạy khi được yêu cầu**, hoặc tại thời điểm bắt đầu một phiên làm việc khi kho lưu trữ đã không được đụng tới trong hơn một tuần.

```sh
python3 tools/docs/housekeeping.py              # trả về mã thoát exit 1 khi có mục cần quyết định
python3 tools/docs/housekeeping.py --stale-days 5
```

Lệnh sẽ báo cáo theo các nhóm vấn đề:

1. **Các mục Ledger quá hạn `next_review`, hoặc thiếu trường này.** Trường thông tin này là rào cản duy nhất ngăn ledger biến thành một đống tài liệu không ai đọc.
2. **Backlog bị đình trệ** — các ticket trong `in_progress/` không có thay đổi vượt quá khoảng thời gian cấu hình, hoặc có phần `## Implementation Log` trống, hoặc chưa từng được commit, hoặc có nhiều hơn 2 ticket cùng chạy một lúc; các ticket trong `open/` không nêu rõ nguyên nhân bị chặn (blocker).
3. **Các ticket đã đóng có phần sai lệch (deviations)** mà không có mục ledger nào trích dẫn — kiểm tra xem có phát sinh tồn đọng nào chưa được xử lý hay không.
4. **Quy tắc gây vướng (protocol friction) đang mở** — cần một quyết định dứt khoát từ chủ dự án, không phải là gia hạn ngày mới.
5. **Tài liệu giao thức không được tham chiếu** — một quy tắc không có tài liệu nào liên kết tới là một quy tắc không ai tuân theo.
6. **Các liên kết tương đối bị hỏng (dead links)** (thông qua `tools/docs/check_doc_links.py`).

## Cần làm gì với kết quả đầu ra

Script kiểm tra không bao giờ tự ý đánh dấu hoàn thành, tự đổi ngày hay xóa bỏ bất kỳ mục nào. Hãy báo cáo các phát hiện cho chủ dự án theo danh sách phân nhóm và để chủ dự án quyết định cho từng mục: bắt tay vào làm (tốt nghiệp thành ticket), dời ngày kèm theo lý do, hoặc hủy bỏ kèm theo lý do. Không tạo thêm file báo cáo riêng — một bản báo cáo không ai yêu cầu sẽ chỉ nhanh chóng trở thành một tài liệu cũ kỹ khác.

## Sau khi di chuyển bất kỳ ticket hay mục ledger nào

```sh
python3 tools/docs/check_doc_links.py --fix-moves
```

Việc di chuyển file sẽ âm thầm làm gãy các liên kết tương đối trỏ tới nó; markdown sẽ không cảnh báo lỗi nếu không được kiểm tra.
