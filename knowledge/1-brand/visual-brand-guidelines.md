# Visual Brand Guidelines — DSC Securities

> **Phạm vi:** ảnh minh hoạ trong bài blog (logo, khổ ảnh, quy tắc cấm). Màu / font / phong cách: `knowledge/1-brand/DESIGN.md` v1.0 — nguồn chuẩn cho mọi thiết kế.
> **Trạng thái:** [Đã cập nhật ✅] — Quản lý Brand Assets và Quy chuẩn Hình ảnh.
> File này được Visual Architect & Image Skill đọc để đảm bảo hình ảnh nhất quán với thương hiệu DSC.

> **Infographic / biểu đồ / ảnh bìa có chữ trong bài viết:** theo [`image-design-system.md`](image-design-system.md) — token màu, font Plus Jakarta Sans (`assets/fonts/`), lưới, component; code `scripts/images/dsc_design.py`.

---

## 1. Brand Colors

Theo brand guideline chính thức — chi tiết, gradient, bảng tương phản: [`DESIGN.md`](DESIGN.md) §2–§3.

| Màu | Hex | Dùng cho |
| :--- | :--- | :--- |
| Gunmetal | `#272D2B` | Chữ, nền tối chính |
| Pine Teal | `#1D4130` | Nền tối thứ hai, chữ xanh trên nền sáng |
| Lime Green | `#2AD03D` | Điểm nhấn chính, nút CTA (chữ Gunmetal) |
| Emerald | `#1BBE72` | Điểm nhấn phụ |
| Frosted Mint | `#8CFFCC` | Nhấn sáng trên nền tối, tag |
| White | `#FFFFFF` | Nền sáng chính |

**Gradient:** Primary `#61CC6C → #14A46E` (đường biểu đồ, icon, thanh nhấn) · Ambient `#156A1F → #31AE40 → #156A1F` / `#354D38 → #2C7B50 → #7D9E9F → #B6C7AF` (nền). Nền sáng nhạt cho isometric 3D: `#F2FBF6`.

**Phong cách ảnh AI:** trừu tượng 3D tông xanh (dải lụa/kính, khối mềm, vệt sáng trên nền tối) — mẫu `guideline/20-abstract.png`.

---

## 2. Brand Assets & Logo Structure

Tất cả các tài sản đồ họa thương hiệu được tổ chức tại thư mục `knowledge/1-brand/assets/`:

```text
knowledge/1-brand/assets/
├── logos/
│   ├── logo-for-light-bg.png    # Logo chữ xanh/tối (dùng cho nền sáng như White / mint nhạt)
│   └── logo-for-dark-bg.png     # Logo chữ trắng (dùng cho nền tối như Gunmetal / Pine Teal)
├── icons/                       # Thư mục lưu trữ Icon thương hiệu (mở rộng tương lai)
└── fonts/                       # Plus Jakarta Sans (Regular→ExtraBold, OFL) — font duy nhất của brand
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
