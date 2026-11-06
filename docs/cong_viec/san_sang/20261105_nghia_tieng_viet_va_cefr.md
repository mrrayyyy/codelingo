---
type: content
owner: claude
stakes: irreversible
priority: P1
skill: vocabulary
opened: 2026-11-05
---

# Bổ sung nghĩa tiếng Việt, câu ví dụ và cải thiện ước lượng cấp độ CEFR

## Ngữ cảnh
Từ điển tích hợp sẵn hiện chỉ có 33 định nghĩa (`backend/app/lexicon.py`, đếm ngày 2026-11-05) và bảng `vocab_items` chưa có trường tiếng Việt nào, dẫn đến hầu hết flashcard đều hiển thị "chưa có định nghĩa" (definition unavailable). Đối với người học Việt Nam, vòng lặp ôn tập rất cần một giải nghĩa tiếng Việt ngắn gọn, một định nghĩa tiếng Anh dễ hiểu và một câu ví dụ mộc mạc. Các từ chưa rõ cấp độ CEFR hiện mặc định gán mức B2.

Ràng buộc từ [xac_minh.md](../../quy_tac/xac_minh.md): nội dung do AI sinh ra phải được dán nhãn rõ ràng là do AI sinh, tuyệt đối không bao giờ được trình bày như dữ kiện từ điển chính thống.

Cập nhật 2026-11-06: chủ dự án chốt nguồn nội dung là **từ điển mở trước, LLM (Groq) bù phần thiếu**. Repo công khai và hiện **chưa có file LICENSE**, nên phải xác định license của dữ liệu từ điển và cách đóng gói (commit vào repo, tải lúc build, hay nạp vào DB bằng script) trước khi viết code. Ticket này chạy sau khi đã deploy nên migration là `irreversible`.

## Tiêu chí chấp nhận
- [ ] Có ADR ghi lại nguồn từ điển được chọn, license, cách đóng gói và ghi công (attribution); thông tin ghi công hiển thị trong app.
- [ ] Đo độ phủ: tỷ lệ từ của repo mẫu Atlas và một repo public nổi tiếng có nghĩa tiếng Việt từ từ điển (không tính LLM), ghi số liệu có ngày.
- [ ] Schema database (thực hiện qua Alembic): bổ sung các cột `meaning_vi`, `definition_en`, `example`, `content_source` (`lexicon | dictionary | ai | user`), `content_checked` cho từng mục từ vựng.
- [ ] Làm giàu dữ liệu theo yêu cầu đơn lẻ và theo lô thông qua adapter LLM được cấu hình, kèm JSON schema nghiêm ngặt; chỉ gửi từ vựng và câu ngữ cảnh ngắn đã lưu — tuyệt đối không gửi cả file mã nguồn.
- [ ] Giao diện dán nhãn rõ ràng cho nội dung do AI sinh và cho phép chủ dự án chỉnh sửa / duyệt nội dung (`content_checked`).
- [ ] Ước lượng CEFR sử dụng phân dải tần suất Zipf của thư viện `wordfreq` cho các từ nằm ngoài từ điển biên soạn sẵn; đánh dấu rõ là giá trị ước lượng.
- [ ] Chế độ offline/không có LLM giữ nguyên cách hoạt động: hiển thị "chưa có thông tin", không tự bịa đặt câu chữ.
- [ ] Kiểm thử tự động với adapter LLM giả lập bao gồm các trường hợp phản hồi hợp lệ, không hợp lệ và dịch vụ ngoại tuyến.

## Kế hoạch
### Khảo sát nguồn từ điển (investigation, làm trước tiên)
- [ ] Đánh giá các ứng viên dữ liệu Anh–Việt mở (ví dụ dữ liệu trích từ Wiktionary, FreeDict, các dự án từ điển Anh–Việt mã nguồn mở khác): license chính xác, điều kiện ghi công/chia sẻ lại, định dạng, kích thước, độ phủ trên tập từ mẫu. Ghi nguồn và ngày tra cứu; không suy đoán license
- [ ] `[user]` Chủ dự án chọn license cho repo CodeLingo (cần cho portfolio và để biết dữ liệu nào tương thích); agent trình bày 2–3 lựa chọn kèm hệ quả
- [ ] Viết ADR (số kế tiếp) `docs/quyet_dinh/NNNN_nguon_tu_dien_mo.md`: nguồn, license, cách đóng gói, cách cập nhật
### Schema
- [ ] Migration thêm cột vào `vocab_items`: `meaning_vi`, `definition_en`, `example`, `content_source`, `content_checked` (default `false`), `cefr_estimated` (default `true`)
- [ ] `[gate]` Push commit migration theo `docs/quy_trinh/tao_migration.md` (`pg_dump` trước)
### Đường ống làm giàu nội dung
- [ ] Script nạp từ điển `scripts/build_dictionary.py` → bảng/file tra cứu theo `(lemma, pos)`; test với dữ liệu nhỏ trong `backend/tests/fixtures/`
- [ ] Module `backend/app/enrichment.py`: thứ tự nguồn `lexicon` (biên soạn sẵn) → từ điển mở → LLM; không ghi đè nội dung `user` hoặc đã `content_checked`
- [ ] Adapter LLM: JSON schema chặt `{meaning_vi, definition_en, example}`; chỉ gửi lemma, từ loại và tối đa 1 câu ngữ cảnh ngắn đã lưu; phản hồi sai schema → bỏ qua và ghi log số lượng, không lưu dữ liệu rác
- [ ] Chạy làm giàu theo lô ngay sau khi import xong (background, tôn trọng giới hạn request của Groq, có retry/backoff); endpoint `POST /vocab/{id}/enrich` (đơn lẻ) và `POST /vocab/enrich` (lô)
- [ ] CEFR: với từ ngoài `lexicon.py`, phân dải theo tần suất Zipf của `wordfreq` (ngưỡng ghi rõ trong code); hiển thị "ước lượng"
### Giao diện
- [ ] Flashcard: nghĩa tiếng Việt nổi bật, định nghĩa tiếng Anh, câu ví dụ, nhãn nguồn (Từ điển / AI sinh / Bạn đã sửa); trang ghi công nguồn từ điển
- [ ] Hộp thoại sửa nội dung; nút "Đã kiểm tra"; bộ lọc "chưa kiểm tra" trong trang từ vựng
- [ ] Xuất CSV/Anki kèm các trường mới
### Kiểm chứng
- [ ] Test: thứ tự ưu tiên nguồn; LLM giả lập trả về hợp lệ / sai schema / lỗi mạng; chế độ không có LLM hiển thị "chưa có thông tin"; phân dải CEFR
- [ ] Đo độ phủ trước/sau trên Atlas + repo public; ghi vào nhật ký thực hiện
### Đồng bộ tài liệu
- [ ] `docs/kien_truc.md` (cột mới, luồng làm giàu), README tính năng, `.env.cloud.example` nếu có biến mới

## Bán kính ảnh hưởng
- Ticket này thêm migration schema. Sau khi đã deploy, mỗi lần push lên `main` là một lần deploy và migration chạy thẳng trên Neon, nơi giữ bản sao duy nhất của lịch sử học tập. Migration lỗi có thể làm app không khởi động được hoặc làm hỏng dữ liệu.
- Giảm thiểu: làm theo `docs/quy_trinh/tao_migration.md`. Migration chỉ **thêm** cột/bảng (cột mới nullable hoặc có default), không xóa hay đổi tên trong cùng đợt; chạy thử trên SQLite và PostgreSQL trong CI; `pg_dump` Neon ngay trước khi push commit chứa migration.
- Phục hồi: revert commit để app chạy lại; nếu dữ liệu đã hỏng thì khôi phục từ bản dump vừa tạo (thao tác `[gate]`).
- Gửi dữ liệu ra Groq: chỉ lemma và câu ngữ cảnh ngắn lấy từ repo công khai; không gửi cả file.

## Nhật ký thực hiện

## Sai lệch
