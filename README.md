# CodeLingo

Luyện tập tiếng Anh công sở từ chính mã nguồn bạn làm việc hàng ngày. Ứng dụng MVP cá nhân (single-user), ưu tiên tính cục bộ (local-first) với giao diện Next.js, đường ống trích xuất từ vựng Python (Tree-sitter + spaCy), xử lý tác vụ import bền vững và flashcard thuật toán FSRS.

**Mô hình triển khai ưu tiên: Đám mây (Cloud), không yêu cầu Docker hay chạy model nặng cục bộ.** Dựa theo quyết định sản phẩm mới nhất, hãy sử dụng [Hướng dẫn triển khai Cloud miễn phí (Free-tier)](docs/cloud-deployment.vi.md): Render host ứng dụng web/API nhẹ, Neon lưu trữ dữ liệu học tập PostgreSQL, GitHub Actions thực thi NLP khi có yêu cầu (on-demand), và các API Groq tùy chọn xử lý giọng nói/viết. Mô hình chạy cục bộ/tự host (Docker Compose) bên dưới vẫn luôn sẵn sàng phục vụ việc phát triển.

## Làm việc trên kho lưu trữ này (Working on this repository)

Đây là kho lưu trữ công khai (public repository) được duy trì và phát triển cùng Claude Code và Gemini/Antigravity. Mọi công việc được theo dõi theo mô hình docs-as-code: bắt đầu với [AGENTS.md](AGENTS.md) và [docs/protocol/](docs/protocol/README.md).
- Tickets theo dõi tại: `docs/backlog/<status>/`
- Phát hiện & nợ kỹ thuật: `docs/ledger/`
- Quyết định kiến trúc: [docs/decisions/](docs/decisions/README.md)
- Định hướng sản phẩm: [Lộ trình phát triển (Roadmap)](docs/product/roadmap.md)

### Quy tắc Ngôn ngữ & Đặt tên cốt lõi
- **Nội dung tài liệu**: Toàn bộ tài liệu (`docs/`, `README.md`, tickets backlog, ledger, ADRs, runbooks) **bắt buộc viết bằng tiếng Việt**.
- **Tên file & Thư mục**: **Bắt buộc giữ 100% bằng tiếng Anh** (ví dụ: `docs/architecture.md`, `docs/backlog/ready/`, `tools/`), tuyệt đối không đổi tên file/thư mục sang tiếng Việt để bảo đảm tính tương thích với tooling, scripts và CI/CD.
- **Giao tiếp**: Trao đổi với chủ dự án bằng tiếng Việt.
- **Mã nguồn & Kỹ thuật**: Code, comment trong code, commit message, shell commands và các thuật ngữ kỹ thuật giữ nguyên chuẩn tiếng Anh.

## Tài liệu thiết kế hệ thống (Design deliverables)

Đọc [Đánh giá kiến trúc, sơ đồ hệ thống, ERD và kế hoạch từng cột mốc](docs/architecture.md). Các hợp đồng plugin tương ứng nằm trong [TypeScript](shared/plugins.ts) và [Python](backend/app/contracts.py); [module chính tả (dictation)](backend/app/plugins.py) là ví dụ hoàn chỉnh về sinh bài tập và chấm điểm.

Phiên bản MVP chọn phương thức import qua file ZIP hoặc link GitHub công khai cùng từ điển mặc định ngoại tuyến (offline). Tính năng đăng nhập đa người dùng và GitHub OAuth cho repo riêng tư tạm thời hoãn lại như đã xác nhận trong thiết kế.

## Chạy với Docker Compose

Yêu cầu Docker và Docker Compose. Chạy từ thư mục gốc của dự án:

```sh
cp .env.example .env
# Chỉnh sửa file .env: thiết lập 2 giá trị ngẫu nhiên khác nhau cho API_KEY và POSTGRES_PASSWORD.
# Tạo chuỗi ngẫu nhiên bằng lệnh: python3 -c 'import secrets; print(secrets.token_urlsafe(32))'
docker compose up --build -d
```

Mở trình duyệt tại **http://localhost:3000**. Chọn **Import repository → Try the Atlas API sample repository**, hoặc import repo GitHub công khai / file ZIP của bạn. Theo dõi tiến độ import tại mục My repositories, duyệt Từ vựng (Vocabulary), và mở Ôn tập ngắt quãng (Spaced review). Lật mở nghĩa từ vựng, tự đánh giá mức độ ghi nhớ; server sẽ lưu lại thời gian ôn tập tiếp theo theo thuật toán FSRS.

Cổng web bind vào loopback cục bộ. PostgreSQL, Redis và API là các dịch vụ nội bộ. Sử dụng từ xa cần có TLS và xác thực qua reverse proxy; bản single-user không có màn hình đăng nhập. File `.env` được đưa vào `.gitignore`. Mật khẩu trong chuỗi kết nối cần bảo đảm URL-safe; `secrets.token_urlsafe` là định dạng phù hợp. Đặt `WEB_PORT` nếu cổng 3000 đã bị chiếm dụng.

```sh
docker compose logs -f api worker
docker compose down                 # dừng dịch vụ, vẫn giữ nguyên dữ liệu học tập
```

Không chạy `docker compose down -v` trừ khi bạn chủ động muốn xóa sạch toàn bộ dữ liệu học tập đã lưu. Sao lưu PostgreSQL bằng `pg_dump`; Redis sử dụng chế độ lưu bền vững AOF cho hàng đợi tác vụ.

## Chạy trực tiếp không cần Docker (Run without Docker)

Yêu cầu **Python 3.11** và **Node.js 22+**. Sử dụng SQLite và background task chạy trong chính tiến trình API (do đó các tác vụ import sẽ không tự phục hồi nếu tiến trình bị sập đột ngột). Docker Compose vẫn là cấu hình triển khai chuẩn.

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.lock
.venv/bin/python -m pip install --no-deps -e backend
npm --prefix frontend ci
.venv/bin/python scripts/dev.py
```

File lockfile sẽ cài sẵn model tiếng Anh spaCy. Nếu cài trực tiếp từ `pyproject.toml`, hãy chạy thêm lệnh `.venv/bin/python -m spacy download en_core_web_sm`. Các dịch vụ cục bộ lắng nghe tại http://localhost:3000 và http://127.0.0.1:8000. Bấm Ctrl-C để dừng cả hai. Lệnh khởi chạy dev sẽ nạp file `.env` gốc và chia sẻ API key với Next.js. Nếu không có `.env`, hệ thống dùng key dev mặc định; Compose yêu cầu cấu hình secret rõ ràng.

## Các tính năng đã triển khai (What is implemented)

- Import giới hạn kích thước với ZIP và GitHub công khai, thăm dò tiến độ (polling), dọn dẹp file tạm, lưu trữ an toàn khi retry, PostgreSQL + Redis/ARQ trong môi trường Compose.
- Sử dụng Tree-sitter bóc tách comment, docstring Python, chuỗi string và tên định danh (identifiers) cho TypeScript/TSX, JavaScript/JSX, Python, Java, và Go. Bóc tách văn bản xuôi Markdown nằm ngoài các khối code block. Tuyệt đối không thực thi mã nguồn người dùng tải lên.
- Tách từ dạng camelCase / snake_case / từ viết tắt (acronyms); chuẩn hóa từ gốc (lemmatization) và gán nhãn từ loại (POS) qua spaCy; loại bỏ stopwords, từ khóa cú pháp, và từ vựng A1 cơ bản; bộ lọc ngôn ngữ và lọc mẫu chuỗi khóa bảo mật; tính toán tần suất theo từng repo, ước lượng CEFR, gán nhãn tags và xếp hạng từ vựng. Thứ hạng tính theo hàm logarit tần suất để các định danh sinh tự động không lấn át văn bản đọc hiểu.
- Khử trùng lặp từ vựng giữa các repository của người dùng, trích xuất 1–3 ngữ cảnh gốc kèm số dòng mã nguồn, xem trước ngữ cảnh mã nguồn chỉ đọc với Monaco Editor có tô sáng từ vựng, hỗ trợ tìm kiếm và lọc từ vựng linh hoạt.
- Tích hợp bộ điều hợp thuật toán FSRS, lập lịch ôn tập bền vững, bảo vệ thẻ học cũ (stale-card), gửi kết quả idempotent, đếm chuỗi ngày học liên tục (streak), mục tiêu hàng ngày và tính điểm luyện tập. Trạng thái “Thành thạo” (Mastered) quy định là sau ít nhất 3 lượt ôn tập và độ ổn định FSRS tối thiểu 14 ngày; đây là tiêu chuẩn phỏng đoán sản phẩm, không phải chứng chỉ ngoại ngữ.
- Bài tập đọc hiểu trắc nghiệm; module luyện nghe chép chính tả (dictation); đọc to so sánh độ khớp giọng nói với văn bản gốc; bài tập viết commit message và phản hồi code review. Các dịch vụ model/giọng nói tùy chọn sẽ tắt cho đến khi được cấu hình.
- Giao diện song ngữ Anh/Việt, cài đặt học tập, xuất dữ liệu ra file CSV và bộ thẻ Anki `.apkg`, API xóa ngữ cảnh repository và xóa từ vựng. Xóa một repository vẫn giữ lại từ vựng đã học và lịch ôn tập của từ đó.
- Định nghĩa từ vựng ngoại tuyến có sẵn kèm phiên âm IPA; hỗ trợ tùy chọn Free Dictionary API (chỉ gửi từ gốc lemma). Endpoint `POST /vocab/{id}/dictionary` làm giàu thêm dữ liệu một từ. Các từ không rõ nghĩa được hiển thị là "chưa có thông tin" thay vì sinh nội dung bịa đặt.

Phạm vi còn lại cho v1: Đăng nhập GitHub OAuth cho repo riêng tư; bóc tách ngữ cảnh từ git-log / pull request; sinh đoạn văn đọc hiểu hoàn chỉnh kèm câu hỏi; bài tập điền từ khi nghe (gap-fill); chấm điểm phát âm theo âm vị (phoneme); kỹ thuật nhại giọng (shadowing) / nói tự do; mô phỏng standup meeting / phỏng vấn đa lượt; đa dạng hóa biến thể bài tập viết; tập ngữ liệu CEFR chuẩn hóa; cơ chế cài đặt và cách ly plugin; migration schema bằng Alembic (hiện tại schema khởi tạo bằng SQLAlchemy `create_all`, không dùng làm chiến lược nâng cấp schema).

## Các dịch vụ cục bộ tùy chọn — thứ tự kích hoạt

Trước tiên hãy kiểm tra quy trình cơ bản: import → trích xuất → ôn tập flashcard. Sau đó mới bật riêng lẻ từng dịch vụ nhận dạng giọng nói / sinh văn bản. Không bắt buộc phải có dịch vụ speech hay LLM để thực hiện import, học từ vựng, đọc hiểu hay luyện flashcard.

1. **TTS / Piper (Tổng hợp giọng nói):** Cài đặt Piper CLI và tải model giọng đọc tiếng Anh định dạng `.onnx` cùng file JSON đi kèm. Đặt biến `PIPER_BINARY` và `PIPER_MODEL` thành đường dẫn **bên trong môi trường chạy API**. Bộ điều hợp chuyển câu qua stdin, chạy không cần shell, giới hạn thời gian thực thi và tự xóa file WAV tạm sau khi phát. Với Docker, mở rộng `backend/Dockerfile` để cài đặt runtime Piper và mount các file model chỉ đọc; chỉ trỏ đường dẫn file thực thi từ máy host vào container là không đủ.
2. **STT / Whisper (Nhận dạng giọng nói):** Chạy dịch vụ faster-whisper cục bộ mở endpoint chuẩn OpenAI `POST /v1/audio/transcriptions`, sau đó đặt `WHISPER_URL` trỏ tới URL cơ sở này. Trình duyệt ghi âm tối đa 60 giây và API nhận file tối đa 10 MiB. Dữ liệu âm thanh được chuyển tiếp tạm thời và CodeLingo không lưu trữ file âm thanh. Bài chấm đọc to so khớp độ tương đồng văn bản chuyển đổi; không chấm điểm chi tiết âm vị hay phát âm. Cần cấu hình chính dịch vụ Whisper không lưu trữ lại âm thanh.
3. **LLM / Ollama (Mô hình ngôn ngữ lớn):** Kéo một model phù hợp với phần cứng của bạn, thiết lập `OLLAMA_URL` và `OLLAMA_MODEL`. Bộ điều hợp gọi endpoint `/api/chat` với JSON schema phản hồi nghiêm ngặt. Kết quả không hợp lệ hoặc lỗi dịch vụ sẽ báo lỗi mà không ghi nhận điểm. Đánh giá từ LLM mang tính chất ước lượng AI. Chỉ có ngữ cảnh bài tập đã chọn và câu trả lời của người học được gửi tới model.

Đối với các dịch vụ chạy trên Docker Desktop máy host, sử dụng `http://host.docker.internal:PORT`; môi trường Linux cần thiết lập ánh xạ host gateway rõ ràng hoặc đưa service vào chung mạng Compose network. Khởi động lại API/web sau khi thay đổi file môi trường. Các dịch vụ STT/LLM được kiểm tra tại thời điểm sử dụng; URL được cấu hình không đồng nghĩa với dịch vụ đang hoạt động thực tế (live health guarantee).

`DICTIONARY_ONLINE=false` giữ cho yêu cầu tra từ điển hoàn toàn ngoại tuyến. Chỉ đổi thành `true` nếu bạn đồng ý gửi từ vựng cần tra cứu tới https://api.dictionaryapi.dev. Bộ điều hợp tra cứu không bao giờ gửi cả câu trích xuất từ repository.

## Kiểm tra hệ thống (Verification)

```sh
.venv/bin/python -m pytest backend/tests -q
npm --prefix frontend run typecheck
npm --prefix frontend run build
# Chạy kiểm thử End-to-End với ứng dụng đang chạy cục bộ hoặc qua Compose:
cd frontend
npx playwright install chromium
npm run test:e2e
```

Bộ test trình duyệt sử dụng dữ liệu mẫu đi kèm, tạo các bản ghi học tập và sau đó tự động xóa ngữ cảnh repo đã import. Chạy test trên database phát triển riêng. Thiết lập `BASE_URL` để kiểm tra cổng cục bộ khác. Các bộ điều hợp gọi model AI được kiểm thử bằng các provider giả lập (replacement providers) và mô phỏng phản hồi khi dịch vụ ngoại tuyến; việc kiểm tra thực tế kết quả TTS/STT/LLM yêu cầu cài đặt và khởi chạy các dịch vụ đó.

Để chạy riêng bộ bóc tách từ vựng:

```sh
.venv/bin/python -m app.extraction backend/tests/fixtures/sample_repo
```

## Cấu trúc thư mục (Layout)

```text
backend/app/
  contracts.py     hợp đồng định kiểu cho plugin và service
  extraction.py    đường ống: tree-sitter → spaCy → bộ lọc → xếp hạng
  lexicon.py       định nghĩa biên soạn thủ công và dữ liệu gốc ước lượng CEFR
  imports.py       giới hạn file nén, vòng đời mã nguồn, worker ARQ
  db.py            mô hình quan hệ và schema ban đầu
  srs.py           bộ điều hợp thuật toán lặp lại ngắt quãng FSRS
  plugins.py       bài tập đọc hiểu, chính tả, đọc to, viết, phản hồi code review
  adapters.py      bộ điều hợp Piper, Whisper, Ollama, từ điển offline/online
  main.py          các API import, từ vựng, ôn tập, bài tập, cài đặt/xuất dữ liệu
backend/tests/     kiểm thử trích xuất, xử lý file nén, plugin và API end-to-end
frontend/          Next.js App Router, server-only API proxy, giao diện người dùng, e2e test
shared/            hợp đồng TypeScript cho plugin
docs/              kiến trúc, giao thức, backlog, ledger, quyết định kiến trúc (ADR), lộ trình
tools/docs/        kiểm tra link tài liệu, dọn dẹp housekeeping, quét lộ secret
scripts/dev.py     lệnh khởi chạy đồng thời hai dịch vụ dev cục bộ
compose.yaml       PostgreSQL, Redis, API, worker, Next.js
```

Không có repository nào được tải tự động từ trước. **Atlas API** là một repo nhỏ được viết riêng cho mục đích kiểm thử; hình minh họa code trên dashboard chỉ mang tính trang trí, không phải nội dung trích xuất của người dùng. Font chữ, Monaco Editor và các web worker của editor đều được phân phối cục bộ. Monaco được build lại từ bản ESM để tích hợp bản vá DOMPurify ghi đè, tránh sử dụng gói vendor bundle chứa phiên bản cũ dễ bị lỗi bảo mật.
