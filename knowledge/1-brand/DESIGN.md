---
name: Chứng khoán DSC — Visual Identity
version: 1.0 (2026-11-25)
status: CHUẨN — theo brand guideline chính thức của DSC (trang 11, 12, 14, 15, 20; ảnh gốc ở knowledge/1-brand/guideline/)
format: DESIGN.md (google-labs-code/design.md)
machine: knowledge/1-brand/brand.json (mọi script đọc màu/font từ đây)
scope: MỌI thiết kế — ảnh social/quảng cáo (/creative), banner CTA trong bài (/cro), landing (/landing, /copy-landing), ảnh & infographic blog (/image, scripts/images/dsc_design.py), ảnh syndication (/syndicate)
---

# DSC Visual Identity

**Luật gốc:** chỉ dùng màu, gradient, font trong file này / `brand.json`. Không tự đặt hex, không thêm font. Cần màu/tông mới → hỏi user, cập nhật file này trước rồi mới dùng.

## 1. Tinh thần
Hiện đại, công nghệ, đáng tin. Nền tối sâu (Gunmetal / Pine Teal) hoặc trắng sạch, điểm nhấn xanh lá tươi (Lime / Emerald), hình trừu tượng xanh có chiều sâu và ánh sáng. Ít chữ, khoảng thở rộng, 1 ảnh = 1 luận điểm.

## 2. Màu thương hiệu (trang 11)
| Token | Hex | Vai trò |
|---|---|---|
| `gunmetal` | `#272D2B` | Nền tối chính, chữ chính trên nền sáng, chữ trên nút Lime |
| `pine_teal` | `#1D4130` | Nền tối thứ hai, card trên nền Gunmetal, **chữ xanh trên nền sáng**, nút trên nền sáng |
| `lime` | `#2AD03D` | Điểm nhấn chính: nút CTA, số liệu tốt, đường biểu đồ, highlight |
| `emerald` | `#1BBE72` | Điểm nhấn phụ: badge, icon, đường biểu đồ thứ hai |
| `frosted_mint` | `#8CFFCC` | Nhấn sáng trên nền tối (eyebrow, mark, glow), tag nền sáng |
| `white` | `#FFFFFF` | Nền sáng chính, chữ trên nền tối |

Tông phụ trợ (`colors.derived` trong brand.json: `ink_2`, `ink_3`, `line`, `track`, `mint_50`…) chỉ để làm chữ phụ, viền, nền nhạt — không làm điểm nhấn.

Dữ liệu xấu / rủi ro: dùng `gunmetal` hoặc `neutral` (không dùng đỏ — đỏ = giảm giá ở TTCK VN).

### Tương phản (WCAG, đã tính)
| Chữ trên nền | Tỉ lệ | Dùng |
|---|---|---|
| White / Gunmetal | 14.0 | ✓ nền tối chuẩn |
| White / Pine Teal | 11.3 | ✓ |
| Frosted Mint / Gunmetal | 11.6 | ✓ eyebrow, số nhấn |
| Lime / Gunmetal | 6.8 | ✓ chữ nhấn trên nền tối |
| Gunmetal / Lime | 6.8 | ✓ **nút CTA chuẩn** |
| Gunmetal / Emerald | 5.8 | ✓ |
| Gunmetal / Frosted Mint | 11.6 | ✓ tag |
| Pine Teal / White | 11.3 | ✓ chữ xanh trên nền sáng |
| White / Lime | 2.1 | ✗ cấm |
| White / Emerald | 2.4 | ✗ cấm |
| Lime hoặc Emerald làm chữ / nền trắng | 2.1–2.4 | ✗ cấm (chỉ dùng cho mảng, đường, icon ≥ 3px) |

## 3. Gradient (trang 12)
| Token | Màu | Dùng |
|---|---|---|
| `primary` | `#61CC6C → #14A46E` (ngang) | Nút CTA lớn, thanh nhấn, mảng màu. Chữ trên nó: Gunmetal |
| `ambient_light` | `#156A1F → #31AE40 → #156A1F` (chéo, vệt sáng giữa) | Nền KV/banner đậm. Chữ trắng (vùng tối ≥ 4.5:1) |
| `ambient_soft` | `#354D38 → #2C7B50 → #7D9E9F → #B6C7AF` (mờ, radial) | Nền mờ ambient sau khối chữ. Đặt chữ ở vùng tối, có scrim nếu cần |

## 4. Chữ (trang 14–15)
Font **duy nhất: Plus Jakarta Sans** (OFL, đủ dấu tiếng Việt) — `knowledge/1-brand/assets/fonts/PlusJakartaSans-*.ttf`. Fallback kỹ thuật: Be Vietnam Pro (chỉ khi môi trường thiếu font). Không dùng font script/serif/Montserrat.

| Cấp | Size / weight (web) | Khổ 1080px (ảnh) |
|---|---|---|
| Heading 1 | 56pt / 700 | 72–96px |
| Heading 2 | 42pt / 700 | 56–64px |
| Heading 3 | 32pt / 700 | 40–48px |
| Heading 4 | 20pt / 600 | 28–32px |
| Paragraph Bold / SemiBold / Regular | 15pt / 700 · 600 · 400 | 24–28px |
| Subtitle SemiBold / Regular / Italic | 14pt / 600 · 400 · 400 italic | 20–22px |

Quy tắc: tối đa 3 cấp chữ/ảnh; tiêu đề line-height 1.1–1.2, chữ thường ≥ 1.4; dùng file đúng weight (không ép đậm); NFC; in hoa chỉ cho eyebrow/badge ngắn.

## 5. Hình ảnh (trang 20)
Phong cách mặc định: **trừu tượng 3D tông xanh**
- dải lụa/kính xanh xoắn lớp, viền tối mảnh;
- khối màu mềm uốn lượn (Lime/Emerald trên nền xanh đen);
- vệt ánh sáng xanh chéo trên nền gần đen;
- nền mờ ambient gradient xanh — xanh xám.

Bố cục: chủ thể lệch một phía, phía còn lại là khoảng thở 40–50% cho khối chữ. Ảnh minh hoạ blog (isometric / infographic) vẫn theo `image-design-system.md` nhưng dùng palette này.

**Cấm:** chữ do AI sinh, logo/nhãn hiệu khác, người thật nhận diện được, tiền mặt/đồng xu rơi, mũi tên lãi "x lần", ảnh chụp lãi/lỗ, màu ngoài palette (tím, cam, xanh dương…).

## 6. Thành phần
- **Logo:** bản trắng trên nền tối, bản màu trên nền sáng; góc trên trái (hoặc trên phải nếu KV chiếm trái); cạnh ≥ 4% khung.
- **Nút CTA:** nền Lime (hoặc gradient `primary`), chữ Gunmetal 700, bo tròn 999px. Trên nền sáng có thể dùng nút Pine Teal chữ trắng.
- **Badge / tag:** viên thuốc nền Frosted Mint chữ Gunmetal (nền sáng) hoặc nền Pine Teal chữ trắng/Frosted Mint (nền tối).
- **Scrim:** gradient từ màu nền, không vẽ khung hộp.
- **Biểu đồ:** chuỗi chính Lime, chuỗi so sánh Emerald → `neutral`, trục/nhãn `ink_3`, lưới `line`.

## 7. Theme mùa vụ (chỉ khi brief ghi rõ Tết / lễ / văn hoá)
Giữ từ v0.1 (rút từ fanpage), token ở `colors.seasonal`:
- **Emerald & Gold** — nền lục bảo sâu `#0B331E`/`#1B5232`, chữ ánh kim `#FFF3C4 → #EFD786 → #C9A24A → #8C6A1F`, ánh xanh `#5BD681`.
- **Ivory Culture** — nền ngà `#F9F4EB`/`#EBE1C1`, nét jade `#6CB298`, motif hạc, sen, trống đồng, sơn thuỷ.
- Font **vẫn là Plus Jakarta Sans** (không script/serif). Logo, CTA, luật tương phản như §2, §6.
- Đỏ sơn mài `#BA382B` chỉ cho cờ, sen, lụa, đèn lồng trong ảnh — không cho chữ, số, biểu đồ.
- Mặc định của mọi việc khác: palette §2.

## 8. Khi nào tự làm, khi nào đặt designer
| Tự làm (`/creative`, `/image`, `/cro`, `/landing`) | Đặt designer |
|---|---|
| Post giáo dục, số liệu tuần, thông báo nghỉ lễ, biến thể A/B quảng cáo, đổi khổ, banner CTA, infographic | KV chính campaign lớn, ảnh cần nhân vật/chất liệu riêng, bộ nhận diện mới |

## 9. Lịch sử
- v1.0 (2026-11-25): thay bảng màu cũ (`#00AD14/#2BE841/#10E7B3/#0D1B2A/#E8F8F2`) và font Be Vietnam Pro + Great Vibes/Cormorant/Playfair/Montserrat bằng brand guideline chính thức. Thiết kế làm trước ngày này (CMP-261124 v1–v3, landing-v1, ảnh blog đã publish) giữ nguyên; token cũ ở `colors.legacy`.
- v0.1 (2026-11-24): bản nháp rút từ 3 bài fanpage → nay là theme mùa vụ §7.
