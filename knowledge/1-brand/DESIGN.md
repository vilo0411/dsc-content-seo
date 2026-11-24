---
name: Chứng khoán DSC — Social & Campaign visuals
version: 0.1 (2026-11-24)
status: DRAFT — rút từ 3 bài fanpage (knowledge/1-brand/fanpage-refs/). Cần ≥ 10–20 bài để chốt; designer/brand owner duyệt trước khi coi là chuẩn.
format: DESIGN.md (google-labs-code/design.md) — mở rộng cho ảnh social/quảng cáo
supersedes: visual-brand-guidelines.md cho ảnh fanpage / quảng cáo / campaign. visual-brand-guidelines.md vẫn áp cho ảnh minh hoạ trong bài blog.
---

# DSC Visual Identity — Social & Campaign

## 1. Tinh thần
Sang trọng, Việt Nam, đáng tin. Mỗi ảnh là **một key visual (KV) tràn khung** + một khối chữ có tầng lớp, không phải infographic phẳng. Hai giọng chính:
- **Emerald & Gold** — sự kiện thị trường, thương hiệu, sản phẩm, campaign: nền lục bảo sâu, ánh kim vàng, ánh sáng phát xanh.
- **Ivory Culture** — lễ, văn hoá, thông báo: nền ngà/kem, tranh màu nước - sơn thuỷ, sen, hạc, kiến trúc Việt.

## 2. Màu (đo từ ảnh fanpage)
| Token | Hex | Dùng |
|---|---|---|
| `emerald-950` | `#0B331E` | nền tối nhất, vùng đặt chữ (scrim) |
| `emerald-800` | `#1B5232` | nền chính Emerald |
| `emerald-600` | `#226435` | mảng sáng, gradient |
| `jade-400` | `#6CB298` | Ivory: nét núi, lá; nhấn nhẹ |
| `glow-400` | `#5BD681` | ánh sáng phát xanh (nến, đường giá) — chỉ trong hình |
| `gold-200` | `#EFD786` | chữ ánh kim sáng |
| `gold-500` | `#C9A24A` | chữ ánh kim giữa (điểm tương phản để QA) |
| `gold-700` | `#A57D3F` | viền, bóng chữ, hoa văn |
| `ivory-50` | `#F9F4EB` | nền Ivory |
| `cream-200` | `#EBE1C1` | giấy, hoạ tiết trống đồng mờ |
| `lacquer-600` | `#BA382B` | **chỉ** cờ, sen, lụa, đèn lồng trong ảnh lễ/văn hoá |
| `brand-green` | `#00AD14` | logo, badge số liệu, nút CTA |

Luật đỏ: **không** dùng đỏ cho chữ, số liệu, biểu đồ, mũi tên giá (đỏ = giảm giá ở TTCK VN). Được dùng đỏ trong motif văn hoá/lễ (cờ, sen, lụa). Ảnh quảng cáo sản phẩm: tránh đỏ.

## 3. Chữ — 3 cấp + nội dung
| Vai trò | Font (OFL, có tiếng Việt) | Kiểu | Ví dụ fanpage |
|---|---|---|---|
| `script` — dòng dẫn cảm xúc | Great Vibes | viết tay, 1 dòng ngắn 2–5 từ | "Tâm thế mới trên", "Chính thức", "Bản sắc Việt" |
| `display-serif` — tiêu đề trang trọng | Cormorant Garamond 700 (hoặc Playfair Display 800) | IN HOA, ánh kim vàng | "HÀNH TRÌNH THỊNH VƯỢNG", "VĂN HÓA" |
| `display-sans` — tiêu đề sự kiện/số liệu | Montserrat 800 | IN HOA, trắng hoặc ánh kim | "NÂNG HẠNG", "VIỆT NAM" |
| `body` — phụ đề, ghi chú, ngày | Be Vietnam Pro 400/700 | thường | "Ngày nghỉ giao dịch" |

Quy tắc: mỗi ảnh tối đa **2 font display** (script + 1 display). Script không quá 5 từ, không dùng cho số. Chữ ánh kim = gradient dọc `#FFF3C4 → #EFD786 → #C9A24A → #8C6A1F` + bóng đổ mềm. Files: `knowledge/1-brand/assets/fonts/`.

## 4. Thành phần
- **Logo**: trắng trên nền tối, xanh trên nền sáng; góc trên phải hoặc trên giữa; cạnh ≥ 4% khung. Có thể dùng bản "DSC SECURITIES".
- **Badge**: viên thuốc bo tròn, nền xanh dương/xanh lá đậm, chữ trắng in hoa — cho tên tổ chức/sự kiện ("FTSE RUSSELL").
- **Thẻ lịch**: thẻ trắng gáy xanh, số ngày lớn, thứ ở gáy — cho thông báo nghỉ lễ/giao dịch.
- **Scrim**: vùng chữ được làm tối/sáng mềm bằng gradient từ màu nền, không có khung hộp.

## 5. Key visual (hình chủ đạo)
- **Motif được dùng**: hạc, sen, trống đồng Đông Sơn (hoa văn), chùa Một Cột, núi sơn thuỷ, lụa cờ, nến chứng khoán phát sáng, đường xu hướng ánh sáng, khối kim loại vàng chạm khắc. Tết: hoa mai, hoa đào, đèn lồng, câu đối (không chữ).
- **Chất liệu**: render 3D/ảnh thật sắc nét, ánh sáng điện ảnh, chiều sâu (bokeh, hạt sáng); hoặc tranh màu nước - lụa cho Ivory.
- **Bố cục**: chủ thể lệch một phía; phía còn lại là **khoảng thở** cho khối chữ (≈ 40–50% khung).
- **Cấm**: chữ do AI sinh, logo/nhãn hiệu khác, người thật nhận diện được, tiền mặt/đồng xu rơi, mũi tên lãi "x lần", ảnh chụp lãi/lỗ.

## 6. Bố cục khối chữ
`[logo]` → `script` → `display` (1–2 dòng) → `sub`/`badge` → `note` pháp lý (nhỏ, đáy). Căn phải hoặc căn giữa theo phía khoảng thở của KV. Khoảng cách dòng display chặt (1.05–1.15).

## 7. Khi nào làm bằng workflow, khi nào đặt designer
| Tự làm (`/creative` + KV từ Gemini) | Đặt designer |
|---|---|
| Post giáo dục, số liệu tuần, thông báo nghỉ lễ, biến thể A/B quảng cáo, đổi khổ | KV chính campaign lớn (Tết, sự kiện nâng hạng), ảnh cần nhân vật/chất liệu riêng, bộ nhận diện mới |

## 8. Mở (cần bổ sung)
- Font thật mà designer DSC đang dùng (hiện thay bằng font OFL gần giống).
- File logo bản "DSC SECURITIES", bản vàng ánh kim.
- Thêm ảnh fanpage để xác nhận tỉ lệ dùng Emerald vs Ivory, vị trí logo chuẩn.
