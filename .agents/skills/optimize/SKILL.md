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
2. `knowledge/1-brand/personas.md` — **chỉ đọc section persona được chọn** sau Bước 1.2 (không load cả 4 persona)
3. `knowledge/1-brand/service-operations.md` — Thông tin sản phẩm/dịch vụ mới nhất
4. `knowledge/3-pipeline/anti-ai-rules.md` — Bộ quy tắc Anti-AI
5. `knowledge/3-pipeline/glossary.md` — Thuật ngữ chuẩn thương hiệu
6. `knowledge/3-pipeline/revision-log.md` — **chỉ grep theo `[slug]`** (`grep -n "[slug]" knowledge/3-pipeline/revision-log.md`), không đọc cả file
7. `.antigravity/memory/instincts.md` — Bản năng rút gọn (+ `instincts-by-scope/<topic>.md` nếu có)
8. `knowledge/4-content/3-finalized/Final-[slug].md` — Bài gốc cần tối ưu

> Đây là lần load context **duy nhất** trong session. Các bước sau (kể cả QA ở Bước 5) không đọc lại các file này.

---

### ⚙️ Bước 1: Intake & Persona Declaration (BẮT BUỘC trước mọi audit)

**Bước 1.1 — Intake & Tracking:**
- Xác nhận file gốc tồn tại tại `knowledge/4-content/3-finalized/Final-[slug].md`. Nếu không tìm thấy: DỪNG và hỏi người dùng.
- `python scripts/topic_status.py [slug] --set Optimizing` (không đọc `topic-clusters.md`).
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

**Bước 2.1 — SEO Collector (SERP Competitor Analysis & Ultra-lightweight Script Crawl):**
- Kích hoạt agent `.antigravity/agents/seo-collector.md` (chỉ Step 1: SERP Research, không tạo Outline).
- **Quy trình thu thập & cào cấu trúc đối thủ tiết kiệm Token (Token-Efficient Flow):**
  1. **SERP Lookup (DataForSEO)**: `python .antigravity/skills/web-serp/scripts/serp_research.py "<keyword>" --top 5` → top 5 URLs Google VN + PAA + Featured Snippet (cache 30 ngày, không dùng `--no-cache`). Bỏ URL của chính dsc.com.vn.
  2. **Automated Crawl & Filter (Chạy Script python `scripts/analyze_competitors.py`)**:
     - Chạy lệnh: `python scripts/analyze_competitors.py <url1> <url2> <url3> ...`
     - Script sẽ tự động xác thực HTTP status, **bỏ qua ngay lập tức** các URL lỗi (4xx, 5xx) hoặc các URL có dung lượng quá ít (thin content / link rác / error redirect < 200 từ).
     - Script chỉ bóc tách cấu trúc Headings (H1, H2, H3, H4) và thống kê Word Count từng section, loại bỏ toàn bộ HTML rác/nav/header/footer để **tối ưu 95%+ token** (không load toàn bộ raw page vào context).
  3. **Đọc báo cáo kết quả**: Sử dụng kết quả xuất ra tại console hoặc file `knowledge/raw/competitors_analysis.json` để điền trực tiếp vào Section 2 của Proposal.

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

Quy trình (1 lệnh, không đọc `anchor-index.md` hay file Final nào):
```bash
python scripts/find_links.py --backfill [slug] --top 5
```
Script tự: quét `anchor-index.md` + toàn bộ `3-finalized/*.md`, lọc bài chưa link tới `https://www.dsc.com.vn/kien-thuc/[slug]`, ưu tiên clicks từ `knowledge/raw/gsc/pages.csv` (nếu có), và trả về **đúng dòng + trích đoạn** có thể chèn anchor. Bạn chỉ chọn anchor text từ trích đoạn đó (KHÔNG dùng exact match keyword).

Bổ sung vào Proposal dưới heading `📎 Backfill Link Suggestions`:
```
📎 Backfill Link Suggestions:
| Bài nguồn (slug) | Đoạn gợi ý chèn link | Anchor text | Clicks/kỳ |
|------------------|----------------------|-------------|-----------|
| [source-slug]    | "[...trích đoạn...]" | "[anchor]"  | [N]       |
```

Bỏ qua Part B hoàn toàn nếu script trả về "Không có bài nào phù hợp".

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
- **Trước khi viết bất kỳ dòng nào:** đọc lại **Content Strategy Header** (Section 0 của Proposal) — Persona, Intent, Product Bridge. `anti-ai-rules.md` và `instincts.md` đã có trong context từ Step 0 — **không đọc lại**; nếu session mới (mất context) thì mới load lại 2 file này.
- Mọi câu viết ra phải đúng Persona, đúng Intent, đúng Product Bridge đã khai báo.
- **Bảo toàn 100% hình ảnh gốc:** Giữ nguyên chính xác vị trí và cú pháp markdown của toàn bộ hình ảnh gốc (`![alt](url)` hoặc link ảnh bọc ngoài link liên kết). Tuyệt đối không xóa bỏ, làm mất hoặc bỏ quên bất kỳ ảnh nào khi viết lại.
- **Tự động sinh ảnh mới & chèn trực tiếp (BẮT BUỘC — KHÔNG chỉ để placeholder):**
  1. Ngay tại Bước 4 (Execution), đối với các vị trí đề xuất ảnh mới tại Section 7.2 của Proposal, kích hoạt skill `image` (`.agents/skills/image/SKILL.md` / tool `generate_image`) để sinh ảnh trực tiếp.
  2. Prompt sinh ảnh tuân thủ nghiêm ngặt DSC Brand Rules: 3D Vector Isometric / Abstract Finance, palette `#00AD14`, `#2BE841`, `#10E7B3`, `#0D1B2A`, `no-text: true` (`Absolutely NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS`), tuyệt đối cấm màu đỏ (`NO RED COLOR`).
  3. Sao chép toàn bộ file ảnh tạo ra vào thư mục `knowledge/4-content/images/` với tên file chuẩn `[slug]-[concept].jpg`.
  4. Chèn trực tiếp đường dẫn Markdown ảnh tương đối chuẩn vào bài nháp: `![Alt text tối ưu SEO chứa keyword](../images/[slug]-[concept].jpg)`.
- Áp dụng tuần tự 7 bước quét (Clarity → Voice → So What → Prove It → Specificity → Emotion → Zero Risk).
- Chỉ sửa các phần được gắn nhãn `[CẬP NHẬT]`, `[XÓA BỎ]`, `[THÊM MỚI]` trong Proposal. Không chạm vào `[GIỮ NGUYÊN]`.

---

### ⚙️ Bước 5: QA (BẮT BUỘC trước khi trình bày)
- Chạy lint trước (kiểm tra luôn bảo toàn ảnh gốc):
  ```bash
  python scripts/qa_lint.py knowledge/4-content/2-drafts/Optimize-[slug].md --original knowledge/4-content/3-finalized/Final-[slug].md --fix
  ```
  Exit 1 → sửa đúng các dòng CRITICAL/MAJOR, chạy lại. Chưa gọi Quality Guardian khi lint chưa PASS.
- Lint PASS → kích hoạt agent `.antigravity/agents/quality-guardian.md`. QA chỉ đọc thêm `Optimize-[slug].md` + Content Strategy Header — **không đọc lại** `anti-ai-rules.md` / `glossary.md` / `instincts.md` (đã có từ Step 0).
- Kết quả PASS → tiếp tục. FAIL → sửa và QA lại **tối đa 2 vòng**; sau vòng 2 vẫn FAIL → dừng, trình bày kèm `⚠️ Remaining issues`.
- **⚠️ KHÔNG TỰ Ý FINALIZE:** Dừng lại tại đây để trình bày bản Optimize nháp đã đạt QA. Không được ghi đè bản Optimize nháp lên file Final ở `3-finalized/`. Việc này chỉ được thực hiện ở lệnh `/approve` tiếp theo.

**🚧 APPROVAL GATE 2:**
> Trình bày bản Optimize đã QA PASS cho người dùng.
> **DỪNG LẠI. Chờ người dùng con người đọc và gõ `/approve` trực tiếp.**
> **LƯU Ý:** Tuyệt đối không tự động ghi đè lên thư mục `3-finalized/` hoặc đánh dấu `Finalized` trước khi có sự chấp thuận rõ ràng của người dùng con người.
> Khi approve: xử lý theo workflow `/approve` (ghi đè lên Final, chạy cơ chế learn/feedback loop, xóa bản nháp và proposal, update topic-clusters).
