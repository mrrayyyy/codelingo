---
type: feature
owner: claude
stakes: irreversible
priority: P2
skill: speaking
opened: 2026-11-05
---

# Mô phỏng nói: standup, phỏng vấn xin việc, code review, demo

**Bị chặn bởi (Blocked by):** [Triển khai cloud](../dang_lam/20261105_trien_khai_cloud_render_neon_groq.md) (yêu cầu cấu hình Groq STT/LLM/TTS đang hoạt động) và [Tách nhỏ giao diện workspace UI](../san_sang/20261105_tach_giao_dien_workspace.md).

## Ngữ cảnh
Kỹ năng nói trong các cuộc họp là mục tiêu kỹ năng hàng đầu của chủ dự án. Hiện tại ứng dụng chỉ có bài tập đọc to (read-aloud), chấm theo độ tương đồng văn bản chuyển đổi. Một bài tập nhập vai tương tác ngắn theo từng lượt sử dụng các bộ điều hợp hiện có: ứng dụng (đóng vai scrum master hoặc reviewer) đặt câu hỏi qua TTS; chủ dự án trả lời bằng giọng nói; STT nhận dạng âm thanh; LLM trả về nhận xét và một phiên bản diễn đạt tự nhiên hơn, để chủ dự án luyện nói nhại lại (shadowing).

Cập nhật 2026-11-06: chủ dự án chọn cả 4 tình huống, làm theo thứ tự **daily standup → phỏng vấn xin việc → code review / thảo luận kỹ thuật → demo / thuyết trình**. Phỏng vấn được ưu tiên thứ hai vì khớp mục tiêu dùng dự án làm portfolio khi ứng tuyển. Kịch bản là dữ liệu (file JSON), nên thêm tình huống mới không phải sửa code plugin. Dịch vụ AI dùng Groq (TTS/STT/LLM) đã cấu hình ở bước triển khai cloud.

## Tiêu chí chấp nhận
- [ ] Plugin mới `speaking.roleplay` xây dựng trên hợp đồng plugin hiện có (`backend/app/contracts.py`, `shared/plugins.ts`), nhận tham số `scenario`.
- [ ] 4 bộ kịch bản: `standup` (hôm qua/hôm nay/blocker, trả lời câu hỏi thêm), `interview` (giới thiệu bản thân, kể về dự án, câu hỏi behavioral và kỹ thuật, dựa trên phần giới thiệu ngắn chủ dự án tự nhập trong hồ sơ), `code_review` (giải thích thiết kế, phản biện, hỏi lại cho rõ), `demo` (giới thiệu tính năng, trả lời câu hỏi). Lời nhắc ưu tiên từ vựng/cụm từ đến hạn của chính người học.
- [ ] Mỗi phiên từ 3–5 lượt trao đổi; mỗi lượt trả về: văn bản gỡ băng, 1–3 điểm cần sửa, câu viết lại tự nhiên hơn, các cụm từ hữu ích — định dạng strict JSON, dán nhãn rõ ràng là nhận xét từ AI.
- [ ] Bước luyện nhại (shadowing): TTS đọc câu viết lại tự nhiên; người học đọc lặp lại theo; hiển thị độ khớp văn bản.
- [ ] Tuyệt đối không lưu trữ file âm thanh; chỉ lưu văn bản gỡ băng và các nhận xét đánh giá.
- [ ] Kiểm thử tự động với các adapter STT/LLM/TTS giả lập.

## Kế hoạch
### Nền tảng
- [ ] Đo độ trễ thực tế của một vòng STT → LLM → TTS trên Groq (từ ticket triển khai cloud); đặt mục tiêu < 6 giây mỗi lượt, nếu không đạt thì trả văn bản trước, audio sau
- [ ] Kiểm tra ghi âm `MediaRecorder` trên Safari iOS và Chrome Android (định dạng hỗ trợ, quyền micro trong PWA); chọn định dạng gửi lên `/speech/transcribe`
### Backend
- [ ] Dữ liệu kịch bản `backend/app/data/kich_ban_noi/{standup,interview,code_review,demo}.json`: vai của app, mục tiêu, câu hỏi mở đầu, gợi ý câu hỏi tiếp theo, cụm từ mục tiêu (liên kết `cum_tu_cong_so.json`)
- [ ] Bảng `speaking_sessions` (`id`, `user_id`, `scenario`, `turns` JSON chứa transcript và nhận xét, `created_at`); **không** lưu audio. Migration Alembic
- [ ] Thêm cột `bio` (giới thiệu ngắn, tùy chọn) vào hồ sơ người dùng để cá nhân hóa kịch bản phỏng vấn; hiển thị rõ nội dung này được gửi tới LLM
- [ ] Router `backend/app/routes/speaking.py`: `POST /speaking/sessions` (tạo phiên, trả câu hỏi đầu + URL audio), `POST /speaking/sessions/{id}/turns` (nhận audio → STT → LLM nhận xét JSON `{transcript, corrections[1..3], natural_version, useful_phrases, next_question}` → TTS câu hỏi tiếp), `POST /speaking/sessions/{id}/shadow` (chấm độ khớp lần nói lặp lại), `GET /speaking/sessions` (lịch sử)
- [ ] Phiên kết thúc sau 3–5 lượt; tóm tắt cuối phiên (điểm mạnh, 3 lỗi lặp lại, cụm từ nên học → tùy chọn thêm vào từ vựng)
- [ ] Ghi `attempts` với skill `speaking` + `duration_ms` để dashboard và phiên học hằng ngày tính được
### Frontend
- [ ] Trang "Luyện nói": chọn tình huống, nút giữ để nói / bấm để bắt đầu-dừng, hiển thị transcript, thẻ nhận xét (nhãn "Nhận xét từ AI"), phát câu diễn đạt tự nhiên, bước shadowing
- [ ] Tích hợp vào phiên học "Hôm nay" thay `read_aloud` qua cấu hình `session_speaking_plugin`
### Kiểm chứng
- [ ] Adapter giả lập STT/LLM/TTS; test JSON sai schema, dịch vụ lỗi, phiên đủ lượt, không lưu audio (kiểm tra thư mục tạm trống sau request)
- [ ] Playwright với micro giả lập (`--use-fake-device-for-media-stream`) cho luồng một lượt
- [ ] `[gate]` Push commit migration theo `docs/quy_trinh/tao_migration.md` (`pg_dump` trước)
- [ ] `[user]` Chủ dự án luyện thật mỗi tình huống ít nhất 1 phiên trên điện thoại; ghi phản hồi vào nhật ký thực hiện
### Đồng bộ tài liệu
- [ ] `docs/kien_truc.md` (plugin, bảng, route), README tính năng, lộ trình

## Bán kính ảnh hưởng
- Ticket này thêm migration schema. Sau khi đã deploy, mỗi lần push lên `main` là một lần deploy và migration chạy thẳng trên Neon, nơi giữ bản sao duy nhất của lịch sử học tập. Migration lỗi có thể làm app không khởi động được hoặc làm hỏng dữ liệu.
- Giảm thiểu: làm theo `docs/quy_trinh/tao_migration.md`. Migration chỉ **thêm** cột/bảng (cột mới nullable hoặc có default), không xóa hay đổi tên trong cùng đợt; chạy thử trên SQLite và PostgreSQL trong CI; `pg_dump` Neon ngay trước khi push commit chứa migration.
- Phục hồi: revert commit để app chạy lại; nếu dữ liệu đã hỏng thì khôi phục từ bản dump vừa tạo (thao tác `[gate]`).
- Dữ liệu gửi ra Groq: giọng nói của người học (không lưu lại), transcript, phần giới thiệu ngắn trong hồ sơ; không gửi mã nguồn.

## Nhật ký thực hiện

## Sai lệch
