---
name: write
description: Kích hoạt quy trình viết bài SEO chuẩn Framework (Full Pipeline).
---

# Quy Trình Viết Bài SEO Full Pipeline

## Options Hỗ Trợ
- `--step`: Viết từng bước, dừng lại chờ `/approve` tại mỗi gate.
- `--auto`: Chạy đến Final không chờ duyệt; gate máy (`outline_lint`, `qa_gate`) vẫn chặn khi FAIL.
- `--no-serp`: Bỏ qua bước SERP research (dùng khi đã có data ngoại tuyến).
- `--sprint`: Chế độ viết hàng loạt (batch), lần lượt từng keyword trong backlog.

---

## Quy trình thực thi chi tiết (Agent Sequencing)

### 🔄 Bước 0: System Context Load (BẮT BUỘC — trước mọi bước)
1. Bộ context bắt buộc ở `CLAUDE.md` §Mandatory Context Protocol — **load 1 lần / session, các giai đoạn sau không đọc lại** (kể cả outline / draft vừa viết trong session).
2. Trạng thái (không đọc `topic-clusters.md`):
   ```bash
   python scripts/topic_status.py --find "[keyword]"        # xác nhận chưa có bài / lấy slug
   python scripts/topic_status.py [slug] --set Outlining    # chưa có dòng: thêm --add --cluster "<tên cluster>"
   ```
3. Persona — `python scripts/persona.py P<n>` sau khi Bước 1.2 xác định P1–P4. Chỉ cần Bridge: `--part bridge`. Viết bài đọc thêm `knowledge/1-brand/service-operations.md` + `knowledge/1-brand/writers/<Writer_Profile>.md`.

---

### ⚙️ Giai đoạn 1: Outlining (SEO Research + Expert Outline)
**Agent phụ trách:** SEO Collector + Brand Guardian (song song)

**Bước 1.0 — Cannibalization Gate:** chạy đúng Bước 0.5 của `.agents/skills/outlining/SKILL.md` (SEO Dashboard MCP hoặc `find_links.py`). Có URL DSC cùng intent đang rank → dừng, đề xuất `/optimize` thay vì viết mới.

**Bước 1.1 — SEO Collector (SERP Research):**
- Theo `.antigravity/skills/seo-outlining/SKILL.md` Step 1–3 (1 lệnh `serp_research.py`; không cần mở `web-serp/SKILL.md`). KHÔNG dùng browser.
- **Chốt khung bài theo block `SERP Format & Intent`** (toplist / how-to / định nghĩa / so sánh) trước khi dựng heading. Lệch khung → `Format_Deviation` + hỏi user. SERP degraded → báo user.
- Lấy từ digest: block `Topic Coverage` (thuật ngữ bắt buộc → `Entities`, chủ đề con đối thủ đều có, nguồn họ trích), PAA nguyên văn, số liệu năm hiện tại kèm URL nguồn.

**Bước 1.2 — Brand Guardian (Brand Context):**
- Chạy song song với 1.1 hoặc ngay sau khi 1.1 hoàn thành.
- Output: `Brand Context Snippet` — Persona, USPs bắt buộc, Anti-AI checklist riêng cho bài này.

**Bước 1.3 — SEO Collector (Expert Outline):**
- `.antigravity/skills/seo-outlining/SKILL.md` → Step 4: Dựng outline (Thesis + Information_Gain ≥ 2 mục có `proof`).
- Tích hợp Brand Context Snippet từ Brand Guardian vào mục 4 của Outline.
- Lưu Outline tại: `knowledge/4-content/1-outlines/[slug].md`.
- Gate: `python scripts/outline_lint.py knowledge/4-content/1-outlines/[slug].md` — FAIL thì sửa, tối đa 2 vòng.

**🚧 APPROVAL GATE 1:**
> Trình bày **tóm tắt ≤ 25 dòng + đường dẫn file** (khung bài, Thesis, từng mục Information_Gain, cây H2/H3, kết quả lint) — không dán outline vào chat.
> **DỪNG LẠI. Chờ người dùng gõ `/approve`.**
> Khi được approve: `python scripts/topic_status.py [slug] --set Outline-Approved`.

---

### ⚙️ Giai đoạn 2: Drafting (Human-centric Draft)
**Agent phụ trách:** Main Agent (drafting) + Quality Guardian (QA)

**Bước 2.1 — Drafting:**
- Theo `.antigravity/skills/seo-drafting/SKILL.md` Step 1 (5 lời hứa của outline: Thesis, Information_Gain, Entities, PAA, bảng dữ liệu có nguồn).
- Outline vừa viết trong session → không mở lại file.
- Lưu draft tại: `knowledge/4-content/2-drafts/Draft-[slug].md`.

**Bước 2.2 — Internal Linking:**
- Quy tắc đặt link: `.antigravity/skills/internal-linking/references/link-rules.md` (2 KB — không cần mở cả SKILL 13 KB).
- **Không đọc `anchor-index.md`**. Lấy ứng viên bằng script:
  ```bash
  python scripts/find_links.py "[keyword]" --top 8 --exclude [slug]
  ```
  Chỉ dùng URL có cột Sitemap ✓. Có thể gọi thêm 1–2 lần với từ khoá phụ của outline.
- Chèn tối thiểu 3-5 internal links vào draft, đặt tự nhiên trong câu.
- **BẮT BUỘC:** Luôn có ít nhất 01 link chuyển đổi mở tài khoản chứng khoán DSC (`https://www.dsc.com.vn/mo-tai-khoan`) tại phần Product Bridge hoặc CTA cuối bài — theo `.antigravity/rules/cta-conversion.md`.

**Bước 2.3 — CRO / CTA Banner:**
- Kích hoạt skill `.antigravity/skills/cro-optimization/SKILL.md`.
- Dựng đoạn Product Bridge (nếu outline chưa có) + chèn banner CTA đúng persona đã chọn ở Bước 1.2.
- **P4 (vốn lớn): không chèn banner**, chỉ link text — xem mục giới hạn một-offer trong skill.
- Chạy trước bước lint là cố ý: banner và đoạn Product Bridge mới phải chịu lint cùng bài.

**Bước 2.4 — QA 3 tầng (Lint → Slop → Fact → Quality Guardian):**
- **Tầng A + B + dữ liệu — 1 lệnh** (in 1 dòng/tầng + chỉ lỗi CRITICAL/MAJOR, dừng ở tầng FAIL đầu tiên):
  ```bash
  python scripts/qa_gate.py knowledge/4-content/2-drafts/Draft-[slug].md --cta --fix
  ```
  Outline tự tìm theo slug. FAIL → sửa đúng dòng được báo rồi chạy lại đúng lệnh này (tầng trước chạy lại miễn phí, không đọc lại báo cáo dài). `SLOP-*`: cách sửa ở `anti-ai-rules.md` §8.7 — sửa đúng chỗ, không viết lại cả bài. `FACT-index-wrong` / `FACT-ticker` sửa bắt buộc; nguồn dữ liệu chết thì gate tự bỏ qua. Cần xem đủ chi tiết 1 tầng → chạy script riêng (`qa_lint.py` / `slop_check.py -v`).
- **Tầng C** — gate PASS → agent `.antigravity/agents/quality-guardian.md` (checklist ngữ nghĩa + truy từng mục Information_Gain), dùng luôn output gate ở trên, không chạy lại lint. Spawn thành sub-agent thì brief theo mục "Context Loading" của file đó. Vòng 1 QG đọc cả bài; QG PASS hoặc trả lỗi → `python scripts/qa_gate.py <draft> --mark-qg`. **Vòng 2 QG chỉ đọc `python scripts/qa_gate.py <draft> --changed`** (các đoạn đã sửa + heading chứa nó), không đọc lại cả bài.
- Kết quả: `PASS` hoặc `FAIL` với danh sách lỗi có số dòng.
- **Giới hạn vòng lặp:** Nếu `FAIL` → sửa và QA lại **tối đa 2 vòng**. Sau vòng 2 vẫn FAIL → dừng, trình bày draft kèm mục `⚠️ Remaining issues` (liệt kê CRITICAL/MAJOR còn lại) cho người dùng quyết định. Không tự lặp vòng 3.

**🚧 APPROVAL GATE 2:**
> `python scripts/article_snapshot.py [slug] --stage gate2` (lưu bản trình duyệt — `/learn` sẽ so với bản Final).
> Trình bày **tóm tắt ≤ 25 dòng + đường dẫn file draft** (dòng gate: score · coverage · trust · slop; từng mục Information_Gain kèm câu trích; ảnh thực tế còn thiếu; Remaining issues) — không dán bài vào chat.
> **DỪNG LẠI. Chờ người dùng review và gõ `/approve`.**

---

### ⚙️ Giai đoạn 3: Finalize & Learn
**Agent phụ trách:** Main Agent + Content Feedback Loop

**Bước 3.1–3.2 — Finalize + Feedback Loop:** làm đúng trình tự stage Draft của `.agents/skills/approve/SKILL.md` (nguồn duy nhất: gate, move file, snapshot, status, HTML CMS, `--log`, revision log, cổng nhận rule). Input của feedback loop: `python scripts/article_snapshot.py [slug] --diff`.

**Bước 3.3 — Delivery:**
- Xác nhận đường dẫn file Final cho người dùng.
- Hiển thị tóm tắt: "Đã học X bài học mới từ vòng viết này."

---

## Luồng Quyết định theo Options

```
/write [keyword]
  └── --step  → Dừng tại mỗi GATE, chờ /approve
  └── --auto  → Không dừng chờ /approve, nhưng gate máy vẫn chặn: outline_lint FAIL / qa_gate FAIL sau 2 vòng → dừng, báo user
  └── --no-serp → Bỏ qua Bước 1.1, dùng data có sẵn trong KB
  └── --sprint  → Lặp lại toàn bộ pipeline cho từng keyword trong backlog
```
