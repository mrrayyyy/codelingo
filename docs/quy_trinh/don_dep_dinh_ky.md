# Dọn dẹp và kiểm tra hệ thống

Quy trình kiểm toán lặp lại định kỳ dành cho sổ nhật ký và danh sách công việc. **Chạy khi được yêu cầu**, hoặc tại thời điểm bắt đầu một phiên làm việc khi kho lưu trữ đã không được đụng tới trong hơn một tuần.

```sh
python3 tools/docs/housekeeping.py              # trả về mã thoát exit 1 khi có mục cần quyết định
python3 tools/docs/housekeeping.py --stale-days 5
```

Lệnh sẽ báo cáo theo các nhóm vấn đề:

1. **Các mục nhật ký quá hạn `next_review`, hoặc thiếu trường này.** Trường thông tin này là rào cản duy nhất ngăn nhật ký biến thành một đống tài liệu không ai đọc.
2. **Công việc bị đình trệ** — các ticket trong `dang_lam/` không có thay đổi vượt quá khoảng thời gian cấu hình, hoặc có phần `## Nhật ký thực hiện` trống, hoặc chưa từng được commit, hoặc có nhiều hơn 2 ticket cùng chạy một lúc; các ticket trong `cho_xu_ly/` không nêu rõ nguyên nhân bị chặn.
3. **Các ticket đã đóng có phần sai lệch** mà không có mục nhật ký nào trích dẫn — kiểm tra xem có phát sinh tồn đọng nào chưa được xử lý hay không.
4. **Vướng mắc quy tắc (protocol friction) đang mở** — cần một quyết định dứt khoát từ chủ dự án, không phải là gia hạn ngày mới.
5. **Tài liệu quy tắc không được tham chiếu** — một quy tắc không có tài liệu nào liên kết tới là một quy tắc không ai tuân theo.
6. **Các liên kết tương đối bị hỏng** (thông qua `tools/docs/check_doc_links.py`).

## Cần làm gì với kết quả đầu ra

Script kiểm tra không bao giờ tự ý đánh dấu hoàn thành, tự đổi ngày hay xóa bỏ bất kỳ mục nào. Hãy báo cáo các phát hiện cho chủ dự án theo danh sách phân nhóm và để chủ dự án quyết định cho từng mục: bắt tay vào làm (tốt nghiệp thành ticket), dời ngày kèm theo lý do, hoặc hủy bỏ kèm theo lý do. Không tạo thêm file báo cáo riêng — một bản báo cáo không ai yêu cầu sẽ chỉ nhanh chóng trở thành một tài liệu cũ kỹ khác.

## Sau khi di chuyển bất kỳ ticket hay mục nhật ký nào

```sh
python3 tools/docs/check_doc_links.py --fix-moves
```

Việc di chuyển file sẽ âm thầm làm gãy các liên kết tương đối trỏ tới nó; markdown sẽ không cảnh báo lỗi nếu không được kiểm tra.
