---
name: Internal Linking & Audit
description: >
  Use this skill when the user needs to build a strong internal link architecture, 
  validate links against live sitemaps, or audit the health of existing links. It ensures that 
  the content ecosystem is interconnected, boosting SEO authority, conversion, and user navigation.
---

# Skill: Internal Linking & Audit

## 🛠️ Procedures

### 🎯 Quy tắc Bắt buộc: Mandatory Conversion Link (Mở tài khoản DSC)
- **100% bài viết trong toàn bộ hệ thống** bắt buộc phải có ít nhất **01 link chuyển đổi** dẫn trực tiếp về trang **Mở tài khoản chứng khoán DSC**:
  - **URL mục tiêu chính thức:** `https://www.dsc.com.vn/mo-tai-khoan`
  - **Vị trí đặt:** Phần Product Bridge (H2 giải pháp DSC) hoặc đoạn Kết luận (Call to Action).
  - **Anchor text BẮT BUỘC có "DSC":** `mở tài khoản DSC`, `mở tài khoản tại DSC`, `mở tài khoản eKYC tại DSC`, `mở tài khoản DSC online`. Đổi anchor cũ: có "DSC" thì bỏ "chứng khoán" (`mở tài khoản chứng khoán tại DSC` → `mở tài khoản tại DSC`); không có "DSC" thì thay bằng DSC (`mở tài khoản chứng khoán` → `mở tài khoản DSC`). *(qa_lint `LINK-cta-anchor`; nút banner HTML không áp dụng.)*
  *(Lý do: anchor đúng từ khóa "cách mở tài khoản chứng khoán" dành cho bài pillar `/kien-thuc/cach-mo-tai-khoan-chung-khoan` — link landing mà dùng anchor từ khóa sẽ tranh tín hiệu với pillar.)*

### 📐 Quy tắc đặt link trong bài (từ đợt sửa cụm Mở TK & Cách chơi, 2026-10-30 — áp dụng cho mọi bài mới/optimize)
1. **Link nằm trong câu có lập luận, không đứng riêng.** Anchor là một phần ý của câu. CẤM dòng `>> Xem thêm: …` / danh sách tiêu đề bài (qa_lint `LINK-xemthem`, MAJOR) và câu chỉ để trỏ đi kiểu "bạn có thể tham khảo bài …", "đọc thêm bài viết …" (`LINK-pointer`).
2. **Ưu tiên gắn link vào cụm từ có sẵn** trong đoạn — chỉ bọc anchor, không đổi chữ. Không có cụm phù hợp mới viết thêm **1 câu** nối tiếp ý của chính đoạn/mục đó: ≤30 từ, ghép cuối đoạn nếu đoạn còn ≤3 câu, ngược lại tách thành đoạn mới ngay sau.
3. **Link đúng section:** đặt link tới bài con ở H2/H3 đang nói về chủ đề đó, không gom cuối bài.
4. **Pillar – hub – spoke** (registry: `knowledge/3-pipeline/internal-links/link-clusters.json`):
   - Bài là hub/spoke của 1 cụm → **bắt buộc** link về pillar (`LINK-pillar`, MAJOR), anchor lấy từ `pillar_anchors`.
   - Spoke trong group có hub → link về hub (`LINK-hub`, MINOR).
   - Pillar link xuống từng hub/spoke ở đúng section nói về chủ đề đó.
   - Anchor trùng `pillar_keyword` / `pillar_anchors` (vd. "cách mở tài khoản chứng khoán", "cách chơi chứng khoán cho người mới") **chỉ được trỏ về pillar** đó (`LINK-pillar-anchor`, MAJOR).
5. **Bài mới thuộc cụm đã có:** khi outline được approve, thêm slug vào `spokes` của đúng group trong `link-clusters.json`, và chạy `find_links.py --backfill <slug>` để pillar/hub link xuống bài mới sau khi publish.
6. **Cụm mới** (topical map mới): thêm 1 object vào `clusters` (id, pillar, pillar_keyword, pillar_anchors, groups) — qa_lint tự áp dụng.

### Mode: Live Sitemap Extraction & Verification (BẮT BUỘC KHÔNG NHẦM LẪN)
1. **Sync Live Sitemap (Tự động):** Trước khi tạo outline hoặc viết draft có chèn internal link, BẮT BUỘC phải đồng bộ dữ liệu sitemap live bằng cách:
   - Chạy script: `python .antigravity/skills/internal-linking/scripts/sync_sitemap.py`
   - Hoặc đọc danh sách URL chính xác từ `.antigravity/skills/internal-linking/scripts/sitemap-cache.json` (được cào từ `https://www.dsc.com.vn/sitemap/sitemap_knowledge.xml`).
2. **Đối soát URL chính xác tuyệt đối:**
   - Tuyệt đối KHÔNG tự suy đoán slug hoặc đoán định dạng URL.
   - Tuyệt đối KHÔNG tự thêm dấu gạch nối cuối `/` nếu URL trên sitemap không có.
   - Tuyệt đối KHÔNG sử dụng đường dẫn cục bộ (dạng `file:///...` hoặc `Final-[slug].md`).
   - 100% URL internal link phải khớp chính xác từng ký tự với URL trên sitemap live (ví dụ: `https://www.dsc.com.vn/kien-thuc/chi-so-ebit-la-gi` thay vì `/ebit-la-gi/`).
3. **Chọn Anchor Text Tự nhiên:** Chọn từ khóa đại diện chuẩn cho bài viết đích, xuất hiện tự nhiên trong mạch văn mà không gây gượng ép.

### Mode: Contextual Insertion (During Drafting & Optimization)
1. **Identify Targets — KHÔNG đọc `anchor-index.md` (180 KB):**
   ```bash
   python scripts/find_links.py "[keyword chính]" --top 8 --exclude [slug]
   python scripts/find_links.py "[keyword phụ từ outline]" --top 5 --exclude [slug]   # nếu cần
   ```
   Script đã đối soát với `sitemap-cache.json` — chỉ dùng dòng có cột **Sitemap ✓**. Nếu ✗ → chạy `sync_sitemap.py` rồi thử lại, hoặc bỏ URL đó.
2. **Find Opportunities:** Tìm các cụm từ khóa có liên hệ logic trong nội dung nháp.
3. **Insert Links:** Đặt link vào anchor text phù hợp (tối đa 1 link trên 100 - 150 từ, tránh nhồi nhét).
4. **Verify:** `qa_lint.py` sẽ tự bắt URL không khớp sitemap, link relative/local, thiếu link mở tài khoản, anchor "Xem thêm".

### Mode: Backfill (After Publishing)
1. **Source Search — 1 lệnh, không đọc file Final nào:**
   ```bash
   python scripts/find_links.py --backfill [slug] --top 5
   ```
   Output: bài nguồn **trên site live** + mục H2 + đoạn có thể bọc anchor, ưu tiên bài có clicks GSC cao (nếu có `knowledge/raw/gsc/pages.csv`). Bài chỉ đang link qua dòng Xem thêm được ghi chú → chuyển link đó vào câu.
2. **Update:** Sửa trên CMS — bọc anchor quanh cụm có sẵn trong đoạn script chỉ ra (HTML hiện tại: `knowledge/raw/live/html/<slug>.html`). Xong chạy `python scripts/sync_live.py --only <các slug nguồn>`.
3. **Register Index:** Cập nhật ngay bài viết mới vào `knowledge/3-pipeline/internal-links/anchor-index.md` (chèn 1 dòng vào cluster phù hợp, không đọc cả file) kèm theo URL chính thức trên sitemap.

### Mode: Live Snapshot (sau khi sửa trên CMS)
Bản publish là nguồn sự thật — CSV Screaming Frog / file Final có thể đã cũ. Snapshot thân bài live nằm ở `knowledge/raw/live/` (git-tracked):
```bash
python scripts/sync_live.py --only slug1,slug2     # sau khi sửa vài bài trên CMS (~2s/bài)
python scripts/sync_live.py                        # toàn bộ sitemap (~3-4 phút, 6 luồng)
python scripts/sync_live.py --from-sf export.csv   # dựng từ export custom extraction của Screaming Frog
python scripts/sync_live.py --show <slug>          # link vào/ra của 1 bài (kind: contextual / xem-them / cta)
git diff --word-diff knowledge/raw/live/html/<slug>.html   # so bản live mới với lần sync trước
```
- Lập kế hoạch sửa link cho bài đã publish → lấy HTML "trước" từ `knowledge/raw/live/html/<slug>.html`, không từ CSV cũ.
- `links.csv` cột `kind=xem-them` = danh sách bài còn dòng "Xem thêm" cần viết lại; `pages.csv` cột `in_contextual=0` = bài chưa có link ngữ cảnh trỏ vào.
- Sync xong thì commit `knowledge/raw/live/` để mốc so sánh lần sau.
- `--compare <slug>` = Final-*.md vs live: link chỉ có trên live (thêm trên CMS — phải giữ) + độ lệch văn bản. Bắt buộc trước `/optimize`.

**Khi nào chạy:**
| Lúc | Lệnh |
|---|---|
| Vừa sửa/publish bài trên CMS (cuối mỗi phiên sửa) | `sync_live.py --only <các slug đã sửa>` |
| Trước `/optimize [slug]` | `sync_live.py --only [slug]` + `--compare [slug]` (đã nằm trong skill optimize) |
| Trước khi lập kế hoạch link / backfill / audit cụm | full `sync_live.py` nếu snapshot > 7 ngày (`find_links --backfill` in cảnh báo tuổi snapshot), rồi `link_audit.py` |
| Định kỳ | full sync mỗi tuần (bắt cả sửa của người khác trên CMS, bài mới/bị gỡ), commit `knowledge/raw/live/` |

### Mode: Audit (Health Check)
1. **Execute Script:** Chạy `python .antigravity/skills/internal-linking/scripts/link_audit.py --orphans`.
2. **Analyze Dashboard:** `knowledge/3-pipeline/internal-links/dashboard.md` — tính trên **toàn site live**: tuân thủ cụm (thiếu link pillar/hub), bài 0 inlink ngữ cảnh, bài còn Xem thêm, anchor trùng trỏ nhiều đích. Người xem dùng `internal-links/link-graph.html` (graph + bảng sắp xếp được).
3. **Fix Issues:** Orphan → `find_links.py --backfill [slug]`; thiếu link pillar → thêm câu có link pillar khi optimize bài đó; anchor trùng → mỗi anchor một đích.

---

## 🚦 Success Assertions
- [ ] Mỗi bài viết có tối thiểu 3 - 5 internal links trỏ tới các bài viết liên quan trong hệ sinh thái DSC.
- [ ] **BẮT BUỘC:** Có ít nhất 01 internal link dẫn về trang mở tài khoản chứng khoán DSC (`https://www.dsc.com.vn/mo-tai-khoan`).
- [ ] **BẮT BUỘC:** 100% internal links và conversion links trong bài viết phải dùng **Absolute URL đầy đủ** (`https://www.dsc.com.vn/kien-thuc/[slug]` hoặc `https://www.dsc.com.vn/mo-tai-khoan`).
- [ ] 100% URL internal link được đối soát và khớp từng ký tự với `sitemap-cache.json` / `sitemap_knowledge.xml`.
- [ ] Không có link gãy (404), anchor text phong phú.
- [ ] Định dạng CMS chuẩn: Tuyệt đối không dùng lưu đồ ASCII Art (`+---+`) hoặc LaTeX formulas trong bài viết.

---

## ⚠️ Gotchas
- **Tự đoán Slug/URL:** Tự bịa slug hoặc dùng slug khác với URL thực tế trên sitemap.
- **Tự thêm dấu `/` ở cuối URL:** Sitemap của DSC chuẩn không có `/` ở cuối các đường dẫn `/kien-thuc/[slug]`.
- **Dùng Relative Path:** Dùng dạng `/kien-thuc/...` hoặc `/mo-tai-khoan` thay vì Absolute URL đầy đủ `https://www.dsc.com.vn/...`.
- **Thiếu link Mở tài khoản:** Quên chèn link mở tài khoản ở phần kết/CTA. *Đây là conversion path bắt buộc của mọi bài SEO.*
