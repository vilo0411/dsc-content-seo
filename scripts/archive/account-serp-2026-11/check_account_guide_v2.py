from pathlib import Path
import subprocess,json,sys
sys.stdout.reconfigure(encoding="utf-8")
r=Path("knowledge/4-content/audits/account-serp-2026-11-04/v2")
draft="knowledge/4-content/2-drafts/serp-2026-11-04-v2/Optimize-cach-mo-tai-khoan-chung-khoan.md"
commands={
"lint":["scripts/qa_lint.py",draft,"--original","knowledge/4-content/audits/account-serp-2026-11-04/baseline-cach-mo-tai-khoan-chung-khoan.md","--cta"],
"style":["scripts/slop_check.py",draft,"-v"],
"facts":["scripts/market_facts.py","--verify",draft]}
results={}
for key,args in commands.items():
 p=subprocess.run([sys.executable]+args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding="utf-8",errors="replace")
 (r/(key+".txt")).write_text(p.stdout,encoding="utf-8")
 results[key]={"exit_code":p.returncode,"report":key+".txt"}
results["status"]="draft-not-published; do not equate lint pass with editorial/final QA pass"
results["reader_review"]="4H2/3H3 match agreed outline; removed fee calculation/FAQ repetition; no invented screenshots; captured images kept as DSC registration-system illustrations, not verified current App version"
(r/"checks.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
p=r/"index.html";t=p.read_text(encoding="utf-8")
t=t.replace("<p>Ảnh và các đích link live","<details><summary>Ghi chú kiểm tra nội bộ</summary><p>Lint 99, slop 94 (còn 2 MINOR). Dữ kiện thêm lấy từ brand profile DSC và bài DSC đang live (Thông tư 120/2020, giờ giao dịch). Chưa đánh dấu toàn bộ QA đạt.</p><p><a href='checks.json'>Các báo cáo kiểm tra</a></p></details><p>Ảnh và các đích link live")
p.write_text(t,encoding="utf-8")
old=r.parent/"index.html";t=old.read_text(encoding="utf-8")
notice="<div class='hold' id='v2-latest'><b>Bài hướng dẫn đã có bản viết lại theo outline VPBankS:</b> <a href='v2/index.html'>Đọc bản mới tại đây</a>. Không dùng bản hướng dẫn cũ bên dưới để cập nhật CMS.</div>"
if "id='v2-latest'" not in t:t=t.replace("<h1>",notice+"<h1>",1)
old.write_text(t,encoding="utf-8")
print(json.dumps(results,ensure_ascii=False))

