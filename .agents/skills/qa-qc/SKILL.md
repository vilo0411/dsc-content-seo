---
name: qa-qc
description: "QA độc lập cuối (Quality Guardian + Brand Guardian): ngữ nghĩa, persona, fact, nguồn — chỉ chạy SAU khi python scripts/qa_gate.py đã PASS. Dùng trước khi trình draft để duyệt hoặc khi user yêu cầu review chất lượng bài."
---

# Skill: Independent Quality Assurance (QA/QC)

> Skill này là entry point cho quy trình QA. Execution chi tiết nằm trong `.agents/skills/qa-qc/references/quality-guardian.md`.

---

## Khi nào dùng skill này

- Sau khi draft hoàn thành, trước khi submit cho user review
- Khi user yêu cầu audit một bài đã có
- Khi re-audit sau khi sửa lỗi từ báo cáo FAIL trước

---

## Quy trình thực thi

Mỗi phần chỉ có 1 nguồn — file này không chép lại:

| Bước | Làm gì | Nguồn chi tiết |
|---|---|---|
| 1. Gate máy (tầng A + B + dữ liệu) | `python scripts/qa_gate.py <draft>` (tự tìm outline; `--fix` sửa lỗi cơ học; bài optimize thêm `--original Final-<slug>.md`). FAIL → sửa **đúng dòng được báo**, không viết lại cả bài, chạy lại đúng lệnh này | `scripts/README.md` |
| 2. Tầng C — checklist ngữ nghĩa | Quality Guardian: CL1–CL9 + truy từng mục Information_Gain. Chỉ chạy khi gate PASS, dùng output gate đã có, không chạy lại lint | `.agents/skills/qa-qc/references/quality-guardian.md` |
| 3. Vòng lặp | Tối đa 2 vòng sửa. Vòng 2 QG chỉ đọc `qa_gate.py <draft> --changed`. Còn FAIL → dừng, trình bày kèm `⚠️ Remaining issues` | `AGENTS.md` §2 |
| 4. Finalize | Chỉ sau PASS + user `/approve` | `.agents/skills/approve/SKILL.md` |

**PASS** = gate exit 0 (0 CRITICAL, 0 MAJOR, slop ≥ 80) **và** 0 CRITICAL + 0 MAJOR ngữ nghĩa. Có MINOR → PASS with notes.

Điểm gate gồm 2 nhóm: hình thức (`anti_ai`, `readability`, `seo`, `link`, `geo`) và **thực chất** (`coverage`: thuật ngữ đối thủ, Information_Gain, PAA, trùng lặp · `trust`: nguồn gốc, miễn trừ, bằng chứng thực tế, hằng số DSC). Bài sạch hình thức nhưng `coverage` / `trust` thấp là bài chưa có lý do để rank — báo rõ 2 điểm này cho user.

## Gotchas

- **Tin tưởng mù quáng Main Agent:** luôn đối chiếu draft với outline gốc — hay bỏ section hoặc đổi angle mà không báo.
- **Không có outline:** gate in cảnh báo; Information_Gain / PAA không được kiểm → báo user, không ghi PASS.
- **Fact-check:** số liệu DSC theo `profile.md`; quy định / phí / hạn mức đối chiếu với URL nguồn đã khai trong outline, không tra cứu tự do.
- **Lặp lại việc của máy bằng mắt:** đếm câu, tìm từ cấm, đếm thuật ngữ… là việc của script.
- **Sửa thay vì báo cáo:** Quality Guardian chỉ audit và báo lỗi có số dòng.
