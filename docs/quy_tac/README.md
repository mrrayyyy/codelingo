# Quy tắc làm việc

Hợp đồng làm việc dành cho bất kỳ ai — dù là chủ dự án hay AI agent (Claude Code, Gemini/Antigravity) — khi làm việc trong kho lưu trữ này. Mọi quy tắc ràng buộc đều được lưu trữ tại đây thay vì nằm rải rác trong file điểm vào của từng agent, nhằm bảo đảm mọi agent đều tuân thủ cùng một quy tắc và việc sửa đổi quy tắc chỉ diễn ra tại một nơi duy nhất.

Các file điểm vào của agent (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) không nắm giữ quy tắc riêng ngoài các con trỏ điều hướng. Một quy tắc chỉ xuất hiện trong file của một agent duy nhất được xem là lỗi: hãy đưa quy tắc đó vào đây.

Được chuyển thể vào ngày 2026-11-05 từ giao thức workspace AIOps của chủ dự án, rút gọn cho phù hợp với dự án ứng dụng do một lập trình viên duy trì (loại bỏ các quy tắc hạ tầng chuyên sâu, Vault hoặc cluster).

| Quy tắc | Nội dung bao hàm |
| :--- | :--- |
| [dieu_huong.md](dieu_huong.md) | Nơi lưu trữ từng loại thông tin và dữ kiện — đọc trước khi phỏng đoán |
| [thuc_thi.md](thuc_thi.md) | Thao tác tự động hóa so với thao tác cần xác nhận trước, chính sách commit và push, bán kính ảnh hưởng |
| [bang_cong_viec.md](bang_cong_viec.md) | Cách theo dõi công việc — `docs/cong_viec/`, trạng thái tính theo thư mục |
| [so_nhat_ky.md](so_nhat_ky.md) | Cách ghi nhận phát hiện và vấn đề — `docs/nhat_ky/`, ghi nhận ngay trong lượt phát hiện |
| [dong_bo_tai_lieu.md](dong_bo_tai_lieu.md) | Thay đổi hành vi hệ thống bắt buộc phải cập nhật tài liệu tương ứng trong cùng ticket |
| [xac_minh.md](xac_minh.md) | Không phỏng đoán; dữ kiện phải có ngày tháng; kết quả test xanh chưa hẳn là lỗi đã được sửa triệt để |
| [bao_mat.md](bao_mat.md) | Kho lưu trữ này là công khai — những điều tuyệt đối không bao giờ được đưa vào |

Quy trình rà soát và kiểm tra các mục quá hạn hoặc bị lãng quên được định nghĩa tại [docs/quy_trinh/don_dep_dinh_ky.md](../quy_trinh/don_dep_dinh_ky.md), chạy khi có yêu cầu.

## Thứ tự đọc

Phiên làm việc mới: **dieu_huong.md** → **thuc_thi.md** → **bao_mat.md**, sau đó là **bang_cong_viec.md** trước khi bắt đầu công việc quan trọng.

## Quy tắc ngôn ngữ và đặt tên

- **Nội dung tài liệu**: Toàn bộ tài liệu (`docs/`, `README.md`, ticket, nhật ký, ADRs, quy trình) **bắt buộc viết bằng tiếng Việt**.
- **Tên thư mục**: **Bắt buộc dùng tiếng Việt không dấu snake_case** (`docs/quy_tac/`, `docs/cong_viec/`, `docs/quyet_dinh/`, `docs/nhat_ky/`, `docs/san_pham/`, `docs/quy_trinh/`, `docs/tam/`).
- **Tên file tài liệu**: Bắt buộc đặt bằng **tiếng Việt không dấu snake_case** (`docs/kien_truc.md`, `docs/xac_minh.md`, `docs/trien_khai_cloud.md`, `YYYYMMDD_<slug>.md`, v.v.). Các file entrypoint chuẩn hệ thống (`README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) giữ nguyên để tương thích với tooling và harness của IDE/agent.
- **Giao tiếp**: Trao đổi với chủ dự án bằng **tiếng Việt**.
- **Mã nguồn, lệnh và từ khóa học thuật/kỹ thuật**: Code, comment trong code, commit message, shell command, API endpoint và các thuật ngữ chuyên ngành (Docker, Next.js, FastAPI, Redis, FSRS, Git, token, OAuth, PR, CI/CD...) giữ nguyên dạng tiếng Anh kỹ thuật chuẩn.

## Thay đổi một quy tắc

Không tự ý đơn phương viết lại quy tắc. Hãy tạo một mục `type: protocol-friction` trong `docs/nhat_ky/dang_mo/`, trích dẫn nhiệm vụ thực tế mà quy tắc đó gây tốn thời gian hoặc cản trở công việc chính đáng, để chủ dự án xem xét và đưa ra quyết định. Mỗi quy tắc đều chỉ rõ lỗi sai mà nó được tạo ra để ngăn chặn, do đó có thể thảo luận và đối chiếu dựa trên bằng chứng thực tế.
