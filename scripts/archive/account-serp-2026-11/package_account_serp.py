"""Package local account SERP rollout drafts and review evidence; no CMS writes."""
import json,html,csv,re,hashlib,difflib,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding="utf-8")
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"knowledge/4-content/audits/account-serp-2026-11-04"
slugs=["cach-mo-tai-khoan-chung-khoan","nen-mo-tai-khoan-chung-khoan-o-dau"]
e=html.escape
def read(p):return p.read_text(encoding="utf-8-sig")
# Correct only source alignment noted by the editor; preserve all original live destinations.
second=ROOT/"knowledge/4-content/2-drafts"/("Optimize-"+slugs[1]+"-serp-2026-11-04.md")
short="https://www.vndirect.com.vn/mo-tai-khoan-chung-khoan/"
long="https://support.vndirect.com.vn/hc/vi/articles/4413910748697-Hướng-dẫn-mở-tài-khoản-trực-tuyến-cho-nhà-đầu-tư-cá-nhân-trong-nước"
for p in [second,OUT/(slugs[1]+".body.html")]:
 t=read(p)
 # Broader paragraph source alignment; VNDIRECT shorter page remains correct for DSTOCK.
 # Keep original draft unchanged here; note precise fuller source separately in implementation notes.
 (OUT/"additional-source-vndirect.txt").write_text(long+"\n",encoding="utf-8")
def tech(slug):
 u="https://www.dsc.com.vn/kien-thuc/"+slug
 with urlopen(u,timeout=30) as r:
  h=r.read().decode("utf-8","replace");status=r.status;final=r.url;robots=r.headers.get("X-Robots-Tag")
 s=BeautifulSoup(h,"html.parser")
 return {"url":u,"http":status,"final_url":final,"canonical":[n.get("href") for n in s.select('link[rel="canonical"]')],"x_robots_tag":robots,"meta_robots":[n.get("content") for n in s.select('meta[name="robots"]')],"h1":[n.get_text(" ",strip=True) for n in s.select("h1")],"ssr_body_has_article_keyword":"mở tài khoản" in s.get_text(" ",strip=True).lower(),"inspection_verdict":"not checked; HTML checks do not prove Google indexing"}
with ThreadPoolExecutor(max_workers=2) as ex:technical=list(ex.map(tech,slugs))
(OUT/"technical-checks.json").write_text(json.dumps(technical,ensure_ascii=False,indent=2),encoding="utf-8")
validation={"primary":{"lint":{"pass":True,"score":99,"critical":0,"major":0,"minor":1},"slop":{"mode":"strict","pass":False,"score":74,"baseline_strict_score":81,"flags":["unanchored_ratio 66.1% > 66% proxy threshold","template similarity 55% to same original article because dated filename","evidence density 1.47/100w","paragraph shape stdev0.49"]},"fact_checker":{"exit_code":0,"checked_dated_index_claims":0,"meaning":"No automated market-index claims found; not a blanket factual verification"},"correction_rounds":2,"publish_ready":False},"secondary":{"lint":{"pass":True,"score":99},"slop":{"mode":"strict","pass":True,"score":91,"baseline_strict_score":64},"fact_checker":{"exit_code":0,"checked_dated_index_claims":0},"editorial_holds":["Original market-share graphic and SSI Top2 wording not verified as current","VNDIRECT wider channel source supplied separately"],"publish_ready":False},"state":"local-drafts-pending-review-not-published","approval_rule":".agents/skills/optimize/SKILL.md Gate2: wait for human /approve before Final"}
preservation={}
for slug in slugs:
 source=read(ROOT/"knowledge/raw/live/html"/(slug+".html"))
 proposed=read(OUT/(slug+".body.html"))
 a=BeautifulSoup(source,"html.parser");b=BeautifulSoup(proposed,"html.parser")
 oldimgs=[x.get("src") for x in a.select("img")];newimgs=[x.get("src") for x in b.select("img")]
 oldlinks={x["href"] for x in a.select("a[href]")};newlinks={x["href"] for x in b.select("a[href]")}
 assert all(i in newimgs for i in oldimgs),(slug,"missing images")
 assert oldlinks.issubset(newlinks),(slug,"missing original links",oldlinks-newlinks)
 preservation[slug]={"original_images":len(oldimgs),"preserved_images":len([i for i in oldimgs if i in newimgs]),"original_unique_destinations":len(oldlinks),"preserved_destinations":len(oldlinks&newlinks),"original_html_sha256":hashlib.sha256(source.encode()).hexdigest(),"proposed_html_sha256":hashlib.sha256(proposed.encode()).hexdigest()}
 before="\n".join(a.stripped_strings);after="\n".join(b.stripped_strings)
 (OUT/(slug+".diff.txt")).write_text("\n".join(difflib.unified_diff(before.splitlines(),after.splitlines(),fromfile="live-before",tofile="proposed-after")),encoding="utf-8")
validation["preservation"]=preservation
(OUT/"rollout-validation.json").write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding="utf-8")
# Baseline numbers transcribed from connected GSC query_search_analytics, not SERP ranks.
gsc=[
["mở tài khoản chứng khoán",slugs[0],97,41.5464,0],
["mở tài khoản chứng khoán",slugs[1],161,17.0621,0],
["cách mở tài khoản chứng khoán",slugs[0],85,35.6588,0],
["cách mở tài khoản chứng khoán",slugs[1],124,16.1048,0],
["mở tài khoản chứng khoán online",slugs[0],67,36.8507,0],
["mở tài khoản chứng khoán online",slugs[1],75,13.2667,0],
["nên mở tài khoản chứng khoán ở đâu",slugs[1],115,5.687,2],
["mở tài khoản chứng khoán ở đâu tốt nhất",slugs[1],173,3.8439,1]]
with (OUT/"gsc-baseline.csv").open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.writer(f);w.writerow(["query","slug","impressions","avg_position","clicks","period_start","period_end","country","source"])
 for row in gsc:w.writerow(row+["2026-10-05","2026-11-01","vnm","connected SEO Dashboard; transcribed query/page rows"])
with (OUT/"monitoring.csv").open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.writer(f);w.writerow(["checkpoint","actual_date","query","page","device","impressions","clicks","ctr","avg_position","google_selected_canonical","last_crawl","notes"])
 for cp in ["T0-publication","T+7","T+14","T+28","T+42"]:
  for q,slug,*_ in gsc:w.writerow([cp,"",q,"https://www.dsc.com.vn/kien-thuc/"+slug,"mobile / desktop","","","","","","","fill only after actual publication; no automation scheduled"])
plan="""# Kế hoạch triển khai cụm mở tài khoản — 04/11/2026

Trạng thái: đã thực hiện bản sửa local cho hai bài; chưa cập nhật Final/CMS.

## Mục tiêu và bằng chứng
- Ảnh SERP người dùng: hướng dẫn VFS #7 cho cách mở, #8 cho mở tài khoản; nhóm so sánh VFS #2, DSC #3. Không biết thời điểm chụp chính xác; không coi đây là lịch sử ranking.
- Giữ bài so sánh cho nhu cầu chọn công ty. Cải thiện bài hướng dẫn cho nhóm mở/cách mở/online; không hứa Google sẽ đổi URL.
- GSC baseline 05/10–01/11/2026 trong gsc-baseline.csv, khác thời điểm ảnh và trước snapshot live03/11.
- Snapshot DataForSEO lọc bớt kết quả, không tái hiện ảnh; không dùng để phủ nhận ảnh.

## Việc đã thực hiện
1. Sync hai bài live, chụp baseline; lấy live làm gốc vì giống Final chỉ57% và13%.
2. So canonical, HTTP, nội dung trong HTML. Chưa có URL Inspection; không tuyên bố Google-selected canonical.
3. Tạo Proposal riêng trước khi sửa; giữ các bản Final/draft cũ.
4. Bài hướng dẫn: đưa bước làm lên trước pháp lý, thêm kiểm tra kênh/gói phí, giữ ảnh thao tác, sửa NFC/OTP/kích hoạt và lô lẻ, thêm3FAQ theo ảnh.
5. Bài lựa chọn: giữ title/H1/công ty, thay claim vốn/thị phần/so sánh thiếu nguồn, thêm bảng kênh đăng ký và điều kiện phí chính thức; giữ hướng dẫn ở mức đoạn dẫn.
6. Giữ6+4 ảnh và13+8 đích liên kết gốc. Thêm CTA đúng đích, không UTM.
7. Lint hai bài99. Slop primary74 chưa đạt; secondary91 đạt. Không có claim chỉ số theo ngày để fact checker kiểm, không đồng nghĩa mọi claim đã xác minh.

## Nguồn dữ kiện cần lưu ý
Biểu phí https://www.dsc.com.vn/bieu-phi hiệu lực20/08/2025 khác cách diễn đạt trong KB cũ: mức0,1% chỉ thuộc nhóm quản lý ghi riêng; tài khoản Môi giới có các bậc0,15–0,3%. Không hứa0,1% kèm Môi giới1:1 cho mọi người.
Form https://www.dsc.com.vn/mo-tai-khoan tách đăng ký, OTP, chọn số, rồi eKYC/hợp đồng. Hoàn tất form không chứng minh đủ điều kiện giao dịch.

## Những việc còn trước xuất bản
- Primary: style gate còn fail sau2vòng sửa. Có false-positive so với chính bài gốc vì filename có ngày, nhưng vẫn còn warning mật độ bằng chứng/nhịp đoạn. Không sửa linter/nhồi số để qua.
- Secondary: kiểm tra nguồn và năm của đồ thị thị phần, ảnh SSI có alt Top2. Giữ asset để tránh mất hình, kèm cảnh báo lịch sử; chưa coi đã xác minh.
- Secondary: nguồn VNDIRECT đầy đủ cho DGO/DSTOCK/mydgo ở additional-source-vndirect.txt; link ngắn trong bài chỉ xác nhận DSTOCK.
- Người phụ trách nghiệp vụ xác nhận quy trình thiết bị, thời gian tiếp nhận và gói dịch vụ trước khi CMS.
- Skill optimize Gate2 chờ người dùng /approve trước ghi Final; không ghi website trong session này.

## Checklist CMS sau khi duyệt
1. Backup body và metadata trong CMS; đối chiếu SHA baseline để tránh đè thay đổi mới.
2. Cập nhật bài hướng dẫn trước: title/meta từ metadata JSON, body từ HTML. Không đổi slug hoặc canonical.
3. Preview desktop/mobile360px; kiểm tra ảnh, bảng, CTA, link nội bộ và điều kiện phí.
4. Cập nhật bài so sánh sau khi xử lý ảnh cũ; giữ title/H1.
5. Kiểm tra live; sync_live chỉ2slug; so ảnh/link và title/meta. Kiểm tra HTTP/noindex/canonical.
6. Trong GSC, URL Inspection cả2URL và request indexing nếu nội dung đã đúng; chưa tự thực hiện.
7. Ghi T0 là ngày publish thật. Không dùng04/11 như ngày publish nếu chưa lênCMS.

## Đo kết quả
T+7 kiểm tra crawl/index; T+14 xem query×URL×device; T+28 vàT+42 đánh giá xu hướng cùng độ dài kỳ.
Mục tiêu bảo vệ nhóm so sánh đồng thời tăng impressions/click của URL hướng dẫn. Vị trí trung bình và CTR phụ thuộc query/device; không đặt cam kết top theo thời hạn.
Nếu URL so sánh vẫn đứng trên hướng dẫn, kiểm tra lại index, canonical, truy vấn thực và chất lượng trang trước khi cân nhắc cấu trúc; không gộp/redirect tự động.
Không mua backlink, không sửa thêm hàng loạt bài vệ tinh và không tạo lịch tự động trong giai đoạn này.
"""
(OUT/"rollout-plan.md").write_text(plan,encoding="utf-8")
css="body{font:15px/1.65 system-ui,sans-serif;max-width:1400px;margin:auto;padding:24px;background:#f4f7f9;color:#153044}section{background:white;border:1px solid #d9e3e8;border-radius:12px;padding:22px;margin:18px 0}h1{font-size:27px}h2{font-size:21px}a{color:#1163ae}button{font:inherit;padding:8px 13px;border:1px solid #ccd9e3;border-radius:7px;background:white;cursor:pointer;margin:5px}.hold{background:#fff4d9;border-left:5px solid #cc8b16;padding:15px}.ok{color:#116b42}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}iframe{border:1px solid #d5dfe7;width:100%;height:850px;border-radius:8px;background:white}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f7f9;padding:15px;max-height:600px;overflow:auto}.badge{display:inline-block;background:#e4edf4;padding:3px 9px;border-radius:5px}table{width:100%;border-collapse:collapse}td,th{padding:9px;border-bottom:1px solid #dae2eb;text-align:left}textarea{width:100%;height:220px}small{color:#5d6f7c}@media(max-width:850px){.grid{grid-template-columns:1fr}body{padding:12px}}"
previewcss="body{font:16px/1.7 system-ui;color:#153044;padding:20px;overflow-wrap:anywhere}img{max-width:100%;height:auto}table{display:block;overflow-x:auto;max-width:100%;border-collapse:collapse}td,th{padding:9px;border:1px solid #d4dfe5;min-width:115px}h2{font-size:23px}a{color:#1067ae}"
def doc(body,title):return "<!doctype html><html lang='vi'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><style>"+previewcss+"</style><h1>"+e(title)+"</h1>"+body+"</html>"
parts=["<!doctype html><html lang='vi'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Kế hoạch và bản sửa DSC — mở tài khoản</title><style>"+css+"</style><h1>Kế hoạch và bản sửa cụm mở tài khoản DSC</h1><p>Chuẩn bị04/11/2026 · <b>Bản nháp local — chưa xuất bản</b></p><div class='hold'>Bài hướng dẫn còn style gate74/100; bài so sánh còn ảnh cũ chưa xác minh. Chưa đánh dấu toàn bộ gói sẵn sàng publish.</div><section><h2>Phạm vi và kiểm tra</h2><p>Giữ2URL. Bài hướng dẫn cho thao tác mở tài khoản; bài lựa chọn cho so sánh công ty. Đối chứng chính là ảnh SERP của người dùng; DataForSEO chỉ bổ sung.</p><table><tr><th>Bài</th><th>Lint</th><th>Style</th><th>Bảo toàn</th></tr><tr><td>Cách mở</td><td>99 PASS</td><td>74 FAIL; baseline strict81</td><td>6ảnh /13đích gốc</td></tr><tr><td>Nên mở ở đâu</td><td>99 PASS</td><td>91 PASS; baseline strict64</td><td>4ảnh /8đích gốc</td></tr></table><p>Fact checker không tìm thấy claim chỉ số theo ngày; không phải chứng nhận mọi dữ kiện. HTTP200, canonical tự trỏ; chưa có URL Inspection.</p><p><a href='rollout-plan.md'>Kế hoạch và checklist CMS</a> · <a href='rollout-validation.json'>Validation JSON</a> · <a href='technical-checks.json'>Kỹ thuật</a> · <a href='gsc-baseline.csv'>GSC baseline</a> · <a href='monitoring.csv'>Bảng theo dõi T0–T+42</a></p></section>"]
for i,slug in enumerate(slugs):
 draft=ROOT/"knowledge/4-content/2-drafts"/("Optimize-"+slug+"-serp-2026-11-04.md")
 content=read(draft);title=re.search(r"^Title: (.+)$",content,re.M).group(1);meta=re.search(r"^Meta_Description: (.+)$",content,re.M).group(1)
 source=read(ROOT/"knowledge/raw/live/html"/(slug+".html"));body=read(OUT/(slug+".body.html"))
 (OUT/(slug+".preview.html")).write_text(doc(body,title),encoding="utf-8")
 parts.append("<section><h2>"+e(title)+"</h2><p><span class='badge'>"+e(slug)+"</span></p><p><b>Title:</b> "+e(title)+"<br><b>Meta:</b> "+e(meta)+"</p><p><a href='"+slug+".body.html'>Body HTML</a> · <a href='"+slug+".preview.html'>Mở preview riêng</a> · <a href='../../2-drafts/"+draft.name+"'>Draft Markdown</a> · <a href='"+slug+".diff.txt'>Diff văn bản</a></p><div class='grid'><div><h3>Live trước sửa</h3><iframe title='Live trước sửa "+str(i)+"' sandbox='allow-popups' srcdoc='"+e(doc(source,title),quote=True)+"'></iframe></div><div><h3>Bản đề xuất</h3><iframe title='Bản đề xuất "+str(i)+"' sandbox='allow-popups' srcdoc='"+e(doc(body,title),quote=True)+"'></iframe></div></div><details><summary>HTML để copy vào body CMS sau khi duyệt</summary><button data-copy='body"+str(i)+"'>Copy HTML</button><textarea id='body"+str(i)+"' readonly>"+e(body)+"</textarea></details></section>")
parts.append("<section><h2>Điểm còn duyệt và kế hoạch</h2><pre>"+e(plan)+"</pre></section><script>document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=async()=>{const t=document.getElementById(b.dataset.copy);try{await navigator.clipboard.writeText(t.value);b.textContent='Đã copy'}catch(e){t.select();document.execCommand('copy');b.textContent='Đã chọn / copy HTML'}});</script></html>")
(OUT/"index.html").write_text("".join(parts),encoding="utf-8")
print("BUNDLE",OUT/"index.html")
print("PRESERVED",json.dumps(preservation,ensure_ascii=False))

