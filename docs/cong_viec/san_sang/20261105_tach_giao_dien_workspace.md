---
type: refactor
owner: claude
stakes: routine
priority: P1
opened: 2026-11-05
---

# Tách nhỏ giao diện workspace UI thành các component theo từng trang

## Ngữ cảnh
File `frontend/components/workspace.tsx` hiện đang gộp cả 6 trang (dashboard, từ vựng, repositories, ôn tập, bài tập, cài đặt) vào chung một client component duy nhất với 33 hooks `useState`; một số dòng dài vượt quá 2.000 ký tự (đo ngày 2026-11-05 bằng lệnh `awk 'length > 400'`). Mọi tính năng trong Giai đoạn 1–3 (phiên học hàng ngày, PWA, mô phỏng nói, luyện nghe) đều sẽ phải thêm màn hình tại đây. Tách nhỏ file này trước tiên sẽ giúp các thay đổi sau này dễ review hơn và cô lập phạm vi lỗi hồi quy (regression).

Không có thay đổi nào về hành vi người dùng trong đợt tái cấu trúc này.

## Tiêu chí chấp nhận
- [ ] Mỗi trang là một component riêng nằm trong thư mục `frontend/components/pages/`, cùng các thành phần chia sẻ chung (hộp thoại import, drawer xem chi tiết từ, thông báo toast).
- [ ] Tách các chuỗi đa ngôn ngữ (i18n) khỏi các lệnh inline `t(en, vi)` vào một module từ điển riêng biệt.
- [ ] Không có dòng mã nguồn nào dài quá 160 ký tự trong thư mục `frontend/components/`.
- [ ] Luồng test Playwright vượt qua bình thường mà không cần sửa code test; ảnh chụp màn hình từng trang trước và sau khi tách trông đồng nhất.

## Kế hoạch
### Trước khi thực hiện
- [ ] Đọc các mục tài liệu về client components và routing trong `frontend/node_modules/next/dist/docs/` của phiên bản Next.js này
- [ ] Chụp ảnh màn hình trước khi sửa của cả 6 trang (sử dụng Playwright, lưu trong `docs/tam/`)
### Tách component
- [ ] Tách state và logic tải dữ liệu dùng chung vào một custom hook (`frontend/lib/use-workspace.ts`)
- [ ] Di chuyển từng trang vào `frontend/components/pages/<page>.tsx`
- [ ] Di chuyển các dialog/drawer vào các file riêng trong `frontend/components/`
- [ ] Di chuyển các chuỗi văn bản i18n vào `frontend/lib/i18n.ts`
### Kiểm chứng
- [ ] Chạy typecheck, build, `npm run test:e2e` đối chiếu với ứng dụng chạy qua `scripts/dev.py`
- [ ] So sánh ảnh chụp màn hình sau khi sửa với ảnh trước khi sửa
- [ ] Đánh giá xem các trang có nên chuyển thành route riêng của App Router hay không (ghi vào mục Sai lệch hoặc tạo ý tưởng trong sổ nhật ký)

## Nhật ký thực hiện

## Sai lệch
