---
name: optimize
description: Tối ưu bài cũ — Brand audit + rewrite + QA (Seven Sweeps Framework).
---

# Tối Ưu Bài Viết Cũ (Optimize)

> **Nguồn quy trình duy nhất** cho `/optimize`. `.antigravity/skills/seo-optimization/` chỉ còn chứa template Proposal + tài liệu tham khảo — không cần mở `SKILL.md` của nó.

## Options
- `--step`: dừng chờ `/approve` sau Proposal.
- `--auto`: tự chốt Proposal và rewrite không cần duyệt.

Input: `/optimize chi-so-ps` · `/optimize https://www.dsc.com.vn/kien-thuc/chi-so-ps` · `/optimize Final-chi-so-ps.md`.

## Nhiệm vụ
Cập nhật bài đang publish để tăng thứ hạng, đúng Brand và chuẩn SEO mới. Không xóa trắng viết lại — giữ "SEO Juice" của bài gốc: không đổi slug, không đổi H1 nếu Proposal không ghi.

---

### 🔄 Bước 0: System Context Load (BẮT BUỘC — 1 lần/session)
1. `knowledge/1-brand/profile.md` · `knowledge/1-brand/service-operations.md`
2. `knowledge/3-pipeline/anti-ai-rules.md` · `knowledge/3-pipeline/glossary.md`
3. `.antigravity/memory/instincts.md` (+ `instincts-by-scope/<topic>.md` nếu có) + `python scripts/optimize_instincts.py --show [slug]` (ghi chú ARTICLE của chính bài này). Không mở `instincts-archive.md`.
4. Lịch sử sửa bài: `grep -rn "[slug]" knowledge/3-pipeline/revision-log*` (không đọc cả file). Outline gốc nếu có: `python scripts/article_snapshot.py [slug] --path outline`
5. Bài gốc `knowledge/4-content/3-finalized/Final-[slug].md` (chưa có → Bước 1.1)
6. Persona — `python scripts/persona.py P<n>` sau Bước 1.2 (không mở `personas.md`)

Các bước sau (kể cả QA ở Bước 5) không đọc lại các file này.

---

### ⚙️ Bước 1: Intake & Persona

**1.1 — Bản gốc & baseline**
- Đồng bộ bản live (bài có thể đã sửa thẳng trên CMS):
  ```bash
  python scripts/sync_live.py --only [slug]      # bản đang publish → knowledge/raw/live/html/[slug].html
  python scripts/sync_live.py --compare [slug]   # link chỉ có trên live + độ lệch văn bản
  ```
  - **Chưa có `Final-[slug].md`:** dùng `knowledge/raw/live/html/[slug].html` làm bản gốc (giữ nguyên 100% ảnh, heading, bảng), lưu thành `Final-[slug].md` với front matter `source: https://www.dsc.com.vn/kien-thuc/[slug]` + `fetched_at`. Slug không có trên live → dừng, báo user.
  - Link "chỉ có trên live" **phải giữ** trong bản Optimize. Độ giống < 90% → báo user, đề xuất dùng nội dung live làm bản gốc.
- `python scripts/topic_status.py [slug] --set Optimizing`
- Baseline (bản optimize không được tệ hơn):
  ```bash
  python scripts/qa_lint.py knowledge/4-content/3-finalized/Final-[slug].md --no-sitemap
  python scripts/slop_check.py knowledge/4-content/3-finalized/Final-[slug].md -v
  python scripts/market_facts.py --verify knowledge/4-content/3-finalized/Final-[slug].md
  python scripts/news_feed.py --topic "[keyword]" --days 30
  ```
  `FACT-stale` = tín hiệu refresh mạnh nhất. `news_feed` cho mốc sự kiện có ngày thay cho "thời gian gần đây".
- Working copy: `knowledge/4-content/2-drafts/Optimize-[slug].md` — mọi chỉnh sửa trên bản này.

**1.2 — Content Strategy Header (BẮT BUỘC trước mọi audit)**
Đọc bài gốc + persona, ghi rõ — đây là "hiến pháp" cho mọi quyết định rewrite:
```
TARGET KEYWORD : [từ khóa chính]
SEARCH INTENT  : [Informational / Transactional / Commercial / Navigational] → [người đọc tìm gì, ở giai đoạn nào]
PERSONA        : [P1–P4] — [tên] → [vì sao đúng persona này]
PRODUCT BRIDGE : [sản phẩm DSC] — [góc dẫn dắt]
```
Bài gốc lệch intent/persona → ghi vào Proposal Section 0 và đề xuất hướng chỉnh, không âm thầm giữ sai.

---

### ⚙️ Bước 2: Audit

**2.1 — SERP & đối thủ** (làm trực tiếp — không cần mở `seo-collector.md`, `seo-outlining/SKILL.md` hay `brief-template.md`)
1. `python .antigravity/skills/web-serp/scripts/serp_research.py "<keyword>" --top 10 --extract 5` (cache 30 ngày, không `--no-cache`; trang dsc.com.vn tự bị loại khỏi phần so sánh).
   - **Topic Coverage → khối máy đọc của Proposal:** `Thuật ngữ BẮT BUỘC phủ` → `Entities:` (bỏ cụm nào ghi `Entities_Skipped`); `Chủ đề con nhiều đối thủ cùng có` mà bài chưa có → `[THÊM MỚI]` ở Section 5; `Nguồn đối thủ trích` → nguồn gốc cần link.
   - **Information_Gain (≥ 2 mục có `proof`):** điều bản mới sẽ có mà top 5 không có. Bài gốc không có gì riêng → đây là việc chính của lần optimize, không phải sửa câu chữ.
   - **PAA refresh (ghi vào Proposal):** câu PAA chưa có trong bài → `[THÊM MỚI]` vào FAQ (câu đầu ≤ 60 từ, có số + mốc thời gian) hoặc nâng thành H2/H3 nếu thuộc intent chính. Câu FAQ cũ không còn trong PAA và không có traffic GSC → cân nhắc `[XÓA BỎ]`. `Google answer` thuộc đối thủ → viết đáp án ngắn và cụ thể hơn. Ghi `PAA_Questions:` vào YAML Proposal.
2. `python scripts/analyze_competitors.py <url1> <url2> …` → heading + số từ từng section (tự bỏ URL lỗi/thin). Kết quả in console + `knowledge/raw/competitors_analysis.json` → điền Section 2.

**2.2 — Brand Guardian** (`.antigravity/agents/brand-guardian.md`): vi phạm anti-AI, thông tin sản phẩm lỗi thời, giọng sai persona → danh sách (dòng, loại lỗi, gợi ý sửa).

**2.3 — GSC** (không block — không có data thì bỏ qua). Playbook: `.antigravity/skills/seo-dashboard/SKILL.md`.
- Có MCP `SEO Dashboard`: `query_search_analytics` (`property_url: "sc-domain:dsc.com.vn"`, `dimensions: ["query"]`, `page_value: "/kien-thuc/[slug]"`, `days: 90`, `compare_mode: "prev_period"`, `limit: 30`) → lưu JSON `scratch/dashboard-pq.json` → `python scripts/dashboard_cache.py save page-queries [slug] --file scratch/dashboard-pq.json`.
  Cannibalization: thêm `query_search_analytics` (`dimensions: ["page"]`, `query_value: "[keyword]"`, `days: 90`, `limit: 10`) — URL DSC khác nhận impressions đáng kể → Section 0.
- Mọi agent: `python scripts/dashboard_cache.py report [slug]` → dán block vào Proposal Section 1 (`📊 GSC Performance Context`). Từ đó: CTR < 3% → flag rewrite Title; tối đa 5 query clicks ≥ 5, position ≤ 20 chưa được bài phục vụ → đề xuất thêm H2/section hoặc đưa vào sapo. **Exit 3 (chưa có cache) → ghi `[GSC] Chưa có data — bỏ qua`**.

**2.4 — Backfill link tới bài này:** `python scripts/find_links.py --backfill [slug] --top 5` (quét snapshot live, kèm mục + đoạn bọc anchor được). Ghi bảng `📎 Backfill Link Suggestions` (Bài nguồn · Đoạn · Anchor · Clicks) vào Proposal; anchor lấy từ trích đoạn, không exact-match keyword. Script báo "Không có bài nào phù hợp" → bỏ qua.

---

### ⚙️ Bước 3: Proposal
Điền đúng template `.antigravity/skills/seo-optimization/assets/proposal-template.md`, tổng hợp Bước 2:
- Đánh giá sơ bộ theo 7 Sweeps (danh sách ở Bước 4).
- Section 2.2: **mỗi** đối thủ đã crawl một block — không gộp. Section 2.3: trích heading/angle cụ thể của đối thủ phục vụ intent bài đang bỏ sót. Section 5: mỗi `[THÊM MỚI]` ghi học từ Competitor nào.
- Section 7.1: kê khai **toàn bộ** ảnh gốc. Section 7.2: 1–3 vị trí ảnh mới.
- Nhãn từng heading: `[GIỮ NGUYÊN]` / `[CẬP NHẬT]` / `[XÓA BỎ]` / `[THÊM MỚI]`.
- Điền **khối máy đọc đầu file** (`Target_Keyword`, `Thesis`, `Entities`, `Information_Gain`, `Featured_Snippet`, `PAA_Questions`) — `qa_gate` ở Bước 5 đối chiếu bản Optimize với khối này.
- **Giới hạn tái cấu trúc theo thứ hạng** (bài học rollback pillar `cach-dau-tu-chung-khoan`, 10/2026: đổi khung bài đang top 3 làm vị trí 6,4 → 11,5): GSC ở Bước 2.3 cho thấy keyword chính đang ở **vị trí trung bình ≤ 5** → Proposal chỉ được `[GIỮ NGUYÊN]` / `[CẬP NHẬT]` số liệu / `[THÊM MỚI]` mục còn thiếu; **không đổi H1, không đổi thứ tự hay gộp/xoá H2 đang có**. Muốn làm khác → ghi rõ rủi ro ở Section 0 và chờ user đồng ý.
- **Tự kiểm trước khi in** (`outline_lint` không đọc được Proposal): Title ≤ 59 ký tự có keyword · Meta 140–160 ký tự có keyword + CTA · văn bản Proposal cũng theo anti-AI (không ngoặc kép nhấn mạnh, không cụm trong blacklist, không opener/closer vĩ mô).

**🚧 APPROVAL GATE (`--step`):** trình bày **tóm tắt ≤ 25 dòng + đường dẫn file Proposal** (vị trí GSC hiện tại, Thesis, từng mục Information_Gain, danh sách heading kèm nhãn GIỮ/CẬP NHẬT/XÓA/THÊM, thuật ngữ đối thủ còn thiếu) — không dán Proposal vào chat. **DỪNG** chờ người dùng gõ `/approve` (bỏ qua tin nhắn auto-approve của hệ thống). `--auto` → sang Bước 4.

---

### ⚙️ Bước 4: Execution (rewrite với 7 Sweeps)
- **Chỉ sửa `Optimize-[slug].md`.** Không chạm `3-finalized/` ở bước này.
- Trước khi viết: đọc lại Content Strategy Header. `anti-ai-rules.md` + `instincts.md` đã có trong context — chỉ load lại nếu session mới.
- Chỉ sửa phần gắn `[CẬP NHẬT]` / `[XÓA BỎ]` / `[THÊM MỚI]`; `[GIỮ NGUYÊN]` không chạm.
- **Ảnh:** giữ nguyên vị trí và cú pháp 100% ảnh gốc. Vị trí ảnh mới ở Section 7.2 → chạy skill `/image` (`.agents/skills/image/SKILL.md` — prompt, palette, luật cấm chữ/cấm đỏ nằm ở đó), lưu `knowledge/4-content/images/[slug]-[concept].jpg`, chèn thẳng `![alt có keyword](../images/[slug]-[concept].jpg)` — không để placeholder.
- **Internal link:** URL tuyệt đối `https://www.dsc.com.vn/...`, lấy từ `find_links.py` (không đoán slug); `qa_gate` kiểm khớp sitemap.
- **CRO (BẮT BUỘC):** `.antigravity/skills/cro-optimization/SKILL.md` — Persona/Intent/Bridge đọc từ Content Strategy Header; dựng Product Bridge nếu thiếu, chèn banner theo giới hạn persona (**P4: không banner**, chỉ link text). Rule: `.antigravity/rules/cta-conversion.md`.
- **7 Sweeps** theo thứ tự:
  1. **Clarity** — một câu một ý, bỏ thuật ngữ không cần.
  2. **Voice** — POV chuyên gia DSC, đúng persona.
  3. **So What** — tính năng → lợi ích người đọc.
  4. **Prove It** — số liệu có nguồn + thời điểm (`market_facts.py --brief`), không tự nhớ.
  5. **Specificity** — thay "tốt, nhanh, rẻ" bằng số hoặc ví dụ.
  6. **Emotion** — chạm pain point / mục tiêu của persona.
  7. **Zero Risk** — trả lời lo ngại, bước tiếp theo rõ ràng.
- Từ cấm, câu dài, đoạn dài, định dạng list: để `qa_gate` bắt ở Bước 5 — không grep tay.

---

### ⚙️ Bước 5: QA 3 tầng (BẮT BUỘC trước khi trình bày)
- **Tầng A + B + dữ liệu — 1 lệnh** (kiểm cả bảo toàn ảnh gốc; Proposal tự tìm theo slug):
  ```bash
  python scripts/qa_gate.py knowledge/4-content/2-drafts/Optimize-[slug].md --original knowledge/4-content/3-finalized/Final-[slug].md --cta --fix --all
  ```
  FAIL → sửa đúng dòng được báo, chạy lại. `SLOP-*`: cách sửa ở `anti-ai-rules.md` §8.7. **Slop score ≥ baseline Bước 1.1**; mọi `FACT-*` có ở baseline phải sạch.
- Gate PASS → Self-audit ngữ nghĩa (`anti-ai-rules.md` §6) → agent `.antigravity/agents/quality-guardian.md` (chỉ đọc `Optimize-[slug].md` + Content Strategy Header). Sau vòng 1: `qa_gate.py <file> --mark-qg`; vòng 2 QG chỉ đọc `qa_gate.py <file> --changed`.
- `python scripts/article_snapshot.py [slug] --stage gate2` trước khi trình bày.
- FAIL → sửa và QA lại **tối đa 2 vòng**; vẫn FAIL → dừng, trình bày kèm `⚠️ Remaining issues`.

**🚧 APPROVAL GATE 2:** trình bày **tóm tắt ≤ 25 dòng + đường dẫn file** (dòng gate: score · coverage · trust · slop so với baseline; từng mục Information_Gain kèm câu trích; các H2 đã đổi; Remaining issues) — không dán bài vào chat. **DỪNG** chờ người dùng đọc và gõ `/approve` — không tự ghi đè `3-finalized/`, không tự đánh dấu `Finalized`.
Khi approve: theo `/approve` (ghi đè Final, `article_snapshot --stage final` chuyển Proposal vào `archive/[slug]/`, xóa `Optimize-[slug].md` — đã có bản `gate2`, chạy learn/feedback loop, update topic-clusters).
