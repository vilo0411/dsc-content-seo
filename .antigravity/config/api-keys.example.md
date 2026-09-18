# API Keys — Template

> Copy file này thành `api-keys.md` (cùng thư mục) và điền key thật vào.
> `api-keys.md` đã được thêm vào `.gitignore` — không bao giờ commit file đó.

---

## DataForSEO (bắt buộc cho SERP research)

Dùng cho `.antigravity/skills/web-serp/scripts/serp_research.py` — lấy top 10 Google (Vietnam, tiếng Việt),
People Also Ask, Featured Snippet, Related Searches.

**Có phí** (~$0.002/keyword với live/advanced). Script cache kết quả 30 ngày tại `knowledge/raw/serp/` — 1 keyword = 1 call.

Lấy login/password tại https://app.dataforseo.com/api-access (password API ≠ password đăng nhập web).

```
DATAFORSEO_LOGIN=you@example.com
DATAFORSEO_PASSWORD=your_api_password
```

---

## Firecrawl

Dùng cho script fallback `scrape.py` khi cả local parser lẫn Jina AI đều fail. Xử lý được JavaScript và Cloudflare.

Lấy key tại https://firecrawl.dev (free tier: 500 credits/tháng).

```
FIRECRAWL_API_KEY=fc-your_key_here
```

---

## Jina AI

Không cần API key — miễn phí, gọi trực tiếp `https://r.jina.ai/{url}`.
Từ 09/2026 `serp_research.py` chỉ gọi Jina khi tầng local (Scrapling parser) lấy được < 300 từ — thường là trang render JS.

Nếu cần tăng rate limit, đăng ký tại https://jina.ai để lấy Bearer token:
```
JINA_API_KEY=jina_your_token_here
```

---

## Google Search Console API

Dùng cho `/gsc-sync` workflow — fetch data clicks, impressions, CTR, position trực tiếp từ GSC.

**Không dùng API key thông thường — dùng OAuth2 credentials (file JSON).**

Xem hướng dẫn đầy đủ tại `.antigravity/config/gsc-config.md`.

Files cần có (gitignored — không commit):
```
.antigravity/config/gsc-credentials.json   ← OAuth client ID/secret (tải từ Google Cloud Console)
.antigravity/config/gsc-token.json         ← Auto-generated sau lần authorize đầu tiên
```

Biến môi trường tùy chọn:
```
GSC_SITE=https://www.dsc.com.vn/           ← Site property trong GSC (mặc định nếu không set)
```

Dependencies:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```
