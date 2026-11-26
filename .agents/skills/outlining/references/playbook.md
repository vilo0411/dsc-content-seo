# Skill: SEO Outlining (Phase 1 & 2)

**Nguồn chi tiết duy nhất** cho bước outline. `.agents/skills/outlining/SKILL.md` (quy trình) và `.agents/skills/outlining/references/seo-collector.md` (vai trò) chỉ trỏ về đây — sửa quy tắc thì sửa ở file này.

Template: [`references/brief-template.md`](references/brief-template.md) · Gate: `python scripts/outline_lint.py <outline>`

---

## Step 1 — SERP & Intent

1. **Chạy 1 lệnh** (query = Target Keyword, không dùng tiêu đề / slug):
   `python .agents/skills/web-serp/scripts/serp_research.py "<keyword>" --top 10 --extract 5`
   Cache 30 ngày. Không `--no-cache` trừ khi user yêu cầu (có phí). Digest mặc định là bản gọn (~6–10 KB): cây heading + số từ từng đối thủ, và block `### Topic Coverage` gộp chung. Chỉ thêm `--full` (dài gấp 3) khi cần câu chủ đề / data point / link của một đối thủ cụ thể.

1b. **SERP có đúng không?** Script in `⚠️ SERP_CHECK` (không có PAA lẫn related searches, hoặc thiếu ≥ 2 rank) → dừng, chạy lại `--no-cache` (báo user vì có phí). Đối chiếu 1 lần với GSC: URL DSC đang rank cho keyword phải nằm trong top 10 của cache. Lệch → nhờ user dán SERP ẩn danh.

2. **Chốt khung bài theo SERP — làm TRƯỚC mọi thứ khác.** Đọc block `### SERP Format & Intent`:
   - `BẮT BUỘC` (≥ 50%) → `Content_Type` = khung đó. Toplist thì Title/H1 có số N ≥ median số mục của đối thủ, thân bài là N mục H3 cùng cấu trúc. How-to thì các bước đánh số.
   - `NGHIÊNG VỀ` (35–50%) → theo khung đó, trừ khi có lý do. Lý do ghi vào `Format_Deviation`.
   - `HỖN HỢP` → mở outline của top 3 (block Competitor) để tự xác định khung, ghi lý do vào phần "Kết luận khung".
   - Nhãn do script tự gán theo heuristic tiêu đề + heading đánh số. Cột "Tín hiệu" cho thấy vì sao. Nhãn sai (ví dụ tiêu đề không có số nhưng thân bài là danh sách) thì sửa trong outline và ghi rõ.
   - **Không tự đổi khung** vì thấy "guide dài thì tốt hơn". Khung lệch SERP thì phải có `Format_Deviation` và user đồng ý.

3. **SERP degraded** (script in `⚠️ SERP_STATUS: degraded`: < 5 organic, hoặc phải dùng fallback WebSearch):
   - Ghi `SERP_Status: degraded`, **báo user ngay** trước khi dựng outline, và đề xuất: chạy lại sau, đổi biến thể keyword, hoặc user dán tay top 10.
   - Đối thủ lấy từ fallback chưa chắc là trang đang rank → không dùng chúng làm chuẩn số từ và không kết luận "không ai có X".
   - PAA tự suy ra (từ FAQ đối thủ, related searches) → ghi `source: inferred`.
   - `Word_Count_Target` tính theo intent (định nghĩa 1.000–1.500, toplist/guide 1.500–2.200), không theo "đối thủ + 10%".

4. **Competitor blocks:** mục 1 của outline có ít nhất 3 block `### Competitor N: domain`, mỗi block 4 dòng: URL · khung + số từ · **điểm /40** (Độ sâu · Trình bày · SEO · UX) · `Mạnh: … · Thiếu: …`. **Không chép cây heading của đối thủ vào outline** — nó nằm trong cache; ai cần xem lại thì chạy lại lệnh ở bước 1 (đọc cache, không tốn phí). Đối thủ điểm cao nhất là chuẩn cần vượt.

5. **Entities — phủ đúng thứ SERP đang nói tới.** Block `### Topic Coverage`:
   - `Thuật ngữ BẮT BUỘC phủ` (≥ 3 đối thủ cùng dùng) → chép vào `Entities:`. Cụm nào là rác hoặc thuộc bài khác → ghi vào `Entities_Skipped: [cụm — lý do]`. Lint đòi outline phủ ≥ 70%, rồi `qa_lint` đòi draft phủ ≥ 70%.
   - `Chủ đề con nhiều đối thủ cùng có` → mỗi chủ đề phải có chỗ trong outline (H2/H3 hoặc 1 đoạn), hoặc ghi lý do bỏ ở Gap Synthesis.
   - `Nguồn đối thủ trích` → gợi ý nguồn gốc cho bảng dữ liệu ở Step 2.

5b. **Đọc nội dung đối thủ, không chỉ heading.** Block `### Structure consensus` (tính từ full text) quyết định khung chi tiết:
   - `Word_Count_Target` quanh median số từ, **không vượt max** của top 5 (bài dài hơn đối thủ bị chê "dài"). Số H2 quanh median.
   - Bài how-to: H2 các bước đặt ở vị trí ≤ median (thường thứ 2–3). Nội dung đối thủ đặt **trước** H2 các bước (ví dụ "Có những cách … nào?" chủ động/bị động) → 1 H2 ngắn trước các bước; phần chiến lược, sai lầm, DSC xếp sau.
   - Một khái niệm đối thủ nào cũng có (vd chủ động/bị động) phải đặt **đúng vai trò** họ dùng ("cách chơi" ≠ "chiến lược"). Không chắc → `serp_research.py "<kw>" --content` (đọc cache, 0 phí) đọc đoạn đó của top 3.
   - Dòng `sapo:` của từng đối thủ → điền mục Sapo plan (xem Step 4).

6. **Gap Synthesis** = mục 2 của brief-template. Gap phải so với top 3 thật, không so với bài yếu.

7. **PAA plan:** chép **nguyên văn** câu PAA script in ra (lint `SERP-paa-fake` đối chiếu với cache; câu tự nghĩ ra phải ghi `source: inferred`). Mỗi câu PAA → `body` (H2/H3, giữ dạng câu hỏi) hoặc `faq`. Câu FAQ không trùng câu đã có ở bài DSC khác (`qa_lint` báo `DUP-faq`). Câu không đối thủ nào có heading khớp thì ưu tiên `body`. Related searches tách thành `same_intent` / `spin_off`. Spin-off không nhồi vào bài, chạy `find_links.py` để xem đã có bài chưa.

## Step 2 — Dữ liệu

- Số thị trường: `python scripts/market_facts.py --brief [--tickers ...]`. Sự kiện có ngày: `python scripts/news_feed.py --topic "<kw>" --days 30`. Không dùng block "CSDL tham chiếu" trong `anti-ai-rules.md` làm nguồn số (đã cũ).
- **Ưu tiên số năm hiện tại.** Mốc của năm trước trở về trước chỉ dùng làm ví dụ lịch sử, ghi rõ đó là ví dụ.
- Mỗi dữ kiện là 1 dòng ở bảng mục 3, đủ các cột: số liệu, mốc, nguồn, trạng thái ✓. **Cột Nguồn phải là URL** (hoặc `market_facts` / `DSC nội bộ`) — lint `DATA-source`. Quy định, phí, hạn mức: URL văn bản gốc thuộc `knowledge/1-brand/source-whitelist.md` (UBCKNN, NHNN, HOSE, VSDC, cổng văn bản Chính phủ…); draft sẽ link đúng URL này tại câu trích (`SRC-missing`).
- Bài hướng dẫn thao tác / đánh giá app: liệt kê ảnh ở mục 6. Trước khi ghi `[ẢNH THỰC TẾ: …]`, tìm ảnh chụp app đã có trên site: `grep -oh '<img[^>]*>' knowledge/raw/live/html/*.html | grep -i "<từ khóa màn hình>"` — có thì ghi URL đó (sẽ được ghép vào khung 800×500). Infographic (bước, chi phí, so sánh kịch bản) ghi rõ số liệu sẽ vẽ — vẽ bằng code theo `knowledge/1-brand/image-design-system.md`. Câu "theo khảo sát / số liệu của DSC" chỉ được dùng khi có con số + mốc thời gian trong bảng này.
- Dữ kiện không xác minh được → **bỏ**, không để `[CẦN XÁC NHẬN]` trong outline. Nếu thiếu dữ kiện quan trọng thì báo user.

## Step 3 — Internal links & cannibalization

- **Keyword đã có chủ:** `outline_lint` báo `KW-pillar` khi keyword trùng `pillar_keyword`/`pillar_anchors` của bài khác hoặc dòng registry có trạng thái `Merged`. Mặc định → `/optimize` bài đó. Chỉ tạo URL mới khi user xác nhận; ghi `Lint_Skip: KW-pillar` vào YAML.
- `python scripts/find_links.py "<keyword>" --top 6`. Không đọc `pages.csv`.
- Chọn **3–6 link `/kien-thuc/`** có Sitemap ✓ (qa_lint của draft cần ≥ 3), cộng thêm link mở tài khoản. Mỗi link gắn với một câu/ý cụ thể của H2, không gắn chung chung cả section.
- Bài thuộc cụm trong `taxonomy.json` → bắt buộc có link pillar (+ hub), và thêm slug vào `spokes`.
- Quy tắc đặt link: `.agents/skills/link/references/link-rules.md`. Mỗi link trong outline ghi luôn **cụm từ có sẵn** trong câu sẽ được bọc (vd Bước 1: “mở tài khoản tại công ty chứng khoán”). Không tìm được cụm tự nhiên → bỏ link đó, không viết câu “… có trong bài [x]” (`LINK-pointer`, MAJOR).

## Step 4 — Dựng outline

Điền đủ template. Các điểm hay bị bỏ:
- `Thesis`: 1–2 câu lập trường của cả bài, không phải câu nêu chủ đề. Mọi H2 phải phục vụ thesis.
- `Information_Gain`: danh sách **≥ 2 mục**, mỗi mục `claim` (điều top 5 không có) · `h2` (mục nào giao nó) · `type` (`calc` tự tính bằng tiền / `dsc-data` / `regulation` điều khoản cụ thể / `screenshot` / `comparison`) · `proof` (con số hoặc cụm từ chắc chắn xuất hiện trong bài). `qa_lint` tìm đúng `proof` trong draft (`IG-missing`), Quality Guardian trích câu giao nó. `proof` đã có ở bài đối thủ → lint báo `IG-not-new`. Không tìm được 2 mục thì bài không có lý do để rank trên đối thủ → báo user.
- Mỗi H2 thân bài có `**Câu hỏi người đọc:**` + `**Ý chính:**` + `**Chuyển ý → H2 sau:**`. Không viết H2 dạng "liệt kê chủ đề + nhét số liệu".
- Có ít nhất 1 H2 chứa keyword hoặc câu hỏi keyword.
- **Sapo plan (instinct I105)** — viết sẵn nguyên văn 2 đoạn trong outline để duyệt cùng cây H2:
  - Đoạn 1: cấm bê nguyên keyword dài làm chủ ngữ đầu câu một cách máy móc; lồng keyword tự nhiên + 1 con số có ngày và mở theo đúng `Content_Type`:
    - *Comparison:* mở bằng khoảng chênh quy ra tiền thật trên 1 mốc vốn chuẩn giữa các lựa chọn, câu 2 nêu biên độ % và keyword.
    - *Definition:* trả lời thẳng bản chất bằng lời thường + 1 số liệu thực tế từ BCTC/thị trường gây bất ngờ.
    - *How-to:* chốt tổng số bước + tên các bước gói trong 1 câu + vốn/thời gian tối thiểu.
    - *Review ("Có nên"):* mở bằng phán quyết có điều kiện (Nên khi A — Không nên khi B) + số liệu kiểm chứng 2 chiều.
    - *Toplist:* nêu tiêu chí xếp hạng + điểm tên ngay đơn vị dẫn đầu kèm con số đỉnh.
    - *Comprehensive Guide:* nêu quy tắc toán học / con số cốt lõi phá bỏ lầm tưởng, rồi đặt keyword vào phạm vi bài.
  - Đoạn 2: Câu 1 mở bằng “Trong bài viết này, Chứng khoán DSC …” giới thiệu nội dung bài theo **ĐÚNG THỨ TỰ các H2 trong outline** (không đảo thứ tự H2 sau lên trước H2 đầu; các phần phụ đi sau “kèm”). Câu 2 mở bằng **“Bạn sẽ thấy vì sao …”** (hoặc **“Qua đó, bạn sẽ thấy …”**) nêu 1–2 hệ quả bằng con số cụ thể từ chính các phần vừa giới thiệu ở Câu 1 để gợi tò mò (xem mẫu đã duyệt ở `Final-cach-choi-chung-khoan.md` và `Final-phan-biet-thi-truong-tien-te-va-thi-truong-von-huong-dan-chi-tiet-cho-nha-dau-tu.md`). Cấm thả 1 câu dữ kiện đứng trơ trọi mà không có cụm chuyển tiếp nối với Câu 1. Không tự khen (“tính sẵn”, “con số cụ thể”).
  - Tổng ≤ 110 từ, mỗi câu ≤ 30 từ.
- **Bài how-to (I119):** bước viết chung cho mọi CTCK (đối thủ top đều vậy). Mã/số riêng DSC (963369, dạng 024C, đuôi tiểu khoản) chỉ nằm ở H2 DSC hoặc CTA (`qa_lint:BRAND-steps`). Ảnh app DSC dùng minh họa được.
- Product Bridge: nối từ kết luận của bài sang các bước cụ thể tại DSC, không phải list tính năng.
- H2 `Kết luận` tóm tắt insight rồi CTA. Không mở bằng "Tóm lại".
- Bài có chủ đề riêng (đã có bài khác chuyên sâu, ví dụ rủi ro) → 1 câu + link, không dựng H2 riêng.
- Tổng `**Target:**` các section = `Word_Count_Target` ±10%.
- Mục 4 Brand Context lấy từ output Brand Guardian. Nếu instinct mâu thuẫn với phản hồi mới của user → ghi rõ, theo phản hồi của user.
- Không viết câu meta kiểu AI ("Trong phần này, chúng ta sẽ…") ngay trong outline.

## Step 5 — Gate

```bash
python scripts/outline_lint.py knowledge/3-seo/content/1-outlines/<slug>.md
```
Lint kiểm: khung bài vs SERP (tự tính lại từ cache), toplist có N, YAML/enum/Thesis, độ phủ thuật ngữ đối thủ (`ENT-outline`), Information_Gain (`IG-*`), PAA có thật trong cache (`SERP-paa-fake`), nguồn từng dữ kiện (`DATA-source`), tổng số từ, Title/Meta/Sapo, keyword trong H2, Kết luận, Bridge, FAQ, Câu hỏi người đọc / Ý chính từng H2, số link, `[CẦN XÁC NHẬN]`, số liệu năm hiện tại, SERP degraded.

- FAIL → sửa → chạy lại, **tối đa 2 vòng**. Còn lỗi → trình bày kèm `⚠️ Remaining issues`.
- Trình bày cho user **tóm tắt ≤ 25 dòng + đường dẫn file outline** (không dán lại outline vào chat): khung bài đã chọn, Thesis, từng mục Information_Gain, cây H2/H3 (chỉ tiêu đề), thuật ngữ đã bỏ qua + lý do, kết quả lint. **Chờ `/approve`.**
