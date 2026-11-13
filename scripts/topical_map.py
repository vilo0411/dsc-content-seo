#!/usr/bin/env python3
"""Topical cluster map: cluster → subgroup → article, with internal-link health and SEO performance on one page.

    python scripts/topical_map.py        # -> knowledge/3-pipeline/internal-links/topical-map.html (open in a browser)

Inputs (all local, 0 network):
  knowledge/3-pipeline/page-audit.csv                 performance per article (page_groups.py report)
  knowledge/3-pipeline/internal-links/link-clusters.json   pillar / hub / spoke registry
  knowledge/raw/live/links.csv                        contextual links currently live (sync_live.py)
Re-run after `sync_live.py` (links changed) or `page_groups.py report` (new GSC/GA4 numbers).
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date

from _common import PIPELINE_DIR, ROOT, setup_utf8
from page_groups import CLUSTERS, SUBGROUPS, OUT_AUDIT, OUT_GROUPS, sg_key

LINK_CLUSTERS = PIPELINE_DIR / "internal-links/link-clusters.json"
LINKS = ROOT / "knowledge/raw/live/links.csv"
OUT = PIPELINE_DIR / "internal-links/topical-map.html"
REG_TO_CLUSTER = {"mo-tai-khoan": "1", "cach-choi-chung-khoan": "2"}  # c3-… → "3" etc. parsed from the id


def fnum(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def build_data() -> dict:
    src = OUT_AUDIT if OUT_AUDIT.exists() else OUT_GROUPS
    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    reg = json.loads(LINK_CLUSTERS.read_text(encoding="utf-8"))["clusters"]

    ctx: dict[str, set] = defaultdict(set)
    for r in csv.DictReader(open(LINKS, encoding="utf-8-sig")):
        if r["kind"] == "contextual":
            m = re.search(r"/kien-thuc/([a-z0-9-]+)", r["to"])
            if m and m.group(1) != r["from"]:
                ctx[r["from"]].add(m.group(1))
    sg_of = {r["slug"]: r["subgroup"] for r in rows}
    cl_of = {r["slug"]: r["cluster"] for r in rows}

    # registry membership: slug -> (registry id, pillar, hub of its group, role)
    member: dict[str, tuple] = {}
    pillars: dict[str, dict] = {}
    for c in reg:
        cl = REG_TO_CLUSTER.get(c["id"]) or re.match(r"c(\d+)-", c["id"]).group(1)
        p = c.get("pillar")
        hubs = [g["hub"] for g in c["groups"] if g.get("hub")]
        pillars[cl] = {"slug": p, "reg": c["id"], "note": c.get("note", ""), "hubs": len(set(hubs)),
                       "hubs_linked": len(set(hubs) & ctx[p]) if p else 0}
        for g in c["groups"]:
            for s in ([g["hub"]] if g.get("hub") else []) + g["spokes"]:
                role = "hub" if s == g.get("hub") else "spoke"
                if s not in member or role == "hub":
                    member[s] = (c["id"], None if g.get("pillar_exempt") else p, g.get("hub"), role)
        if p:
            member[p] = (c["id"], p, None, "pillar")

    arts = []
    for r in rows:
        s = r["slug"]
        reg_id, p, hub, role = member.get(s, ("", None, None, ""))
        need_p = bool(p) and role != "pillar" and p not in ctx[s]
        need_h = bool(hub) and role == "spoke" and hub not in ctx[s]
        out_c = [t for t in ctx[s] if t in cl_of]
        arts.append({
            "s": s, "t": r["title"], "c": r["cluster"], "g": r["subgroup"], "i": r["intent"], "r": role, "reg": reg_id,
            "np": need_p, "nh": need_h, "pl": p or "", "hb": hub or "",
            "cl": round(fnum(r.get("clicks"))), "pc": round(fnum(r.get("prev_clicks"))),
            "im": round(fnum(r.get("impressions"))), "ctr": round(fnum(r.get("ctr")), 2),
            "pos": round(fnum(r.get("position")), 1) if r.get("position") else None,
            "tq": r.get("top_query", ""), "q10": int(fnum(r.get("q_top10"))), "qs": int(fnum(r.get("q_striking"))),
            "se": round(fnum(r.get("sessions"))), "er": round(fnum(r.get("engagement_rate")) * 100),
            "ke": round(fnum(r.get("key_events"))), "lb": r.get("labels", ""), "pr": fnum(r.get("priority")),
            "ic": int(fnum(r.get("in_contextual"))), "oc": len(out_c),
            "ocs": sum(1 for t in out_c if cl_of[t] == r["cluster"]),
            "w": int(fnum(r.get("words"))),
        })
    xc = Counter()
    for f_, ts in ctx.items():
        for t_ in ts:
            if f_ in cl_of and t_ in cl_of and cl_of[f_] != cl_of[t_]:
                xc[tuple(sorted((cl_of[f_], cl_of[t_]), key=int))] += 1
    idx = {a["s"]: i for i, a in enumerate(arts)}
    live_edges = sorted({(idx[f_], idx[t_]) for f_, ts in ctx.items() if f_ in idx for t_ in ts if t_ in idx})
    has_perf = src == OUT_AUDIT
    return {"le": live_edges, "xc": [[a, b, n] for (a, b), n in xc.items()], "clusters": CLUSTERS, "subgroups": SUBGROUPS, "pillars": pillars, "arts": arts,
            "perf": has_perf, "built": date.today().isoformat(),
            "order": sorted({a["g"] for a in arts}, key=sg_key)}


TEMPLATE = r"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Topical cluster map — DSC /kien-thuc</title>
<style>
.viz-root{color-scheme:light;--page:#f9f9f7;--surface-1:#fcfcfb;--text-primary:#0b0b0b;--text-secondary:#52514e;--muted:#898781;
 --grid:#e1e0d9;--base:#c3c2b7;--ring:rgba(11,11,11,.10);--good:#0ca30c;--warning:#fab219;--serious:#ec835a;--critical:#d03b3b;
 --none:#c3c2b7;--up2:#256abf;--up1:#86b6ef;--mid:#e1e0d9;--dn1:#f0a3a2;--dn2:#e34948;--sel:#2a78d6;--up-text:#006300}
@media (prefers-color-scheme:dark){:root:where(:not([data-theme="light"])) .viz-root{color-scheme:dark;--page:#0d0d0d;--surface-1:#1a1a19;
 --text-primary:#f0efec;--text-secondary:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--base:#383835;--ring:rgba(255,255,255,.10);
 --none:#52514e;--up2:#5598e7;--up1:#1c5cab;--mid:#383835;--dn1:#8f3434;--dn2:#e66767;--sel:#3987e5;--up-text:#0ca30c}}
:root[data-theme="dark"] .viz-root{color-scheme:dark;--page:#0d0d0d;--surface-1:#1a1a19;--text-primary:#f0efec;--text-secondary:#c3c2b7;
 --muted:#898781;--grid:#2c2c2a;--base:#383835;--ring:rgba(255,255,255,.10);--none:#52514e;--up2:#5598e7;--up1:#1c5cab;--mid:#383835;
 --dn1:#8f3434;--dn2:#e66767;--sel:#3987e5;--up-text:#0ca30c}
*{box-sizing:border-box}body{margin:0}
.viz-root{font:13px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--page);color:var(--text-primary);min-height:100vh}
header{padding:16px 20px 8px}h1{font-size:18px;margin:0 0 4px}.sub{color:var(--text-secondary)}
.bar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:8px 20px;position:sticky;top:0;background:var(--page);z-index:5;border-bottom:1px solid var(--grid)}
.seg{display:inline-flex;border:1px solid var(--base);border-radius:6px;overflow:hidden}.seg button{border:0;background:transparent;color:var(--text-secondary);padding:5px 10px;cursor:pointer;font:inherit}
.seg button.on{background:var(--text-primary);color:var(--surface-1)}
select,input[type=search]{font:inherit;padding:4px 8px;border:1px solid var(--base);border-radius:6px;background:var(--surface-1);color:var(--text-primary)}
.legend{display:flex;flex-wrap:wrap;gap:10px;color:var(--text-secondary);font-size:12px}.legend span{display:inline-flex;align-items:center;gap:5px}
.sw{width:11px;height:11px;border-radius:50%;display:inline-block;box-shadow:0 0 0 1px var(--ring)}
main{display:grid;grid-template-columns:minmax(0,1fr) 440px;gap:16px;padding:12px 20px 40px}
@media (max-width:1100px){main{grid-template-columns:1fr}}
.card{background:var(--surface-1);border:1px solid var(--ring);border-radius:10px;padding:12px 14px;margin-bottom:14px}
.ch{display:flex;flex-wrap:wrap;gap:6px 16px;align-items:baseline;margin-bottom:8px}.ch h2{font-size:15px;margin:0}
.kpi{color:var(--text-secondary);font-variant-numeric:tabular-nums}.kpi b{color:var(--text-primary);font-weight:600}
.pill{display:flex;gap:10px;align-items:center;padding:6px 8px;border-radius:8px;background:var(--page);margin-bottom:8px;font-size:12px;color:var(--text-secondary)}
.pill .ph{border:2px dashed var(--critical);color:var(--critical);border-radius:6px;padding:2px 8px;font-weight:600}
.health{display:flex;gap:2px;height:8px;width:160px;border-radius:4px;overflow:hidden;background:var(--grid)}
.health i{display:block;height:100%}
.sg{display:grid;grid-template-columns:230px 1fr;gap:10px;padding:7px 4px;border-top:1px solid var(--grid);cursor:pointer;border-radius:6px}
.sg:hover{background:var(--page)}.sg.sel{outline:2px solid var(--sel);outline-offset:-2px}
.sgl{font-size:12px}.sgl b{font-size:13px}.sgl .kpi{display:block}
.dots{display:flex;flex-wrap:wrap;gap:3px;align-items:center;align-content:center;min-height:24px}
.d{border-radius:50%;flex:none;box-shadow:0 0 0 1px var(--ring);position:relative}
.d.hub{box-shadow:0 0 0 2px var(--surface-1),0 0 0 4px var(--text-primary)}.d.pillar{border-radius:4px;box-shadow:0 0 0 2px var(--surface-1),0 0 0 4px var(--text-primary)}
.d.dim{opacity:.15}.d.hit{box-shadow:0 0 0 2px var(--surface-1),0 0 0 4px var(--sel)}
.rank{display:inline-block;min-width:22px;padding:0 5px;border-radius:9px;background:var(--text-primary);color:var(--surface-1);font-size:11px;text-align:center;margin-right:4px}
aside{position:sticky;top:56px;align-self:start;max-height:calc(100vh - 70px);overflow:auto}
table{border-collapse:collapse;width:100%;font-size:12px}th,td{padding:4px 5px;border-bottom:1px solid var(--grid);text-align:left;vertical-align:top}
th{color:var(--muted);font-weight:500;cursor:pointer;white-space:nowrap;position:sticky;top:0;background:var(--surface-1)}td.n{text-align:right;font-variant-numeric:tabular-nums}
.tag{display:inline-block;font-size:11px;padding:0 5px;border-radius:4px;border:1px solid var(--base);color:var(--text-secondary);margin:1px 2px 1px 0;white-space:nowrap}
.st{white-space:nowrap}.st .sw{margin-right:4px}.up{color:var(--up-text)}.dn{color:var(--critical)}
a{color:inherit}.tip{position:fixed;pointer-events:none;background:var(--surface-1);color:var(--text-primary);border:1px solid var(--base);border-radius:8px;padding:8px 10px;font-size:12px;max-width:340px;box-shadow:0 4px 16px rgba(0,0,0,.12);z-index:20;display:none}
.tip b{display:block;margin-bottom:3px}.tip .kpi{display:block}
#graph{background:var(--surface-1);border:1px solid var(--ring);border-radius:10px;height:calc(100vh - 150px);min-height:600px;position:relative;overflow:hidden}
#graph svg{width:100%;height:100%;cursor:grab;display:block}#graph svg.drag{cursor:grabbing}
.gl{font-size:13px;fill:var(--text-secondary);pointer-events:none}.gc{font-size:30px;font-weight:600;fill:var(--text-primary);pointer-events:none}
.gk{font-size:18px;fill:var(--text-secondary);pointer-events:none}.gn{cursor:pointer}.gn.dim{opacity:.12}
.zoom{position:absolute;right:10px;top:10px;display:flex;flex-direction:column;gap:4px}.zoom button{width:28px;height:28px;border:1px solid var(--base);border-radius:6px;background:var(--surface-1);color:var(--text-primary);cursor:pointer;font:inherit}
.gh{position:absolute;left:10px;bottom:8px;font-size:11px;color:var(--muted)}
.order td{cursor:pointer}.note{font-size:12px;color:var(--text-secondary)}
</style></head>
<body><div class="viz-root">
<header><h1>Topical cluster map — /kien-thuc</h1>
<div class="sub" id="meta"></div></header>
<div class="bar">
 <span class="seg" id="view"><button data-v="graph" class="on">Đồ thị đề xuất</button><button data-v="live">Đồ thị hiện tại</button><button data-v="list">Danh sách nhóm</button></span>
 <label class="legend" id="xcl"><input type="checkbox" id="xcb"> Link giữa các cụm</label>
 <span class="seg" id="mode"><button data-m="link" class="on">Màu: link pillar/hub</button><button data-m="delta">Màu: Δ clicks</button><button data-m="label">Màu: nhãn audit</button></span>
 <select id="lab"><option value="">Lọc nhãn: tất cả</option><option>rank-drop</option><option>striking</option><option>ctr-low</option><option>engage-low</option><option>convert-low</option><option>dead</option><option value="np">Thiếu link pillar</option><option value="nh">Thiếu link hub</option><option value="noreg">Chưa vào registry</option></select>
 <input type="search" id="q" placeholder="Tìm slug / tiêu đề…">
 <span class="legend" id="legend"></span>
</div>
<main><section><div id="graph"><svg id="svg"></svg><div class="zoom"><button id="zi">+</button><button id="zo">−</button><button id="zf" title="Vừa khung">⤢</button></div><div class="gh">Cuộn để zoom · kéo để di chuyển · bấm node để mở batch audit</div></div><div id="map" hidden></div></section><aside class="card" id="panel"></aside></main>
<div class="tip" id="tip"></div>
</div>
<script>
const D=__DATA__;
const $=s=>document.querySelector(s), fmt=n=>(n||0).toLocaleString("vi-VN"), pct=(a,b)=>b?Math.round((a-b)/b*100):null;
let mode="link", lab="", q="", selSg=null, sortKey="pr", sortDir=-1;
const A=D.arts, byG={}; A.forEach(a=>(byG[a.g]=byG[a.g]||[]).push(a));
const maxC=Math.max(...A.map(a=>a.cl),1);
function stat(a){ if(a.r==="pillar") return ["good","Pillar"]; if(!a.reg) return ["none","Chưa vào registry"];
 if(a.np) return ["critical","Thiếu link pillar"]; if(a.nh) return ["warning","Thiếu link hub"]; return ["good","Đủ link pillar/hub"]; }
function dcol(a){ const d=pct(a.cl,a.pc); if(!a.pc&&!a.cl) return ["none","Không có clicks"]; if(d===null) return ["up2","Mới có clicks"];
 if(d<=-30) return ["dn2","Giảm ≥ 30%"]; if(d<=-10) return ["dn1","Giảm 10–30%"]; if(d<10) return ["mid","±10%"]; if(d<30) return ["up1","Tăng 10–30%"]; return ["up2","Tăng ≥ 30%"]; }
const LABC={"rank-drop":"critical","ctr-low":"serious","engage-low":"serious","striking":"warning","convert-low":"warning","dead":"none"};
function lcol(a){ const l=a.lb.split(" ").filter(Boolean); for(const k of ["dead","rank-drop","ctr-low","engage-low","striking","convert-low"]) if(l.includes(k)) return [LABC[k],k]; return ["good","Không nhãn"]; }
function col(a){ return mode==="link"?stat(a):mode==="delta"?dcol(a):lcol(a); }
function size(a){ return Math.round(8+22*Math.sqrt(a.cl/maxC)); }
function match(a){ if(q && !(a.s.includes(q)||a.t.toLowerCase().includes(q))) return false;
 if(!lab) return true; if(lab==="np") return a.np; if(lab==="nh") return a.nh; if(lab==="noreg") return !a.reg&&a.r!=="pillar"; return a.lb.split(" ").includes(lab); }
function agg(rs){ const cl=rs.reduce((s,a)=>s+a.cl,0), pc=rs.reduce((s,a)=>s+a.pc,0), im=rs.reduce((s,a)=>s+a.im,0);
 const sp=rs.filter(a=>a.r==="spoke"||a.r==="hub"); return {n:rs.length,cl,pc,im,d:pct(cl,pc),ctr:im?cl/im*100:0,
 np:rs.filter(a=>a.np).length,nh:rs.filter(a=>a.nh).length,noreg:rs.filter(a=>!a.reg&&a.r!=="pillar").length,
 ok:sp.filter(a=>!a.np&&!a.nh).length,sp:sp.length,pr:rs.reduce((s,a)=>s+a.pr,0),
 orph:rs.filter(a=>a.ic===0).length,lab:rs.reduce((m,a)=>{a.lb.split(" ").filter(Boolean).forEach(k=>m[k]=(m[k]||0)+1);return m},{})}; }
const G={}; D.order.forEach(g=>G[g]=agg(byG[g]));
const rank=[...D.order].sort((x,y)=>G[y].pr-G[x].pr); const rk={}; rank.forEach((g,i)=>rk[g]=i+1);
function dtxt(d){ return d===null?"–":`<span class="${d<0?"dn":"up"}">${d>0?"+":""}${d}%</span>`; }
function legend(){ if(view==="live"){ const n=LIVEN||["…","…","…"];
  $("#legend").innerHTML=`<span><i class="sw" style="background:var(--muted)"></i>Link trong cùng nhóm con (${n[0]})</span><span><i class="sw" style="background:var(--sel)"></i>Link khác nhóm, cùng cluster (${n[1]})</span><span><i class="sw" style="background:var(--serious)"></i>Link sang cluster khác (${n[2]})</span><span>Chỉ link ngữ cảnh trong thân bài đang live · vị trí node giữ nguyên như đồ thị đề xuất</span>`; return; }
 const L=mode==="link"?[["good","✓ Đủ link pillar/hub"],["warning","! Thiếu link hub"],["critical","✕ Thiếu link pillar"],["none","○ Chưa vào registry"]]
 :mode==="delta"?[["dn2","Giảm ≥ 30%"],["dn1","Giảm 10–30%"],["mid","±10%"],["up1","Tăng 10–30%"],["up2","Tăng ≥ 30% / mới"],["none","Không có clicks"]]
 :[["critical","rank-drop"],["serious","ctr-low / engage-low"],["warning","striking / convert-low"],["none","dead"],["good","Không nhãn"]];
 $("#legend").innerHTML=L.map(([c,t])=>`<span><i class="sw" style="background:var(--${c})"></i>${t}</span>`).join("")+
 `<span>■ pillar · ◎ hub · ● bài · kích thước = clicks 90 ngày</span>`; }
function renderList(){ let h="";
 for(const [cl,name] of Object.entries(D.clusters)){
  const gs=D.order.filter(g=>g.replace(/[a-z]$/,"")===cl); if(!gs.length) continue;
  const rs=gs.flatMap(g=>byG[g]), a=agg(rs), P=D.pillars[cl]||{}, pa=A.find(x=>x.s===P.slug);
  const inC=rs.reduce((s,x)=>s+x.ocs,0), outC=rs.reduce((s,x)=>s+x.oc,0);
  const okw=a.sp?a.ok/a.sp*160:0, hw=a.sp?a.nh/a.sp*160:0, pw=a.sp?a.np/a.sp*160:0;
  h+=`<div class="card" id="c${cl}"><div class="ch"><h2>C${cl}. ${name}</h2>
   <span class="kpi"><b>${a.n}</b> bài · <b>${fmt(a.cl)}</b> clicks ${dtxt(a.d)} · CTR ${a.ctr.toFixed(2)}% · link trong cụm <b>${outC?Math.round(inC/outC*100):0}%</b> · 0 inlink ngữ cảnh: <b>${a.orph}</b></span></div>
   <div class="pill">${P.slug?`<span class="d pillar" style="width:14px;height:14px;background:var(--${col(pa||{r:"pillar"})[0]})"></span>
     <span>Pillar <a href="https://www.dsc.com.vn/kien-thuc/${P.slug}" target="_blank">${P.slug}</a>${pa?` · ${fmt(pa.cl)} clicks · pos ${pa.pos??"–"}`:""} · link xuống hub <b>${P.hubs_linked}/${P.hubs}</b></span>`
     :`<span class="ph">Chưa có pillar</span>`}
     <span title="Tỷ lệ bài trong cụm (hub+spoke) đủ link / thiếu hub / thiếu pillar" class="health"><i style="width:${okw}px;background:var(--good)"></i><i style="width:${hw}px;background:var(--warning)"></i><i style="width:${pw}px;background:var(--critical)"></i></span>
     <span>${a.ok}/${a.sp} đủ link${a.noreg?` · ${a.noreg} chưa vào registry`:""}</span>${P.note?`<span>· ${P.note}</span>`:""}</div>`;
  for(const g of gs){ const s=G[g];
   h+=`<div class="sg${selSg===g?" sel":""}" data-g="${g}"><div class="sgl"><span class="rank" title="Thứ tự audit">${rk[g]}</span><b>${g} ${D.subgroups[g]||""}</b>
    <span class="kpi">${s.n} bài · ${fmt(s.cl)} clk ${dtxt(s.d)} · thiếu link ${s.np+s.nh}</span></div><div class="dots">`+
    [...byG[g]].sort((x,y)=>({pillar:0,hub:1}[x.r]??2)-({pillar:0,hub:1}[y.r]??2)||y.cl-x.cl).map(x=>{const z=size(x),c=col(x)[0];
     return `<span class="d ${x.r==="hub"||x.r==="pillar"?x.r:""} ${match(x)?((q||lab)?"hit":""):"dim"}" data-s="${x.s}" style="width:${z}px;height:${z}px;background:var(--${c})"></span>`}).join("")+`</div></div>`; }
  h+=`</div>`; }
 $("#map").innerHTML=h; panel(); }
function panel(){
 if(!selSg){ $("#panel").innerHTML=`<h2 style="font-size:15px;margin:0 0 6px">Thứ tự audit theo nhóm con</h2>
  <p class="note">Điểm ưu tiên = clicks mất + clicks có thể lấy thêm (CTR thấp / query vị trí 4–15). Bấm 1 nhóm để xem từng bài = 1 batch audit.</p>
  <table class="order"><thead><tr><th>#</th><th>Nhóm</th><th>Bài</th><th>Clicks</th><th>Δ</th><th>Thiếu link</th><th>Ưu tiên</th></tr></thead><tbody>`+
  rank.map(g=>{const s=G[g];return `<tr data-g="${g}"><td class="n">${rk[g]}</td><td>${g} ${D.subgroups[g]||""}</td><td class="n">${s.n}</td><td class="n">${fmt(s.cl)}</td><td class="n">${dtxt(s.d)}</td><td class="n">${s.np+s.nh}</td><td class="n">${fmt(Math.round(s.pr))}</td></tr>`}).join("")+`</tbody></table>`; return; }
 const s=G[selSg], rs=[...byG[selSg]].sort((x,y)=>{const a=x[sortKey],b=y[sortKey];return (typeof a==="string"?a.localeCompare(b):(a??-1)-(b??-1))*sortDir});
 const L=Object.entries(s.lab).sort((x,y)=>y[1]-x[1]).map(([k,v])=>`<span class="tag">${k} ${v}</span>`).join("");
 const hub=byG[selSg].find(a=>a.r==="hub");
 $("#panel").innerHTML=`<p class="note"><a href="#" id="back">← Thứ tự audit</a></p>
  <h2 style="font-size:15px;margin:0 0 4px"><span class="rank">${rk[selSg]}</span>${selSg} ${D.subgroups[selSg]||""}</h2>
  <div class="kpi">${s.n} bài · <b>${fmt(s.cl)}</b> clicks ${dtxt(s.d)} · CTR ${s.ctr.toFixed(2)}% · thiếu link pillar ${s.np} · thiếu hub ${s.nh}${s.noreg?` · chưa registry ${s.noreg}`:""}</div>
  <div class="note">Hub: ${hub?`<a target="_blank" href="https://www.dsc.com.vn/kien-thuc/${hub.s}">${hub.s}</a>`:"chưa có"}</div><div style="margin:6px 0">${L}</div>
  <table><thead><tr>${[["t","Bài"],["r","Vai trò"],["cl","Clicks"],["dd","Δ"],["pos","Pos"],["qs","Striking"],["se","Sess."],["ic","Inlink"],["pr","Ưu tiên"]].map(([k,t])=>`<th data-k="${k}">${t}${sortKey===k?(sortDir<0?" ↓":" ↑"):""}</th>`).join("")}</tr></thead><tbody>`+
  rs.map(a=>{const st=stat(a);return `<tr><td><a target="_blank" href="https://www.dsc.com.vn/kien-thuc/${a.s}">${a.t||a.s}</a><div class="st"><i class="sw" style="background:var(--${st[0]})"></i>${st[1]}</div>${a.lb.split(" ").filter(Boolean).map(k=>`<span class="tag">${k}</span>`).join("")}${a.tq?`<div class="note">top query: ${a.tq}</div>`:""}</td>
   <td>${a.r||"–"}</td><td class="n">${fmt(a.cl)}</td><td class="n">${dtxt(pct(a.cl,a.pc))}</td><td class="n">${a.pos??"–"}</td><td class="n">${a.qs}</td><td class="n">${fmt(a.se)}</td><td class="n">${a.ic}</td><td class="n">${fmt(Math.round(a.pr))}</td></tr>`}).join("")+`</tbody></table>`;
 $("#back").onclick=e=>{e.preventDefault();selSg=null;history.replaceState(null,"",location.pathname);render();}; }
A.forEach(a=>a.dd=pct(a.cl,a.pc));
document.addEventListener("click",e=>{const th=e.target.closest("th[data-k]"); if(th){const k=th.dataset.k; sortDir=sortKey===k?-sortDir:-1; sortKey=k; panel(); return;}
 const r=e.target.closest("[data-g]"); if(r){selSg=r.dataset.g; history.replaceState(null,"","#"+selSg); render(); if(view!=="list"&&r.closest("#panel")) focusSg(selSg); else document.querySelector(`.sg[data-g="${selSg}"]`)?.scrollIntoView({block:"nearest"});}});
$("#mode").onclick=e=>{const b=e.target.closest("button"); if(!b) return; mode=b.dataset.m; document.querySelectorAll("#mode button").forEach(x=>x.classList.toggle("on",x===b)); render();};
$("#lab").onchange=e=>{lab=e.target.value; render();}; $("#q").oninput=e=>{q=e.target.value.trim().toLowerCase(); render();};
const tip=$("#tip"), bySlug=Object.fromEntries(A.map(a=>[a.s,a]));
document.addEventListener("mousemove",e=>{const d=e.target.closest(".d[data-s],.gn[data-s]"); if(d&&!d.dataset.s){tip.style.display="none";return;} if(!d){tip.style.display="none";return;}
 const a=bySlug[d.dataset.s], st=stat(a);
 tip.innerHTML=`<b>${a.t||a.s}</b><span class="kpi">${a.g} · ${a.r||"chưa vào registry"} · ${a.i}</span>
  <span class="kpi">Clicks 90 ngày <b>${fmt(a.cl)}</b> (kỳ trước ${fmt(a.pc)}) · pos ${a.pos??"–"} · CTR ${a.ctr}%</span>
  <span class="kpi">Query top 10: ${a.q10} · striking: ${a.qs}${a.tq?` · top: “${a.tq}”`:""}</span>
  <span class="kpi">Sessions ${fmt(a.se)} · eng. ${a.er}% · key events ${a.ke}</span>
  <span class="kpi">Inlink ngữ cảnh ${a.ic} · link ra ${a.oc} (${a.ocs} trong cụm) · ${fmt(a.w)} từ</span>
  <span class="kpi">${st[1]}${a.np?` → cần link ${a.pl}`:""}${a.nh?` → cần link ${a.hb}`:""}</span>${a.lb?`<span class="kpi">Nhãn: ${a.lb}</span>`:""}`;
 tip.style.display="block"; const x=Math.min(e.clientX+14,innerWidth-360), y=Math.min(e.clientY+14,innerHeight-tip.offsetHeight-10); tip.style.left=x+"px"; tip.style.top=y+"px";});
$("#meta").innerHTML=`${A.length} bài · ${Object.keys(D.clusters).length} cluster · ${D.order.length} nhóm con · dữ liệu ${D.perf?"GSC 90 ngày (page-audit.csv)":"chưa có performance — chạy page_groups.py report"} · link live theo snapshot sync_live · sinh ${D.built} bởi <code>scripts/topical_map.py</code>`;
// ───────── graph view: cluster = radial (pillar centre → subgroup/hub ring → articles), clusters on a big ring ─────────
let view="graph", showXC=false, VB=null, LAY=null, LIVEN=null;
const NS="http://www.w3.org/2000/svg";
function layout(){
 const P={}, CL=[];
 for(const [cl,name] of Object.entries(D.clusters)){
  const gs=D.order.filter(g=>g.replace(/[a-z]$/,"")===cl); if(!gs.length) continue;
  const pil=(D.pillars[cl]||{}).slug, r1=70+10*gs.length, items=[];
  const w=gs.map(g=>Math.max(4,byG[g].filter(a=>a.r!=="hub"&&a.s!==pil).length)), W=w.reduce((s,x)=>s+x,0);
  let a0=-Math.PI/2, R=r1+30;
  gs.forEach((g,k)=>{ const span=w[k]/W*2*Math.PI, mid=a0+span/2, hub=byG[g].find(a=>a.r==="hub");
   const gx=Math.cos(mid)*r1, gy=Math.sin(mid)*r1, gid=hub?hub.s:"#"+g;
   items.push({id:gid,x:gx,y:gy,kind:hub?"hub":"grp",g,ang:mid,art:hub});
   const sp=byG[g].filter(a=>a!==hub&&a.s!==pil).sort((x,y)=>y.cl-x.cl);
   let rr=r1+48, i=0;
   while(i<sp.length){ const cap=Math.max(1,Math.floor(span*rr/15)); const row=sp.slice(i,i+cap);
    row.forEach((a,j)=>{ const t=a0+span*(j+0.5)/row.length; items.push({id:a.s,x:Math.cos(t)*rr,y:Math.sin(t)*rr,kind:"art",g,art:a,parent:gid}); });
    i+=cap; R=Math.max(R,rr+16); rr+=15; }
   a0+=span; });
  const pa=A.find(a=>a.s===pil);
  items.push({id:pil||"#P"+cl,x:0,y:0,kind:pil?"pillar":"nop",art:pa,g:pa?pa.g:null});
  CL.push({cl,name,R,items}); }
 // clusters on a big ring, arc length ∝ diameter
 const gap=240, tot=CL.reduce((s,c)=>s+2*c.R+gap,0), BR=Math.max(tot/(2*Math.PI),700); let t=-Math.PI/2;
 CL.forEach(c=>{ const span=(2*c.R+gap)/BR; t+=span/2; c.cx=Math.cos(t)*BR; c.cy=Math.sin(t)*BR; t+=span/2;
  c.items.forEach(it=>{it.X=it.x+c.cx; it.Y=it.y+c.cy; P[it.id]=it;}); });
 return {CL,P,BR};
}
function el(tag,attrs,parent){ const e=document.createElementNS(NS,tag); for(const k in attrs) e.setAttribute(k,attrs[k]); parent&&parent.appendChild(e); return e; }
function nodeColor(it){ if(it.kind==="grp") return "var(--surface-1)"; if(it.kind==="nop") return "var(--surface-1)"; return `var(--${col(it.art||{r:"pillar",lb:""})[0]})`; }
function drawGraph(){
 if(!LAY) LAY=layout(); const {CL,P,BR}=LAY, svg=$("#svg"); svg.innerHTML="";
 const root=el("g",{id:"gr"},svg), gE=el("g",{},root), gX=el("g",{},root), gN=el("g",{},root), gT=el("g",{},root);
 if(showXC){ const mx=Math.max(...D.xc.map(x=>x[2]),1);
  D.xc.forEach(([a,b,n])=>{ const A_=CL.find(c=>c.cl===a), B_=CL.find(c=>c.cl===b); if(!A_||!B_) return;
   const mxp=(A_.cx+B_.cx)/2*0.35, myp=(A_.cy+B_.cy)/2*0.35;
   const p=el("path",{d:`M${A_.cx},${A_.cy} Q${mxp},${myp} ${B_.cx},${B_.cy}`,fill:"none",stroke:"var(--sel)","stroke-opacity":.28,"stroke-width":1+12*n/mx},gX);
   p.innerHTML=`<title>C${a} ↔ C${b}: ${n} link ngữ cảnh</title>`; }); }
 el("circle",{cx:0,cy:0,r:46,fill:"var(--text-primary)"},gN); const rt=el("text",{x:0,y:6,"text-anchor":"middle",class:"gk",style:"fill:var(--surface-1);font-weight:600"},gT); rt.textContent="/kien-thuc";
 for(const c of CL){ el("line",{x1:0,y1:0,x2:c.cx,y2:c.cy,stroke:"var(--grid)","stroke-width":3},gE); }
 for(const c of CL){
  el("circle",{cx:c.cx,cy:c.cy,r:c.R,fill:"var(--surface-1)"},gE);
  el("circle",{cx:c.cx,cy:c.cy,r:c.R,fill:"none",stroke:"var(--grid)","stroke-width":1},gE);
  const tl=el("text",{x:c.cx,y:c.cy-c.R-34,"text-anchor":"middle",class:"gc"},gT); tl.textContent=`C${c.cl}. ${c.name}`;
  const ag=agg(c.items.filter(i=>i.art&&i.kind!=="nop").map(i=>i.art));
  const sl=el("text",{x:c.cx,y:c.cy-c.R-10,"text-anchor":"middle",class:"gk"},gT); sl.textContent=`${ag.n} bài · ${fmt(ag.cl)} clicks · ${ag.d===null?"":(ag.d>0?"+":"")+ag.d+"%"} · ${ag.np+ag.nh} thiếu link`;
  const pid=c.items.find(i=>i.kind==="pillar"||i.kind==="nop").id;
  for(const it of c.items){ if(view==="live"&&it.kind!=="hub"&&it.kind!=="grp") continue;
   if(it.kind==="hub"||it.kind==="grp"){ // subgroup → pillar
    const miss=it.art?it.art.np:false;
    if(view!=="live") el("line",{x1:P[pid].X,y1:P[pid].Y,x2:it.X,y2:it.Y,stroke:miss?"var(--critical)":"var(--base)","stroke-width":miss?1.6:1.4,"stroke-dasharray":miss?"4 3":(it.kind==="grp"?"2 3":"")},gE);
    const lbl=el("text",{x:it.X+Math.cos(it.ang)*14,y:it.Y+Math.sin(it.ang)*14+3,"text-anchor":Math.cos(it.ang)>0.2?"start":Math.cos(it.ang)<-0.2?"end":"middle",class:"gl"},gT);
    lbl.textContent=`${it.g} ${D.subgroups[it.g]||""}`; }
   if(it.kind==="art"){ const a=it.art, miss=a.nh||(a.np&&!a.hb);
    el("line",{x1:P[it.parent].X,y1:P[it.parent].Y,x2:it.X,y2:it.Y,stroke:miss?"var(--critical)":"var(--base)","stroke-width":miss?.9:.6,"stroke-opacity":miss?.75:.55,"stroke-dasharray":miss?"3 2":""},gE); } }
  for(const it of c.items){
   const a=it.art, on=!a||match(a), cls="gn"+((q||lab)&&!on?" dim":"")+(a&&a.g===selSg?" sel":"");
   let n;
   if(it.kind==="pillar"){ n=el("rect",{x:it.X-13,y:it.Y-13,width:26,height:26,rx:4,fill:nodeColor(it),stroke:"var(--text-primary)","stroke-width":2.5,class:cls},gN); }
   else if(it.kind==="nop"){ n=el("circle",{cx:it.X,cy:it.Y,r:20,fill:"var(--surface-1)",stroke:"var(--critical)","stroke-width":2,"stroke-dasharray":"5 3",class:"gn"},gN);
    const t1=el("text",{x:it.X,y:it.Y+3,"text-anchor":"middle",class:"gl",style:"fill:var(--critical);font-weight:600"},gT); t1.textContent="chưa có pillar"; }
   else if(it.kind==="grp"){ n=el("rect",{x:it.X-6,y:it.Y-6,width:12,height:12,transform:`rotate(45 ${it.X} ${it.Y})`,fill:"var(--surface-1)",stroke:"var(--muted)","stroke-width":1.5,class:cls},gN); }
   else { const r=it.kind==="hub"?Math.max(7,size(a)/2+2):Math.max(3.5,size(a)/2.4);
    n=el("circle",{cx:it.X,cy:it.Y,r,fill:nodeColor(it),stroke:it.kind==="hub"?"var(--text-primary)":"var(--surface-1)","stroke-width":it.kind==="hub"?2.2:1,class:cls},gN); }
   if(a&&a.g===selSg) n.setAttribute("stroke",it.kind==="art"?"var(--sel)":n.getAttribute("stroke")), n.setAttribute("stroke-width",it.kind==="art"?2:3);
   n.dataset.s=a?a.s:""; n.dataset.g=it.g||""; } }
 if(view==="live"){ const pos=i=>P[A[i].s]; let n=[0,0,0];
  const gL=el("g",{},root); root.insertBefore(gL,gN);
  for(const [f,t] of D.le){ const a=pos(f), b=pos(t); if(!a||!b) continue;
   const same=A[f].g===A[t].g?0:A[f].c===A[t].c?1:2; n[same]++;
   el("line",{x1:a.X,y1:a.Y,x2:b.X,y2:b.Y,stroke:["var(--muted)","var(--sel)","var(--serious)"][same],"stroke-width":same===2?.7:.8,"stroke-opacity":same===2?.35:.6},gL); }
  LIVEN=n; }
 if(!VB){ const m=BR+Math.max(...CL.map(c=>c.R))+80; VB=[-m,-m,2*m,2*m]; }
 svg.setAttribute("viewBox",VB.join(" "));
}
function zoomAt(f,cx,cy){ const [x,y,w,h]=VB, nw=w*f, nh=h*f; VB=[cx-(cx-x)*f,cy-(cy-y)*f,nw,nh]; $("#svg").setAttribute("viewBox",VB.join(" ")); }
function svgPt(e){ const s=$("#svg"), r=s.getBoundingClientRect(); return [VB[0]+(e.clientX-r.left)/r.width*VB[2], VB[1]+(e.clientY-r.top)/r.height*VB[3]]; }
$("#svg").addEventListener("wheel",e=>{e.preventDefault(); const [x,y]=svgPt(e); zoomAt(e.deltaY>0?1.15:1/1.15,x,y);},{passive:false});
let drag=null; $("#svg").addEventListener("mousedown",e=>{drag={x:e.clientX,y:e.clientY,vb:[...VB],moved:false}; $("#svg").classList.add("drag");});
addEventListener("mousemove",e=>{ if(!drag) return; const s=$("#svg").getBoundingClientRect(), dx=(e.clientX-drag.x)/s.width*VB[2], dy=(e.clientY-drag.y)/s.height*VB[3];
 if(Math.abs(e.clientX-drag.x)+Math.abs(e.clientY-drag.y)>3) drag.moved=true; VB=[drag.vb[0]-dx,drag.vb[1]-dy,VB[2],VB[3]]; $("#svg").setAttribute("viewBox",VB.join(" ")); });
addEventListener("mouseup",()=>{ setTimeout(()=>{drag=null;},0); $("#svg").classList.remove("drag"); });
$("#zi").onclick=()=>zoomAt(1/1.3,VB[0]+VB[2]/2,VB[1]+VB[3]/2); $("#zo").onclick=()=>zoomAt(1.3,VB[0]+VB[2]/2,VB[1]+VB[3]/2); $("#zf").onclick=()=>{VB=null;drawGraph();};
$("#svg").addEventListener("click",e=>{ if(drag&&drag.moved) return; const n=e.target.closest(".gn"); if(!n||!n.dataset.g) return; e.stopPropagation(); selSg=n.dataset.g; history.replaceState(null,"","#"+selSg); render(); });
$("#view").onclick=e=>{const b=e.target.closest("button"); if(!b) return; view=b.dataset.v; document.querySelectorAll("#view button").forEach(x=>x.classList.toggle("on",x===b));
 $("#graph").hidden=view==="list"; $("#map").hidden=view!=="list"; $("#xcl").style.display=view==="graph"?"":"none"; render();};
$("#xcb").onchange=e=>{showXC=e.target.checked; render();};
// focus a subgroup in the graph (deep link / table click)
function focusSg(g){ if(view==="list"||!LAY) return; const its=Object.values(LAY.P).filter(i=>i.g===g); if(!its.length) return;
 const xs=its.map(i=>i.X), ys=its.map(i=>i.Y), cx=(Math.min(...xs)+Math.max(...xs))/2, cy=(Math.min(...ys)+Math.max(...ys))/2, m=Math.max(260,Math.max(...xs)-Math.min(...xs),Math.max(...ys)-Math.min(...ys))*1.4;
 VB=[cx-m/2,cy-m/2,m,m]; $("#svg").setAttribute("viewBox",VB.join(" ")); }

function render(){ legend(); if(view!=="list") drawGraph(); else renderList(); if(view==="live") legend(); panel(); }
const qv=new URLSearchParams(location.search).get("view"); if(["graph","live","list"].includes(qv)){ view=qv; document.querySelectorAll("#view button").forEach(x=>x.classList.toggle("on",x.dataset.v===qv)); $("#graph").hidden=view==="list"; $("#map").hidden=view!=="list"; }
const h0=decodeURIComponent(location.hash.slice(1)); if(byG[h0]) selSg=h0;
render(); if(selSg) focusSg(selSg);
addEventListener("hashchange",()=>{const g=decodeURIComponent(location.hash.slice(1)); if(byG[g]){selSg=g;render();focusSg(g);}});
</script></body></html>
"""


def main():
    setup_utf8()
    data = build_data()
    OUT.write_text(TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False)), encoding="utf-8")
    a = data["arts"]
    print(f"[OK] {OUT.relative_to(ROOT)} — {len(a)} bài · thiếu link pillar {sum(x['np'] for x in a)} · "
          f"thiếu hub {sum(x['nh'] for x in a)} · chưa vào registry {sum(1 for x in a if not x['reg'] and x['r'] != 'pillar')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
