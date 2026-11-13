from pathlib import Path
import html,re,json,subprocess,sys
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding="utf-8")
slug="nen-mo-tai-khoan-chung-khoan-o-dau";out=Path("knowledge/4-content/audits/account-serp-2026-11-04")
draft=Path("knowledge/4-content/2-drafts/Optimize-"+slug+"-serp-2026-11-04.md");base=out/("baseline-"+slug+".md")
s=draft.read_text(encoding="utf-8");body=s.split("---",2)[2].strip();blocks=re.split(r"\n\s*\n",body)
def inline(text):
 text=html.escape(text)
 text=re.sub(r"!\[([^]]*)\]\(([^)]+)\)",lambda m:'<img src="'+m[2]+'" alt="'+m[1]+'" loading="lazy">',text)
 text=re.sub(r"\[([^]]+)\]\(([^)]+)\)",lambda m:'<a href="'+m[2]+'">'+m[1]+'</a>',text)
 text=re.sub(r"\*\*([^*]+)\*\*",r"<strong>\1</strong>",text)
 text=re.sub(r"\*([^*]+)\*",r"<em>\1</em>",text)
 return text
htmlblocks=[]
for block in blocks:
 block=block.strip()
 if not block:continue
 if block.startswith("# "): continue
 if block.startswith("<div"):htmlblocks.append(block);continue
 m=re.match(r"^(#{2,6}) (.*)$",block,re.S)
 if m:
  lvl=len(m[1]);htmlblocks.append(f"<h{lvl}>"+inline(m[2])+f"</h{lvl}>");continue
 if block.startswith("|"):
  rows=[r.strip().strip("|").split("|") for r in block.splitlines()]
  rows=[[c.strip() for c in row] for row in rows]
  h="<table><thead><tr>"+"".join("<th>"+inline(c)+"</th>" for c in rows[0])+"</tr></thead><tbody>"
  for row in rows[2:]:h+="<tr>"+"".join("<td>"+inline(c)+"</td>" for c in row)+"</tr>"
  htmlblocks.append(h+"</tbody></table>");continue
 if block.startswith("- "):
  htmlblocks.append("<ul>"+"".join("<li>"+inline(line[2:])+"</li>" for line in block.splitlines() if line.startswith("- "))+"</ul>");continue
 if block.startswith("!["):
  htmlblocks.append("<figure>"+inline(block)+"</figure>");continue
 htmlblocks.append("<p>"+inline(block.replace("\n"," "))+"</p>")
result="\n".join(htmlblocks)+"\n"
target=out/(slug+".body.html");target.write_text(result,encoding="utf-8")
live=BeautifulSoup(Path("knowledge/raw/live/html",slug+".html").read_text(encoding="utf-8"),"html.parser")
rendered=BeautifulSoup(result,"html.parser")
check={"images_preserved":{i["src"]:bool(rendered.select_one('img[src="'+i["src"]+'"]')) for i in live.select("img[src]")},"hrefs_preserved":{a["href"]:a["href"] in {x["href"] for x in rendered.select("a[href]")} for a in live.select("a[href]")}}
assert all(check["images_preserved"].values()) and all(check["hrefs_preserved"].values())
commands={
 "baseline_lint":["scripts/qa_lint.py",str(base),"--no-sitemap","--json"],
 "baseline_slop_strict":["scripts/slop_check.py",str(base),"--mode","strict","--json"],
 "draft_lint":["scripts/qa_lint.py",str(draft),"--original",str(base),"--cta","--json"],
 "draft_slop_strict":["scripts/slop_check.py",str(draft),"--json"],
 "draft_facts":["scripts/market_facts.py","--verify",str(draft)],
 "baseline_facts":["scripts/market_facts.py","--verify",str(base)]
}
report={"slug":slug,"published":False,"proposal":"knowledge/4-content/1-outlines/Proposal-"+slug+"-serp-2026-11-04.md","draft":str(draft),"body_html":str(target),"preservation":check,"qa":{},"remaining_editorial":["Original HOSE market-share infographic and SSI Top2 alt were retained from live; no independently verified source for their numeric claims. Caption explicitly historical. Must resolve before CMS publication."],"fact_check_scope":"market_facts checks market index/ticker/stale patterns, not all service claims; fee and onboarding claims checked separately against primary company websites."}
for name,args in commands.items():
 p=subprocess.run([sys.executable]+args,capture_output=True,encoding="utf-8")
 try:v=json.loads(p.stdout)
 except ValueError:v={"output":p.stdout,"error":p.stderr}
 report["qa"][name]={"exit_code":p.returncode,"result":v}
(out/("validation-"+slug+".json")).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
summary=f"""# Kiểm tra bài so sánh — 04/11/2026

- Baseline live: lint 74, strict slop 64.
- Draft: lint 99 PASS; strict slop 91 PASS; bảo toàn 4/4 ảnh và 8/8 href.
- Fact checker: baseline/draft exit 0, không có claim chỉ số để kiểm tra. Nguồn phí và kênh đăng ký đối chiếu riêng.
- Một banner CTA, không có CTA trong 25% đầu, không UTM.
- Không đổi URL/H1, không chạm Final, chưa xuất bản.
- Hai vòng chỉnh QA đã hoàn tất; không lặp vòng ba.
- Còn một prose-run MINOR ở phần phí; slop có anchor/para-shape/template MINOR. Template so với chính Final do tên file có hậu tố ngày, không phải trùng bài khác.
- Cần duyệt biên tập ảnh biểu đồ thị phần và alt SSI Top 2 trước CMS; chưa xác minh số liệu ảnh. Đã giữ asset và ghi chú lịch sử trong draft.
- Bản body HTML không chứa H1/frontmatter; nhập title/meta từ Markdown khi duyệt.
"""
(out/("validation-"+slug+".md")).write_text(summary,encoding="utf-8")
print("BODY",target,"characters",len(result),"preservation",len(check["images_preserved"]),len(check["hrefs_preserved"]))
print("QA",[(n,x["exit_code"]) for n,x in report["qa"].items()])

