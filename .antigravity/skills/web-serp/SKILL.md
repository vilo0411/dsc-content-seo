---
name: Web SERP
description: >
  SERP lookup via DuckDuckGo HTML + competitor content extraction via Jina AI Reader.
  Fallback chain: DuckDuckGo HTML → Jina AI → Firecrawl script → Manual paste.
---

# Skill: Web SERP (Fast Research Layer)

Skill này thay thế toàn bộ browser-based browsing trong các bước SERP research và competitor extraction.

- **SERP Discovery:** DuckDuckGo HTML search — không cần API key
- **Content Extraction:** Jina AI Reader (`r.jina.ai`) — clean markdown, miễn phí, không cần API key
- **Extraction Fallback:** Firecrawl script — xử lý được JavaScript, Cloudflare

---

## ⚙️ Cách hoạt động

```
Bước 1: DuckDuckGo HTML → top URLs
              ↓ (fail) → Manual Paste

Bước 2: r.jina.ai/{url} × N → content extraction song song
              ↓ (429 / rỗng) → scrape.py (Firecrawl) × N
              ↓ (vẫn fail) → Manual Paste từng URL
```

---

## 🔍 Function 1: SERP Lookup (DuckDuckGo)

**Mục đích:** Lấy top URLs từ search cho một keyword.

**Cách gọi:**
```
WebFetch: https://html.duckduckgo.com/html/?q={keyword_url_encoded}
```

**Ví dụ:**
```
Keyword: lãi suất tiết kiệm ACB 2025
URL: https://html.duckduckgo.com/html/?q=l%C3%A3i+su%E1%BA%A5t+ti%E1%BA%BFt+ki%E1%BB%87m+ACB+2025
```

**Parse HTML output — lấy top URLs:**
- Tìm các thẻ `<a class="result__url">` hoặc `<a class="result__a">` → lấy href
- Lọc và decode redirect URLs nếu cần

**Lọc URLs:**
- Bỏ: `google.com`, `facebook.com`, `youtube.com`, `tiktok.com`, ads redirect
- Ưu tiên: domain `.vn`, báo lớn (vnexpress, cafef, tinnhanhchungkhoan, vneconomy, vietstock)
- Lấy top 5–7 URLs hợp lệ để extract

**Fallback nếu DuckDuckGo thất bại:**

| Tình huống | Fallback |
|---|---|
| DuckDuckGo không trả về kết quả | Xuất **Manual Paste Template** (xem cuối file), yêu cầu user paste SERP |

---

## 📄 Function 2: Content Extraction

**Mục đích:** Trích xuất heading structure và data points từ một competitor URL.

**Cách gọi:**
```
WebFetch: https://r.jina.ai/{competitor_url}
```

**Ví dụ:**
```
WebFetch: https://r.jina.ai/https://cafef.vn/bai-viet-ve-lai-suat.html
```

**Bước 1 — Xác định vùng nội dung chính (bắt buộc trước khi extract):**

Jina trả về toàn bộ trang dưới dạng markdown, bao gồm cả header/footer/nav. Phải loại bỏ các vùng sau trước khi parse:

| Vùng cần loại bỏ | Dấu hiệu nhận biết trong markdown |
|---|---|
| Header / Nav | Cụm links ngắn liên tiếp ở đầu file (`[Trang chủ]`, `[Danh mục]`, `[Đăng nhập]`...) |
| Footer | Cụm links ngắn liên tiếp ở cuối file (`[Chính sách]`, `[Liên hệ]`, `[Facebook]`...) |
| Sidebar / Related | Block `## Bài viết liên quan`, `## Xem thêm`, `## Tags:` |
| Breadcrumb | Dòng dạng `Home > Danh mục > Bài viết` |
| Author / Meta block | Dòng ngắn chứa ngày đăng, tên tác giả đứng độc lập |

**Quy tắc xác định vùng nội dung chính:**
- Tìm **H1 đầu tiên** (`# ...`) → đây là điểm bắt đầu của bài viết
- Tìm điểm kết thúc: section cuối cùng có nội dung thực sự (đoạn văn > 2 câu), trước khi xuất hiện cụm links footer
- Chỉ extract trong vùng H1-đầu → cuối-nội-dung, bỏ phần còn lại

**Bước 2 — Extract từ vùng nội dung chính:**
- **Headings**: Dòng bắt đầu bằng `#`, `##`, `###`, `####` → H1–H4
- **Data points**: Số liệu, %, bảng (dòng bắt đầu `|`), ngày tháng cụ thể
- **Intent**: Đoạn đầu của mỗi section — trả lời câu hỏi gì của reader?
- **Special elements**: Tìm từ khóa `calculator`, `FAQ`, `bảng so sánh`, `câu hỏi`

---

## ⚡ Parallel Execution (BẮT BUỘC)

Sau khi có danh sách URLs từ Function 1, **gọi tất cả Function 2 song song** trong một lượt WebFetch — không gọi tuần tự.

```
# Đúng — song song
Gọi đồng thời: r.jina.ai/URL1, r.jina.ai/URL2, r.jina.ai/URL3, r.jina.ai/URL4, r.jina.ai/URL5

# Sai — tuần tự (chậm)
Gọi URL1 → đợi → gọi URL2 → đợi → ...
```

Thời gian ước tính: ~5–10s cho cả 5 URLs song song (so với 2–3 phút browser tuần tự).

---

## ⚠️ Fallback & Error Handling

| Tình huống | Xử lý |
|---|---|
| Jina trả về 429 (rate limit) | Đợi 5s, retry một lần. Nếu vẫn lỗi → chuyển sang **Script Fallback** |
| Jina trả về nội dung rỗng / < 200 ký tự | Chuyển sang **Script Fallback** cho URL đó |
| DuckDuckGo không có URL .vn | Dùng kết quả .com hoặc báo user thiếu SERP data |
| Heading structure không parse được | Extract toàn bộ text, để Main Agent tự identify sections |

---

## 🛠️ Script Fallback: Firecrawl (khi Jina quá tải)

**File:** `.antigravity/skills/web-serp/scripts/scrape.py`

**Yêu cầu (cài 1 lần):**
```bash
pip install firecrawl-py
```

Thêm API key vào `.antigravity/config/api-keys.md`:
```
FIRECRAWL_API_KEY=fc-your_key_here
```
Lấy key tại: https://firecrawl.dev (có free tier)

**Cách dùng:**

```bash
# Scrape nhiều URLs cùng lúc (chạy song song)
python .antigravity/skills/web-serp/scripts/scrape.py \
  https://cafef.vn/bai-1.html \
  https://vnexpress.net/bai-2.html \
  https://vietstock.vn/bai-3.html

# Hoặc từ file (mỗi dòng 1 URL)
python .antigravity/skills/web-serp/scripts/scrape.py --file urls.txt
```

**Output:** Cùng format với Jina extraction — paste thẳng vào Outline generation, không cần chỉnh.

**Ưu điểm so với Jina:** Xử lý được JavaScript, Cloudflare, và hầu hết bot protection.

---

## 📋 Output Format (Chuẩn cho mọi caller)

Sau khi chạy xong cả 2 functions, output theo format sau trước khi chuyển sang Outline generation:

```
### SERP Results: {keyword}
Top URLs tìm được: {N} URLs hợp lệ

---

### Competitor 1: {domain}
- URL: {full url}
- Headings:
  - H1: ...
  - H2: ... → [intent]
  - H2: ... → [intent]
    - H3: ...
- Data points: [số liệu / bảng / ngày cụ thể]
- Special elements: [FAQ / calculator / bảng so sánh]
- Gap so với bài mình: [họ có gì, mình chưa có]

### Competitor 2: ...
```

---

## 📊 Competitor Gap Synthesis (BẮT BUỘC sau khi extract xong tất cả competitors)

Sau khi có đủ output từ tất cả competitors, tổng hợp thành 1 block trước khi chuyển sang Outline generation:

```
## Competitor Gap Synthesis: {keyword}

### Gaps — tất cả/hầu hết competitors đều bỏ qua:
1. [gap cụ thể] — ví dụ: "Không ai giải thích cách đọc tín hiệu false breakout"
2. [gap cụ thể]
3. [gap cụ thể nếu có]

### Unique angles DSC có thể khai thác:
- [angle 1 — liên kết với DSC product/service]
- [angle 2]

### Content format gaps:
- [ví dụ: "Không ai có bảng so sánh", "Không ai có FAQ schema", "Không ai có ví dụ với mã VN cụ thể"]

### Recommended Featured Snippet target:
- Dạng: [Paragraph | List | Table | None]
- Lý do: [vì top 1-3 hiện tại không có / vì query dạng how-to / vì có bảng so sánh rõ]
```

Block này là input trực tiếp cho Outline generation — giúp tránh lặp lại những gì competitors đã làm.

---

## 📋 Manual Paste Template (Fallback cuối cùng)

Khi DuckDuckGo thất bại, xuất template này và yêu cầu user paste:

```
─────────────────────────────────────────
[YÊU CẦU] Không lấy được SERP tự động.

Vui lòng:
1. Search Google: "{keyword}"
2. Copy 5 URLs top kết quả (bỏ qua ads)
3. Paste vào đây theo format:

URL1: https://...
URL2: https://...
URL3: https://...
URL4: https://...
URL5: https://...
─────────────────────────────────────────
```

Sau khi user paste URLs → tiếp tục Function 2 bình thường.

---

## 🔗 Used By

- `.antigravity/agents/seo-collector.md` — Step 1 SERP research
- `.antigravity/skills/seo-outlining/SKILL.md` — Step 1 Plan
- `.antigravity/skills/seo-optimization/SKILL.md` — Phase 1 Audit (khi cần SERP freshness check)
