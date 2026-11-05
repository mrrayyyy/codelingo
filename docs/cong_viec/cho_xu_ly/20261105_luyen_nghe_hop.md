---
type: feature
owner: claude
stakes: routine
priority: P2
skill: listening
opened: 2026-11-05
---

# Luyện nghe các cuộc họp kỹ thuật

**Bị chặn bởi (Blocked by):** [Triển khai cloud](../san_sang/20261105_trien_khai_cloud_render_neon_groq.md) (yêu cầu dịch vụ TTS và LLM) và [Tách nhỏ giao diện workspace UI](../san_sang/20261105_tach_giao_dien_workspace.md).

## Ngữ cảnh
Kỹ năng nghe là một kỹ năng ưu tiên hàng đầu; hiện tại hệ thống chỉ mới có bài tập chép chính tả câu đơn lẻ. Các đoạn hội thoại mô phỏng cuộc họp ngắn (2 hoặc 3 người nói, dài 45–90 giây) được xây dựng tự động xung quanh các từ vựng và cụm từ cần ôn tập của người học sẽ giúp rèn luyện khả năng theo dõi thảo luận thực tế.

## Tiêu chí chấp nhận
- [ ] Plugin `listening.meeting`: LLM soạn một đoạn hội thoại ngắn xoay quanh 3–5 từ vựng/cụm từ mục tiêu (định dạng strict JSON, dán nhãn nội dung do AI sinh); TTS đọc hội thoại với các giọng đọc khác nhau tùy theo khả năng của provider.
- [ ] Bài tập gồm: 3 câu hỏi trắc nghiệm đọc hiểu (ý chính, chi tiết, mục đích/thái độ) và 1 bài tập điền từ/cụm từ mục tiêu vào chỗ trống.
- [ ] Tùy chọn tốc độ phát âm thanh 0.8× / 1× và chỉ hiển thị bản gỡ băng (transcript) sau khi người học đã nộp bài trả lời.
- [ ] File âm thanh đã sinh được lưu cache theo từng bài tập kèm giới hạn dung lượng, hoặc sinh lại theo nhu cầu — quyết định và ghi lại giải pháp.
- [ ] Kiểm thử với adapter giả lập; logic chấm điểm mang tính tất định (deterministic).

## Kế hoạch

## Nhật ký thực hiện

## Sai lệch
