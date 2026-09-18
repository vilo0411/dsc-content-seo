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
  - **Anchor text gợi ý:** `mở tài khoản chứng khoán`, `mở tài khoản chứng khoán online`, `mở tài khoản trực tuyến eKYC tại DSC`, `mở tài khoản eKYC tại DSC`.
  *(Lưu ý: Không nhầm lẫn với bài blog kiến thức target key "cách mở tài khoản chứng khoán" có slug `/kien-thuc/cach-mo-tai-khoan-chung-khoan`).*

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
   Output: bài nguồn + số dòng + trích đoạn có thể chèn anchor, ưu tiên bài có clicks GSC cao (nếu có `knowledge/raw/gsc/pages.csv`).
2. **Update:** Chỉ mở đúng file/dòng script chỉ ra, chèn anchor lấy từ chính câu trong trích đoạn.
3. **Register Index:** Cập nhật ngay bài viết mới vào `knowledge/3-pipeline/anchor-index.md` (chèn 1 dòng vào cluster phù hợp, không đọc cả file) kèm theo URL chính thức trên sitemap.

### Mode: Audit (Health Check)
1. **Execute Script:** Chạy `python .antigravity/skills/internal-linking/scripts/link_audit.py --orphans`.
2. **Analyze Dashboard:** Xem báo cáo tại `knowledge/3-pipeline/internal-link-dashboard.md` (chỉ tính link giữa các file trong `3-finalized/`).
3. **Fix Issues:** Với mỗi orphan → `find_links.py --backfill [slug]`; với "Over-exact" → đa dạng hoá anchor.

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
