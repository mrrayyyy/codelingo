# Giao thức làm việc (Protocol)

Hợp đồng làm việc dành cho bất kỳ ai — dù là chủ dự án hay AI agent (Claude Code, Gemini/Antigravity) — khi làm việc trong kho lưu trữ này. Mọi quy tắc ràng buộc đều được lưu trữ tại đây thay vì nằm rải rác trong file điểm vào của từng agent, nhằm bảo đảm mọi agent đều tuân thủ cùng một quy tắc và việc sửa đổi quy tắc chỉ diễn ra tại một nơi duy nhất.

**Các file điểm vào của agent (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) không nắm giữ quy tắc riêng ngoài các con trỏ điều hướng.** Một quy tắc chỉ xuất hiện trong file của một agent duy nhất được xem là lỗi: hãy đưa quy tắc đó vào đây.

Được chuyển thể vào ngày 2026-11-05 từ giao thức workspace AIOps của chủ dự án, rút gọn cho phù hợp với dự án ứng dụng do một lập trình viên duy trì (loại bỏ các quy tắc hạ tầng chuyên sâu, Vault hoặc cluster).

| Giao thức | Nội dung bao hàm |
| :--- | :--- |
| [NAVIGATION.md](NAVIGATION.md) | Nơi lưu trữ từng loại thông tin/dữ kiện — đọc trước khi phỏng đoán |
| [EXECUTION.md](EXECUTION.md) | Thao tác tự động vs thao tác cần xác nhận (gated), chính sách commit và push, bán kính ảnh hưởng |
| [KANBAN.md](KANBAN.md) | Cách theo dõi công việc — `docs/backlog/`, trạng thái tính theo thư mục |
| [LEDGER.md](LEDGER.md) | Cách ghi nhận phát hiện/vấn đề — `docs/ledger/`, ghi nhận ngay trong lượt phát hiện |
| [DOC_SYNC.md](DOC_SYNC.md) | Thay đổi hành vi hệ thống phải cập nhật tài liệu tương ứng trong cùng ticket |
| [VERIFICATION.md](VERIFICATION.md) | Không phỏng đoán; dữ kiện phải có ngày tháng; kết quả test xanh chưa hẳn là lỗi đã được sửa triệt để |
| [SECRETS.md](SECRETS.md) | Kho lưu trữ này là công khai — những điều tuyệt đối không bao giờ được đưa vào |

Quy trình rà soát và kiểm tra các mục quá hạn hoặc bị lãng quên được định nghĩa tại [docs/runbooks/housekeeping.md](../runbooks/housekeeping.md), chạy khi có yêu cầu.

## Thứ tự đọc (Reading order)

Phiên làm việc mới: **NAVIGATION** → **EXECUTION** → **SECRETS**, sau đó là **KANBAN** trước khi bắt đầu công việc quan trọng.

## Ngôn ngữ & Quy tắc đặt tên (Language & Naming Rules)

- **Nội dung tài liệu**: Toàn bộ tài liệu (`docs/`, `README.md`, ticket, ledger, ADRs, runbooks) **bắt buộc viết bằng tiếng Việt**.
- **Tên file & Thư mục**: **Bắt buộc luôn giữ 100% bằng tiếng Anh** (`docs/protocol/README.md`, `docs/backlog/ready/`, `tools/`, v.v.), tuyệt đối không đổi tên file/thư mục sang tiếng Việt để bảo đảm tính tương thích với tooling, scripts và CI/CD.
- **Giao tiếp**: Trao đổi với chủ dự án bằng **tiếng Việt**.
- **Mã nguồn, Lệnh & Thuật ngữ kỹ thuật**: Code, comment trong code, commit message, shell command, API endpoint và các thuật ngữ kỹ thuật tiêu chuẩn giữ nguyên dạng tiếng Anh kỹ thuật khi cần.

## Thay đổi một quy tắc giao thức (Changing a protocol)

Không tự ý đơn phương viết lại quy tắc. Hãy tạo một mục `type: protocol-friction` trong `docs/ledger/open/`, trích dẫn nhiệm vụ thực tế mà quy tắc đó gây tốn thời gian hoặc cản trở công việc chính đáng, để chủ dự án xem xét và đưa ra quyết định. Mỗi quy tắc đều chỉ rõ lỗi sai mà nó được tạo ra để ngăn chặn, do đó có thể thảo luận và đối chiếu dựa trên bằng chứng thực tế.
