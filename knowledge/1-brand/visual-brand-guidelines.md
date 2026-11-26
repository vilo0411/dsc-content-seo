# Visual Brand Guidelines — DSC Securities (Blog & AI Illustration Spec)

> **Phân ranh giới MECE (Tránh trùng lặp bảng màu & font):**
> - **Nguồn chuẩn duy nhất về Màu sắc, Gradient, Font chữ (`Plus Jakarta Sans`), Tương phản WCAG và Theme mùa vụ:** Xem [`knowledge/1-brand/DESIGN.md`](DESIGN.md) v1.0 (máy đọc: [`knowledge/1-brand/brand.json`](brand.json)).
> - **Nguồn chuẩn về Lưới, Token PIL, Component vẽ Infographic & Ảnh bìa bằng code (`scripts/images/dsc_design.py`):** Xem [`knowledge/1-brand/image-design-system.md`](image-design-system.md).
> - **File này (`visual-brand-guidelines.md`)** chỉ quy định **Cấu trúc thư mục Assets, Quy tắc ghép Logo tự động, Khổ ảnh chuẩn CMS Blog và Quy tắc cấm (Negative Rules)** khi dùng AI sinh ảnh minh họa không chữ (`/image`).

---

## 1. Brand Assets & Logo Structure

Tất cả các tài sản đồ họa thương hiệu được tổ chức tại thư mục `knowledge/1-brand/assets/`:

```text
knowledge/1-brand/assets/
├── logos/
│   ├── logo-for-light-bg.png    # Logo chữ xanh/tối (dùng cho nền sáng như White / mint nhạt #F2FBF6)
│   └── logo-for-dark-bg.png     # Logo chữ trắng (dùng cho nền tối như Gunmetal #272D2B / Pine Teal #1D4130)
├── fonts/                       # Plus Jakarta Sans (Regular→ExtraBold, OFL) — font duy nhất của brand
├── library/                     # Kho nền & asset đã duyệt (quản lý bởi scripts/asset_lib.py)
└── screens/                     # Ảnh chụp màn hình thật App DSC Trading dùng cho infographic hướng dẫn
```

### Quy tắc ghép Logo:
- **Vị trí cố định:** Góc **trên bên trái** (`Top-Left`, lề `4%`).
- **Tự động nhận diện nền:**
  - Nếu nền ảnh sáng $\rightarrow$ sử dụng `logo-for-light-bg.png`.
  - Nếu nền ảnh tối $\rightarrow$ sử dụng `logo-for-dark-bg.png`.

---

## 2. Standard Blog Image Sizes & Aspect Ratios (Chuẩn CMS DSC)

- **Ảnh bìa (Featured Image):** `1000×600 px` (tỷ lệ `5:3`). Thẻ HTML: `<img style="aspect-ratio:1000/600;" … width="1000" height="600">`.
- **Ảnh trong bài (Inline Image / H2 Infographic):** `800×500 px` (tỷ lệ `16:10`). Thẻ HTML: `<img style="aspect-ratio:800/500;" … width="800" height="500">`.
- *(Khổ ảnh cho Social Feed `1080×1080`, Portrait `1080×1350`, Story `1080×1920`, Link Ad `1200×628` xem trong `brand.json` → `sizes`).*

---

## 3. Negative Rules (Quy tắc cấm bắt buộc cho mọi hình ảnh)

- **Strict No-Text Rule cho ảnh AI:** Tuyệt đối 0% chữ rác/typography lỗi do AI tự sinh. Mọi chữ và số liệu trên ảnh bắt buộc phải render bằng code qua font `Plus Jakarta Sans` thật (`dsc_design.py` hoặc `creative.py`).
- **No Red Rule:** Tuyệt đối không sử dụng màu đỏ cho chữ, số, biểu đồ hoặc mũi tên giá (tránh thị giác giảm giá chứng khoán tại Việt Nam; dữ liệu giảm/rủi ro dùng màu `gunmetal` `#272D2B` hoặc `neutral` `#B9C3BF`).
- **No Competitor Assets:** Không xuất hiện logo, giao diện app hoặc nhãn hiệu của đối thủ cạnh tranh.
- **Zero-Clutter Rule:** Không dùng chi tiết mạng lưới rác, đường nối chằng chịt, tiền mặt/đồng xu rơi hay ảnh chụp màn hình lãi/lỗ giả lập.
