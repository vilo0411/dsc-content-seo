# Skill: SEO Drafting (Phase 3 & 4)

Chuyển Outline đã duyệt thành draft. Quy tắc viết nằm ở `anti-ai-rules.md` + `instincts.md` (đã load ở Step 0) — file này chỉ ghi thứ tự làm và những điểm máy sẽ kiểm.

## Step 1: Execute (Drafting & Quality)

1. **Outline** là hợp đồng: `knowledge/4-content/1-outlines/[slug].md`. Vừa viết trong session thì không mở lại.
2. **Viết theo 5 lời hứa của outline** (mỗi lời hứa có check máy ở `qa_lint.py`):
   - **Thesis** là kết luận thật của bài; mọi H2 phục vụ nó.
   - **Information_Gain**: mỗi mục phải xuất hiện đúng ở `h2` đã khai, chứa đúng `proof`, và được giải thích đủ để người đọc dùng được (`IG-missing`). Đây là phần đối thủ không có — viết kỹ nhất ở đây, không phải ở phần ai cũng viết.
   - **Entities**: dùng tự nhiên các thuật ngữ trong `Entities:` (`ENT-missing`, cần ≥ 70%). Viết tắt (UBCKNN, NAV, CTCK…) phải viết đầy đủ ở lần đầu; một thực thể chỉ có một cách viết.
   - **PAA_Questions**: từng câu thành H2/H3 hoặc FAQ, giữ dạng câu hỏi (`PAA-missing`). Không dùng lại H2 / câu FAQ đã có ở bài DSC khác (`DUP-h2`, `DUP-faq`) — link sang bài đó.
   - **Bảng dữ liệu mục 3**: chỉ dùng số trong bảng. Câu trích quy định / số liệu có nguồn thì **link thẳng tới URL nguồn gốc** của dòng đó (domain trong `knowledge/3-pipeline/source-whitelist.md`), anchor là tên văn bản / báo cáo (`SRC-missing`). Không viết "theo khảo sát của DSC" nếu không có số + mốc thời gian (`SRC-unshown`).
3. **Trả lời trước, giải thích sau** (`GEO-h2-answer`): câu đầu dưới mỗi H2 ≤ 40 từ, nhắc đúng đối tượng của heading và trả lời luôn; đọc rời khỏi bài vẫn đủ nghĩa. Dưới H2 dạng "X là gì" mở bằng "X là …" là đúng. Không mở mục bằng câu dẫn ("Trong phần này…", "Để hiểu…").
4. **Trình bày:** đoạn 2–3 câu gộp theo ý (không tách mỗi câu một đoạn), câu ≤ 30 từ. Trước danh sách có câu dẫn kết thúc bằng `:`; nhãn đầu mục viết `**Nhãn**: nội dung`. Link nội bộ theo `Internal_Links:` của outline, URL tuyệt đối `https://www.dsc.com.vn/...`, đặt trong câu.
5. **Bằng chứng thực tế:** bài hướng dẫn thao tác / đánh giá app cần ảnh chụp màn hình thật. Chưa có ảnh → đặt `[ẢNH THỰC TẾ: màn hình cần chụp]` đúng vị trí và báo user (placeholder còn sót ở bản Final là CRITICAL). Bài có nhận định mua/bán mã cụ thể → thêm câu miễn trừ (I113).
6. **Tự soát trước khi chạy gate** — 3 câu hỏi cho từng H2:
   - *So what?* Có câu nói rõ vì sao người đọc cần mục này không.
   - *Prove it:* nhận định nào ("quan trọng", "hiệu quả", "đáng kể", "nhiều") chưa có số / ví dụ → thay bằng số trong bảng dữ liệu hoặc xoá.
   - *Load-bearing:* có ít nhất 1 câu gồm thực thể + con số + mốc thời gian (anti-ai-rules §8.2). Mốc thời gian chỉ gắn với số liệu, không gắn trước định nghĩa (§8.3).
7. **Gate:** `python scripts/qa_gate.py knowledge/4-content/2-drafts/Draft-[slug].md --fix` → Quality Guardian (xem `.antigravity/skills/qa-qc/SKILL.md`).
8. **Trình bày cho user — tóm tắt ≤ 25 dòng + đường dẫn file draft, không dán bài vào chat:** dòng kết quả gate (score · coverage · trust · slop), từng mục Information_Gain kèm 1 câu trích, số từ so với target, ảnh thực tế còn thiếu, `⚠️ Remaining issues` nếu có.

## Step 2: Finalize & Learn

Sau khi user `/approve`: làm đúng trình tự ở `.agents/skills/approve/SKILL.md` (nguồn duy nhất cho move file, snapshot, status, HTML CMS, log, feedback loop).
