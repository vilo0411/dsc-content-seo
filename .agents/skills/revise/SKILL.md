---
name: revise
description: Sửa nội dung bài viết theo yêu cầu chat — có context load bắt buộc.
---

# Chỉnh Sửa Bài Viết (Revise)

## Nhiệm vụ
Chỉnh sửa một đoạn / section cụ thể trong bài viết theo yêu cầu của người dùng, đảm bảo bản sửa không vi phạm anti-ai-rules.

---

## Bước 0: Context Load (BẮT BUỘC — đọc đủ 4 file trước khi chạm vào bất kỳ nội dung nào)

1. `knowledge/3-pipeline/anti-ai-rules.md` — toàn bộ, không skip section nào
2. `.antigravity/memory/instincts.md` — lỗi đã học từ các vòng sửa trước
3. `knowledge/3-pipeline/glossary.md` — thuật ngữ chuẩn thương hiệu
4. File cần sửa (Draft hoặc Final tương ứng với slug)

---

## Bước 1: Xác định phạm vi sửa

Xác nhận với người dùng:
- **File:** `[path/to/file]`
- **Phạm vi:** `[section / heading / đoạn cụ thể người dùng yêu cầu]`
- **Yêu cầu:** `[mô tả lại yêu cầu sửa của người dùng để tránh hiểu nhầm]`

Nếu người dùng không chỉ rõ slug hoặc section → hỏi lại trước khi làm.

---

## Bước 2: Viết bản sửa

- Chỉ sửa đúng phạm vi được yêu cầu. Không chạm vào phần còn lại của bài.
- Áp dụng quy tắc 3S: Specific · Story · Statistics — không viết vague.
- Tone: đúng Persona của bài (đọc từ Content Strategy Header hoặc hỏi user nếu không rõ).

---

## Bước 3: Self-Audit (BẮT BUỘC trước khi trình bày bản sửa)

**3a. Lint máy** — sau khi ghi bản sửa vào file (hoặc vào file tạm), chạy:
```bash
python scripts/qa_lint.py [path/to/file]
```
Lint bắt: blacklist trigger phrases, emphatic quotes, hedge words, forbidden terms, câu > 30 từ, đoạn > 3 câu, link sai, mốc thời gian mơ hồ… Nếu bản sửa tạo thêm CRITICAL/MAJOR ở các dòng vừa sửa → sửa ngay. (Lỗi có sẵn ở phần khác của bài không thuộc phạm vi — chỉ báo cho user.)

**3b. Đọc lại bằng mắt** (phần lint không làm được):
- [ ] Câu đầu không phải opener vĩ mô (nếu sửa mở bài)
- [ ] Câu kết không phải summary/closer AI (nếu sửa kết bài)
- [ ] Mọi số liệu có nguồn + thời điểm hoặc ghi `[CẦN XÁC NHẬN]`
- [ ] Đúng Persona / Product Bridge của bài

---

## Bước 4: Trình bày

Trình bày bản sửa dưới dạng diff rõ ràng:

```
❌ BẢN CŨ:
[đoạn gốc]

✅ BẢN SỬA:
[đoạn mới]
```

Sau đó hỏi: *"Bạn muốn ghi đè vào file hay cần chỉnh thêm?"*

Chỉ ghi đè vào file khi người dùng xác nhận.
