---
name: Web SERP
description: >
  Fast, browser-free SERP lookup and competitor content extraction using Jina AI Reader.
  Replaces slow browser navigation with parallel WebFetch calls.
---

# Skill: Web SERP (Fast Research Layer)

Skill này thay thế toàn bộ browser-based browsing trong các bước SERP research và competitor extraction. Dùng Jina AI Reader — miễn phí, không cần API key, trả về clean markdown.

---

## ⚙️ Cách hoạt động

Jina AI Reader nhận bất kỳ URL nào và trả về nội dung dưới dạng clean markdown, đã strip quảng cáo, nav, footer. Claude Code gọi trực tiếp qua WebFetch.

```
Base URL: https://r.jina.ai/{target_url}
```

---

## 🔍 Function 1: SERP Lookup

**Mục đích:** Lấy danh sách top URLs từ Bing search results cho một keyword.

**Cách gọi:**
```
WebFetch: https://r.jina.ai/https://www.bing.com/search?q={keyword_url_encoded}
```

**Ví dụ:**
```
Keyword: lãi suất tiết kiệm ACB 2025
URL: https://r.jina.ai/https://www.bing.com/search?q=l%C3%A3i+su%E1%BA%A5t+ti%E1%BA%BFt+ki%E1%BB%87m+ACB+2025
```

**Parse output — lấy top 5–10 URLs:**
- Tìm các dòng dạng `[title](https://...)` trong markdown output
- Lọc bỏ: `bing.com`, `microsoft.com`, `facebook.com`, `youtube.com`, các URL ads
- Ưu tiên: domain `.vn`, domain báo lớn (vnexpress, cafef, tinnhanhchungkhoan, vneconomy)
- Validate: bỏ qua URL không có domain rõ ràng hoặc dạng redirect lạ

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
| Jina trả về 429 (rate limit) | Đợi 5s, retry một lần. Nếu vẫn lỗi → bỏ qua URL đó |
| Jina trả về nội dung rỗng / < 200 ký tự | Bỏ qua URL, ghi chú "extraction failed" |
| Bing SERP không có URL .vn | Dùng kết quả .com hoặc báo user thiếu SERP data |
| Heading structure không parse được | Extract toàn bộ text, để Main Agent tự identify sections |

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

## 🔗 Used By

- `.antigravity/agents/seo-collector.md` — Step 1 SERP research
- `.antigravity/skills/seo-outlining/SKILL.md` — Step 1 Plan
- `.antigravity/skills/seo-optimization/SKILL.md` — Phase 1 Audit (khi cần SERP freshness check)
