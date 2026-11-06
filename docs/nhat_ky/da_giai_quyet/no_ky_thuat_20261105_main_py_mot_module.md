---
type: tech-debt
status: resolved
discovered: 2026-11-05
source: product review in 20261105_khoi_tao_quy_trinh_tai_lieu_agent
severity: low
owner: claude
---

# Toàn bộ 26 route API nằm dồn trong một module 549 dòng

## Ngữ cảnh và bằng chứng
Lệnh `grep -c '^@app\.' backend/app/main.py` → 26 routes; `wc -l` → 549 dòng (ngày 2026-11-05). Các route cho hồ sơ người dùng (profile), dashboard, import, từ vựng, ôn tập, xuất dữ liệu, bài tập, giọng nói, tra từ điển và callback từ cloud đều nằm chung trong một file duy nhất. Hiện tại vẫn tạm ổn; nhưng các plugin luyện nói và nghe sắp tới sẽ bổ sung thêm nhiều route quản lý phiên học.

## Hành động khuyến nghị
Khi bắt đầu ticket đầu tiên của Giai đoạn 3 (Phase 3), hãy tách file này thành các module sử dụng `APIRouter` (`routes/imports.py`, `routes/review.py`, `routes/practice.py`, `routes/cloud.py`, v.v.) như một mục đầu tiên trong kế hoạch thực hiện, không thay đổi hành vi và sử dụng bộ test hiện có làm lưới bảo vệ an toàn.

## Giải quyết
2026-11-06: chuyển thành ticket [20261106_tach_router_api](../../cong_viec/san_sang/20261106_tach_router_api.md), làm ngay sau lần deploy đầu tiên, trước các tính năng Giai đoạn 1–3. Ticket này cũng chuẩn hóa dependency `get_current_user` để chuẩn bị cho đa người dùng.
