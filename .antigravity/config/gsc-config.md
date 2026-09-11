# Google Search Console API — Hướng dẫn Setup

## Bước 1: Tạo Google Cloud Project & Enable API

1. Vào [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới (hoặc chọn project có sẵn)
3. Vào **APIs & Services → Library**
4. Tìm **"Google Search Console API"** → Enable

## Bước 2: Tạo OAuth2 Credentials

1. Vào **APIs & Services → Credentials**
2. Click **"Create Credentials" → "OAuth client ID"**
3. Application type: **Desktop app**
4. Tải file JSON về → đổi tên thành `gsc-credentials.json`
5. Đặt vào thư mục này: `.antigravity/config/gsc-credentials.json`

> **Lưu ý:** `gsc-credentials.json` và `gsc-token.json` đã được thêm vào `.gitignore` — không bao giờ commit 2 file này.

## Bước 3: Cấu hình site property

Mở file `.antigravity/config/gsc-credentials.json` để xác nhận đúng project.

Sau đó set biến môi trường (hoặc script tự detect):

```bash
# Trong terminal trước khi chạy script
set GSC_SITE=https://www.dsc.com.vn/

# Hoặc truyền trực tiếp
python scripts/sync_gsc.py --site https://www.dsc.com.vn/
```

Site property mặc định nếu không set: `https://www.dsc.com.vn/`

## Bước 4: Chạy lần đầu (Authorization)

```bash
python scripts/sync_gsc.py
```

- Lần đầu: browser tự động mở → đăng nhập Google account có quyền truy cập GSC
- Sau khi authorize: token được lưu tại `.antigravity/config/gsc-token.json`
- Các lần sau: tự động refresh token, không cần thao tác thủ công

## Bước 5: Kiểm tra kết quả

Sau khi chạy thành công:
- `knowledge/raw/gsc/queries.csv` — top queries (page, query, clicks, impressions, ctr, position)
- `knowledge/raw/gsc/pages.csv` — page performance (page, clicks, impressions, ctr, position)

## Các lệnh hữu ích

```bash
# Fetch 30 ngày gần nhất (mặc định, skip nếu cache < 7 ngày)
python scripts/sync_gsc.py

# Fetch 90 ngày
python scripts/sync_gsc.py --days=90

# Bỏ qua cache check, fetch ngay
python scripts/sync_gsc.py --force

# Generate opportunity report từ cache hiện tại
python scripts/process_gsc.py

# Full sync + report (dùng trong /gsc-sync workflow)
python scripts/sync_gsc.py && python scripts/process_gsc.py
```

## Dependencies

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Troubleshooting

| Lỗi | Nguyên nhân | Fix |
|-----|-------------|-----|
| `FileNotFoundError: gsc-credentials.json` | Chưa đặt file credentials | Làm lại Bước 2 |
| `HttpError 403` | Account không có quyền GSC | Dùng account có Verified Owner trong GSC |
| `Token expired` | Token cũ hết hạn | Xóa `gsc-token.json`, chạy lại |
| `No data returned` | Site property sai | Kiểm tra GSC_SITE khớp với property trong GSC |
