# Skill: Content Feedback Loop (Learning & Synthesis)

This skill is the "Brain" of the project. It ensures that the system never makes the same mistake twice by analyzing the history of user feedback and manual revisions.

## 🛠️ Execution Strategy: Analyze-Synthesize-Update

This skill is triggered after the FINAL `/approve` of an article.

### Step 1: Historical Audit (Multi-version Analysis)
1. **Gather Data**: `python scripts/article_snapshot.py <slug> --diff` (bản trình duyệt ở Gate 2 → Final; `--from gate2.prev` nếu có nhiều vòng) + phản hồi của user trong chat. Không mở cả hai bài.
2. **Diff Analysis**: Identify consistent manual changes made by the user or requested in feedback.
3. **Pattern Recognition**:
   - What words/phrases does the user consistently remove?
   - What structure/tone does the user consistently ask for?
   - What factual corrections were made?

### Step 2: Synthesis of Rules
1. **Rule Generation**: Convert identified patterns into actionable instructions.
   - Example: "User removed 'Trong kỷ nguyên số' 3 times" -> Rule: Add to `Anti_AI_Flags`.
   - Example: "User asked for more 'Specific Statistics' in every H2" -> Rule: Update `brief-template.md` requirements.
2. **Persona Update**: Adjust the writing persona if the feedback relates to Tone (e.g., "Too formal").

### Step 3: Knowledge Base Update

**Cổng nhận rule (bắt buộc, hỏi từng bài học):**
1. *"Lỗi này có lặp lại ở một bài KHÁC chủ đề không?"* Không → **không tạo rule**. Ghi vào `revision-log.md` là đủ. Chi tiết nội dung riêng của một bài (bảng GRDP các tỉnh, mã BCM/KBC, số liệu bài X) không bao giờ là rule.
2. *"Máy có bắt được không?"* (regex, đếm, cấu trúc) Có → thêm check vào `qa_lint.py` / `outline_lint.py` / `slop_check.py`, hoặc thêm cụm từ vào `anti-ai-rules-blacklist.md`. Rule chỉ còn 1 dòng với `Checklist:` + `Máy kiểm: full`.
3. *"Đã có rule cùng chủ đề chưa?"* Tra `python scripts/optimize_instincts.py --show <tag>` (tag đang dùng: sapo, van-phong, heading, cau-ngan, moc-thoi-gian, so-lieu, dsc-san-pham, product-bridge, ket-luan, banner, trinh-bay, dinh-dang, link, intent, how-to, toplist, optimize, phan-hoi, nen-tang + 1 tag mỗi topic). Có → **sửa rule đó tại chỗ (giữ ID)**, không thêm rule mới. Phản hồi mới mâu thuẫn rule cũ → sửa rule cũ theo phản hồi mới, ghi ngày vào `Cập nhật:`. Chỉ hỏi user khi phản hồi mơ hồ.

| Loại bài học | Ghi vào |
| :--- | :--- |
| Cụm từ cấm / pattern regex | `anti-ai-rules-blacklist.md` hoặc check trong lint |
| Judgment call lặp lại được ở bài khác | `instincts-archive.md` (thêm mới hoặc sửa rule cùng Tag) |
| Raw event (bài nào, ngày nào, sửa gì, chi tiết nội dung riêng) | `revision-log.md` — luôn ghi, qua `python scripts/revision_log.py add …` (không mở file) |

**Format rule (archive):**
```
### [Tên ngắn — 1 chủ đề, không ghép "A & B & C"]
- **ID:** I0xx                         (rule mới: số lớn nhất + 1; sửa rule cũ: giữ ID)
- **Trạng thái:** ACTIVE
- **Tag:** sapo | product-bridge | heading | so-lieu | faq | link | cta | toplist | ...
- **Nguồn:** [slug]
- **Phản hồi từ User:** "[quote gốc — giữ nguyên, nối thêm khi sửa rule]"
- **Bản năng:** [tối đa 3 ý, tổng ≤ 450 ký tự, viết thành hành động. Không kể lại bài đã sửa gì.]
- **Phạm vi:** Global | Chỉ topic: X   (rule chỉ đúng với 1 chủ đề → Chỉ topic, không để Global)
- **Checklist:** qa_lint:CL2-softban    (nếu có check máy liên quan)
- **Máy kiểm:** full | partial
- **Cập nhật:** YYYY-MM-DD
```
Rule bị thay hẳn → `Trạng thái: DEPRECATED` + `Thay bởi: I0xx`. Không xoá khỏi archive.

**Đồng bộ + gate:** `python scripts/optimize_instincts.py --check`. Script không bao giờ cắt rule. Nó báo `LONG` (rule > 450 ký tự), `TAG-DUP` (2 rule ACTIVE cùng tag + phạm vi), `BUDGET` (`instincts.md` > 8.000 ký tự), `ORPHAN`, `SUPERSEDE`. Còn báo lỗi → sửa archive rồi chạy lại. **Không sửa tay `instincts.md`.**

**Đo hiệu quả:** `qa_lint.py --log` (chạy trong `/approve`) ghi từng check vào `knowledge/3-pipeline/qa-check-log.csv`. `python scripts/optimize_instincts.py --stats` cho biết check của mỗi rule còn bắn ở bao nhiêu bài sau ngày `Cập nhật`. Còn bắn → rule chưa hiệu quả, cần viết lại hoặc chuyển thành lint. Nhiều tháng không bắn và rule có `Máy kiểm: full` → ứng viên rút khỏi core.

4. **Report to User**: *"Đã học X bài học — Y rule sửa tại chỗ (ID…), Z rule mới, W bài học chỉ ghi revision-log (không qua cổng)."*

## 🚦 Triggers
- Triggered automatically after a final `/approve` command.
- Can be triggered manually with `/learn [article_path]` to analyze a specific history.

## ⚠️ Critical Rule
- **No Over-generalization**: A one-time correction might be topic-specific. Only synthesize into a "General Rule" if the pattern is repeated or explicitly stated as a global preference.
- **Một nguồn rule:** rule viết bài chỉ nằm trong archive/instincts (agent Antigravity, Cursor… đều đọc được). Không lưu rule viết bài vào memory riêng của một công cụ (Claude auto-memory) — memory chỉ trỏ về ID rule.
