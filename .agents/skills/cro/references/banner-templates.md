# Banner CTA Templates — DSC

> Inline style 100% (WordPress strip `<style>`). Palette, font và tương phản theo `knowledge/1-brand/DESIGN.md` v1.0 + `.agents/rules/cta-conversion.md` mục 5. Không thêm hex ngoài template.
> Placeholder: `{{HEADLINE}}` `{{SUB}}` `{{BUTTON}}` `{{URL}}`. Thay hết trước khi chèn — không để placeholder sót lại trong bài.
>
> `{{URL}}` = `https://www.dsc.com.vn/mo-tai-khoan` (mặc định, không UTM).

---

## Chọn template nào

| Template | Dùng khi |
| :--- | :--- |
| `primary-midarticle` | Mặc định cho banner giữa bài, đặt ngay sau đoạn Product Bridge |
| `slim-inline` | Bài dài > 2500 từ cần thêm một điểm chạm mà không muốn ngắt mạch đọc; hoặc persona P1/P3 (CTA mềm) |
| `closing` | Kết bài — luôn dùng bản này, không dùng lại `primary-midarticle` ở cuối |

---

## 1. `primary-midarticle`

Nền Gunmetal → Pine Teal (chữ trắng 11.3–14:1), nút Lime chữ Gunmetal (6.8:1), dòng phụ Frosted Mint.

```html
<div style="background: linear-gradient(135deg, #272D2B 0%, #1D4130 100%); border-radius: 12px; padding: 30px; margin: 30px 0; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 10px 30px rgba(39, 45, 43, 0.25); position: relative; overflow: hidden; color: #ffffff; gap: 20px; flex-wrap: wrap;">
  <div aria-hidden="true" style="position: absolute; top: -50%; right: -20%; width: 300px; height: 300px; background: radial-gradient(circle, rgba(42, 208, 61, 0.20) 0%, rgba(42, 208, 61, 0) 70%); border-radius: 50%;"></div>
  <div style="flex: 1 1 260px; position: relative; z-index: 1;">
    <p style="font-size: 22px; line-height: 1.35; margin: 0 0 10px 0; font-weight: 700; color: #ffffff;">{{HEADLINE}}</p>
    <p style="font-size: 15px; line-height: 1.5; margin: 0; color: #8CFFCC;">{{SUB}}</p>
  </div>
  <a href="{{URL}}" style="background: #2AD03D; color: #272D2B; padding: 14px 32px; border-radius: 30px; text-decoration: none; font-weight: 700; font-size: 16px; display: inline-block; position: relative; z-index: 1;">{{BUTTON}}</a>
</div>
```

**Khác gì bản cũ — và tại sao** (bảng lịch sử; màu hiện hành theo DESIGN.md v1.0 từ 2026-11-25, thay Navy/`#2BE841` bằng Gunmetal/Pine Teal/Lime):

| Thay đổi | Lý do |
| :--- | :--- |
| Nền `#27ae60` → gradient `#0D1B2A → #0A3D2E` | `#27ae60` không có trong brand palette; chữ trắng trên nền đó chỉ đạt 2.9:1, trượt WCAG AA |
| Nút trắng chữ xanh → nút `#2BE841` chữ `#0D1B2A` | Trắng-trên-xanh-lá 3.0:1 trượt AA. Nút xanh sáng trên nền tối vừa đạt 10.2:1 vừa nổi hơn hẳn |
| Vòng tròn trắng mờ → radial gradient xanh lá mờ | Đúng brand accent, không làm loãng chữ phía dưới |
| `opacity: 0.95` ở dòng phụ → màu đặc `#E8F8F2` | `opacity` làm tương phản khó kiểm soát; dùng màu pastel mint của brand cho chắc chắn |
| Nút bỏ `white-space: nowrap` | Kèm padding 32px, nút dài sẽ tràn khung ở màn hình 360px |
| `flex: 1` → `flex: 1 1 260px` | Cho khối chữ xuống dòng gọn thay vì bị bóp còn vài ký tự mỗi dòng |
| Thêm `line-height` | Headline 22px không có line-height sẽ dính dòng khi wrap trên mobile |

Headline giảm 24px → 22px: 24px hai dòng trên mobile chiếm quá nhiều chiều cao màn hình.

---

## 2. `slim-inline`

Dải mỏng, không ngắt mạch đọc. Viền trái xanh lá làm điểm nhấn thay vì nền đậm.

```html
<div style="border-left: 4px solid #2AD03D; background: #F2FBF6; border-radius: 0 8px 8px 0; padding: 18px 22px; margin: 28px 0; display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;">
  <p style="margin: 0; font-size: 16px; line-height: 1.5; color: #272D2B; flex: 1 1 240px;">{{HEADLINE}}</p>
  <a href="{{URL}}" style="background: #1D4130; color: #ffffff; padding: 11px 24px; border-radius: 24px; text-decoration: none; font-weight: 600; font-size: 15px; display: inline-block;">{{BUTTON}}</a>
</div>
```

Tương phản: Gunmetal `#272D2B` trên `#F2FBF6` ≈ 13.3:1 · nút trắng trên Pine Teal `#1D4130` 11.3:1.
Template này **không dùng `{{SUB}}`** — chỉ một dòng.

---

## 3. `closing`

Kết bài. Khối dọc, có chỗ cho lý do cuối cùng.

```html
<div style="background: linear-gradient(135deg, #272D2B 0%, #1D4130 100%); border-radius: 14px; padding: 34px 30px; margin: 36px 0; text-align: center; color: #ffffff;">
  <p style="font-size: 23px; line-height: 1.35; margin: 0 0 12px 0; font-weight: 700; color: #ffffff;">{{HEADLINE}}</p>
  <p style="font-size: 15px; line-height: 1.6; margin: 0 0 22px 0; color: #8CFFCC; max-width: 520px; margin-left: auto; margin-right: auto;">{{SUB}}</p>
  <a href="{{URL}}" style="background: #2AD03D; color: #272D2B; padding: 15px 38px; border-radius: 30px; text-decoration: none; font-weight: 700; font-size: 16px; display: inline-block;">{{BUTTON}}</a>
</div>
```

---

## Quy tắc chung khi chèn

1. Chèn banner kèm **một dòng trống trước và sau** khối HTML, để markdown không nuốt đoạn văn liền kề.
2. Không thêm `target="_blank"` — link cùng domain.
3. Không sửa màu trong template. Cần biến thể màu → sửa file này, không sửa tại chỗ trong bài.
4. Sinh biến thể A/B là đổi **copy**, không đổi template, trừ khi đang test chính bố cục.
5. Sau khi chèn: `python scripts/qa_lint.py <file> --cta`.
