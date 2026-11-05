# Đánh giá sản phẩm và lộ trình phát triển

Mục tiêu của chủ dự án (xác nhận ngày 2026-11-05): công cụ học tập **cá nhân** phục vụ giao tiếp tiếng Anh công sở, sử dụng hàng ngày mà không cần chạy bất cứ thứ gì trên máy tính cá nhân. Kỹ năng trọng tâm: **nói** (họp hành, standup meeting), **nghe**, **đọc/từ vựng**. Mức độ ưu tiên trong 1–2 tháng tới: sử dụng cloud hàng ngày, luyện tập tiếng Anh thực chiến công sở, nâng cao chất lượng nội dung.

## Đánh giá hiện trạng (2026-11-05)

Bằng chứng: `pytest backend/tests` → 53 bài test vượt qua; `npm run typecheck` → sạch lỗi; mã nguồn tại mốc `codelingo e5d8c8e`.

### Điểm mạnh
- **Nền tảng kỹ thuật vững chắc.** Xử lý file nén có giới hạn an toàn, bộ lọc ngăn lộ secret, tuyệt đối không thực thi code nguồn người dùng, đáp án bài tập lưu giữ phía máy chủ, quy trình ôn tập FSRS idempotent và có cơ chế bảo vệ thẻ cũ, hiển thị rõ ràng "chưa có thông tin" thay vì bịa đặt dữ liệu.
- **Hợp đồng plugin bài bản** (TypeScript và Python) với 5 plugin luyện tập đang hoạt động trơn tru — cho phép gắn thêm các dạng bài tập mới mà không cần chỉnh sửa mã nguồn lõi.
- **Thiết kế kiến trúc Cloud miễn phí thông minh**: Sử dụng GitHub Actions làm worker xử lý NLP khi có yêu cầu (on-demand), giúp máy tính cá nhân và ứng dụng web đều gọn nhẹ.
- **Hệ thống Test và CI đầy đủ** bao gồm kiểm thử luồng người dùng trên trình duyệt chạy qua runner đám mây.

### Những thiếu sót cần khắc phục cho mục tiêu của chủ dự án

| # | Thiếu sót | Bằng chứng | Tác động tới việc học hàng ngày |
| :--- | :--- | :--- | :--- |
| 1 | **Chưa từng được triển khai thực tế** | [xac_minh.md](../xac_minh.md): "Managed cloud deployment has not been executed" | Ứng dụng chưa từng đến tay người dùng duy nhất của nó. Mọi thứ chỉ là giả thuyết cho đến khi nó được sử dụng hàng ngày. |
| 2 | **Hầu như không có định nghĩa từ vựng, không có nghĩa tiếng Việt** | `lexicon.py`: chỉ có 33 định nghĩa; bảng `vocab_items` chưa có cột tiếng Việt | Hầu hết flashcard hiển thị "definition unavailable" — vòng lặp ôn tập cốt lõi còn rất yếu đối với người học Việt Nam. |
| 3 | **Chỉ học từ đơn lẻ, chưa học cụm từ công sở** | Khóa khử trùng lặp là `(lemma, POS)`; trích xuất chỉ xếp hạng từ đơn | Trong các cuộc họp, mọi người giao tiếp bằng các cụm từ ngữ cảnh ("walk me through", "I'm blocked on", "let's take this offline"), chứ không phải các từ đơn lẻ từ tên biến. |
| 4 | **Kỹ năng nói và nghe còn rất sơ sài** | Chỉ có chép chính tả và đọc to; bài đọc to chỉ so khớp văn bản bóc tách | Hai kỹ năng ưu tiên hàng đầu lại chưa có tính năng luyện tập hội thoại thực tế. |
| 5 | **Giao diện UI bị dồn vào một component quá lớn** | `workspace.tsx`: 33 hooks `useState`, dòng code dài tới 2.332 ký tự | Mỗi màn hình luyện tập mới đều phải sửa chung một file; làm chậm tốc độ phát triển và dễ phát sinh lỗi hồi quy (regression). |
| 6 | **Chưa có công cụ migration schema database** | README: "uses SQLAlchemy `create_all`" | Thay đổi schema đầu tiên sau khi có dữ liệu thật trên Neon sẽ đối mặt với nguy cơ mất toàn bộ lịch sử ôn tập. |
| 7 | **Tồn tại 3 chế độ job, 2 cấu hình triển khai** | `config.py` có `job_mode`; tồn tại cả Compose lẫn Render | Tăng chi phí bảo trì không cần thiết cho một ứng dụng người dùng đơn ([nhật ký](../nhat_ky/dang_mo/y_tuong_20261105_don_gian_hoa_che_do_job.md)). |
| 8 | **Nguy cơ bảo mật mã nguồn công ty trên pipeline cloud** | Cấu hình cloud gửi repo import tới Actions/Neon/Groq | Rủi ro chính sách bảo mật nếu import repository công ty nơi làm việc ([nhật ký](../nhat_ky/dang_mo/lo_hong_quy_trinh_20261105_bao_mat_ma_nguon_cong_ty.md)). |
| 9 | **Dịch vụ gói miễn phí tự ngủ khi nhàn rỗi** | Dịch vụ web miễn phí của Render sẽ tạm dừng khi không có request | Khởi động nguội (cold start) trước phiên ôn tập 3 phút sẽ phá vỡ thói quen học hàng ngày; cần có vỏ ứng dụng PWA và trạng thái loading mượt mà. |

### Nhận định định hướng
Mã nguồn hiện tại đang đi trước sản phẩm. Bước đi có đòn bẩy cao nhất lúc này không phải là làm thêm tính năng mới mà là **đưa ứng dụng lên hoạt động thực tế trên cloud và sử dụng mỗi ngày**, sau đó giải quyết ngay những vấn đề mà việc sử dụng hàng ngày bộc lộ: trước hết là nghĩa tiếng Việt, sau đó đến nội dung theo cụm từ, và bài tập luyện nghe nói tương tác dựa trên hợp đồng plugin hiện có. Giữ phạm vi ở mức ứng dụng cá nhân — các tính năng đa người dùng, OAuth và cách ly plugin phức tạp hãy để lại sau.

## Lộ trình phát triển

Trạng thái của từng ticket chính là thư mục chứa nó trong `docs/cong_viec/`.

### Giai đoạn 0 — Xây dựng nền móng (Tuần 1) · Mức P1
| Ticket | Lý do cần làm ngay |
| :--- | :--- |
| [Alembic migrations](../cong_viec/san_sang/20261105_migration_alembic.md) | Bắt buộc phải có trước khi dữ liệu thật được ghi vào database Neon |
| [Tách nhỏ giao diện workspace UI](../cong_viec/san_sang/20261105_tach_giao_dien_workspace.md) | Mọi tính năng giao diện sau này đều phải can thiệp vào UI |

### Giai đoạn 1 — Chạy thực tế và dùng hàng ngày (Tuần 1–2) · Mức P1
| Ticket | Lý do cần làm ngay |
| :--- | :--- |
| [Triển khai lên Render + Neon + Groq](../cong_viec/san_sang/20261105_trien_khai_cloud_render_neon_groq.md) | Khắc phục thiếu sót 1 |
| [PWA có thể cài đặt và phiên học 10 phút mỗi ngày](../cong_viec/cho_xu_ly/20261105_phien_hoc_pwa_hang_ngay.md) | Khắc phục thiếu sót 9; biến tính năng thành thói quen học tập |

### Giai đoạn 2 — Nâng cao chất lượng nội dung (Tuần 2–4) · Mức P1–P2
| Ticket | Lý do cần làm ngay |
| :--- | :--- |
| [Bổ sung nghĩa tiếng Việt và cải thiện ước lượng CEFR](../cong_viec/san_sang/20261105_nghia_tieng_viet_va_cefr.md) | Khắc phục thiếu sót 2 |
| [Trích xuất cụm từ công sở và lịch sử commit git](../cong_viec/san_sang/20261105_cum_tu_va_lich_su_git.md) | Khắc phục thiếu sót 3 |

### Giai đoạn 3 — Luyện Nghe và Nói thực chiến (Tuần 4–8) · Mức P2
| Ticket | Lý do cần làm ngay |
| :--- | :--- |
| [Mô phỏng buổi họp Standup meeting](../cong_viec/cho_xu_ly/20261105_mo_phong_noi_standup.md) | Khắc phục thiếu sót 4, kỹ năng quan trọng hàng đầu |
| [Luyện nghe trong các cuộc họp kỹ thuật](../cong_viec/cho_xu_ly/20261105_luyen_nghe_hop.md) | Khắc phục thiếu sót 4 |

### Các tính năng sau này (Chưa xếp lịch)
Luyện phỏng vấn xin việc, các biến thể bài tập viết (văn phong Slack / Email), biểu đồ phân tích tiến độ theo từng kỹ năng, chấm phát âm chi tiết ở cấp độ âm vị (phoneme), chế độ đa người dùng / đăng nhập OAuth. Khi nảy sinh ý tưởng mới, hãy ghi nhận vào sổ nhật ký dạng `type: idea` và nâng cấp thành ticket khi hoàn thành một giai đoạn.

## Phương pháp đo lường tiến độ
Đo lường hàng tuần theo từng kỹ năng: số phút luyện tập, số lượt làm bài, điểm trung bình, và tỷ lệ ghi nhớ FSRS (tỷ lệ thẻ được đánh giá ở mức Good/Easy). Bổ sung các chỉ số này vào dashboard trong ticket phiên học hàng ngày; trước thời điểm đó, tiêu chí chấp nhận của từng ticket là thước đo chính.
