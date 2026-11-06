---
type: content
owner: claude
stakes: irreversible
priority: P2
skill: reading
opened: 2026-11-05
---

# Học các cụm từ công sở và khai thác lịch sử commit git làm nguồn ngữ cảnh

## Ngữ cảnh
Từ vựng hiện tại được khử trùng lặp theo bộ khóa `(lemma, part_of_speech)`, do đó ứng dụng chỉ đang dạy các từ đơn lẻ. Tiếng Anh công sở trong thực tế lại vận hành chủ yếu dựa trên các cụm từ — ví dụ: "walk me through", "I'm blocked on", "ship it behind a flag", "let's take this offline". Commit message và mô tả Pull Request (PR) là nguồn văn bản xuôi phong phú nhất hàng ngày chứa những cụm từ này, và đã được liệt kê trong phạm vi còn lại của README.

Cập nhật 2026-11-06: nguồn import là repo GitHub công khai và file ZIP. Import GitHub hiện tải archive `codeload` (`backend/app/imports.py`), **không có thư mục `.git`**, nên commit message phải lấy qua GitHub REST API trên runner. Bộ cụm từ soạn sẵn được chia theo các tình huống luyện nói chủ dự án đã chọn (standup, phỏng vấn, code review, demo) để ticket [mô phỏng nói](../cho_xu_ly/20261105_mo_phong_noi_standup.md) dùng lại.

## Tiêu chí chấp nhận
- [ ] Đường ống trích xuất giữ lại các cụm danh từ phổ biến và cụm động từ qua spaCy song song với từ gốc (lemma), được xếp hạng theo cùng cơ chế.
- [ ] Tập dữ liệu mẫu ban đầu khoảng ~150 cụm từ thông dụng trong họp hành/standup/code-review kèm nghĩa tiếng Việt, do dự án tự biên soạn.
- [ ] Import GitHub lấy N commit message gần nhất (N cấu hình được, mặc định 200) qua GitHub REST API khi chạy trên runner, lọc secret như mọi văn bản khác và đóng góp câu ngữ cảnh loại `commit`. Import ZIP không đọc `.git` (ghi rõ lý do an toàn trong tài liệu).
- [ ] Các cụm từ xuất hiện bình thường trong các bài tập ôn tập và đọc hiểu; giữ nguyên cách hoạt động của các từ đơn hiện có.
- [ ] Bổ sung các bài test trích xuất với dữ liệu mẫu cho cụm từ và commit message.

## Kế hoạch
### Mô hình dữ liệu
- [ ] Quyết định cách lưu cụm từ: thêm cột `kind` (`word | phrase`) vào `vocab_items`, khóa duy nhất vẫn là `(user_id, lemma, part_of_speech)` với `lemma` là dạng chuẩn hóa của cụm (chữ thường, lemma từng từ); ghi lý do vào nhật ký thực hiện
- [ ] Migration `kind` (default `word`) + loại ngữ cảnh `commit`
- [ ] `[gate]` Push commit migration theo `docs/quy_trinh/tao_migration.md` (`pg_dump` trước)
### Bộ cụm từ soạn sẵn
- [ ] `backend/app/data/cum_tu_cong_so.json`: khoảng 150 cụm do dự án tự soạn (không chép từ nguồn có bản quyền), mỗi mục có `phrase`, `meaning_vi`, `example`, `scenario` (`standup | interview | code_review | demo | meeting`), `cefr`
- [ ] Nạp bộ cụm từ vào enrichment (nguồn `lexicon`) để có nghĩa tiếng Việt ngay
### Trích xuất
- [ ] `backend/app/extraction.py`: spaCy `Matcher`/`PhraseMatcher` cho bộ cụm soạn sẵn + mẫu phrasal verb (động từ + `prt`) + cụm danh từ phổ biến; chỉ áp dụng trên văn bản xuôi (comment, docstring, Markdown, commit), không áp dụng trên identifier
- [ ] Xếp hạng cụm theo cùng cơ chế log-tần suất; ngưỡng tối thiểu để tránh cụm nhiễu; giới hạn số cụm mỗi repo
- [ ] `scripts/cloud_extract.py`: với import GitHub, gọi API commits (dùng `GITHUB_TOKEN` của workflow để có hạn mức cao hơn; xác minh giới hạn request và ghi ngày), lấy message, bỏ merge commit/bot, cắt độ dài
### Bài tập và giao diện
- [ ] Thẻ ôn tập và bài đọc hiểu hiển thị cụm từ như từ đơn; nhãn "Cụm từ" và bộ lọc trong trang từ vựng
- [ ] Ngữ cảnh `commit` hiển thị dạng câu, không mở Monaco
### Kiểm chứng
- [ ] Fixture: văn bản có cụm soạn sẵn + phrasal verb; danh sách commit message giả lập (có chuỗi giống secret để kiểm tra bộ lọc)
- [ ] Test cụm từ không làm thay đổi kết quả từ đơn hiện có trên `backend/tests/fixtures/sample_repo`
- [ ] Import thật một repo public qua Actions; ghi số cụm và ví dụ (chỉ repo công khai)
### Đồng bộ tài liệu
- [ ] `docs/kien_truc.md` §4 (cụm từ, nguồn commit), README tính năng

## Bán kính ảnh hưởng
- Ticket này thêm migration schema. Sau khi đã deploy, mỗi lần push lên `main` là một lần deploy và migration chạy thẳng trên Neon, nơi giữ bản sao duy nhất của lịch sử học tập. Migration lỗi có thể làm app không khởi động được hoặc làm hỏng dữ liệu.
- Giảm thiểu: làm theo `docs/quy_trinh/tao_migration.md`. Migration chỉ **thêm** cột/bảng (cột mới nullable hoặc có default), không xóa hay đổi tên trong cùng đợt; chạy thử trên SQLite và PostgreSQL trong CI; `pg_dump` Neon ngay trước khi push commit chứa migration.
- Phục hồi: revert commit để app chạy lại; nếu dữ liệu đã hỏng thì khôi phục từ bản dump vừa tạo (thao tác `[gate]`).

## Nhật ký thực hiện

## Sai lệch
