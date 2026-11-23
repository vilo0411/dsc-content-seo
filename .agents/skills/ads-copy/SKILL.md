---
name: ads-copy
description: Viết quảng cáo Google Ads (Responsive Search Ads, sitelink, callout) cho DSC theo persona và keyword, đúng giới hạn ký tự và ràng buộc quảng cáo tài chính. Dùng khi cần ad copy, RSA, headline quảng cáo, viết lại quảng cáo CTR thấp.
---

# Ads Copy

`/ads-copy [campaign | ad group | keyword] [--variants N]` — chỉ soạn bản nháp, không đẩy lên tài khoản.

## Bước 0: Context
1. `.agents/context.md` (mục 5 Ràng buộc là bắt buộc)
2. `knowledge/1-brand/brand-facts.json` — số nào đưa vào ad phải có ở đây với `status: verified`
3. `knowledge/1-brand/anti-ai-rules-blacklist.md` · `knowledge/1-brand/glossary.md`
4. Persona: `python scripts/persona.py --matrix` → chọn 1 persona theo keyword
5. Ad group đang có (nếu viết lại): MCP `get_ads_breakdown` + `get_ads_search_terms` — lấy search term thật làm ngôn ngữ người dùng

## Bước 1: Brief (trình user trước khi viết)
Keyword chính · persona · landing URL · 1 lợi ích chính + 2 lợi ích phụ (từ brand-facts / profile) · CTA theo persona.
Landing không khớp intent của keyword → báo user và đề xuất `/copy-landing`, không viết ad cho landing sai.

## Bước 2: Viết RSA
- **15 headline ≤ 30 ký tự**, **4 description ≤ 90 ký tự** (đếm cả dấu cách; chữ có dấu tính 1 ký tự).
- Phân bổ headline: 3–4 chứa keyword · 3 lợi ích có số (phí, thời gian mở tài khoản 3 phút… lấy từ brand-facts) · 2–3 CTA · 2 tin cậy (thương hiệu, môi giới 1:1) · 2 xử lý lo ngại của persona.
- Mỗi headline đọc riêng vẫn đủ nghĩa (Google ghép ngẫu nhiên). Không lặp ý giữa các headline.
- Đề xuất pin: chỉ pin headline 1 khi buộc phải có (brand / pháp lý).
- Kèm 4 sitelink (≤ 25 ký tự + 2 dòng mô tả ≤ 35) và 4–6 callout (≤ 25).

**Cấm:** hứa lợi nhuận / "lãi chắc", "không rủi ro", "số 1", "tốt nhất" khi không có nguồn, số chưa verified, chữ hoa toàn bộ, dấu chấm than ở headline. Câu nghi vấn pháp lý → gắn `[CẦN PHÁP CHẾ DUYỆT]`.

## Bước 3: Tự kiểm
Chạy script đếm ký tự (vd `python -c "for s in [...]: print(len(s), s)"`), bảng hoá kết quả. Soát lại blacklist + glossary. Mọi số đối chiếu brand-facts.

## Output → `knowledge/4-channels/ads/YYYY-MM-DD-<ad-group>-rsa.md`
`Status: Draft` · brief · bảng headline (text · số ký tự · nhóm · pin) · bảng description · sitelink · callout · ghi chú pháp chế. `--variants N`: N bộ khác góc (lợi ích / lo ngại / tin cậy) để A/B.

## Related Skills
`/ads-audit` (chọn ad group cần viết lại) · `/copy-landing` (landing khớp ad) · `/cro`
