# Creative engine — ảnh quảng cáo / post social

> **Chuẩn hình ảnh: `knowledge/1-brand/DESIGN.md` v1.0** (brand guideline chính thức: Gunmetal / Pine Teal / Lime / Emerald / Frosted Mint, 3 gradient, font duy nhất Plus Jakarta Sans, ảnh trừu tượng xanh). Engine đọc màu/font từ `brand.json` — không đặt hex/font tay trong design.json. Theme mùa vụ `emerald`/`ivory` chỉ khi brief ghi Tết/lễ (§7). Ảnh blog: `image-design-system.md` (cùng palette).

## 0. Luồng key visual (mặc định cho quảng cáo / ảnh bìa / post chính)
```
copy đã lint → init → chỉnh design.json: layout kv-right|kv-left|kv-center, theme dark|pine (mùa vụ: emerald|ivory), type sans|(trống),
  slot badge / script / headline / sub, mục "kv": {subject, motifs, mood}
→ creative.py pick <design.json>                 → chọn nền trong thư viện asset (0 quota) — knowledge/1-brand/assets/library/README.md
     + "layers": motif tách nền (dải lụa/kính xanh, vệt sáng; mùa vụ: hạc, mai…) đặt chồng lên nền
→ (chỉ ảnh chưa có nền) creative.py generate <design.json> --dry-run   → kiểm prompt (không TODO, có luật cấm chữ/logo, chừa khoảng trống, không tiếng Việt có dấu)
→ creative.py generate <design.json> [--only id] → gọi Codex CLI (`codex exec -s read-only`, tài khoản ChatGPT đã đăng nhập,
     không cần API key) → ảnh gốc assets/<id>.raw.png → cắt đúng khổ assets/<id>.png; log ở generate-log.jsonl
     Mỗi ảnh tạo 1 lần (tốn quota Codex, ~1 phút/ảnh); muốn tạo lại phải --force. Không có Codex → `creative.py prompt` ra prompts.md để dán tay.
→ creative.py render <design.json>     → tự gắn assets/<id>.png, đo tương phản trên nền ảnh thật (CONTRAST-photo)
→ duyệt như dưới. Ảnh quan trọng (KV campaign lớn) → đặt designer (DESIGN.md §7)
```
Chưa có ảnh → render vẫn chạy (khung sọc "KV chưa có") và báo `KV-missing`.

Học từ tabcom-designer-plugin (Annie-246): tạo ảnh qua Codex CLI; kiểm prompt trước khi tạo; mỗi ảnh tạo 1 lần; **không đính kèm ảnh mẫu** cho model (nó sẽ chép gần y hệt) — ảnh mẫu chỉ được phân tích thành chữ trong DESIGN.md; logo luôn dán bằng code. Khác tabcom: chữ tiếng Việt **không** để model vẽ (dễ sai dấu, không khoá được theo copy đã duyệt) — engine đặt chữ HTML lên ảnh.

> Dùng chung cho Ads, Social, Campaign. Engine: `scripts/creative.py` (HTML → PNG bằng Chromium qua Playwright). Skill: `/creative`.
> Học từ design-agent-plugin (runbylinh): design.json là nguồn duy nhất, chữ là chữ HTML thật, QA máy + QA mắt, duyệt theo version, đo hiệu quả theo mẫu.

## 1. Luồng
```
copy đã lint (ads/copy-vN.md, social/<kênh>-…-vN.md)
  → creative.py init <copy>            → <kênh>/creatives/design.json   (1 mục / ảnh, chữ lấy từ `chữ trên ảnh: "…"`)
  → agent chỉnh design.json            (layout, theme, sub/cta/note, **nhấn**, slide carousel)
  → creative.py render <design.json>   → v<N>/<id>.png · html/ · qa.json · preview.html
  → QA máy (exit 1 nếu lỗi) + creative-qa nhìn ảnh  → tối đa 2 vòng sửa
  → GATE: user duyệt
  → creative.py approve … --xac-nhan "<lời user>"  → <job>/approved/<JOB>-<id>-v<N>.png
  → sửa sau duyệt: render --bump (ra v<N+1>, không đè bản đã duyệt)
```

## 2. design.json
```json
{"job": "CMP-…", "source": "copy-v1.md", "channel": "ads", "version": 1, "approved": [],
 "creatives": [
   {"id": "ads-v1", "layout": "thesis", "theme": "dark", "size": "1080x1350",
    "text": {"headline": "Mở tài khoản **3 phút**, ngay trên điện thoại", "sub": "", "cta": "", "note": ""},
    "image": null},
   {"id": "facebook-v2-02", "group": "facebook-v2", "layout": "rows", "size": "1080x1080",
    "text": {"headline": "1. Phí giao dịch", "items": ["…", "…"]}}
 ]}
```
- `**…**` trong headline = cụm nhấn (gradient trên nền tối, vạch highlight trên nền sáng).
- `image`: `{"src": "<đường dẫn>", "focus": "x% y%"}` — ảnh minh hoạ **không chữ**, copy vào `<kênh>/creatives/assets/`. `focus` = điểm giữ lại khi cắt cho vừa khung. Layout có vùng `image`: `hero` (mọi khổ), `thesis` (khổ ngang).
- **Chữ khoá:** chữ trong `chữ trên ảnh: "…"` của copy phải xuất hiện đủ, đúng thứ tự trong `eyebrow → big → headline`. Được thêm nhãn phụ (vd. eyebrow "Môi giới 1:1"), không được bỏ hay đổi chữ khoá. Nhãn phụ vẫn qua compliance.
- `layers`: `[{"src": "lib:<id>" | đường dẫn, "box": [x, y, w, h], "opacity", "rotate", "flip", "cover", "blend": "screen"}]` — motif/ánh sáng chồng lên nền, dưới chữ; dùng được cả ở layout không có vùng ảnh (`bignum`, `rows`) để làm nền.
- `"big_style": "gold3d"` (layout `bignum`): số 3D vàng đắp nổi bằng CSS — ngày, năm, %, mốc kỷ niệm.
- `note`: dòng pháp lý nhỏ. `init` tự thêm "Theo biểu phí hiện hành…" khi chữ trên ảnh có `%`.

## 3. Layout (`layouts/*.json`)
| Layout | Style | Theme mặc định | Dùng cho |
|---|---|---|---|
| `thesis` | S01 | dark | 1 luận điểm / ảnh quảng cáo 1 dòng chữ (theme `paper`/`mint` cho S03/S02, `pine` cho biến thể nền xanh) |
| `kv-right` / `kv-left` / `kv-center` | KV | dark | key visual trừu tượng tràn khung + khối chữ (DESIGN.md §5) |
| `rows` | S03 | paper | 2–4 hàng cùng tiêu chí, slide giữa carousel |
| `steps` | S02 | mint | 3–4 bước có số |
| `cta-end` | S04 | dark | slide cuối carousel: câu chốt + nút + pháp lý |
| `hero` | S01+ | tự theo độ sáng ảnh | **mặc định cho quảng cáo / ảnh bìa**: minh hoạ isometric DSC chiếm ~55–60% khung, hoà vào nền; nhãn + tiêu đề + câu phụ |
| `bignum` | S01+ | dark | 1 con số lớn (phí, thời gian, 1:1) làm tâm điểm — con số phải nằm trong chữ khoá |

Slot chữ: `eyebrow` (nhãn nhỏ in hoa), `big` (số lớn), `headline`, `sub`, `cta`, `note`, `items`. Carousel có `page`/`pages` → tự vẽ chấm chỉ trang. Theme: `dark` (Gunmetal, nút Lime), `pine` (Pine Teal), `mint` (mint nhạt, nút Pine Teal), `paper` (trắng, nút Lime); mùa vụ `emerald`, `ivory`. Nền dark có lưới mờ như ảnh featured DSC; `hero` tắt lưới để ảnh liền nền.

Mỗi layout có 4 khổ: `4:5` (1080×1350), `1:1` (1080×1080), `9:16` (1080×1920, có vùng an toàn), `1.91:1` (1200×628). Box là phân số của khung `[x, y, w, h]`. Cỡ chữ = phân số của cạnh ngắn (`xs` 0.026 … `xxl` 0.095), khổ ngang ×1.25.
**Khung tự giãn:** slot ngay dưới tiêu đề bỏ trống → tiêu đề chiếm chỗ và căn giữa; không có ảnh minh hoạ → chữ dàn hết bề ngang.
Thêm layout mới = thêm 1 file JSON cùng schema; `python scripts/creative.py layouts` để xem.

## 4. QA máy (`qa.json`)
| Rule | Mức | Bắt gì |
|---|---|---|
| `FONT-not-loaded` | lỗi | Plus Jakarta Sans không nạp được glyph `Ắệờ` |
| `FIT-overflow` / `FIT-shrunk` | lỗi / lưu ý | chữ tràn khi đã thu còn 60% / phải thu < 85% |
| `FIT-off-canvas` | lỗi | chữ ra ngoài khung |
| `SAFE-zone` | lưu ý | 9:16: chữ ngoài vùng 14%–80% chiều cao (giao diện app che) |
| `MOBILE-small` | lưu ý | chữ < 9,5px khi xem ở màn 390px |
| `CONTRAST-low` | lỗi / lưu ý | < 4,5:1 (chữ nhỏ) hoặc < 3:1 (chữ ≥ 40px quy đổi khung 1080) |
| `RED-pixels` | lỗi / lưu ý | > 0,3% điểm ảnh đỏ. Motif văn hoá (cờ, sen, lụa) → đặt `"allow_red": true` thành lưu ý (DESIGN.md §2) |
| `KV-missing` | lỗi | layout KV chưa có ảnh (`assets/<id>.png`) |
| `CONTRAST-photo` | lỗi / lưu ý | chữ trên ảnh KV: chụp lại khi ẩn chữ, đo phân vị 10/90 độ sáng dưới mỗi khối chữ |
| `LOGO-missing` | lỗi | thiếu file logo |
| `TEXT-locked` | lỗi | chữ trên ảnh khác `chữ trên ảnh: "…"` trong file copy |
| `FIELD-placeholder` / `FIELD-missing` | lỗi | còn TODO / thiếu headline |
| `WORDS-on-image` | lưu ý | ảnh quảng cáo > 8 từ, ảnh khác > 14 từ |
| `COMP-*`, `AI-*` | theo mkt_lint | compliance tài chính + cụm cấm trên chữ trong ảnh |

Máy **không** thấy: bố cục cân hay lệch, khoảng trống thừa, ảnh có "nói" đúng ý post không, dòng ngắt xấu. → `.agents/core/agents/creative-qa.md` xem ảnh (đọc PNG) trước gate.

## 5. Ảnh minh hoạ
Thứ tự tìm ảnh:
1. **Kho DSC có sẵn** `knowledge/3-seo/content/images/` (~80 minh hoạ isometric đã đăng — cùng bộ nhận diện). Tìm theo tên: `ls knowledge/3-seo/content/images | grep -i -E "app|tai-khoan|…"`.
2. Không có ảnh hợp → prompt theo `/image` (luật No-Text, No-Red, palette) → user tạo bằng Gemini → lưu vào `assets/`.

**Quảng cáo:** tránh minh hoạ có đồng xu, ký hiệu $, mũi tên/biểu đồ đi lên, tên lửa — dễ đọc thành hứa lợi nhuận (compliance-finance §3). Post giáo dục được dùng nhẹ nhưng không làm tâm điểm. Chữ, số, logo luôn do engine dựng.

## 5b. Một mẫu → nhiều kênh (`adapt`)
```bash
python scripts/creative.py adapt <design.json> --channel meta-ads|facebook|instagram|linkedin|zalo|tiktok|youtube|google-display [--only id]
python scripts/creative.py adapt <design.json> --sizes 1080x1920,1200x628
```
Nhân bản ảnh sang các khổ của kênh (id `<id>-<khổ>`, giữ chữ khoá của bản gốc) → `render` lại. Bảng khổ `CHANNEL_SIZES` trong script là **đề xuất biên tập** — nền tảng đổi thông số thường xuyên, kiểm lại khi đăng (đặc biệt Zalo OA).

## 6. Đặt tên khi đưa lên Meta (để đo theo mẫu)
Tên ad: `<JOB> | <id> | v<N>` (vd. `CMP-261124-mo-tai-khoan-tet-2027 | ads-v1 | v1`). `/ads-learn` ghép số Meta với `design.json` theo `id` → so hiệu quả theo layout / theme / khung copy (như `hieu-qua` của design-agent).
