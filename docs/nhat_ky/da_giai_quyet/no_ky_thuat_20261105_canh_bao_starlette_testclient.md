---
type: tech-debt
status: resolved
discovered: 2026-11-05
source: backend test run, 20261105_khoi_tao_quy_trinh_tai_lieu_agent
severity: low
owner: claude
---

# Cảnh báo lỗi thời (deprecation) của test client: httpx với starlette.testclient

## Ngữ cảnh và bằng chứng
Chạy lệnh `.venv/bin/python -m pytest backend/tests -q` vào ngày 2026-11-05 → `53 passed, 1 warning`: `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead` (phát sinh từ `fastapi/testclient.py:1`). Hiện tại cảnh báo này vô hại; nhưng một bản phát hành Starlette trong tương lai có thể loại bỏ hoàn toàn đường dẫn này và làm gãy toàn bộ các bài test API cùng một lúc.

## Hành động khuyến nghị
Kiểm tra ghi chú phát hành (release notes) của Starlette để xem phương án thay thế chuẩn, ghim hoặc nâng cấp phiên bản trong `backend/pyproject.toml` và `backend/requirements.lock`, xác nhận cảnh báo biến mất và các bài test vẫn vượt qua bình thường.

## Giải quyết
2026-11-06: gộp vào ticket [20261106_bo_che_do_arq_redis](../../cong_viec/dang_lam/20261106_bo_che_do_arq_redis.md) vì cùng sửa `backend/pyproject.toml` và sinh lại `backend/requirements.lock`.
