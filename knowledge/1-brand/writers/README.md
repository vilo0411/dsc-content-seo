# Writer Profiles — Giọng Viết theo Loại Bài

3 profiles giọng viết, phân loại theo **loại bài** (không phải theo persona người đọc).  
Agent đọc file này khi drafting để biết cần viết theo style nào.

> **Quy tắc ưu tiên:** `anti-ai-rules.md` + `glossary.md` > writer profiles. Khi có xung đột, tuân theo rules — không theo giọng của profile.

## Chọn profile theo loại bài

| Profile | File | Loại bài | Persona chính |
|---|---|---|---|
| `educational` | `educational.md` | "X là gì", khái niệm cơ bản, how-to | P2 (F0 — Nhà đầu tư mới) |
| `analytical` | `analytical.md` | Phân tích kỹ thuật, chỉ báo, báo cáo tài chính | P3 (Active Trader) |
| `comparison` | `comparison.md` | So sánh lãi suất, so sánh sàn, so sánh sản phẩm | P1 (Người tiết kiệm thận trọng) |

## Cách khai báo trong Outline

Trong YAML header của outline, thêm:
```yaml
Writer_Profile: educational | analytical | comparison
```

## Khi nào dùng profile nào

- **"ADX là gì"** → `analytical` (P3, giả định người đọc đã biết trading cơ bản)
- **"Lãi suất tiết kiệm ACB"** → `comparison` (P1, cần số liệu rõ ràng, bảng so sánh)
- **"Chứng khoán là gì"** → `educational` (P2, giải thích từ đầu, không dùng jargon)
- **"Báo cáo lưu chuyển tiền tệ"** → `analytical` hoặc `educational` tùy search intent
