---
type: docs
owner: claude
stakes: routine
priority: P2
opened: 2026-11-06
---

# README portfolio: ảnh/GIF demo, sơ đồ kiến trúc, link demo

**Bị chặn bởi (Blocked by):** [Hệ thống thiết kế giao diện](20261106_he_thong_thiet_ke_giao_dien.md), [Trang demo công khai](20261106_trang_demo_cong_khai.md).

## Ngữ cảnh
README hiện là tài liệu vận hành dài, bắt đầu bằng hướng dẫn Docker; người xem repo không hiểu sản phẩm trong một phút. Chủ dự án chốt ngày 2026-11-06: README **giữ toàn bộ tiếng Việt** (không đổi quy tắc ngôn ngữ), bổ sung ảnh/GIF demo, sơ đồ kiến trúc và link demo.

## Tiêu chí chấp nhận
- [ ] Phần đầu README (trước mục cài đặt): mô tả một đoạn, link demo, badge CI, 3–5 ảnh chụp (desktop + mobile, sáng/tối) và một GIF ngắn (≤ 5 MB) cho luồng import → flashcard → luyện nói.
- [ ] Sơ đồ kiến trúc Mermaid (Next.js → FastAPI → Neon, GitHub Actions, Groq) khớp với `docs/kien_truc.md`.
- [ ] Mục "Điểm kỹ thuật đáng chú ý" (an toàn file nén, lọc secret, FSRS idempotent, hợp đồng plugin, cloud miễn phí) dẫn link tới code.
- [ ] Hướng dẫn chạy dev và deploy chuyển xuống dưới hoặc sang `docs/`, README vẫn có link tới.
- [ ] Ảnh được sinh lại bằng một script Playwright (`frontend/scripts/screenshots.ts`) để cập nhật dễ dàng; không ảnh nào chứa secret hay URL kèm thông tin đăng nhập.

## Kế hoạch
### Tư liệu
- [ ] Viết `frontend/scripts/screenshots.ts` chụp các trang trên dữ liệu demo; lưu vào `docs/hinh_anh/`
- [ ] Quay GIF luồng chính (Playwright video → chuyển sang GIF/WebP bằng ffmpeg), tối ưu dung lượng
### Viết README
- [ ] Sắp xếp lại cấu trúc README theo tiêu chí; giữ tiếng Việt
- [ ] Đồng bộ sơ đồ với `docs/kien_truc.md`
- [ ] `python3 tools/docs/check_doc_links.py` và `scan_secrets.py` sạch
- [ ] `[user]` Chủ dự án đọc duyệt README trên GitHub

## Nhật ký thực hiện

## Sai lệch
