# Quy tắc đặt link trong bài

Áp dụng cho mọi bài mới / optimize (từ đợt sửa cụm Mở TK & Cách chơi, 2026-10-30). Nguồn duy nhất — `/drafting`, `/write`, `/optimize`, `/link` đọc file này thay vì cả `internal-linking/SKILL.md`.

Ứng viên link: `python scripts/find_links.py "<keyword>" --top 8 --exclude <slug>` — chỉ dùng URL có cột Sitemap ✓, chép nguyên URL script in ra (không tự đoán slug, không thêm `/` cuối). `qa_lint.py` đối chiếu sitemap (`LINK-sitemap`).

1. **Link nằm trong câu có lập luận, không đứng riêng.** Anchor là một phần ý của câu. CẤM dòng `>> Xem thêm: …` / danh sách tiêu đề bài (qa_lint `LINK-xemthem`, MAJOR) và câu chỉ để trỏ đi kiểu "bạn có thể tham khảo bài …", "đọc thêm bài viết …" (`LINK-pointer`).
2. **Ưu tiên gắn link vào cụm từ có sẵn** trong đoạn — chỉ bọc anchor, không đổi chữ. Không có cụm phù hợp mới viết thêm **1 câu** nối tiếp ý của chính đoạn/mục đó: ≤30 từ, ghép cuối đoạn nếu đoạn còn ≤3 câu, ngược lại tách thành đoạn mới ngay sau.
3. **Link đúng section:** đặt link tới bài con ở H2/H3 đang nói về chủ đề đó, không gom cuối bài. **Không mặc định ghép vào đoạn Kết luận/CTA** (câu "xem hướng dẫn ở bài riêng" dính sau CTA đọc như phần thêm). Tìm đoạn thân bài mà nội dung dẫn tới bài đích (chỗ người đọc sắp hành động: bước vào lệnh, danh sách Lưu ý, cụm từ có sẵn chưa gắn link); không có chỗ hợp thì bỏ bài đó.
4. **Pillar – hub – spoke** (registry: `knowledge/3-pipeline/internal-links/link-clusters.json`):
   - Bài là hub/spoke của 1 cụm → **bắt buộc** link về pillar (`LINK-pillar`, MAJOR), anchor lấy từ `pillar_anchors`.
   - Spoke trong group có hub → link về hub (`LINK-hub`, MINOR).
   - Pillar link xuống từng hub/spoke ở đúng section nói về chủ đề đó.
   - Anchor trùng `pillar_keyword` / `pillar_anchors` (vd. "cách mở tài khoản chứng khoán", "cách chơi chứng khoán cho người mới") **chỉ được trỏ về pillar** đó (`LINK-pillar-anchor`, MAJOR).
5. **Bài mới thuộc cụm đã có:** khi outline được approve, thêm slug vào `spokes` của đúng group trong `link-clusters.json`, và chạy `find_links.py --backfill <slug>` để pillar/hub link xuống bài mới sau khi publish.
6. **Cụm mới** (topical map mới): thêm 1 object vào `clusters` (id, pillar, pillar_keyword, pillar_anchors, groups) — qa_lint tự áp dụng.
