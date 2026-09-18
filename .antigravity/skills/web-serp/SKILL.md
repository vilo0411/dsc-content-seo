---
name: Web SERP
description: >
  SERP lookup via DataForSEO (Google, Vietnam, vi) + competitor content extraction (local Scrapling parser → Jina AI Reader),
  gộp trong 1 script có cache. Fallback: DataForSEO → DuckDuckGo HTML → Manual paste; extraction: local parser → Jina (cả 2 trong script) → Firecrawl script → Manual paste.
---

# Skill: Web SERP (Fast Research Layer)

Skill này thay thế toàn bộ browser-based browsing trong các bước SERP research và competitor extraction.

- **SERP Discovery:** DataForSEO `serp/google/organic/live/advanced` — Google thật, `location_code=2704` (Vietnam), `language_code=vi`. Trả về organic + People Also Ask + Featured Snippet + Related Searches trong **1 call**.
- **Content Extraction:** 2 tầng ngay trong script, song song (ThreadPool 5):
  1. **Local** — `urllib` + Scrapling parser + markdownify (~1s/trang, không API, không rate-limit). Chọn container nhiều chữ nhất trong `article`/`main`/`.post-content`…, bỏ nav/header/footer/aside, xuất markdown ATX.
  2. **Jina AI Reader** (`r.jina.ai`, miễn phí, ~8s/trang) — chỉ khi local trả về < 300 từ (trang render bằng JS như vcbs.com.vn, hdbank.com.vn).
  Cần `pip install scrapling markdownify` (**parser only** — không cài `scrapling[fetchers]`, xem Lưu ý AV bên dưới). Thiếu package → script tự bỏ qua tầng local, dùng Jina như cũ. Cache ghi `source: local|jina` cho từng competitor.
- **Cache:** `knowledge/raw/serp/<slug>.json`, 30 ngày. Có cache → **0 API call**.

---

## 💰 Nguyên tắc chi phí (BẮT BUỘC)

DataForSEO **có phí** (~$0.002 / keyword). Để tiết kiệm:

1. **1 keyword = 1 call.** Script luôn kiểm tra cache trước; chỉ gọi API khi chưa có cache hoặc cache > 30 ngày.
2. **Không dùng `--no-cache`** trừ khi user yêu cầu refresh rõ ràng.
3. **Không gọi lại** cho biến thể keyword gần giống (ví dụ "ROA là gì" vs "chỉ số ROA là gì") — dùng cache của keyword chính.
4. Chỉ `--extract` đúng số URL cần (mặc định 5, tối đa 7). Local parser nhanh, Jina chậm; kết quả extract cũng được cache.

> **⚠️ Lưu ý AV (máy công ty):** chỉ cài `pip install scrapling markdownify`. **Không** cài `scrapling[fetchers]` / `scrapling install` — gói `curl-cffi` (giả TLS fingerprint) và `patchright` đã khiến Kaspersky Endpoint xóa `python.exe` (18/09/2026). Khôi phục bằng `py install --force 3.14` rồi cài lại `pillow scrapling markdownify`.
5. Script không retry khi lỗi — đọc message, sửa nguyên nhân rồi chạy lại.
6. Dòng `Cost: $...` cuối output là chi phí thực của lần chạy — báo lại user nếu > $0.01.

---

## ⚙️ Cách hoạt động

```
python serp_research.py "<keyword>" --top 10 --extract 5
   ├─ cache hit  → in kết quả ngay ([cache], $0)
   └─ cache miss → DataForSEO 1 call → lưu cache
        ↓ (fail) → DuckDuckGo HTML (WebFetch)
        ↓ (fail) → Manual Paste
   └─ --extract N → local parser × N song song (ThreadPool 5) → block Competitor
        ↓ (< 300 từ / lỗi HTTP / thiếu scrapling) → r.jina.ai cho URL đó
        ↓ (URL lỗi / rỗng) → ghi "Lỗi: Không extract được", không retry
        ↓ (nhiều URL fail) → scrape.py (Firecrawl) cho các URL đó
        ↓ (vẫn fail) → Manual Paste từng URL
```

---

## 🔍 Function 1 + 2: `serp_research.py` (lệnh mặc định — luôn dùng cái này)

```bash
python .antigravity/skills/web-serp/scripts/serp_research.py "{keyword}" --top 10 --extract 5
```

| Flag | Mặc định | Ý nghĩa |
|---|---|---|
| `--top N` | 10 | Số organic hiển thị (tối đa 10 — script luôn fetch depth 10) |
| `--extract N` | 0 | Extract nội dung N URL đầu tiên **theo thứ tự rank** (local parser, Jina fallback). Env `LOCAL_FETCH=0` để ép dùng Jina |
| `--content` | — | In **toàn văn** markdown đã lọc của các competitor đã extract (đọc kỹ 1 bài, không dùng làm input Outline) |
| `--json` | — | Output JSON (dùng khi cần parse tự động) |
| `--no-cache` | — | Bỏ qua cache, gọi API lại (**tốn tiền** — chỉ khi user yêu cầu) |
| `--raw` | — | Dump payload gốc DataForSEO (debug, cũng tốn 1 call) |

**Output (text):**
1. `### SERP Results` — top URLs: rank / title / URL / description (đã lọc google, facebook, youtube, tiktok, mạng xã hội)
2. `### Featured Snippet` — nếu Google đang hiện (domain + đoạn text) → quyết định Featured Snippet target
3. `### People Also Ask` — dùng trực tiếp làm gợi ý FAQ section
4. `### Related Searches` — gợi ý secondary keywords / H2
5. `### Competitor N: {domain}` × N (khi `--extract`):
   - `Tổng`: số từ, số section, số internal/external link
   - `Outline`: từng H1–H4 (kể cả `[Intro]`) kèm **số từ của section** và **câu chủ đề** → biết đối thủ đào sâu chỗ nào
   - `Entities`: tên riêng / acronym / ticker xuất hiện nhiều (ROE×12, Forbes, VN-Index...) → phủ entity khi viết
   - `Data points`: tối đa 8 câu có số liệu
   - `Internal links (anchor → URL)`: cách đối thủ link nội bộ → gợi ý cluster/anchor cho bài mình
   - `External links`: domain nguồn tham khảo
   - `Special elements`, dòng `Gap so với bài mình: [điền]`
6. Khung trống `## Competitor Gap Synthesis` — agent **phải điền** trước khi sang Outline
7. `Cost: $x.xxxx`

**Cấu hình (1 lần):** thêm vào `.antigravity/config/api-keys.md` (đã gitignore):
```
DATAFORSEO_LOGIN=...
DATAFORSEO_PASSWORD=...
```
Lấy tại https://app.dataforseo.com/api-access. Xem `.antigravity/config/api-keys.example.md`.

**Lỗi thường gặp:**

| Message | Xử lý |
|---|---|
| `Missing config: DATAFORSEO_...` | Chưa điền `api-keys.md` |
| `DataForSEO HTTP 401` | Sai login/password API (password API ≠ password web) |
| `DataForSEO task error 40201/40202` | Hết tiền / quá rate limit → báo user nạp tiền, không chạy lại |
| Script lỗi mạng | Fallback DuckDuckGo: `WebFetch https://html.duckduckgo.com/html/?q={keyword_url_encoded}`, parse `<a class="result__a">` |
| Cả hai fail | Xuất **Manual Paste Template** (cuối file) |

---

**Đọc toàn văn 1 bài đối thủ** (khi cần hiểu cách họ triển khai, không chỉ heading):
```bash
python .antigravity/skills/web-serp/scripts/serp_research.py "{keyword}" --extract 3 --content
```
Nội dung đã cache cùng SERP → $0, in ngay. Chỉ dùng khi thật cần vì tốn context (~1.500–2.000 từ/bài).

---

## 📄 Extraction thủ công (chỉ khi `--extract` không lấy được URL nào đó)

```
WebFetch: https://r.jina.ai/{competitor_url}
```

Jina trả về toàn bộ trang dạng markdown kể cả header/footer/nav. Quy tắc lọc (script đã tự làm; làm tay khi fallback):

| Vùng cần loại bỏ | Dấu hiệu |
|---|---|
| Header / Nav | Cụm links ngắn liên tiếp ở đầu file (`[Trang chủ]`, `[Danh mục]`, `[Đăng nhập]`...) |
| Footer | Cụm links ngắn liên tiếp ở cuối file (`[Chính sách]`, `[Liên hệ]`, `[Facebook]`...) |
| Sidebar / Related | Block `## Bài viết liên quan`, `## Xem thêm`, `## Tags:` |
| Breadcrumb | Dòng dạng `Home > Danh mục > Bài viết` |
| Author / Meta block | Dòng ngắn chứa ngày đăng, tên tác giả đứng độc lập |

- Bắt đầu từ **H1 đầu tiên**, kết thúc ở section cuối có nội dung thật (đoạn > 2 câu) trước footer. Giữ tối đa 2.000 từ đầu.
- Extract: Headings (`#`–`####`), Data points (số, %, bảng `|`, ngày cụ thể), Intent từng section, Special elements (`calculator`, `FAQ`, `bảng so sánh`).

Fallback tiếp theo khi Jina 429 / rỗng nhiều URL: `python .antigravity/skills/web-serp/scripts/scrape.py <url1> <url2> ...` (Firecrawl, cần `FIRECRAWL_API_KEY`, `pip install firecrawl-py`). Output cùng format.

---

## 📋 Output Format (Chuẩn cho mọi caller)

Đây chính là format script in ra; khi làm tay phải theo đúng format này:

```
### SERP Results: {keyword}
Organic hợp lệ: {N}

---

### Competitor 1: {domain}
- URL: {full url}
- Tổng: ~1342 từ | 6 sections | 7 internal links | 0 external links
- Outline (số từ / section — câu chủ đề):
  - [Intro] (67 từ) — ...
  - H2: 1. ROA là gì? (143 từ) — ROA là viết tắt của...
  - H2: 3. Công thức ROA (277 từ) — ...
    - H3: ... (120 từ) — ...
- Entities: ROA×26, ROE×8, Việt Nam×2, WACC
- Data points:
  - Theo Forbes, ROA trên 5% được coi là tốt...
- Internal links (anchor → URL):
  - "Chỉ số ROE" → https://.../chi-so-roe
- External links: forbes.com
- Special elements: So sánh, List
- Gap so với bài mình: [họ có gì, mình chưa có]

### Competitor 2: ...
```

Agent chỉ cần điền `Gap so với bài mình` và (tuỳ chọn) ghi `→ [intent]` cạnh H2 nếu câu chủ đề chưa đủ rõ.

---

## 📊 Competitor Gap Synthesis (BẮT BUỘC sau khi extract xong tất cả competitors)

Điền khung script đã in:

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
- Lý do: [dựa vào block Featured Snippet hiện tại + dạng query]
```

Block này là input trực tiếp cho Outline generation — giúp tránh lặp lại những gì competitors đã làm. Dùng `People Also Ask` cho FAQ và `Related Searches` cho secondary keywords.

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

Sau khi user paste URLs → extract thủ công qua Jina như trên.

---

## 🔗 Used By

- `.antigravity/agents/seo-collector.md` — Step 1 SERP research
- `.antigravity/skills/seo-outlining/SKILL.md` — Step 1 Plan
- `.agents/skills/optimize/SKILL.md` — Bước 2.1 SERP Lookup
