# API Keys — Template

> Copy file này thành `api-keys.md` (cùng thư mục) và điền key thật vào.
> `api-keys.md` đã được thêm vào `.gitignore` — không bao giờ commit file đó.

---

## Firecrawl

Dùng cho script fallback khi Jina AI quá tải. Xử lý được JavaScript và Cloudflare.

Lấy key tại https://firecrawl.dev (free tier: 500 credits/tháng).

```
FIRECRAWL_API_KEY=fc-your_key_here
```

---

## Jina AI

Không cần API key — miễn phí, gọi trực tiếp `https://r.jina.ai/{url}`.

Nếu cần tăng rate limit, đăng ký tại https://jina.ai để lấy Bearer token:
```
JINA_API_KEY=jina_your_token_here
```
