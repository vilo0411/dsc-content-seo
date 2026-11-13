from pathlib import Path
import json
root=Path("knowledge/4-content/audits/account-serp-2026-11-04")
review="""# Independent Quality Guardian — 04/11/2026

Secondary semantic review: FAIL before publication. Lint99/100 does not override these findings.

- CRITICAL CL5, draft lines106/122: retained image/alt still asserts HOSE bán niên2026 and SSI Top2. Historical/unverified captions do not prove the graphic. Verify original source or replace the asset before CMS.
- MAJOR, line96: VNDIRECT row describes DGO/DSTOCK/mydgo while linked landing explicitly supports DSTOCK. Correct source: https://support.vndirect.com.vn/hc/vi/articles/4413910748697-Hướng-dẫn-mở-tài-khoản-trực-tuyến-cho-nhà-đầu-tư-cá-nhân-trong-nước .
- MAJOR, line178: CTA promises support1:1 automatically while article says confirm service package. Make entitlement conditional and preserve registration href in the next approved revision.
- Comparison intent and conditional fee distinctions otherwise retained.
- Primary was not submitted for final semantic PASS because raw strict slop74 failed after2correction rounds.

No publication, Final overwrite or indexing request was executed. HTML review passed: four comparison frames, no JS errors; primary6images, secondary4images; previews at360px had scrollWidth360px.
"""
(root/"independent-review.md").write_text(review,encoding="utf-8")
p=root/"rollout-validation.json";d=json.loads(p.read_text(encoding="utf-8"))
d["secondary"]["semantic_qa"]={"pass":False,"critical":1,"major":2,"review":"independent-review.md","findings":["Unverified graphic/alt claims","VNDIRECT source alignment","CTA implies unconditional1:1 entitlement"]}
d["browser_validation"]={"js_errors":[],"comparison_iframes":4,"mobile_360":{"primary_scroll_width":360,"secondary_scroll_width":360}}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8")
p=root/"rollout-plan.md";t=p.read_text(encoding="utf-8");t+="\n## Kiểm tra độc lập cuối\n\nBài so sánh chưa đạt QA ngữ nghĩa:1critical về ảnh/alt,2major về nguồn VNDIRECT và CTA1:1. Xem independent-review.md. Không sử dụng điểm lint99 làm bằng chứng sẵn sàng xuất bản.\n"
p.write_text(t,encoding="utf-8")
p=root/"index.html";t=p.read_text(encoding="utf-8")
banner="""<section class="hold"><h2>Kết quả biên tập độc lập: chưa đủ điều kiện xuất bản</h2><p>Bài so sánh còn 1 CRITICAL (ảnh/alt về thị phần và SSI Top2 chưa xác minh), 2 MAJOR (nguồn VNDIRECT và CTA hứa hỗ trợ1:1 tự động). Bài hướng dẫn còn style gate74/100.</p><p><a href="independent-review.md">Xem báo cáo độc lập và dòng cần xử lý</a>. Đã giữ nguyên4+6ảnh, nhưng bảo toàn ảnh không đồng nghĩa dữ kiện trong ảnh đúng.</p></section>"""
t=t.replace("<section><h2>Phạm vi và kiểm tra</h2>",banner+"<section><h2>Phạm vi và kiểm tra</h2>")
p.write_text(t,encoding="utf-8")
print("Review and holds attached.")

