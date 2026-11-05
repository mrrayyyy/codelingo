<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

## Hướng dẫn cho Frontend
- Đọc tài liệu trong `node_modules/next/dist/docs/` trước khi viết code cho Next.js để tránh các lỗi API không tương thích.
- Tuân thủ quy tắc ngôn ngữ chung của dự án:
  - Tài liệu, ghi chú hướng dẫn viết bằng **tiếng Việt**.
  - Tên thư mục dùng tiếng Việt không dấu snake_case trong `docs/`.
  - Tên file, component, route, hook và thư mục mã nguồn giữ nguyên bằng **tiếng Anh**.
  - Code, TypeScript types, comment kỹ thuật và git commit giữ nguyên tiếng Anh.
