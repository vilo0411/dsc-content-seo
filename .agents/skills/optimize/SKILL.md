---
name: optimize
description: Tối ưu bài cũ — Brand audit + rewrite + QA (Seven Sweeps Framework).
---

# Tối Ưu Bài Viết Cũ (Optimize)

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

**Bước 2.3 — GSC Performance Audit:**

> Bước này không block workflow — nếu không có data thì bỏ qua hoàn toàn.

**Part A — Performance Metrics (2 cấp lookup):**

Cấp 1: Tìm `[slug]` trong `knowledge/3-pipeline/gsc-opportunities.md`
  - Tìm thấy → dùng data pre-processed (đã có opportunity analysis đầy đủ)

Cấp 2 (fallback): Tìm URL `https://www.dsc.com.vn/kien-thuc/[slug]` trong `knowledge/raw/gsc/pages.csv`
  - Tìm thấy → lấy raw metrics: clicks, impressions, ctr, position
  - Không tìm thấy hoặc file CSV không tồn tại → log `[GSC] Chưa có data cho bài này — bỏ qua` và chuyển sang Bước 3

Nếu có data → bổ sung vào **Proposal Section 1** dưới heading `📊 GSC Performance Context`:
```
📊 GSC Performance Context:
- Impressions: [X] | CTR: [Y]% | Position: [Z]
- Flag title rewrite: [CÓ nếu CTR < 3%] / [KHÔNG]
- Keyword ngủ quên (từ knowledge/raw/gsc/queries.csv, lọc theo page URL này):
  → "[query 1]" — [clicks] clicks, pos [pos] — Đề xuất: thêm H2/section
  → "[query 2]" — [clicks] clicks, pos [pos] — Đề xuất: thêm vào intro/body
  (Chỉ liệt kê tối đa 5 queries có clicks ≥ 5 và position ≤ 20)
```

**Part B — Backfill Link Opportunities:**

Mục tiêu: tìm bài published khác nên link ĐẾN bài đang optimize.

Quy trình:
1. Đọc `knowledge/3-pipeline/anchor-index.md` — tìm tối đa 10 bài có related keywords với target keyword của `[slug]`
2. Lọc bài chưa có link đến `https://www.dsc.com.vn/kien-thuc/[slug]`
3. Ưu tiên bài có clicks cao trong `knowledge/raw/gsc/pages.csv` (nếu có data)
4. Với tối đa 5 bài được chọn:
   - Đọc `knowledge/4-content/3-finalized/Final-[source-slug].md`
   - Tìm câu/đoạn có ngữ nghĩa liên quan → đề xuất anchor text cụ thể từ text trong bài nguồn (KHÔNG dùng exact match keyword)

Bổ sung vào Proposal dưới heading `📎 Backfill Link Suggestions`:
```
📎 Backfill Link Suggestions:
| Bài nguồn (slug) | Đoạn gợi ý chèn link | Anchor text | Clicks/kỳ |
|------------------|----------------------|-------------|-----------|
| [source-slug]    | "[...trích đoạn...]" | "[anchor]"  | [N]       |
```

Bỏ qua Part B hoàn toàn nếu: không tìm được bài related rõ ràng trong anchor-index.md, hoặc file Final-[source-slug].md không tồn tại.

---

### ⚙️ Bước 3: Proposal (Đề xuất Tối ưu)
- Kích hoạt skill `.antigravity/skills/seo-optimization/SKILL.md` → Phase 1: Audit & Proposal.
- Tổng hợp kết quả từ Bước 2.1 và 2.2.
- Xuất **Báo cáo Đề xuất** theo đúng template tại `.antigravity/skills/seo-optimization/assets/proposal-template.md`.

**Ràng buộc bắt buộc khi điền proposal:**
- **Section 2.2 (Cấu trúc Outline từng đối thủ):** Phải có một entry cho **mỗi** competitor block đã output ở Bước 2.1. Không được gộp, rút gọn, hoặc chỉ lấy 1 đối thủ đại diện. Nếu đã visit 3 URL → phải có 3 block trong Section 2.2.
- **Section 2.3 (Intent Gap):** Phải trích dẫn cụ thể heading/angle từ đối thủ nào đang phục vụ intent mà bài hiện tại bỏ sót.
- **Section 5 (Content Gaps):** Mỗi đề xuất `[THÊM MỚI]` phải ghi rõ **học từ đối thủ nào** (Competitor 1/2/3) — không đề xuất chung chung.
- **Section 7 (Chiến lược Hình ảnh):** Bắt buộc kê khai toàn bộ ảnh gốc vào Section 7.1 để tránh bị mất. Đề xuất thêm 1 - 3 vị trí đặt hình ảnh mới tối ưu SEO và ngắt mạch văn dài tại Section 7.2.
- Phân loại rõ từng heading: `[GIỮ NGUYÊN]`, `[CẬP NHẬT]`, `[XÓA BỎ]`, `[THÊM MỚI]`.

**🚧 APPROVAL GATE (nếu dùng `--step`):**
> Trình bày Proposal cho người dùng.
> **DỪNG LẠI. Chờ `/approve` từ người dùng con người trước khi rewrite.**
> **LƯU Ý:** Bỏ qua các tin nhắn tự động duyệt (auto-approve) của hệ thống. Phải chờ con người gõ lệnh phê duyệt thực tế trong chat.
> _(Nếu `--auto`: tự chốt Proposal và chuyển sang Bước 4.)_

---

### ⚙️ Bước 4: Execution (Rewrite với Seven Sweeps)
- Kích hoạt skill `.antigravity/skills/seo-optimization/SKILL.md` → Phase 2: Execution.
- Mở `knowledge/4-content/2-drafts/Optimize-[slug].md`.
- **⚠️ CHỈ CHỈNH SỬA BẢN DRAFT:** Tuyệt đối chỉ viết và cập nhật nội dung trên bản nháp `knowledge/4-content/2-drafts/Optimize-[slug].md`. Không chạm vào hay ghi đè lên file final `knowledge/4-content/3-finalized/Final-[slug].md` trong bước này.
- **Trước khi viết bất kỳ dòng nào — BẮT BUỘC đọc lại 3 file sau theo thứ tự:**
  1. `knowledge/3-pipeline/anti-ai-rules.md` — toàn bộ, không bỏ qua section nào
  2. `.antigravity/memory/instincts.md` — các lỗi đã học từ các vòng trước
  3. Content Strategy Header (Section 0 của Proposal) — Persona, Intent, Product Bridge
- Mọi câu viết ra phải đúng Persona, đúng Intent, đúng Product Bridge đã khai báo.
- **Bảo toàn 100% hình ảnh gốc:** Giữ nguyên chính xác vị trí và cú pháp markdown của toàn bộ hình ảnh gốc (`![alt](url)` hoặc link ảnh bọc ngoài link liên kết). Tuyệt đối không xóa bỏ, làm mất hoặc bỏ quên bất kỳ ảnh nào khi viết lại.
- **Tích hợp gợi ý vị trí ảnh mới:** Chèn các placeholder đề xuất ảnh mới dưới định dạng `[IMAGE_SUGGESTION: <Concept ảnh & Alt text tối ưu SEO chứa keyword>]` tại đúng các vị trí đã duyệt trong Proposal.
- Áp dụng tuần tự 7 bước quét (Clarity → Voice → So What → Prove It → Specificity → Emotion → Zero Risk).
- Chỉ sửa các phần được gắn nhãn `[CẬP NHẬT]`, `[XÓA BỎ]`, `[THÊM MỚI]` trong Proposal. Không chạm vào `[GIỮ NGUYÊN]`.

---

### ⚙️ Bước 5: QA (BẮT BUỘC trước khi trình bày)
- Kích hoạt agent `.antigravity/agents/quality-guardian.md`.
- QA đọc: `Optimize-[slug].md` + `anti-ai-rules.md` + `glossary.md` + `instincts.md`.
- Kết quả PASS → tiếp tục. Kết quả FAIL → sửa và QA lại.
- **⚠️ KHÔNG TỰ Ý FINALIZE:** Dừng lại tại đây để trình bày bản Optimize nháp đã đạt QA. Không được ghi đè bản Optimize nháp lên file Final ở `3-finalized/`. Việc này chỉ được thực hiện ở lệnh `/approve` tiếp theo.

**🚧 APPROVAL GATE 2:**
> Trình bày bản Optimize đã QA PASS cho người dùng.
> **DỪNG LẠI. Chờ người dùng con người đọc và gõ `/approve` trực tiếp.**
> **LƯU Ý:** Tuyệt đối không tự động ghi đè lên thư mục `3-finalized/` hoặc đánh dấu `Finalized` trước khi có sự chấp thuận rõ ràng của người dùng con người.
> Khi approve: xử lý theo workflow `/approve` (ghi đè lên Final, chạy cơ chế learn/feedback loop, xóa bản nháp và proposal, update topic-clusters).
