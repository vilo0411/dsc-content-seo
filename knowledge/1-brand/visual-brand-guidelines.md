# Visual Brand Guidelines — DSC Securities

> **Phạm vi:** ảnh minh hoạ trong bài blog. Ảnh fanpage / quảng cáo / campaign theo `knowledge/1-brand/DESIGN.md` (2026-11-24).
> **Trạng thái:** [Đã cập nhật ✅] — Quản lý Brand Assets và Quy chuẩn Hình ảnh.
> File này được Visual Architect & Image Skill đọc để đảm bảo hình ảnh nhất quán với thương hiệu DSC.

> **Infographic / biểu đồ / ảnh bìa có chữ trong bài viết:** theo [`image-design-system.md`](image-design-system.md) — token màu, font Be Vietnam Pro (`assets/fonts/`), lưới, component; code `scripts/images/dsc_design.py`.

---

## 1. Brand Colors

| Màu | Hex | Dùng cho |
| :--- | :--- | :--- |
| Brand Green | `#00AD14` | Primary accent, logo, key elements |
| Bright Green | `#2BE841` | Gradient start, energy highlight |
| Teal | `#10E7B3` | Gradient end, digital accent |
| Dark Navy | `#0D1B2A` | Text, dark backgrounds |
| Light Mint Pastel | `#E8F8F2` | Nền sáng chủ đạo cho ảnh Isometric 3D |
| White | `#FFFFFF` | Primary background |

**Gradient chuẩn:** Linear `#2BE841` → `#10E7B3` — dùng cho chart lines, icon accent, overlay.

---

## 2. Brand Assets & Logo Structure

Tất cả các tài sản đồ họa thương hiệu được tổ chức tại thư mục `knowledge/1-brand/assets/`:

```text
knowledge/1-brand/assets/
├── logos/
│   ├── logo-for-light-bg.png    # Logo chữ xanh/tối (dùng cho nền sáng như Light Mint/Pastel/White)
│   └── logo-for-dark-bg.png     # Logo chữ trắng (dùng cho nền tối như Dark Navy)
├── icons/                       # Thư mục lưu trữ Icon thương hiệu (mở rộng tương lai)
└── fonts/                       # Be Vietnam Pro (Regular→ExtraBold, OFL) — font chữ trong ảnh
```

### Quy tắc ghép Logo:
- **Vị trí cố định:** Góc **trên bên trái** (`Top-Left`, lề `4%`).
- **Tự động nhận diện nền:**
  - Nếu nền ảnh sáng $\rightarrow$ sử dụng `logo-for-light-bg.png`.
  - Nếu nền ảnh tối $\rightarrow$ sử dụng `logo-for-dark-bg.png`.

---

## 3. Standard Image Sizes & Aspect Ratios

**Ảnh bìa (featured): 1000×600 px (5:3). Ảnh trong bài: 800×500 px (16:10).** Đúng chuẩn CMS DSC. Thẻ ảnh trong bài: `<img style="aspect-ratio:800/500;" … width="800" height="500">`. Bố cục cho khung này: `image-design-system.md` §4.

---

## 4. Negative Rules (Quy tắc cấm)

- Tuyệt đối 0% chữ rác/typography lỗi do AI tự sinh (`Strict No-Text Rule`).
- Tuyệt đối không sử dụng màu đỏ (tránh thị giác giảm giá chứng khoán).
- Không có logo của đối thủ cạnh tranh.
- Không có chi tiết mạng lưới rác, đường nối chằng chịt gây rối mắt (`Zero-Clutter Rule`).
