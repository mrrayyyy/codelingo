# Đánh giá sản phẩm và lộ trình phát triển

Mục tiêu của chủ dự án (xác nhận ngày 2026-11-05, bổ sung 2026-11-06): dự án **cá nhân**, trước hết là công cụ để chủ dự án tự học tiếng Anh công sở, dùng hằng ngày mà không cần chạy gì trên máy tính cá nhân. Nếu làm tốt, CodeLingo sẽ thành **portfolio** khi ứng tuyển hoặc được mở cho người dùng khác. Kỹ năng trọng tâm: **nói** (họp hành, standup meeting), **nghe**, **đọc/từ vựng**. Mức độ ưu tiên trong 1–2 tháng tới: sử dụng cloud hàng ngày, luyện tập tiếng Anh thực chiến công sở, nâng cao chất lượng nội dung.

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
| 7 | **Tồn tại 3 chế độ job, 2 cấu hình triển khai** — đã chốt bỏ ARQ/Redis ([ADR 0004](../quyet_dinh/0004_bo_che_do_arq_redis.md)) | `config.py` có `job_mode`; tồn tại cả Compose lẫn Render | Tăng chi phí bảo trì không cần thiết cho một ứng dụng người dùng đơn ([nhật ký](../nhat_ky/da_giai_quyet/y_tuong_20261105_don_gian_hoa_che_do_job.md)). |
| 8 | ~~Nguy cơ bảo mật mã nguồn công ty~~ — **đã hủy 2026-11-06**: tiền đề sai, dự án không dùng mã nguồn công ty | — | Nguồn import là repo GitHub công khai và file ZIP ([nhật ký](../nhat_ky/da_huy/lo_hong_quy_trinh_20261105_bao_mat_ma_nguon_cong_ty.md)). |
| 9 | **Dịch vụ gói miễn phí tự ngủ khi nhàn rỗi** | Dịch vụ web miễn phí của Render sẽ tạm dừng khi không có request | Khởi động nguội (cold start) trước phiên ôn tập 3 phút sẽ phá vỡ thói quen học hàng ngày; cần có vỏ ứng dụng PWA và trạng thái loading mượt mà. |
| 10 | **Không import được repo public lớn** (bổ sung 2026-11-06) | `backend/app/imports.py`: archive GitHub tối đa 20 MiB; 5.000 file; callback tối đa 500 mục | Nguồn học chính chủ dự án chọn (repo nổi tiếng) hầu như vượt các giới hạn này. |
| 11 | **Chưa có file LICENSE** (bổ sung 2026-11-06) | `ls LICENSE*` → không có | Cần cho portfolio và để biết dữ liệu từ điển mở nào được phép đóng gói. |

### Nhận định định hướng
Mã nguồn hiện tại đang đi trước sản phẩm. Bước đi có đòn bẩy cao nhất lúc này không phải là làm thêm tính năng mới mà là **đưa ứng dụng lên hoạt động thực tế trên cloud và sử dụng mỗi ngày**, sau đó giải quyết ngay những vấn đề mà việc sử dụng hàng ngày bộc lộ: trước hết là nghĩa tiếng Việt, sau đó đến nội dung theo cụm từ, và bài tập luyện nghe nói tương tác dựa trên hợp đồng plugin hiện có. Phạm vi trong 1–2 tháng tới vẫn là ứng dụng một người dùng; riêng phần dữ liệu được chuẩn bị sẵn cho đa người dùng (mọi truy vấn qua `get_current_user`), còn đăng nhập/OAuth và cách ly plugin phức tạp để lại sau.

## Định hướng đã chốt (2026-11-06)

Chủ dự án trả lời qua các hộp thoại câu hỏi ngày 2026-11-06. Các quyết định này là đầu vào cố định cho mọi ticket; muốn đổi phải hỏi lại chủ dự án ([thuc_thi.md](../quy_tac/thuc_thi.md), mục "Không tự ý thay đổi quyết định đã chốt").

| Chủ đề | Quyết định |
| :--- | :--- |
| Thứ tự ưu tiên | Giữ lộ trình: dùng cloud hằng ngày → chất lượng nội dung → luyện nói/nghe tương tác |
| Hạ tầng | Render + Neon + GitHub Actions + Groq, gói miễn phí ([ADR 0001](../quyet_dinh/0001_uu_tien_cloud_mien_phi.md)) |
| Chế độ job | Bỏ ARQ/Redis; giữ `inline` + `github_actions`; Compose rút gọn ([ADR 0004](../quyet_dinh/0004_bo_che_do_arq_redis.md)) |
| Nguồn học | Repo GitHub công khai: repo nổi tiếng và repo của chính chủ dự án; file ZIP. Không hỗ trợ repo private qua token |
| Đa người dùng | Chuẩn bị schema và truy vấn theo user; chưa làm đăng nhập |
| Nghĩa từ, ví dụ | Từ điển mở trước (kiểm tra license), LLM Groq bù phần thiếu, gắn nhãn nguồn, cho phép sửa |
| Luyện nói | Cả 4 tình huống, theo thứ tự: daily standup → phỏng vấn xin việc → code review → demo/thuyết trình |
| Phiên học | Khoảng 10 phút mỗi ngày, trên điện thoại và Mac (PWA, mobile-first) |
| Ngôn ngữ | Giao diện mặc định tiếng Việt (giữ nút chuyển); toàn bộ tài liệu kể cả README giữ tiếng Việt |
| Portfolio | Thiết kế UI chỉn chu; README có ảnh/GIF demo và sơ đồ kiến trúc; trang demo công khai với dữ liệu mẫu |
| Nhịp làm việc | Chủ dự án gần như toàn thời gian; agent làm liên tục từ ticket này sang ticket kế, chỉ dừng ở mục `[gate]` và `[user]` |

## Lộ trình phát triển

Trạng thái của từng ticket chính là thư mục chứa nó trong `docs/cong_viec/`. Thứ tự dưới đây là thứ tự thực hiện; agent lấy ticket kế tiếp chưa xong theo thứ tự này. Thời lượng là **ước lượng** với nhịp gần toàn thời gian, không phải cam kết.

### Giai đoạn 0 — Nền móng (ước lượng 2–3 ngày) · P1
| # | Ticket | Lý do |
| :--- | :--- | :--- |
| 1 | [Bỏ ARQ/Redis, xử lý cảnh báo Starlette](../cong_viec/san_sang/20261106_bo_che_do_arq_redis.md) | Gọn code và tài liệu trước khi khóa schema bằng migration |
| 2 | [Alembic migrations](../cong_viec/san_sang/20261105_migration_alembic.md) | Bắt buộc có trước khi dữ liệu thật được ghi vào Neon; tạo quy trình `tao_migration.md` cho mọi migration sau |

### Giai đoạn 1 — Chạy thật và dùng hằng ngày (ước lượng 1–1,5 tuần) · P1
| # | Ticket | Lý do |
| :--- | :--- | :--- |
| 3 | [Triển khai Render + Neon + Groq](../cong_viec/san_sang/20261105_trien_khai_cloud_render_neon_groq.md) | Khắc phục thiếu sót 1; cần chủ dự án tạo tài khoản và secret (`[user]`) |
| 4 | [Tách router API, `get_current_user`](../cong_viec/san_sang/20261106_tach_router_api.md) | Nền cho mọi route mới và cho đa người dùng/demo |
| 5 | [Tách nhỏ giao diện workspace](../cong_viec/san_sang/20261105_tach_giao_dien_workspace.md) | Nền cho mọi màn hình mới |
| 6 | [Hệ thống thiết kế giao diện](../cong_viec/cho_xu_ly/20261106_he_thong_thiet_ke_giao_dien.md) | Mobile-first, dark mode, mặc định tiếng Việt; mục tiêu portfolio |
| 7 | [PWA và phiên học 10 phút](../cong_viec/cho_xu_ly/20261105_phien_hoc_pwa_hang_ngay.md) | Khắc phục thiếu sót 9; biến tính năng thành thói quen (dùng tạm bài nghe/nói hiện có) |

### Giai đoạn 2 — Chất lượng nội dung (ước lượng 1,5 tuần) · P1
| # | Ticket | Lý do |
| :--- | :--- | :--- |
| 8 | [Import repo public lớn, thư mục con](../cong_viec/cho_xu_ly/20261106_import_repo_public_lon.md) | Khắc phục thiếu sót 10; mở khóa nguồn học chính |
| 9 | [Nghĩa tiếng Việt, ví dụ, CEFR](../cong_viec/san_sang/20261105_nghia_tieng_viet_va_cefr.md) | Khắc phục thiếu sót 2 và 11 (chọn license, nguồn từ điển) |
| 10 | [Cụm từ công sở và commit message](../cong_viec/san_sang/20261105_cum_tu_va_lich_su_git.md) | Khắc phục thiếu sót 3; bộ cụm từ chia theo tình huống nói |

### Giai đoạn 3 — Luyện nói và nghe thực chiến (ước lượng 2 tuần) · P1–P2
| # | Ticket | Lý do |
| :--- | :--- | :--- |
| 11 | [Mô phỏng nói: standup → phỏng vấn → code review → demo](../cong_viec/cho_xu_ly/20261105_mo_phong_noi_standup.md) | Khắc phục thiếu sót 4, kỹ năng quan trọng nhất |
| 12 | [Luyện nghe hội thoại công sở](../cong_viec/cho_xu_ly/20261105_luyen_nghe_hop.md) | Khắc phục thiếu sót 4; dùng chung tình huống với luyện nói |

### Giai đoạn 4 — Portfolio (ước lượng 1 tuần) · P2
| # | Ticket | Lý do |
| :--- | :--- | :--- |
| 13 | [Trang demo công khai](../cong_viec/cho_xu_ly/20261106_trang_demo_cong_khai.md) | Nhà tuyển dụng bấm thử không cần mật khẩu, không chạm dữ liệu thật |
| 14 | [README portfolio](../cong_viec/cho_xu_ly/20261106_readme_portfolio.md) | Ảnh/GIF demo, sơ đồ kiến trúc, link demo |

### Các điểm dừng cần chủ dự án
- `[user]`: tạo tài khoản Neon/Render/Groq và nhập secret (#3); duyệt giao diện trên điện thoại (#6); cài PWA và học thử (#7); chọn license repo (#9); luyện thử nói/nghe (#11, #12); chọn phương án demo (#13); duyệt README (#14).
- `[gate]`: lần deploy đầu (#3); mỗi lần push migration sau khi đã deploy (#7, #8 nếu thêm cột, #9, #10, #11) — luôn `pg_dump` trước; tạo dịch vụ demo (#13).

### Các tính năng sau này (chưa xếp lịch)
Đăng nhập đa người dùng/OAuth, biến thể bài tập viết (Slack/email), chấm phát âm cấp âm vị, biểu đồ tiến độ chi tiết theo kỹ năng. Khi nảy ra ý tưởng mới, ghi vào sổ nhật ký dạng `type: idea` và nâng thành ticket khi xong một giai đoạn.

## Phương pháp đo lường tiến độ
Đo lường hàng tuần theo từng kỹ năng: số phút luyện tập, số lượt làm bài, điểm trung bình, và tỷ lệ ghi nhớ FSRS (tỷ lệ thẻ được đánh giá ở mức Good/Easy). Bổ sung các chỉ số này vào dashboard trong ticket phiên học hàng ngày; trước thời điểm đó, tiêu chí chấp nhận của từng ticket là thước đo chính.
