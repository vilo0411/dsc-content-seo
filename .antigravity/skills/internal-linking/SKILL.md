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

### Mode: Live Sitemap Extraction & Verification (MANDATORY / BẮT BUỘC)
1. **Fetch & Parse Sitemap:** Khi thực hiện chèn internal link (cho cả quá trình Drafting và Optimization), BẮT BUỘC phải dùng công cụ đọc URL để lấy danh sách URL trực tiếp từ sitemap:
   `https://www.dsc.com.vn/sitemap/sitemap_knowledge.xml`
   Tuyệt đối KHÔNG tự ý suy diễn slug, KHÔNG sử dụng đường dẫn file cục bộ (dạng `file:///...` hoặc `Final-[slug].md`) trong bài viết. 100% link nội bộ và link chuyển đổi trong bài viết phải dùng URL tuyệt đối trực tiếp của website (dạng `https://www.dsc.com.vn/kien-thuc/[slug]`).
2. **Đối soát URL thực tế:** Đối chiếu tên file/slug muốn liên kết với danh sách URL thực tế từ sitemap để lấy URL chuẩn xác nhất trên website (ví dụ: bài viết local tên `Final-rsi-la-gi.md` thực tế trên sitemap live có URL là `https://www.dsc.com.vn/kien-thuc/chi-so-rsi-la-gi`).
3. **Chọn Anchor Text Tự nhiên:** Chọn từ khóa đại diện chuẩn cho bài viết đích, xuất hiện tự nhiên trong mạch văn mà không gây gượng ép.


### Mode: Contextual Insertion (During Drafting & Optimization)
1. **Identify Targets:** **KHÔNG đọc toàn bộ `anchor-index.md`**. Dùng Grep tìm trong `knowledge/3-pipeline/anchor-index.md` với từ khóa liên quan đến topic (2–3 lần grep với các term khác nhau) để lấy 3–5 bài phù hợp nhất. Đối soát URL với Sitemap DSC nếu cần xác nhận slug live.
2. **Find Opportunities:** Tìm các cụm từ khóa có liên hệ logic trong nội dung nháp.
3. **Insert Links:** Đặt link vào anchor text phù hợp (tối đa 1 link trên 100 - 150 từ, tránh nhồi nhét).

### Mode: Backfill (After Publishing)
1. **Source Search:** Quét `knowledge/4-content/3-finalized/` để tìm các bài cũ có thể trỏ ngược lại bài viết mới vừa xuất bản (tạo liên kết 2 chiều).
2. **Update:** Bổ sung anchor text và link vào bài cũ một cách tự nhiên.
3. **Register Index:** Cập nhật ngay bài viết mới vào `knowledge/3-pipeline/anchor-index.md`.

### Mode: Audit (Health Check)
1. **Execute Script:** Chạy `python .antigravity/skills/internal-linking/scripts/link_audit.py`.
2. **Analyze Dashboard:** Xem báo cáo tại `knowledge/3-pipeline/internal-link-dashboard.md`.
3. **Fix Issues:** Khắc phục tình trạng "Orphan pages" (bài không có link trỏ tới) hoặc "Over-optimized anchors".

---

## 🚦 Success Assertions
- [ ] Mỗi bài viết có tối thiểu 3 - 5 internal links trỏ tới các bài viết liên quan trong hệ sinh thái DSC.
- [ ] **BẮT BUỘC:** Có ít nhất 01 internal link dẫn về trang mở tài khoản chứng khoán DSC (`https://www.dsc.com.vn/mo-tai-khoan`).
- [ ] **BẮT BUỘC:** 100% internal links và conversion links trong bài viết phải dùng **Absolute URL đầy đủ** (`https://www.dsc.com.vn/kien-thuc/[slug]` hoặc `https://www.dsc.com.vn/mo-tai-khoan`), không dùng relative path `/kien-thuc/...`.
- [ ] 100% URL internal link được đối soát từ Sitemap live (`sitemap_knowledge.xml`) hoặc `anchor-index.md`.
- [ ] Không có link gãy (404), anchor text phong phú (Exact vs. Partial vs. Topical Phrase).
- [ ] Định dạng CMS chuẩn: Tuyệt đối không dùng lưu đồ ASCII Art (`+---+`) hoặc LaTeX formulas trong bài viết vì gây lỗi vỡ khung giao diện trên CMS. Sử dụng bảng Markdown hoặc danh sách có cấu trúc.

---

## ⚠️ Gotchas
- **Dùng Relative Path:** Dùng dạng `/kien-thuc/...` hoặc `/mo-tai-khoan` thay vì Absolute URL đầy đủ `https://www.dsc.com.vn/...`.
- **Thiếu link Mở tài khoản:** Quên chèn link mở tài khoản ở phần kết/CTA. *Đây là conversion path bắt buộc của mọi bài SEO.*
- **Lưu đồ ASCII trong Code Block:** Không bao giờ dùng ASCII flowchart/diagram trong cặp dấu ``` vì CMS không hỗ trợ co giãn và gây vỡ layout mobile. Thay bằng Bảng Markdown hoặc Danh sách đánh số.
- **Link ảo / Đoán URL:** Không tự suy diễn slug URL. Phải lấy từ sitemap hoặc file Finalized thực tế.
- **Generic Anchors:** Tránh dùng anchor vô nghĩa như "tại đây", "xem thêm". Sử dụng chính xác thực thể/từ khóa chuyên môn.
- **Link Stuffing:** Nhồi quá nhiều link trong 1 đoạn văn. Giữ mật độ 1 link / 100-150 từ.
