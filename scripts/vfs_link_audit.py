#!/usr/bin/env python3
"""VFS public HTML link audit. Knowledge archives + service hubs + deterministic cross-section sample."""
import sys, re, json, csv, time, random, hashlib
from pathlib import Path
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.parse import urlsplit, urlunsplit, urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding="utf-8")
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"knowledge/raw/competitors/vfs"
OUT.mkdir(parents=True,exist_ok=True)
(OUT/"html").mkdir(exist_ok=True)
HOST="https://www.vfs.com.vn"
pages={}; links=[]; failures=[]; discovery={}
def norm(u):
 p=urlsplit(u)
 h=p.netloc.lower()
 if h in ("vfs.com.vn","www.vfs.com.vn"): h="www.vfs.com.vn"
 return urlunsplit(("https" if h=="www.vfs.com.vn" else p.scheme,h,p.path.rstrip("/") or "/",p.query,""))
def get(u):
 key=hashlib.sha256(u.encode()).hexdigest()[:20]; f=OUT/"html"/(key+".html")
 if f.exists(): return 200,u,f.read_text(encoding="utf-8")
 for attempt in range(2):
  try:
   time.sleep(.25)
   with urlopen(Request(u,headers={"User-Agent":"Mozilla/5.0 (compatible; LinkResearch/1.0)"}),timeout=22) as r:
    s=r.read().decode("utf-8","replace"); final=r.url; status=r.status
   f.write_text(s,encoding="utf-8"); return status,final,s
  except HTTPError as e: return e.code,u,""
  except Exception as e:
   if attempt: return 0,u,str(e)
 return 0,u,""
def inside(a,selector): return any(p.name and p.select_one(":scope") is not None and False for p in []) # unused
def crawl(u):
 status,final,text=get(u)
 if status!=200:
  failures.append({"url":u,"status":status,"error":text[:180]}); return None
 s=BeautifulSoup(text,"html.parser")
 article=s.select_one("article")
 body=s.select_one("article .descrpition, article .entry-content")
 h=s.select_one("h1"); title=h.get_text(" ",strip=True) if h else (s.title.get_text(" ",strip=True) if s.title else u)
 cats=[c.removeprefix("category-") for c in (article.get("class",[]) if article else []) if c.startswith("category-")]
 group="Kiến thức" if any(c.startswith("kien-thuc") for c in cats) else ("Danh mục" if "/kien-thuc" in u or "/danh-muc" in u else ("Bài khác" if article else "Trang dịch vụ / hub"))
 rows=[]
 for a in s.select("a[href]"):
  if a.find_parent("noscript"): continue
  raw=a.get("href","").strip()
  if not raw or raw.startswith(("#","javascript:","mailto:","tel:","data:")): continue
  target=norm(urljoin(final,raw))
  if urlsplit(target).scheme not in ("http","https"): continue
  parents=list(a.parents)
  if body and body in parents: loc="body"
  elif any(x.get("id")=="breadcrumbs" or "breadcrumbs-wrapper" in x.get("class",[]) for x in parents if x.name): loc="breadcrumb"
  elif any(x.name=="header" or x.get("id")=="masthead" for x in parents if x.name): loc="header"
  elif any(x.name=="footer" or "main-footer" in x.get("class",[]) for x in parents if x.name): loc="footer"
  elif any("share" in x.get("class",[]) for x in parents if x.name): loc="share"
  else: loc="other"
  txt=a.get_text(" ",strip=True); alt=" | ".join(dict.fromkeys(i.get("alt","") for i in a.select("img") if i.get("alt")))
  host=urlsplit(target).hostname or ""
  kind="internal" if host=="www.vfs.com.vn" else ("subdomain" if host.endswith(".vfs.com.vn") else "external")
  if re.search(r"\.(pdf|docx?|xlsx?|zip)(?:[?#]|$)",target,re.I): kind="file-"+kind
  block=a.find_parent(["p","li"])
  mode="related" if loc=="body" and block and re.search(r"xem thêm|tham khảo|đọc thêm",block.get_text(" ",strip=True),re.I) else ("contextual" if loc=="body" else loc)
  rows.append({"from":u,"to":target,"anchor":txt,"image_alt":alt,"kind":kind,"location":loc,"mode":mode,"rel":" ".join(a.get("rel",[])),"raw_href":raw})
 canonical=s.select_one('link[rel="canonical"]')
 page={"url":u,"final_url":norm(final),"status":status,"title":title,"group":group,"categories":" | ".join(cats),"body_found":bool(body),"words":len(body.get_text(" ",strip=True).split()) if body else 0,"canonical":canonical.get("href","") if canonical else ""}
 return page,rows,s
def batch(urls,label):
 urls=sorted(set(norm(u) for u in urls)-set(pages))
 print(label,len(urls),flush=True)
 with ThreadPoolExecutor(max_workers=4) as ex:
  for i,r in enumerate(ex.map(crawl,urls),1):
   if r:
    p,l,s=r; pages[p["url"]]=p; links.extend(l)
   if i%40==0: print("  fetched",i,"/",len(urls),flush=True)
def locs(text): return re.findall(r"<loc>\s*(.*?)\s*</loc>",text)
# Enumerate all sitemap URLs without assuming old news URLs are current pages.
st,fi,xml=get(HOST+"/sitemap_index.xml")
maps=locs(xml); sitemap_urls=[]
with ThreadPoolExecutor(max_workers=4) as ex:
 for sm,r in zip(maps,ex.map(get,maps)):
  vals=locs(r[2]) if r[0]==200 else []
  discovery[sm]=len(vals); sitemap_urls.extend(vals)
(OUT/"sitemap-inventory.json").write_text(json.dumps({"sitemaps":discovery,"urls":sitemap_urls},ensure_ascii=False,indent=1),encoding="utf-8")
print("Sitemap URLs",len(sitemap_urls),flush=True)
# Follow archive pagination; collect actual article URLs from archive cards, excluding global menus.
archives=[HOST+"/kien-thuc",HOST+"/kien-thuc/kien-thuc-dau-tu",HOST+"/kien-thuc/kien-thuc-ky-thuat"]
seen=set(); knowledge=set()
while archives and len(seen)<100:
 todo=sorted(set(norm(u) for u in archives)-seen); archives=[]
 if not todo: break
 with ThreadPoolExecutor(max_workers=3) as ex:
  for u,r in zip(todo,ex.map(crawl,todo)):
   seen.add(u)
   if not r: continue
   p,l,s=r; pages[u]=p; links.extend(l)
   for a in s.select("main a[href]"):
    t=norm(urljoin(u,a["href"]))
    if urlsplit(t).hostname!="www.vfs.com.vn": continue
    if a.find_parent(class_="pagination") or "/page/" in t:
     if t not in seen: archives.append(t)
    elif a.find_parent("header") is None and a.get_text(" ",strip=True) and not re.search(r"/(kien-thuc|danh-muc|en)(/|$)",urlsplit(t).path): knowledge.add(t)
 print("Archives",len(seen),"article candidates",len(knowledge),flush=True)
batch(knowledge,"Knowledge/archive candidates")
page_urls=[norm(u) for u in sitemap_urls if any(x in u for x in ["/san-pham","/dich-vu","/ket-noi","/dang-ky","/ho-tro","/huong-dan","/trung-tam","/danh-muc","/kien-thuc","/tin-tuc"]) and "/en/" not in u and "/tabid/" not in u]
# Cover major entrypoints and deterministic sample from other modern posts; bounded crawl is disclosed.
modern=sorted(set(norm(u) for u in sitemap_urls if "/tabid/" not in u and "/en/" not in u and "/wp-" not in u)-set(pages))
rng=random.Random(20261104)
sample=rng.sample(modern,min(120,len(modern)))
batch([HOST+"/",HOST+"/trung-tam-kien-thuc",HOST+"/dang-ky-mo-tai-khoan"]+page_urls+sample,"Hubs/services and other-section sample")
# Expand only knowledge articles found via actual article body links.
extra={l["to"] for l in links if l["location"]=="body" and l["kind"]=="internal" and l["to"] not in pages and not re.search(r"/(wp-|tabid|en/)",l["to"])}
batch(sorted(extra)[:250],"Additional in-body targets (max 250)")
def writecsv(name,rows,fields=None):
 if not rows and not fields: return
 with (OUT/name).open("w",newline="",encoding="utf-8-sig") as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0])); w.writeheader(); w.writerows(rows)
# Use unique referring pages for inlinks; occurrences are kept separately.
for u,p in pages.items():
 incoming=[l for l in links if l["to"]==u and l["from"]!=u]
 outgoing=[l for l in links if l["from"]==u]
 p.update(in_pages=len({l["from"] for l in incoming}),in_body_pages=len({l["from"] for l in incoming if l["location"]=="body"}),out_internal_pages=len({l["to"] for l in outgoing if l["kind"]=="internal" and l["to"]!=u}),out_body_internal_pages=len({l["to"] for l in outgoing if l["kind"]=="internal" and l["location"]=="body" and l["to"]!=u}),out_external=sum(l["kind"]=="external" for l in outgoing),out_body_external=sum(l["kind"]=="external" and l["location"]=="body" for l in outgoing))
writecsv("pages.csv",list(pages.values())); writecsv("links.csv",links)
writecsv("failures.csv",failures,["url","status","error"])
anchors=Counter((l["anchor"] or "[ảnh: "+l["image_alt"]+"]" if l["image_alt"] else l["anchor"] or "[trống]",l["kind"],l["location"]) for l in links)
ar=[{"anchor":a,"kind":k,"location":z,"occurrences":n} for (a,k,z),n in anchors.most_common()]
writecsv("anchors.csv",ar)
kb=[p for p in pages.values() if p["group"]=="Kiến thức"]
body=[l for l in links if l["location"]=="body"]
meta={"date":"2026-11-04","sitemap_urls":len(sitemap_urls),"crawled_pages":len(pages),"archive_pages":len(seen),"archive_candidates":len(knowledge),"knowledge_articles":len(kb),"link_occurrences":len(links),"body_links":len(body),"failures":len(failures),"scope":"Toàn bộ phân trang kiến thức tìm thấy (tối đa 100 archive); trang dịch vụ/hub từ sitemap; 120 URL hiện đại lấy mẫu seed 20261104; mở rộng tối đa 250 đích body. Không phải full-site crawl, không đo backlink từ website bên ngoài; không chạy JavaScript hoặc trích liên kết bên trong PDF.","sitemaps":discovery}
(OUT/"_meta.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
data={"meta":meta,"pages":list(pages.values()),"links":links,"anchors":ar,"failures":failures}
(OUT/"audit-data.json").write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
print(json.dumps(meta,ensure_ascii=False,indent=2),flush=True)

