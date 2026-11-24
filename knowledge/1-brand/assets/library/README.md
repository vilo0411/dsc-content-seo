# Thư viện asset dựng ảnh

Tạo 1 lần, dùng lại nhiều lần → ảnh ra trong vài giây, không tốn quota Codex cho bài thường.
Engine: `scripts/asset_lib.py` · dùng trong ảnh: `scripts/creative.py pick` / `"image": {"src": "lib:<id>"}` / `"layers"`.

| Thư mục | Là gì | Dùng |
|---|---|---|
| `bg/` | Nền KV có **chừa sẵn chỗ chữ** (`side`: left/right/top/center). Bản dọc 1080×1920 (cắt được 4:5, 1:1, 9:16), bản ngang 1920×1080 (1.91:1) | layout `kv-right` (chừa phải), `kv-left` (chừa trái), `kv-center` (chừa trên) |
| `motif/` | Vật thể **tách nền** PNG trong suốt (hạc, mai, sen, đèn lồng, điện thoại lục bảo, khối vàng, mặt trống đồng) | `"layers": [{"src": "lib:mo-…", "box": [x, y, w, h]}]` đặt chồng lên nền |
| `overlay/` | Ánh sáng trên nền đen (vệt sáng vàng, kim tuyến) | `"layers": [{"src": "lib:ov-…", "box": [0,0,1,1], "blend": "screen", "cover": true}]` |
| `texture/` | Hoạ tiết vàng tách nền (trống đồng, mây), giấy dó, nhung lục bảo | lớp phủ, nền thông báo |
| `spec.json` | **Danh sách muốn có** (sửa ở đây để thêm asset) | `asset_lib.py build` |
| `index.json` | **Đã có**: thẻ, nguồn + giấy phép (tác giả Unsplash), prompt, số lần dùng, trạng thái | `find`, `pick` |

## Lệnh
```bash
python scripts/asset_lib.py plan                                  # spec + đã có / chưa
python scripts/asset_lib.py build [--only id] [--source codex|unsplash] [--limit N] [--dry-run] [--force]
python scripts/asset_lib.py find --theme emerald --side right --aspect 4:5 --tags "Tết,hoa mai" --season tet
python scripts/asset_lib.py stock-preview <id> [--query "…"]      # 8 ứng viên Unsplash → chọn → stock-pin <id> <photo_id>
python scripts/asset_lib.py add <file> --id … --kind bg --theme … --side … --master tall --tags "…"   # nhập KV đã duyệt vào kho
python scripts/asset_lib.py reject <id> --ly-do "…"                # loại asset xấu (không bị chọn nữa)
python scripts/asset_lib.py sheet                                 # library-sheet.jpg để xem cả kho
```

## Asset lặp lại nhiều (rút từ 14 bài fanpage DSC + 106 ads đối thủ, 24/11/2026)
| Asset | Nguồn thấy | Trong kho |
|---|---|---|
| Số 3D vàng đắp nổi ("2026", "29", ngày lễ) | fanpage F06/F07/F09, ABS, VPBankS, KBSV | **Engine CSS** `"big_style": "gold3d"` (layout `bignum`) — số bất kỳ, 0 quota |
| Lụa cờ đỏ sao vàng | fanpage F00/F02/F09/F10, ABS | `mo-flag-silk`, nền `bg-em-flag-r/-w` |
| Nền lục bảo + nến phát sáng | fanpage F02/F05/F18/F23 | `bg-em-candles-r/-t/-w` |
| Vệt sáng vàng, kim tuyến | fanpage F07/F09/F10 | `ov-gold-swoosh`, `ov-gold-sparkle`, nền `bg-em-goldlight-c` |
| Sao vàng 3D, bồ câu | fanpage F10 | `mo-star-gold`, `mo-doves` |
| Thiết bị màn hình trống (laptop, tay cầm điện thoại/máy tính bảng) | fanpage F04/F08/F18, hầu hết đối thủ | `mo-laptop`, `mo-hand-phone`, `mo-tablet-hands`, `mo-phone-emerald` |
| Bò tót low-poly | fanpage F06 | `mo-bull-glow` |
| Thẻ lịch nghỉ / giao dịch lại | fanpage F01/F07/F10 | _chưa — thành phần HTML (việc sau)_ |
| Logo khoá chữ "DSC SECURITIES" / "DSC \| CÔNG TY CỔ PHẦN CHỨNG KHOÁN DSC" | hầu hết bài fanpage | _cần file gốc từ DSC_ |
Không lấy từ đối thủ: đồng xu 3D, hộp quà, mascot, người mẫu cầm thẻ ưu đãi (motif khuyến mãi — DSC không có ưu đãi).

## Quy tắc
- **Thứ tự lấy nền:** `creative.py pick` (thư viện) → không có thì `creative.py generate` (Codex, tốn quota) → KV quan trọng thì đặt designer.
- **KV mới đã duyệt → `add` vào thư viện** để kho lớn dần sau mỗi chiến dịch.
- **Không lặp:** `pick` ưu tiên asset ít dùng / lâu chưa dùng; không cho 2 ảnh cùng bộ dùng chung 1 nền.
- **Ảnh Unsplash:** Unsplash License — dùng thương mại được, không bắt buộc ghi công; tác giả + link lưu trong `index.json`. Không dùng ảnh có người nhận diện được cho quảng cáo tài chính.
- **Motif tách nền:** Codex vẽ trên nền magenta #FF00FF → chroma key (không cần rembg). Vật có màu hồng/tím sẽ bị ăn mất → tạo lại hoặc đổi màu nền key.
- Mọi asset theo `knowledge/1-brand/DESIGN.md` (lục bảo + vàng / ngà văn hoá; cấm chữ, logo, xu, mũi tên lãi).
