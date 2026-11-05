---
type: content
owner: claude
stakes: routine
priority: P2
skill: reading
opened: 2026-11-05
---

# Học các cụm từ công sở và khai thác lịch sử commit git làm nguồn ngữ cảnh

## Context
Từ vựng hiện tại được khử trùng lặp theo bộ khóa `(lemma, part_of_speech)`, do đó ứng dụng chỉ đang dạy các từ đơn lẻ. Tiếng Anh công sở trong thực tế lại vận hành chủ yếu dựa trên các cụm từ (phrases / chunks) — ví dụ: "walk me through", "I'm blocked on", "ship it behind a flag", "let's take this offline". Commit message và mô tả Pull Request (PR) là nguồn văn bản xuôi phong phú nhất hàng ngày chứa những cụm từ này, và đã được liệt kê trong phạm vi còn lại của README ("trích xuất git-log/PR").

## Acceptance Criteria
- [ ] Đường ống trích xuất giữ lại các cụm danh từ phổ biến và cụm động từ (verb-particle phrases) qua spaCy song song với từ gốc (lemma), được xếp hạng theo cùng cơ chế.
- [ ] Tập dữ liệu mẫu ban đầu khoảng ~150 cụm từ thông dụng trong họp hành/standup/code-review kèm nghĩa tiếng Việt, do dự án tự biên soạn.
- [ ] Các lượt import ZIP/GitHub có lịch sử `.git` (giới hạn: N commit gần nhất) đóng góp các câu trong commit message làm câu ngữ cảnh thực tế.
- [ ] Các cụm từ xuất hiện bình thường trong các bài tập ôn tập và đọc hiểu; giữ nguyên cách hoạt động của các từ đơn hiện có.
- [ ] Bổ sung các bài test trích xuất với dữ liệu mẫu (fixtures) cho cụm từ và commit message.

## Plan
Viết chi tiết khi bắt tay vào thực hiện. Kiểm tra giới hạn xử lý file nén trong `backend/app/imports.py` trước khi đọc thư mục `.git`.

## Implementation Log

## Deviations
