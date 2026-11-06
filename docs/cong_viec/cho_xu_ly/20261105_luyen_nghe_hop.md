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

Cập nhật 2026-11-06: chủ đề hội thoại dùng chung 4 tình huống của ticket [mô phỏng nói](20261105_mo_phong_noi_standup.md) (standup, phỏng vấn, code review, demo) để luyện nghe và luyện nói bổ trợ nhau. Làm sau ticket luyện nói. Quyết định mặc định: **không lưu file audio**, chỉ lưu kịch bản văn bản; audio sinh lại khi cần, cache tạm có TTL. Ticket không thêm bảng mới nếu tái dùng được `exercises`.

## Tiêu chí chấp nhận
- [ ] Plugin `listening.meeting`: LLM soạn một đoạn hội thoại ngắn xoay quanh 3–5 từ vựng/cụm từ mục tiêu (định dạng strict JSON, dán nhãn nội dung do AI sinh); TTS đọc hội thoại với các giọng đọc khác nhau tùy theo khả năng của provider.
- [ ] Bài tập gồm: 3 câu hỏi trắc nghiệm đọc hiểu (ý chính, chi tiết, mục đích/thái độ) và 1 bài tập điền từ/cụm từ mục tiêu vào chỗ trống.
- [ ] Tùy chọn tốc độ phát âm thanh 0.8× / 1× và chỉ hiển thị bản gỡ băng (transcript) sau khi người học đã nộp bài trả lời.
- [ ] File âm thanh đã sinh được lưu cache theo từng bài tập kèm giới hạn dung lượng, hoặc sinh lại theo nhu cầu — quyết định và ghi lại giải pháp.
- [ ] Kiểm thử với adapter giả lập; logic chấm điểm mang tính tất định (deterministic).

## Kế hoạch
### Khảo sát
- [ ] Kiểm tra các giọng TTS Groq khả dụng (tên giọng, số giọng) để gán giọng khác nhau cho từng người nói; ghi ngày tra cứu
- [ ] Quyết định phát audio: sinh audio từng câu rồi client phát tuần tự (đơn giản, không cần ghép WAV) hay ghép một file phía server; ghi lý do
### Backend
- [ ] Plugin `listening.meeting` (`backend/app/plugins.py` hoặc module riêng): LLM sinh JSON `{scenario, speakers[2..3], lines[{speaker, text}], questions[3]{type: gist|detail|attitude, choices, answer}, cloze{sentence, answer}}` xoay quanh 3–5 từ/cụm đến hạn; kiểm tra schema chặt, đáp án lưu phía server như các plugin khác
- [ ] Endpoint audio từng câu `/practice/{exercise_id}/audio?line=N` với cache tạm trên đĩa (TTL, giới hạn dung lượng), xóa bởi `cleanup_spool`
- [ ] Chấm điểm tất định: trắc nghiệm so khớp đáp án; điền từ so khớp lemma/không phân biệt hoa thường
### Frontend
- [ ] Trình phát: chọn tốc độ 0.8×/1× (`playbackRate`), nghe lại từng câu, transcript chỉ hiện sau khi nộp bài
- [ ] Tích hợp vào phiên học "Hôm nay" thay `dictation` qua `session_listening_plugin`
### Kiểm chứng
- [ ] Adapter LLM/TTS giả lập; test schema sai, dịch vụ lỗi, chấm điểm, cache TTL
- [ ] Playwright: làm một bài nghe end-to-end với audio giả lập
- [ ] `[user]` Chủ dự án làm thử 3 bài ở các tình huống khác nhau và phản hồi độ tự nhiên
### Đồng bộ tài liệu
- [ ] `docs/kien_truc.md` (plugin, endpoint audio), README tính năng, lộ trình

## Nhật ký thực hiện

## Sai lệch
