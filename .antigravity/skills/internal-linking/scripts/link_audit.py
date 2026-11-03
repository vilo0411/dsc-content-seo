#!/usr/bin/env python3
"""Internal-link audit on the LIVE site (snapshot from scripts/sync_live.py).

Reads knowledge/raw/live/{pages.csv,links.csv,_meta.json} + internal-links/link-clusters.json
(+ knowledge/raw/gsc/pages.csv for clicks, optional) and writes:

  knowledge/3-pipeline/internal-links/dashboard.md    — for agents: cluster compliance, orphans,
                                                        pages still using "Xem thêm", anchor conflicts
  knowledge/3-pipeline/internal-links/link-graph.html — for humans: interactive graph + table
                                                        (offline, no CDN; gitignored — regenerate)

Usage:  python .antigravity/skills/internal-linking/scripts/link_audit.py [--orphans]
        (run scripts/sync_live.py first when the snapshot is older than a week)
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[4]
LIVE = ROOT / "knowledge/raw/live"
IL = ROOT / "knowledge/3-pipeline/internal-links"
CLUSTERS = IL / "link-clusters.json"
GSC_PAGES = ROOT / "knowledge/raw/gsc/pages.csv"
OUT_MD = IL / "dashboard.md"
OUT_HTML = IL / "link-graph.html"
KB = "https://www.dsc.com.vn/kien-thuc/"
STALE_DAYS = 7


def read_csv(p: Path) -> list[dict]:
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s.lower())
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()


def load_clicks() -> dict[str, int]:
    if not GSC_PAGES.exists():
        return {}
    out = {}
    for r in read_csv(GSC_PAGES):
        url = (r.get("page") or r.get("Page") or r.get("url") or "").rstrip("/")
        if url.startswith(KB):
            try:
                out[url[len(KB):]] = int(float(r.get("clicks") or r.get("Clicks") or 0))
            except ValueError:
                pass
    return out


def build() -> dict:
    if not (LIVE / "pages.csv").exists():
        sys.exit("Chưa có snapshot live — chạy: python scripts/sync_live.py")
    pages = read_csv(LIVE / "pages.csv")
    links = [r for r in read_csv(LIVE / "links.csv") if r["kind"] in ("contextual", "xem-them")]
    meta = json.loads((LIVE / "_meta.json").read_text(encoding="utf-8")) if (LIVE / "_meta.json").exists() else {}
    clusters = json.loads(CLUSTERS.read_text(encoding="utf-8"))["clusters"] if CLUSTERS.exists() else []
    clicks = load_clicks()

    # slug -> (cluster index 1.., role, group name, hub of the group)
    member: dict[str, tuple[int, str, str, str | None]] = {}
    for ci, c in enumerate(clusters, 1):
        member[c["pillar"]] = (ci, "pillar", "", None)
        for g in c["groups"]:
            if g.get("hub"):
                member[g["hub"]] = (ci, "hub", g["name"], None)
            for s in g["spokes"]:
                member[s] = (ci, "spoke", g["name"], g.get("hub"))

    idx = {p["slug"]: i for i, p in enumerate(pages)}
    out_ctx: dict[str, set] = defaultdict(set)
    in_xem: Counter = Counter()
    edges = []
    for r in links:
        tgt = r["to"].rstrip("/").rsplit("/", 1)[-1]
        if r["from"] not in idx or tgt not in idx or tgt == r["from"]:
            continue
        if r["kind"] == "contextual":
            out_ctx[r["from"]].add(tgt)
        else:
            in_xem[tgt] += 1
        edges.append([idx[r["from"]], idx[tgt], 0 if r["kind"] == "contextual" else 1, r["anchor"], r["section"]])

    nodes = []
    for p in pages:
        s = p["slug"]
        ci, role, group, hub = member.get(s, (0, "", "", None))
        warn = []
        if ci and role != "pillar" and clusters[ci - 1]["pillar"] not in out_ctx[s]:
            warn.append("chưa link pillar")
        if hub and hub not in out_ctx[s]:
            warn.append("chưa link hub")
        nodes.append({"s": s, "t": p["title"], "c": ci, "r": role, "g": group, "w": int(p["words"]),
                      "ic": int(p["in_contextual"]), "ix": in_xem[s], "oc": int(p["out_contextual"]),
                      "ox": int(p["out_xem_them"]), "cta": int(p["out_cta"]), "k": clicks.get(s),
                      "warn": warn})

    # Same anchor text used for several different targets (contextual links only).
    anchor_targets: dict[str, Counter] = defaultdict(Counter)
    for r in links:
        if r["kind"] == "contextual" and r["anchor"]:
            anchor_targets[norm(r["anchor"])][r["to"].rsplit("/", 1)[-1]] += 1
    conflicts = sorted(((a, t) for a, t in anchor_targets.items() if len(t) > 1),
                       key=lambda x: -sum(x[1].values()))

    return {"nodes": nodes, "edges": edges, "clusters": [{"name": c["name"], "pillar": c["pillar"]} for c in clusters],
            "meta": meta, "conflicts": conflicts, "has_clicks": bool(clicks)}


# ──────────────────────────── markdown dashboard ────────────────────────────

def write_md(d: dict) -> None:
    N, meta = d["nodes"], d["meta"]
    last = meta.get("last_run", "?")
    age = (datetime.now() - datetime.fromisoformat(last)).days if last != "?" else 999
    ctx_edges = sum(1 for e in d["edges"] if e[2] == 0)
    xem_edges = len(d["edges"]) - ctx_edges
    orphans = [n for n in N if n["ic"] == 0]
    xem_pages = sorted((n for n in N if n["ox"] > 0), key=lambda n: (-(n["k"] or 0), -n["ox"]))
    key = (lambda n: -(n["k"] or 0)) if d["has_clicks"] else (lambda n: -n["w"])
    L = [
        "# Internal Link Dashboard — site live",
        "",
        f"> Sinh tự động bởi `link_audit.py` từ snapshot `knowledge/raw/live/` (sync {last[:16]}). "
        "Không sửa tay. Graph tương tác: `internal-links/link-graph.html`.",
    ]
    if age > STALE_DAYS:
        L += ["", f"> ⚠ Snapshot đã {age} ngày — chạy `python scripts/sync_live.py` rồi chạy lại audit."]
    L += ["", "## Tổng quan", "",
          "| Chỉ số | Giá trị |", "|---|---:|",
          f"| Bài live | {len(N)} |",
          f"| Link ngữ cảnh (trong câu) giữa các bài | {ctx_edges} |",
          f"| Link nằm trong dòng Xem thêm | {xem_edges} |",
          f"| Bài còn dòng Xem thêm | {len(xem_pages)} |",
          f"| Bài 0 inlink ngữ cảnh | {len(orphans)} |",
          f"| Bài trong cụm thiếu link pillar/hub | {sum(1 for n in N if n['warn'])} |", ""]

    for ci, c in enumerate(d["clusters"], 1):
        mem = [n for n in N if n["c"] == ci]
        order = {"pillar": 0, "hub": 1, "spoke": 2}
        mem.sort(key=lambda n: (order.get(n["r"], 3), n["g"], n["s"]))
        L += [f"## Cụm: {c['name']} (pillar `{c['pillar']}`)", "",
              "| Bài | Vai trò | Nhóm | In ngữ cảnh | In Xem thêm | Out ngữ cảnh | Cảnh báo |",
              "|---|---|---|---:|---:|---:|---|"]
        for n in mem:
            L.append(f"| {n['s']} | {n['r']} | {n['g']} | {n['ic']} | {n['ix']} | {n['oc']} | "
                     f"{'⚠ ' + ', '.join(n['warn']) if n['warn'] else ''} |")
        L.append("")

    L += [f"## Bài 0 inlink ngữ cảnh ({len(orphans)}) — top 40 theo {'clicks GSC' if d['has_clicks'] else 'số từ'}", "",
          "Backfill: `python scripts/find_links.py --backfill <slug>`", "",
          "| Bài | Clicks | Từ | In Xem thêm |", "|---|---:|---:|---:|"]
    for n in sorted(orphans, key=key)[:40]:
        L.append(f"| {n['s']} | {n['k'] if n['k'] is not None else '-'} | {n['w']} | {n['ix']} |")
    L += ["", f"## Bài còn dòng Xem thêm ({len(xem_pages)}) — top 40", "",
          "Viết lại thành câu có ngữ cảnh khi optimize bài (rule `LINK-xemthem`).", "",
          "| Bài | Link Xem thêm | Link ngữ cảnh | Clicks |", "|---|---:|---:|---:|"]
    for n in xem_pages[:40]:
        L.append(f"| {n['s']} | {n['ox']} | {n['oc']} | {n['k'] if n['k'] is not None else '-'} |")
    L += ["", "## Anchor trùng nhau trỏ tới nhiều bài khác nhau — top 25", "",
          "Một anchor nên đại diện cho một bài. Anchor trùng keyword pillar phải trỏ về pillar.", "",
          "| Anchor | Số đích | Đích (số lần) |", "|---|---:|---|"]
    for a, t in d["conflicts"][:25]:
        L.append(f"| {a} | {len(t)} | " + ", ".join(f"{s} ({n})" for s, n in t.most_common(4)) + " |")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")


# ──────────────────────────── HTML graph ────────────────────────────

HTML = r"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Internal link live — DSC /kien-thuc</title>
<style>
.viz-root{--surface-1:#fcfcfb;--surface-2:#f3f2ee;--text-primary:#0b0b0b;--text-secondary:#52514e;--muted:#898781;
  --grid:#e1e0d9;--ring:rgba(11,11,11,.10);--s1:#2a78d6;--s2:#eb6834;--edge:rgba(82,81,78,.16);--edge-hi:#0b0b0b}
@media (prefers-color-scheme:dark){:root:where(:not([data-theme="light"])) .viz-root{color-scheme:dark;--surface-1:#1a1a19;--surface-2:#242423;
  --text-primary:#f0efec;--text-secondary:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--ring:rgba(255,255,255,.10);--s1:#3987e5;--s2:#d95926;
  --edge:rgba(195,194,183,.14);--edge-hi:#f0efec}}
:root[data-theme="dark"] .viz-root{color-scheme:dark;--surface-1:#1a1a19;--surface-2:#242423;--text-primary:#f0efec;--text-secondary:#c3c2b7;
  --muted:#898781;--grid:#2c2c2a;--ring:rgba(255,255,255,.10);--s1:#3987e5;--s2:#d95926;--edge:rgba(195,194,183,.14);--edge-hi:#f0efec}
*{box-sizing:border-box}body{margin:0}
.viz-root{font:14px/1.5 system-ui,-apple-system,"Segoe UI",Arial,sans-serif;background:var(--surface-1);color:var(--text-primary);min-height:100vh;padding:20px 24px}
h1{font-size:20px;margin:0 0 2px}.sub{color:var(--text-secondary);margin:0 0 16px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:14px}
.tile{background:var(--surface-2);border-radius:8px;padding:10px 12px}.tile b{display:block;font-size:22px;font-variant-numeric:tabular-nums}
.tile span{color:var(--text-secondary);font-size:12px}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:10px}
.bar input[type=search],.bar select,.bar button{font:inherit;color:var(--text-primary);background:var(--surface-1);border:1px solid var(--grid);border-radius:6px;padding:6px 10px}
.bar input[type=search]{width:260px}.bar label{color:var(--text-secondary);display:flex;gap:5px;align-items:center;cursor:pointer}
.bar button{cursor:pointer}.grow{flex:1}
.legend{display:flex;flex-wrap:wrap;gap:16px;color:var(--text-secondary);font-size:12px;margin-bottom:8px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:-1px}
.wrap{display:grid;grid-template-columns:1fr 360px;gap:12px}
#cv{width:100%;height:68vh;background:var(--surface-1);border:1px solid var(--grid);border-radius:8px;display:block;cursor:grab}
#panel{border:1px solid var(--grid);border-radius:8px;padding:12px 14px;height:68vh;overflow:auto;font-size:13px}
#panel h2{font-size:15px;margin:0 0 4px}#panel h3{font-size:13px;margin:14px 0 4px;color:var(--text-secondary)}
#panel ul{margin:0;padding-left:16px}#panel li{margin:2px 0}#panel a{color:var(--text-primary)}
.k{display:inline-block;font-size:11px;border:1px solid var(--grid);border-radius:4px;padding:0 4px;color:var(--text-secondary);margin-right:4px}
.warn{font-weight:600}.muted{color:var(--text-secondary)}
.jump{cursor:pointer;text-decoration:underline dotted}
#tip{position:fixed;pointer-events:none;background:var(--surface-1);color:var(--text-primary);border:1px solid var(--grid);border-radius:6px;
  padding:8px 10px;font-size:12px;box-shadow:0 2px 10px rgba(0,0,0,.15);max-width:340px;display:none;z-index:5}
#tip b{display:block;margin-bottom:3px}
table{width:100%;border-collapse:collapse;margin-top:16px;font-size:13px;font-variant-numeric:tabular-nums}
th,td{padding:5px 8px;border-bottom:1px solid var(--grid);text-align:left}th{cursor:pointer;color:var(--text-secondary);font-weight:600;position:sticky;top:0;background:var(--surface-1)}
td.n,th.n{text-align:right}tr:hover td{background:var(--surface-2)}
@media (max-width:1000px){.wrap{grid-template-columns:1fr}#panel{height:auto}}
</style></head>
<body><div class="viz-root">
<h1>Internal link — site live (/kien-thuc)</h1>
<p class="sub" id="sub"></p>
<div class="tiles" id="tiles"></div>
<div class="bar">
 <input type="search" id="q" placeholder="Tìm slug / tiêu đề…">
 <select id="fc"></select>
 <label><input type="checkbox" id="fx"> Hiện link Xem thêm</label>
 <label><input type="checkbox" id="fo"> Đánh dấu bài 0 inlink ngữ cảnh</label>
 <span class="grow"></span>
 <button id="reset">Bố cục lại</button><button id="theme">Sáng / tối</button>
</div>
<div class="legend" id="legend"></div>
<div class="wrap"><canvas id="cv"></canvas><div id="panel"><p class="muted">Rê chuột vào một bài để xem nhanh, bấm để ghim và xem toàn bộ link vào/ra. Lăn chuột để zoom, kéo nền để di chuyển.</p></div></div>
<table id="tb"><thead></thead><tbody></tbody></table>
<div id="tip"></div>
</div>
<script>
const D=__DATA__;
const N=D.nodes,E=D.edges,KB="https://www.dsc.com.vn/kien-thuc/";
const CL=["Ngoài cụm",...D.clusters.map(c=>c.name)];
const root=document.querySelector(".viz-root"),cv=document.getElementById("cv"),ctx=cv.getContext("2d"),tip=document.getElementById("tip");
const css=v=>getComputedStyle(root).getPropertyValue(v).trim();
const color=c=>c===1?css("--s1"):c===2?css("--s2"):css("--muted");
const outE=N.map(()=>[]),inE=N.map(()=>[]);E.forEach((e,i)=>{outE[e[0]].push(i);inE[e[1]].push(i)});
N.forEach(n=>n.rad=3+Math.sqrt(n.ic)*1.6+(n.r==="pillar"?4:0));
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const fmt=n=>n==null?"–":n.toLocaleString("vi-VN");

// header + tiles
const ctxN=E.filter(e=>e[2]===0).length;
document.getElementById("sub").textContent=`Snapshot ${String(D.meta.last_run||"?").replace("T"," ").slice(0,16)} · nguồn knowledge/raw/live (sync_live.py) · ${N.length} bài`;
const tiles=[["Bài live",N.length],["Link ngữ cảnh",ctxN],["Link Xem thêm",E.length-ctxN],["Bài còn Xem thêm",N.filter(n=>n.ox>0).length],
 ["Bài 0 inlink ngữ cảnh",N.filter(n=>n.ic===0).length],["Bài cụm thiếu link pillar/hub",N.filter(n=>n.warn.length).length]];
document.getElementById("tiles").innerHTML=tiles.map(t=>`<div class="tile"><b>${fmt(t[1])}</b><span>${t[0]}</span></div>`).join("");
const fc=document.getElementById("fc");
fc.innerHTML=`<option value="-1">Tất cả bài</option>`+CL.map((c,i)=>i?`<option value="${i}">Cụm: ${esc(c)} (+ bài nối trực tiếp)</option>`:"").join("")+`<option value="0">Chỉ bài ngoài cụm</option>`;
function legend(){document.getElementById("legend").innerHTML=CL.map((c,i)=>`<span><i style="background:${color(i)}"></i>${esc(c)}</span>`).join("")+
 `<span>◎ viền đậm = pillar · viền mảnh = hub</span><span>○ rỗng = 0 inlink ngữ cảnh (khi bật)</span><span>kích thước = số inlink ngữ cảnh</span><span>- - - = link Xem thêm</span>`}
legend();

// visibility
let vis=new Set(N.map((_,i)=>i));
function computeVis(){
 const c=+fc.value,q=document.getElementById("q").value.trim().toLowerCase();vis=new Set();
 if(c===-1)N.forEach((_,i)=>vis.add(i));
 else if(c===0)N.forEach((n,i)=>{if(!n.c)vis.add(i)});
 else{N.forEach((n,i)=>{if(n.c===c){vis.add(i);outE[i].forEach(k=>{if(E[k][2]===0)vis.add(E[k][1])});inE[i].forEach(k=>{if(E[k][2]===0)vis.add(E[k][0])})}})}
 match=q?new Set(N.map((n,i)=>i).filter(i=>N[i].s.includes(q)||N[i].t.toLowerCase().includes(q))):null;
}
let match=null;

// force layout (O(n^2) repulsion, fine for ~1k nodes), runs in slices to keep the page responsive
let W=0,H=0,dpr=1,scale=1,tx=0,ty=0,running=0;
function resize(){dpr=window.devicePixelRatio||1;const r=cv.getBoundingClientRect();W=r.width;H=r.height;cv.width=W*dpr;cv.height=H*dpr;draw()}
function layout(){
 const run=++running;
 const es=E.filter(e=>e[2]===0&&vis.has(e[0])&&vis.has(e[1]));
 const deg=new Map();es.forEach(e=>{deg.set(e[0],(deg.get(e[0])||0)+1);deg.set(e[1],(deg.get(e[1])||0)+1)});
 // Pages with no in-sentence link in the current view would drift to a far ring and shrink the
 // network to a dot — simulate only connected pages, park isolates in a grid underneath.
 // Same for small islands (2-5 pages linking only each other): keep the largest component in the
 // simulation, pack every other component (members kept adjacent) into the grid.
 const adj=new Map();es.forEach(e=>{for(const[a,b]of[[e[0],e[1]],[e[1],e[0]]]){if(!adj.has(a))adj.set(a,[]);adj.get(a).push(b)}});
 const comp=new Map();let comps=[];for(const i of vis){if(comp.has(i))continue;const q=[i],m=[];comp.set(i,comps.length);
  while(q.length){const u=q.pop();m.push(u);for(const v of adj.get(u)||[])if(!comp.has(v)){comp.set(v,comps.length);q.push(v)}}comps.push(m)}
 comps.sort((a,b)=>b.length-a.length);
 const ids=comps.length&&comps[0].length>1?comps[0]:[];
 const iso=comps.slice(ids.length?1:0).sort((a,b)=>b.length-a.length||N[a[0]].c-N[b[0]].c).flat();
 const n=ids.length,k=Math.sqrt(1e6/Math.max(n,1));
 ids.forEach(i=>{const a=Math.random()*6.283,r=200+Math.random()*300;const c=N[i].c;N[i].x=r*Math.cos(a)+(c===1?-250:c===2?250:0);N[i].y=r*Math.sin(a)});
 let it=0,T=60;const ITER=260;
 function parkIsolates(){if(!iso.length)return;let x0=1e9,x1=-1e9,y1=-1e9;for(const i of ids){x0=Math.min(x0,N[i].x);x1=Math.max(x1,N[i].x);y1=Math.max(y1,N[i].y)}
  if(!ids.length){x0=0;x1=800;y1=0}const g=Math.max(14,k*.45),cols=Math.max(10,Math.floor((x1-x0)/g));
  iso.forEach((i,j)=>{N[i].x=x0+(j%cols)*g;N[i].y=y1+g*3+Math.floor(j/cols)*g})}
 function step(){if(run!==running)return;
  for(let s=0;s<8&&it<ITER;s++,it++){
   for(const i of ids){N[i].dx=0;N[i].dy=0}
   for(let a=0;a<n;a++){const p=N[ids[a]];for(let b=a+1;b<n;b++){const q=N[ids[b]];let dx=p.x-q.x,dy=p.y-q.y,d2=dx*dx+dy*dy+.01;const f=k*k/d2;dx*=f;dy*=f;p.dx+=dx;p.dy+=dy;q.dx-=dx;q.dy-=dy}}
   for(const e of es){const p=N[e[0]],q=N[e[1]];const dx=p.x-q.x,dy=p.y-q.y,d=Math.sqrt(dx*dx+dy*dy)+.01,f=d/k;p.dx-=dx*f;p.dy-=dy*f;q.dx+=dx*f;q.dy+=dy*f}
   for(const i of ids){const p=N[i];p.dx-=p.x*.012*k/40;p.dy-=p.y*.012*k/40;const d=Math.sqrt(p.dx*p.dx+p.dy*p.dy)+.01,m=Math.min(d,T);p.x+=p.dx/d*m;p.y+=p.dy/d*m}
   T=Math.max(1,T*.985)}
  parkIsolates();fit();draw();if(it<ITER)setTimeout(step,0)}
 step()}
function fit(){let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;for(const i of vis){const p=N[i];x0=Math.min(x0,p.x);x1=Math.max(x1,p.x);y0=Math.min(y0,p.y);y1=Math.max(y1,p.y)}
 if(x0>x1)return;scale=Math.min(W/(x1-x0+80),H/(y1-y0+80));tx=W/2-scale*(x0+x1)/2;ty=H/2-scale*(y0+y1)/2}
const sx=p=>p.x*scale+tx,sy=p=>p.y*scale+ty;

let hover=-1,sel=-1;
function draw(){
 ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);
 const showX=document.getElementById("fx").checked,showO=document.getElementById("fo").checked,focus=sel>=0?sel:hover;
 const nb=new Set();if(focus>=0){nb.add(focus);outE[focus].forEach(k=>nb.add(E[k][1]));inE[focus].forEach(k=>nb.add(E[k][0]))}
 ctx.lineWidth=1;
 for(const e of E){if(!vis.has(e[0])||!vis.has(e[1]))continue;if(e[2]===1&&!showX)continue;
  ctx.strokeStyle=css("--edge");ctx.setLineDash(e[2]===1?[3,3]:[]);ctx.beginPath();ctx.moveTo(sx(N[e[0]]),sy(N[e[0]]));ctx.lineTo(sx(N[e[1]]),sy(N[e[1]]));ctx.stroke()}
 ctx.setLineDash([]);
 if(focus>=0){ctx.strokeStyle=css("--edge-hi");ctx.fillStyle=css("--edge-hi");
  for(const k of [...outE[focus],...inE[focus]]){const e=E[k];if(!vis.has(e[0])||!vis.has(e[1]))continue;if(e[2]===1&&!showX)continue;
   const a=N[e[0]],b=N[e[1]];ctx.lineWidth=1.5;ctx.setLineDash(e[2]===1?[4,3]:[]);ctx.beginPath();ctx.moveTo(sx(a),sy(a));ctx.lineTo(sx(b),sy(b));ctx.stroke();ctx.setLineDash([]);
   const ang=Math.atan2(sy(b)-sy(a),sx(b)-sx(a)),r=b.rad*Math.max(.6,Math.min(scale*1.5,1.6))+2,hx=sx(b)-Math.cos(ang)*r,hy=sy(b)-Math.sin(ang)*r;
   ctx.beginPath();ctx.moveTo(hx,hy);ctx.lineTo(hx-7*Math.cos(ang-.4),hy-7*Math.sin(ang-.4));ctx.lineTo(hx-7*Math.cos(ang+.4),hy-7*Math.sin(ang+.4));ctx.fill()}}
 const sf=Math.max(.6,Math.min(scale*1.5,1.6));
 for(const i of vis){const p=N[i],r=p.rad*sf,dim=(focus>=0&&!nb.has(i))||(match&&!match.has(i));
  ctx.globalAlpha=dim?.15:(p.c?1:.65);ctx.beginPath();ctx.arc(sx(p),sy(p),r,0,6.283);
  if(showO&&p.ic===0){ctx.fillStyle=css("--surface-1");ctx.fill();ctx.lineWidth=1.5;ctx.strokeStyle=color(p.c);ctx.stroke()}
  else{ctx.fillStyle=color(p.c);ctx.fill();ctx.lineWidth=2;ctx.strokeStyle=css("--surface-1");ctx.stroke()}
  if(p.r==="pillar"||p.r==="hub"){ctx.beginPath();ctx.arc(sx(p),sy(p),r+3,0,6.283);ctx.lineWidth=p.r==="pillar"?2.5:1.2;ctx.strokeStyle=css("--text-primary");ctx.stroke()}}
 ctx.globalAlpha=1;ctx.font="600 12px system-ui,Segoe UI,Arial";ctx.lineJoin="round";
 for(const i of vis){const p=N[i];if(!(p.r==="pillar"||i===focus||(match&&match.has(i)&&match.size<15)))continue;
  // pillars of different clusters sit close together: cluster 1 labels above, others below
  const lx=sx(p)+p.rad*sf+5,ly=sy(p)+(p.r==="pillar"&&i!==focus?(p.c===1?-10:16):4),t=p.t.slice(0,48);
  ctx.lineWidth=4;ctx.strokeStyle=css("--surface-1");ctx.strokeText(t,lx,ly);ctx.fillStyle=css("--text-primary");ctx.fillText(t,lx,ly)}
}
function pick(mx,my){let best=-1,bd=1e9;const sf=Math.max(.6,Math.min(scale*1.5,1.6));
 for(const i of vis){const p=N[i],dx=sx(p)-mx,dy=sy(p)-my,d=dx*dx+dy*dy,r=p.rad*sf+6;if(d<r*r&&d<bd){bd=d;best=i}}return best}

// interaction
let drag=null;
cv.addEventListener("mousedown",e=>{drag={x:e.clientX,y:e.clientY,tx,ty,moved:false};cv.style.cursor="grabbing"});
window.addEventListener("mouseup",e=>{if(drag&&!drag.moved){const r=cv.getBoundingClientRect();const i=pick(e.clientX-r.left,e.clientY-r.top);if(e.target===cv){sel=i;showPanel(i);draw()}}drag=null;cv.style.cursor="grab"});
cv.addEventListener("mousemove",e=>{const r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
 if(drag){const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>3)drag.moved=true;tx=drag.tx+dx;ty=drag.ty+dy;draw();return}
 const i=pick(mx,my);if(i!==hover){hover=i;draw()}
 if(i>=0){const n=N[i];tip.style.display="block";tip.innerHTML=`<b>${esc(n.t)}</b>${esc(CL[n.c])}${n.r?" · "+n.r:""}${n.g?" · "+esc(n.g):""}<br>
 In ngữ cảnh <b style="display:inline">${n.ic}</b> · In Xem thêm ${n.ix} · Out ngữ cảnh ${n.oc} · Out Xem thêm ${n.ox} · CTA ${n.cta}${n.k!=null?"<br>Clicks GSC "+fmt(n.k):""}${n.warn.length?"<br>⚠ "+n.warn.join(", "):""}`;
  tip.style.left=Math.min(e.clientX+14,innerWidth-350)+"px";tip.style.top=(e.clientY+14)+"px"}else tip.style.display="none"});
cv.addEventListener("mouseleave",()=>{tip.style.display="none";hover=-1;draw()});
cv.addEventListener("wheel",e=>{e.preventDefault();const r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top,f=e.deltaY<0?1.15:1/1.15;
 tx=mx-(mx-tx)*f;ty=my-(my-ty)*f;scale*=f;draw()},{passive:false});

function showPanel(i){const P=document.getElementById("panel");if(i<0){P.innerHTML='<p class="muted">Bấm vào một bài để xem link vào/ra.</p>';return}
 const n=N[i],li=(k,dir)=>{const e=E[k],o=N[dir==="out"?e[1]:e[0]];return `<li><span class="k">${e[2]?"Xem thêm":"ngữ cảnh"}</span><span class="jump" data-i="${dir==="out"?e[1]:e[0]}">${esc(o.s)}</span> — “${esc(e[3])}”${e[4]?` <span class="muted">§${esc(e[4].slice(0,50))}</span>`:""}</li>`};
 P.innerHTML=`<h2>${esc(n.t)}</h2><a href="${KB+n.s}" target="_blank" rel="noopener">${esc(n.s)}</a>
 <p class="muted">${esc(CL[n.c])}${n.r?" · "+n.r:""}${n.g?" · "+esc(n.g):""} · ${fmt(n.w)} từ${n.k!=null?" · "+fmt(n.k)+" clicks":""} · ${n.cta} link CTA</p>
 ${n.warn.length?`<p class="warn">⚠ ${n.warn.join(", ")}</p>`:""}
 <h3>Link ra (${outE[i].length})</h3><ul>${outE[i].map(k=>li(k,"out")).join("")||"<li class=muted>—</li>"}</ul>
 <h3>Link vào (${inE[i].length})</h3><ul>${inE[i].map(k=>li(k,"in")).join("")||"<li class=muted>—</li>"}</ul>
 <p class="muted">HTML hiện tại: knowledge/raw/live/html/${esc(n.s)}.html</p>`;
 P.querySelectorAll(".jump").forEach(a=>a.onclick=()=>{select(+a.dataset.i)})}
function select(i){if(!vis.has(i)){fc.value="-1";computeVis();layout()}sel=i;showPanel(i);draw()}

// table
const COLS=[["s","Bài"],["c","Cụm"],["r","Vai trò"],["w","Từ",1],["ic","In ngữ cảnh",1],["ix","In Xem thêm",1],["oc","Out ngữ cảnh",1],["ox","Out Xem thêm",1],["cta","CTA",1],["k","Clicks",1],["warn","Cảnh báo"]];
let sortK="ic",sortD=1;
function table(){const th=document.querySelector("#tb thead"),tb=document.querySelector("#tb tbody");
 th.innerHTML="<tr>"+COLS.map(c=>`<th class="${c[2]?"n":""}" data-k="${c[0]}">${c[1]}${sortK===c[0]?(sortD>0?" ▲":" ▼"):""}</th>`).join("")+"</tr>";
 th.querySelectorAll("th").forEach(h=>h.onclick=()=>{const k=h.dataset.k;sortD=sortK===k?-sortD:(COLS.find(c=>c[0]===k)[2]?-1:1);sortK=k;table()});
 const rows=[...vis].filter(i=>!match||match.has(i)).sort((a,b)=>{let x=N[a][sortK],y=N[b][sortK];if(sortK==="warn"){x=x.length;y=y.length}x=x??-1;y=y??-1;return (x>y?1:x<y?-1:0)*sortD});
 tb.innerHTML=rows.map(i=>{const n=N[i];return `<tr data-i="${i}"><td><span class="jump">${esc(n.s)}</span></td><td>${esc(CL[n.c])}</td><td>${n.r}</td>`+
  ["w","ic","ix","oc","ox","cta","k"].map(k=>`<td class="n">${fmt(n[k])}</td>`).join("")+`<td>${n.warn.length?"⚠ "+n.warn.join(", "):""}</td></tr>`}).join("");
 tb.querySelectorAll("tr").forEach(r=>r.onclick=()=>{select(+r.dataset.i);cv.scrollIntoView({behavior:"smooth",block:"center"})})}

function refresh(relayout){computeVis();if(relayout)layout();else draw();table()}
document.getElementById("q").addEventListener("input",()=>refresh(false));
fc.addEventListener("change",()=>{sel=-1;showPanel(-1);refresh(true)});
document.getElementById("fx").addEventListener("change",draw);
document.getElementById("fo").addEventListener("change",draw);
document.getElementById("reset").onclick=()=>layout();
document.getElementById("theme").onclick=()=>{const dark=document.documentElement.dataset.theme?document.documentElement.dataset.theme==="dark":matchMedia("(prefers-color-scheme: dark)").matches;
 document.documentElement.dataset.theme=dark?"light":"dark";legend();draw()};
window.addEventListener("resize",()=>{resize()});
resize();refresh(true);
</script></body></html>
"""


def write_html(d: dict) -> None:
    data = {"nodes": d["nodes"], "edges": d["edges"], "clusters": d["clusters"], "meta": d["meta"]}
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    OUT_HTML.write_text(HTML.replace("__DATA__", js), encoding="utf-8", newline="\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orphans", action="store_true", help="in danh sách bài 0 inlink ngữ cảnh ra terminal")
    a = ap.parse_args()
    d = build()
    IL.mkdir(parents=True, exist_ok=True)
    write_md(d)
    write_html(d)
    N = d["nodes"]
    print(f"✓ {len(N)} bài · {len(d['edges'])} link giữa các bài → {OUT_MD.relative_to(ROOT)} · {OUT_HTML.relative_to(ROOT)}")
    if a.orphans:
        for n in sorted((n for n in N if n["ic"] == 0), key=lambda n: -(n["k"] or 0)):
            print(f"  {n['s']}  (clicks {n['k'] if n['k'] is not None else '-'}, in Xem thêm {n['ix']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
