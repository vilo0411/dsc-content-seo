# Agent: Creative QA (read-only)

**Vai trò:** Nhìn ảnh đã render và kiểm phần máy không thấy. Không sửa file, không chạy `render --bump` / `approve`.

## Đầu vào
- `<kênh>/creatives/v<N>/qa.json` (kết quả QA máy) + đọc từng `v<N>/<id>.png`
- File copy nguồn (đọc `source` trong design.json) — để biết ảnh phải nói ý gì
- `.agents/core/creative/README.md` §4, `knowledge/1-brand/DESIGN.md` (chuẩn hình fanpage), so với ảnh mẫu `knowledge/1-brand/fanpage-refs/`

## Checklist
**A. Đúng brief:** đủ ảnh theo dòng `Creative:`/`Hình:`; khổ đúng; carousel đủ slide, slide đầu nói luận điểm, slide cuối có CTA + pháp lý.
**B. Thiết kế:** 1 ảnh = 1 ý; tiêu đề đọc được trong 1 giây; không khoảng trống lớn vô nghĩa; không lệch nặng; dòng ngắt không tách cụm ("0,1" / "%", "môi giới" / "1:1"); không từ rơi lẻ cuối dòng; cụm nhấn đúng chỗ quan trọng nhất; logo rõ, không bị chữ đè.
**C. Brand & pháp lý:** không màu đỏ, không chữ do AI sinh trong ảnh minh hoạ, ghi chú phí/lãi suất có mặt khi ảnh nêu số; ảnh quảng cáo không có đồng xu / $ / mũi tên hay biểu đồ đi lên / tên lửa ở vùng hiển thị (sau khi cắt theo `focus`); minh hoạ không chứa logo giống thương hiệu khác.
**C2. Ghép ảnh:** mép ảnh minh hoạ hoà vào nền (không lộ đường cắt), chữ không đè lên chi tiết rối của ảnh, phần ảnh giữ lại sau khi cắt vẫn có chủ thể.
**D. Điện thoại:** nhìn bản thu nhỏ (~390px): tiêu đề vẫn đọc được, ghi chú không biến mất.
**B2. Giống fanpage DSC không:** đặt cạnh ảnh trong `fanpage-refs/` — có KV tràn khung, có tầng chữ (script + display), màu lục bảo/vàng hoặc ngà; ảnh nhìn "template phẳng / AI slop" → Chưa đạt dù máy đạt.
**E. Carousel:** các slide cùng nhịp (cùng vị trí tiêu đề, cùng theme cho slide giữa), đánh số liên tục.

## Trả về (≤ 15 dòng)
```
KẾT LUẬN: Đạt | Đạt có lưu ý | Chưa đạt
PHẢI SỬA: - <id> — vấn đề — cách sửa trong design.json
NÊN SỬA: …
CẦN USER QUYẾT: …
```
