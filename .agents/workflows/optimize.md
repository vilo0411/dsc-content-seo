---
description: Tối ưu bài cũ — Brand audit + rewrite + QA (Seven Sweeps Framework)
---

# Lệnh: /optimize [slug] [options]

## Options Hỗ Trợ
- `--step`: Tối ưu chi tiết từng bước — dừng chờ `/approve` sau Proposal.
- `--auto`: Tối ưu nhanh — tự động chốt Proposal và rewrite không cần duyệt.

## Nhiệm vụ
Cập nhật và tối ưu lại một bài viết cũ đang tồn tại để tăng thứ hạng, đảm bảo tính cập nhật của Brand và tiêu chuẩn SEO mới. Không xóa trắng viết lại — giữ "SEO Juice" của bài gốc.

---

## Quy trình thực thi chi tiết (Agent Sequencing)

### 🔄 Bước 0: System Context Load (BẮT BUỘC — trước mọi bước)
1. `knowledge/1-brand/profile.md` — Brand identity, USPs hiện tại
2. `knowledge/1-brand/personas.md` — 4 persona + ma trận Persona → Product Bridge
3. `knowledge/1-brand/service-operations.md` — Thông tin sản phẩm/dịch vụ mới nhất
4. `knowledge/3-pipeline/anti-ai-rules.md` — Bộ quy tắc Anti-AI
5. `knowledge/3-pipeline/glossary.md` — Thuật ngữ chuẩn thương hiệu
6. `knowledge/3-pipeline/revision-log.md` — Xem lỗi cũ đã được ghi nhận để không lặp
7. `.antigravity/memory/instincts.md` — Bản năng học được từ các vòng sửa trước
8. `knowledge/4-content/3-finalized/Final-[slug].md` — Bài gốc cần tối ưu

---

### ⚙️ Bước 1: Intake & Persona Declaration (BẮT BUỘC trước mọi audit)

**Bước 1.1 — Intake & Tracking:**
- Xác nhận file gốc tồn tại tại `knowledge/4-content/3-finalized/Final-[slug].md`. Nếu không tìm thấy: DỪNG và hỏi người dùng.
- Cập nhật `knowledge/4-content/topic-clusters.md` → trạng thái `Optimizing`.
- Tạo working copy: `knowledge/4-content/2-drafts/Optimize-[slug].md`.
  - Toàn bộ chỉnh sửa diễn ra trên bản copy này. Bài gốc không bị chạm đến.

**Bước 1.2 — Intent & Persona Declaration (BẮT BUỘC — thực hiện trước khi chạy bất kỳ audit nào):**

Đọc bài gốc + `personas.md`, sau đó xác định và **ghi rõ** 4 thông số sau. Đây là "hiến pháp" cho toàn bộ quá trình optimize — mọi quyết định rewrite phải nhất quán với 4 thông số này:

```
TARGET KEYWORD : [từ khóa chính của bài]
SEARCH INTENT  : [Informational / Transactional / Commercial / Navigational]
               → [Mô tả cụ thể: người dùng đang tìm gì, ở giai đoạn nào trong hành trình quyết định?]
PERSONA        : [P1 / P2 / P3 / P4] — [Tên persona]
               → [1 câu mô tả tại sao bài này phục vụ đúng persona này, không phải persona khác]
PRODUCT BRIDGE : [Tên sản phẩm DSC phù hợp] — [Góc dẫn dắt tự nhiên]
```

> **Nếu bài gốc đang phục vụ sai intent hoặc sai persona so với keyword:** Ghi rõ sự lệch lạc này vào Proposal (Section 0) và đề xuất hướng chỉnh — KHÔNG âm thầm giữ sai intent khi rewrite.

---

### ⚙️ Bước 2: Audit (Thu thập bối cảnh & Khám bệnh)

**Bước 2.1 — SEO Collector (SERP Competitor Analysis):**
- Kích hoạt agent `.antigravity/agents/seo-collector.md` (chỉ Step 1: SERP Research, không tạo Outline).
- **Dùng skill `.antigravity/skills/web-serp/SKILL.md`** — không dùng browser trực tiếp:
  1. **SERP Lookup**: WebFetch `https://r.jina.ai/https://www.bing.com/search?q=<từ+khóa+url+encoded>` → lấy top 5–10 URLs
  2. **Content Extraction**: Gọi **song song** tất cả URLs qua `https://r.jina.ai/{url}` → lọc header/footer, chỉ extract vùng nội dung chính
- Với mỗi đối thủ, thu thập và ghi lại đầy đủ:
  1. **Search Intent** — người dùng đang tìm gì (informational / transactional / commercial / navigational)?
  2. **Cấu trúc Outline** — toàn bộ H1, H2, H3 theo thứ tự xuất hiện.
  3. **Nội dung từng section** — section đó xử lý angle gì, trả lời câu hỏi nào của reader?
  4. **Yếu tố đặc biệt** — bảng so sánh, calculator, FAQ schema, số liệu cụ thể, expert quote, hình ảnh.
  5. **Content Gap** — nội dung/angle đối thủ có mà bài hiện tại đang thiếu.
- Output của bước này phải đủ để điền vào **Section 2 (Competitor Analysis)** của proposal-template.

**Bước 2.2 — Brand Guardian (Anti-AI + Brand Audit):**
- Kích hoạt agent `.antigravity/agents/brand-guardian.md`.
- Phân tích bài cũ: tìm vi phạm anti-ai-rules, thông tin sản phẩm lỗi thời, giọng văn sai persona.
- Output: danh sách lỗi cụ thể (dòng, loại lỗi, gợi ý sửa).

---

### ⚙️ Bước 3: Proposal (Đề xuất Tối ưu)
- Kích hoạt skill `.antigravity/skills/seo-optimization/SKILL.md` → Phase 1: Audit & Proposal.
- Tổng hợp kết quả từ Bước 2.1 và 2.2.
- Xuất **Báo cáo Đề xuất** theo đúng template tại `.antigravity/skills/seo-optimization/assets/proposal-template.md`.

**Ràng buộc bắt buộc khi điền proposal:**
- **Section 2.2 (Cấu trúc Outline từng đối thủ):** Phải có một entry cho **mỗi** competitor block đã output ở Bước 2.1. Không được gộp, rút gọn, hoặc chỉ lấy 1 đối thủ đại diện. Nếu đã visit 3 URL → phải có 3 block trong Section 2.2.
- **Section 2.3 (Intent Gap):** Phải trích dẫn cụ thể heading/angle từ đối thủ nào đang phục vụ intent mà bài hiện tại bỏ sót.
- **Section 5 (Content Gaps):** Mỗi đề xuất `[THÊM MỚI]` phải ghi rõ **học từ đối thủ nào** (Competitor 1/2/3) — không đề xuất chung chung.
- Phân loại rõ từng heading: `[GIỮ NGUYÊN]`, `[CẬP NHẬT]`, `[XÓA BỎ]`, `[THÊM MỚI]`.

**🚧 APPROVAL GATE (nếu dùng `--step`):**
> Trình bày Proposal cho người dùng.
> **DỪNG LẠI. Chờ `/approve` trước khi rewrite.**
> _(Nếu `--auto`: tự chốt Proposal và chuyển sang Bước 4.)_

---

### ⚙️ Bước 4: Execution (Rewrite với Seven Sweeps)
- Kích hoạt skill `.antigravity/skills/seo-optimization/SKILL.md` → Phase 2: Execution.
- Mở `knowledge/4-content/2-drafts/Optimize-[slug].md`.
- **Trước khi viết bất kỳ dòng nào — BẮT BUỘC đọc lại 3 file sau theo thứ tự:**
  1. `knowledge/3-pipeline/anti-ai-rules.md` — toàn bộ, không bỏ qua section nào
  2. `.antigravity/memory/instincts.md` — các lỗi đã học từ các vòng trước
  3. Content Strategy Header (Section 0 của Proposal) — Persona, Intent, Product Bridge
- Mọi câu viết ra phải đúng Persona, đúng Intent, đúng Product Bridge đã khai báo.
- Áp dụng tuần tự 7 bước quét (Clarity → Voice → So What → Prove It → Specificity → Emotion → Zero Risk).
- Chỉ sửa các phần được gắn nhãn `[CẬP NHẬT]`, `[XÓA BỎ]`, `[THÊM MỚI]` trong Proposal. Không chạm vào `[GIỮ NGUYÊN]`.

---

### ⚙️ Bước 5: QA (BẮT BUỘC trước khi trình bày)
- Kích hoạt agent `.antigravity/agents/quality-guardian.md`.
- QA đọc: `Optimize-[slug].md` + `anti-ai-rules.md` + `glossary.md` + `instincts.md`.
- Kết quả PASS → tiếp tục. Kết quả FAIL → sửa và QA lại.

**🚧 APPROVAL GATE 2:**
> Trình bày bản Optimize đã QA PASS cho người dùng.
> **DỪNG LẠI. Chờ người dùng đọc và gõ `/approve`.**
> Khi approve: xử lý theo workflow `/approve` (ghi đè lên Final, xóa bản nháp, update topic-clusters).
