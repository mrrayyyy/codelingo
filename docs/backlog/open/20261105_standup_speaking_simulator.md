---
type: feature
owner: claude
stakes: routine
priority: P2
skill: speaking
opened: 2026-11-05
---

# Mô phỏng buổi họp Standup và cuộc họp công sở (Stand-up speaking simulator)

**Blocked by:** [Triển khai cloud](../ready/20261105_cloud_deploy_render_neon_groq.md) (yêu cầu cấu hình Groq STT/LLM/TTS đang hoạt động) và [Tách nhỏ giao diện workspace UI](../ready/20261105_split_workspace_ui.md).

## Context
Kỹ năng nói trong các cuộc họp là mục tiêu kỹ năng hàng đầu của chủ dự án. Hiện tại ứng dụng chỉ có bài tập đọc to (read-aloud), chấm theo độ tương đồng văn bản chuyển đổi. Một bài tập nhập vai tương tác ngắn theo từng lượt sử dụng các bộ điều hợp hiện có: ứng dụng (đóng vai scrum master hoặc reviewer) đặt câu hỏi qua TTS; chủ dự án trả lời bằng giọng nói; STT nhận dạng âm thanh; LLM trả về nhận xét và một phiên bản diễn đạt tự nhiên hơn, để chủ dự án luyện nói nhại lại (shadowing).

## Acceptance Criteria
- [ ] Plugin mới `speaking.standup` xây dựng trên hợp đồng plugin hiện có (`backend/app/contracts.py`, `shared/plugins.ts`).
- [ ] Các tình huống mô phỏng: cuộc họp daily standup, giải thích một vấn đề bị chặn (blocker), đề nghị làm rõ thông tin, cập nhật tiến độ công việc trong buổi review. Lời nhắc ưu tiên dùng các từ vựng và cụm từ mà chính chủ dự án đã thu thập.
- [ ] Mỗi phiên từ 3–5 lượt trao đổi; mỗi lượt trả về: văn bản gỡ băng, 1–3 điểm cần sửa, câu viết lại tự nhiên hơn, các cụm từ hữu ích — định dạng strict JSON, dán nhãn rõ ràng là nhận xét từ AI.
- [ ] Bước luyện nhại (shadowing): TTS đọc câu viết lại tự nhiên; người học đọc lặp lại theo; hiển thị độ khớp văn bản (dán nhãn rõ ràng, không phải điểm số phát âm chuẩn chỉ).
- [ ] Tuyệt đối không lưu trữ file âm thanh; chỉ lưu văn bản gỡ băng và các nhận xét đánh giá.
- [ ] Kiểm thử tự động với các adapter STT/LLM/TTS giả lập.

## Implementation Log

## Deviations
