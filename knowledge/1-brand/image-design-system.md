# DSC Image Design System — ảnh trong bài viết Kiến thức

> Áp dụng cho ảnh bìa và infographic/biểu đồ trong bài SEO. Mã nguồn: `scripts/images/dsc_design.py` (token + component). Sửa token ở cả 2 nơi.
> Ví dụ chuẩn: `scripts/images/generate_cach_choi_chung_khoan_images.py` → `knowledge/3-seo/content/images/cach-choi-chung-khoan-*.jpg`.
> Bổ sung cho `visual-brand-guidelines.md` (màu gốc, logo, quy tắc cấm). Chỗ nào 2 file khác nhau, file này thắng với ảnh trong bài viết.

## 1. Hướng thiết kế
**Editorial fintech:** sạch, nhiều khoảng trắng, số liệu là nhân vật chính. Mỗi ảnh trả lời đúng 1 câu hỏi của section, đọc được trong 3 giây trên điện thoại.

- Ảnh phải chứa **số liệu thật của bài**: phí, %, mốc T+2, giá. Không dùng ảnh minh họa chung chung kiểu bàn tay chỉ biểu đồ.
- Chữ trong ảnh do code vẽ (PIL + font thật), **không** dùng AI vẽ chữ. Ảnh AI chỉ dùng cho nền và vật thể không có chữ (theo `/image`).
- Mỗi ảnh có đúng 1 điểm nhấn: con số lớn nhất **hoặc** cột nổi bật nhất. Mọi thứ còn lại đều trung tính.

## 2. Màu (token)
| Token | Hex | Vai trò |
|---|---|---|
| `navy` | `#0D1B2A` | Chữ chính, nền ảnh bìa, **dữ liệu xấu / rủi ro** (thay cho đỏ) |
| `navy_800` / `navy_700` | `#13263A` / `#1C3348` | Bề mặt trên nền tối (card, ô nhập) |
| `green` | `#00AD14` | Dữ liệu tốt / điểm nhấn chính; nền chip số |
| `green_700` | `#00801A` | **Chữ xanh trên nền sáng** (đạt độ tương phản AA). Không dùng `green` cho chữ nhỏ trên nền trắng |
| `bright` → `teal` | `#2BE841` → `#10E7B3` | Gradient: **chỉ dùng trên nền navy** (chữ nhấn, đường biểu đồ, glow) |
| `ink_2` | `#425466` | Chữ phụ, phụ đề |
| `ink_3` | `#7A8A99` | Chú thích, nguồn, nhãn trục |
| `neutral` | `#B6C2CC` | Dữ liệu so sánh / mốc "không làm gì" |
| `line` / `track` | `#DCE7E1` / `#E6F0EA` | Viền card, đường kẻ / nền thanh bar |
| `mint_50` / `mint_100` | `#F4FAF7` / `#E8F8F2` | Nền ảnh sáng / nền tag |

Quy tắc dữ liệu: tốt = `green`, xấu = `navy`, so sánh = `neutral`. **Không dùng đỏ**, kể cả cho số âm. Dấu âm dùng ký tự “−”.

## 3. Chữ
Font **Be Vietnam Pro** (OFL, thiết kế cho tiếng Việt), lưu ở `knowledge/1-brand/assets/fonts/`. Không dùng Arial / Segoe.

| Token | Weight / size (px trên khung 800×500) | Dùng cho |
|---|---|---|
| `display` | ExtraBold 46 | Tiêu đề ảnh bìa (tối đa 3 dòng) |
| `h1` | Bold 26 | Tiêu đề infographic (1 dòng, ≤ 42 ký tự) |
| `h2` | SemiBold 17 | Tiêu đề card, tên bước |
| `body` / `body_m` | Regular / Medium 14 | Mô tả, nhãn hàng |
| `caption` | Medium 12 (**nhỏ nhất**) | Nguồn, chú thích, tag |
| `eyebrow` | SemiBold 11, IN HOA, giãn chữ 1.2 | Nhãn chủ đề góc phải trên |
| `num_xl` / `num_l` / `num_m` | ExtraBold 46 / ExtraBold 26 / Bold 19 | Số liệu: mỗi ảnh tối đa 1 số `num_xl` |

Câu chữ trong ảnh: viết hoa đầu câu, không viết hoa toàn bộ (trừ eyebrow). Số theo kiểu Việt Nam: `30.000`, `0,3%`.

## 4. Lưới và khung
- **Kích thước (chuẩn CMS DSC):** ảnh trong bài **800×500** (16:10); **ảnh bìa 1000×600** (5:3), vẽ trên khung 800×480 với cùng bộ cỡ chữ rồi xuất ra 1000×600 (`Canvas(FEATURED, …, out=FEATURED_OUT)`). Vẽ ở 3× rồi thu nhỏ để khử răng cưa.
- Thẻ ảnh trong bài: `<img style="aspect-ratio:800/500;" src="…" alt="…" width="800" height="500">`, theo mẫu thẻ ảnh trên site live. Ảnh bìa: `aspect-ratio:1000/600`, `width="1000" height="600"`.
- **Lề:** 40 px. **Bước khoảng cách:** bội số của 4 (8/12/16/20). Card cách nhau 10–16.
- **Khung infographic (`inline_frame`)**, từ trên xuống:
  1. Logo nền sáng góc trên bên trái, cao 20 px, cách lề 40 px. Eyebrow nằm cùng hàng, căn phải.
  2. Tiêu đề `h1`, bên dưới là phụ đề `body`/`ink_2` nêu điều kiện của số liệu.
  3. Vùng nội dung, từ khoảng y 124 đến y 442: các card.
  4. Footer: đường kẻ `line`, bên trái ghi nguồn (`caption`/`ink_3`), bên phải `dsc.com.vn` (`green_700`).
- **Card:** nền trắng, viền 1 px `line`, bo góc 14, bóng mềm (blur 12, độ đậm 10%, lệch xuống 5).
- Khung 800×500 ngang và thấp: chuỗi 4–5 bước dàn **thành cột ngang**, so sánh 2 vế dàn **thành 2 card cạnh nhau**.

## 5. Component
| Component | Quy chuẩn | Ví dụ |
|---|---|---|
| **Các bước (cột)** | 5 card cột ngang, cách nhau 10. Chip số 32×32 bo 10, nền `green`; bước cuối nền `navy`. Tên bước `h2` (tối đa 2–3 dòng), mô tả `body`, tag dán đáy card | `-5-buoc.jpg` |
| **Stat lớn** | Nhãn `caption`/`ink_3` ở trên, số `num_xl`/`navy` bên dưới | `-chi-phi-hoa-von.jpg` |
| **Thanh chia phần + chú giải** | Các phần cao 12, bo 6, cách nhau 4; bên dưới mỗi dòng gồm chấm màu + nhãn + giá trị căn phải. Kết card bằng 1 dòng kết luận có số `num_m`/`green_700` | như trên |
| **Bar ngang** | Nhãn và giá trị trên cùng 1 dòng, thanh nằm dưới: nền `track` cao 12, bar `green`/`navy`. Giá trị ghi cả % và tiền | như trên |
| **Cột so sánh 2 kịch bản** | 2 card cạnh nhau. Kịch bản tăng có cột mọc lên, kịch bản giảm có cột rủ xuống; kèm giá trị `num_l` và chú thích "còn … triệu" | `-margin-2-chieu.jpg` |
| **Ảnh chụp app** | Ảnh chụp thật, cắt đúng vùng cần xem, đặt trong card trắng ở bên phải. Chấm số xanh đặt cạnh từng vùng thao tác; bên trái là danh sách bước cùng số. Ảnh chụp gốc lưu ở `knowledge/1-brand/assets/screens/` | `-dat-lenh-lo.jpg` |
| **Tag** | Cao 22, bo tròn hoàn toàn, nền `mint_100`, chữ `caption`/`green_700` | Online, T+2 |
| **Ảnh bìa** | Nền `navy` có 2 vùng sáng mờ. Bên trái: logo nền tối, eyebrow pill, tiêu đề `display` (dòng cuối tô gradient), 3 stat `num_m`. Bên phải: mockup điện thoại hiển thị số liệu của bài, kèm 1 card nổi màu trắng đặt trên vùng biểu đồ (không che chữ) | `-featured.jpg` |

## 6. Checklist trước khi chèn ảnh
- [ ] Mọi số trong ảnh khớp với số trong bài (giá, %, ngày).
- [ ] Footer ghi nguồn khi ảnh có phí, thuế, lãi suất hoặc giá.
- [ ] Không có đỏ, không có logo đối thủ, không có chữ do AI sinh.
- [ ] Đúng kích thước: ảnh trong bài 800×500, ảnh bìa 1000×600; chữ nhỏ nhất 12 px; không chữ nào bị card / mockup che.
- [ ] Chỉ có 1 điểm nhấn màu, phần còn lại dùng `navy` / `neutral`.
- [ ] Tên file `<slug>-<chu-de>.jpg`, alt chứa keyword và mô tả đúng nội dung ảnh.
