"""Article registry - ONE row per article URL: cluster, link role, pipeline status, anchors.

Single source for internal linking and article status (replaces anchor-index.md, anchor-keys.csv
and the status table in topic-clusters.md). File: knowledge/3-seo/strategy/pages.csv
Link architecture (pillar / hub / spoke, pillar anchors) stays in strategy/taxonomy.json.

    python scripts/registry.py build [--force]   # one-time: merge the legacy files into pages.csv
    python scripts/registry.py refresh           # after page_groups.py build / sync_live: add new live
                                                  # URLs, update title/cluster/role; never touches status/anchors
    python scripts/registry.py check             # unmapped file slugs, duplicate main keywords, taxonomy gaps
    python scripts/registry.py show <slug>       # one row, all fields
    python scripts/registry.py cluster [<code>]  # topic strategy: section core/outer/off, entity, bridge_to,
                                                  # attributes + which are not yet covered (gaps); no code = table
    python scripts/registry.py suggest-core      # data view: clicks / key events share per cluster vs section

Strategy fields (section, entity, bridge_to, attributes) live ONLY in taxonomy.json "topics" - edit there.

Columns
  slug          URL slug on dsc.com.vn/kien-thuc/ (live slug once published; file slug before that)
  file_slug     our content file name (Final-<file_slug>.md) - may differ from the live slug
  live          yes = in the sitemap snapshot
  status        Planned · Outlining · Outline-Approved · Optimizing · Finalized · Merged · Live (never went
                through this pipeline)
  cluster, cluster_name, subgroup, subgroup_name   from page_groups.py taxonomy
  role, hub     pillar / hub / spoke and the hub this article should link up to (taxonomy.json)
  anchor        suggested anchor text · key_chinh / key_phu = main / secondary keywords (key_phu "|"-separated)
  keywords      other related terms · merged_into (status Merged) · note
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from _common import FINAL_DIR, ROOT, STRATEGY_DIR, setup_utf8, unaccent

REGISTRY = STRATEGY_DIR / "pages.csv"
TAXONOMY = STRATEGY_DIR / "taxonomy.json"
PAGE_GROUPS = STRATEGY_DIR / "page-groups.csv"
PAGE_AUDIT = STRATEGY_DIR / "page-audit.csv"
BRAND_FACTS = ROOT / "knowledge/1-brand/brand-facts.json"
SECTIONS = ("core", "outer", "off")                              # /kien-thuc topics
SITE_SECTIONS = ("core", "outer", "trust", "off", "topics")      # site areas; "topics" = split by taxonomy topics
SITEMAP_CACHE = ROOT / ".agents/skills/link/scripts/sitemap-cache.json"
LEGACY = {  # only read by `build`
    "anchor_index": ROOT / "knowledge/3-seo/links/anchor-index.md",
    "anchor_keys": ROOT / "knowledge/3-seo/links/anchor-keys.csv",
    "topic_clusters": STRATEGY_DIR / "topic-clusters.md",
}
FIELDS = ["slug", "file_slug", "live", "status", "title", "cluster", "cluster_name", "subgroup", "subgroup_name",
          "role", "hub", "anchor", "key_chinh", "key_phu", "keywords", "merged_into", "legacy_cluster", "note"]
STATUSES = ["Planned", "Outlining", "Outline-Pending", "In Progress", "Outline-Approved", "Optimizing",
            "Finalized", "Merged", "Live"]
BASE_URL = "https://www.dsc.com.vn/kien-thuc/"


# ---------------------------------------------------------------- shared API (used by other scripts)

def load() -> list[dict]:
    if not REGISTRY.exists():
        sys.exit(f"Chưa có {REGISTRY.relative_to(ROOT)} — chạy: python scripts/registry.py build")
    with REGISTRY.open(encoding="utf-8-sig", newline="") as f:
        return [{k: (r.get(k) or "") for k in FIELDS} for r in csv.DictReader(f)]


def save(rows: list[dict]) -> None:
    rows.sort(key=lambda r: (_cluster_key(r["subgroup"] or r["cluster"]), r["slug"]))
    with REGISTRY.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def find(rows: list[dict], slug: str) -> list[dict]:
    """Rows whose live slug or file slug equals `slug` (exact first, then substring)."""
    s = slug.strip().strip("/").rsplit("/", 1)[-1]
    exact = [r for r in rows if s in (r["slug"], r["file_slug"])]
    return exact or [r for r in rows if s in r["slug"] or (r["file_slug"] and s in r["file_slug"])]


def url(row: dict) -> str:
    return BASE_URL + row["slug"]


def terms(row: dict) -> str:
    """All keyword-ish text of a row, for matching."""
    return " | ".join(x for x in (row["anchor"], row["key_chinh"], row["key_phu"], row["keywords"], row["title"]) if x)


def match_cluster(rows: list[dict], text: str) -> tuple[str, str, str, str] | None:
    """(cluster, cluster_name, subgroup, subgroup_name) whose name/code contains `text` (accent-insensitive)."""
    q = unaccent(text).strip()
    groups = {(r["cluster"], r["cluster_name"], r["subgroup"], r["subgroup_name"]) for r in rows if r["subgroup"]}
    exact = [g for g in groups if q == unaccent(g[2])]            # subgroup code, e.g. "3b"
    if len(exact) == 1:
        return exact[0]
    named = [g for g in groups if q in unaccent(g[3])]           # part of the subgroup name
    if len(named) == 1:
        return named[0]
    clusters = {(r["cluster"], r["cluster_name"]) for r in rows
                if r["cluster"] and (q == r["cluster"] or q in unaccent(r["cluster_name"]))}
    if len(clusters) == 1:
        c, n = next(iter(clusters))
        return c, n, "", ""
    return None


# ---------------------------------------------------------------- helpers

def _cluster_key(code: str):
    m = re.match(r"(\d+)([a-z]?)", code or "")
    return (int(m.group(1)), m.group(2)) if m else (99, "")


def _md_rows(path: Path):
    """(section heading, slug, cells) for each table row that contains a /kien-thuc/ URL."""
    if not path.exists():
        return
    section = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = re.sub(r"\s*\(\d+ bài\)\s*$", "", line[3:]).strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        m = re.search(r"/kien-thuc/([a-z0-9-]+)", " ".join(cells[:2]))
        if m and len(cells) >= 4:
            yield section, m.group(1), cells


def _sitemap() -> set[str]:
    """Live slugs: sitemap + pages sync_live fetched directly (CMS leaves some articles out of the sitemap;
    sync_live deletes the snapshot of a removed / 301 page, so a snapshot on disk means the URL is live)."""
    live = {f.stem for f in (ROOT / "knowledge/raw/live/html").glob("*.html")}
    if not SITEMAP_CACHE.exists():
        return live
    return live | {u.rstrip("/").rsplit("/", 1)[-1] for u in json.loads(SITEMAP_CACHE.read_text(encoding="utf-8")).get("urls", [])}


def _taxonomy_roles() -> dict[str, tuple[str, str]]:
    """slug -> (role, hub slug to link up to)."""
    out: dict[str, tuple[str, str]] = {}
    if not TAXONOMY.exists():
        return out
    for c in json.loads(TAXONOMY.read_text(encoding="utf-8")).get("clusters", []):
        pillar = c.get("pillar") or ""
        if pillar:
            out[pillar] = ("pillar", "")
        for g in c.get("groups", []):
            hub = g.get("hub") or ""
            if hub:
                out.setdefault(hub, ("hub", pillar))
            for s in g.get("spokes", []):
                out.setdefault(s, ("spoke", hub or pillar))
    return out


def final_path(file_slug: str) -> Path:
    return FINAL_DIR / f"Final-{file_slug}.md"


def _final_titles() -> dict[str, str]:
    out = {}
    for f in FINAL_DIR.glob("Final-*.md"):
        head = f.read_text(encoding="utf-8", errors="replace")[:4000]
        m = re.search(r"^Title:\s*(.+)$", head, re.M) or re.search(r"^#\s+(.+)$", head, re.M)
        out[f.stem[6:]] = m.group(1).strip() if m else ""
    return out


def _map_to_live(file_slug: str, title: str, live: dict[str, str]) -> str:
    """Live slug for a file slug that is not itself live: unique prefix/containment match, else best
    title match (ratio >= 0.8). Empty when ambiguous - `check` lists those for a human."""
    cands = [s for s in live if s.startswith(file_slug + "-") or f"-{file_slug}-" in f"-{s}-"]
    if len(cands) == 1:
        return cands[0]
    for pref in (file_slug + "-la-gi", "chi-bao-" + file_slug):   # common CMS slug shapes
        if pref in live:
            return pref
    if title:
        t = unaccent(title)
        scored = sorted(((SequenceMatcher(None, t, unaccent(lt)).ratio(), s) for s, lt in live.items() if lt), reverse=True)
        if scored and scored[0][0] >= 0.8 and (len(scored) == 1 or scored[0][0] - scored[1][0] >= 0.05):
            return scored[0][1]
    return ""


def _content_target(file_slug: str) -> str:
    """Live slug whose body matches Final-<file_slug>.md (weekly_review.content_match) — catches articles
    the CMS published under an unrelated URL; empty when no page is a clear match."""
    import weekly_review as wr  # same matcher the publish ledger uses
    best, score, _, second = wr.content_match(file_slug)
    return best if best and score >= wr.MATCH_MIN and score - second >= wr.MATCH_MARGIN else ""


def _groups() -> dict[str, dict]:
    if not PAGE_GROUPS.exists():
        return {}
    with PAGE_GROUPS.open(encoding="utf-8-sig", newline="") as f:
        return {r["slug"]: r for r in csv.DictReader(f)}


def _classify(slug: str, title: str) -> tuple[str, str, str, str]:
    """Cluster for a URL that page_groups.py has not seen (planned / not yet live)."""
    import page_groups as pg  # heavy module; import only when needed
    overrides = {r["slug"].strip(): r["subgroup"].strip() for r in pg.read_csv(pg.OVERRIDES)} if pg.OVERRIDES.exists() else {}
    sector = {r["ticker"].upper(): r["subgroup"] for r in pg.read_csv(pg.TICKER_SECTOR)}
    sg, *_ = pg.classify(slug, title, overrides, pg.link_groups(), sector)
    cl = re.match(r"\d+", sg).group(0) if sg else ""
    return cl, pg.CLUSTERS.get(cl, ""), sg, pg.SUBGROUPS.get(sg, "")


def _apply_structure(row: dict, groups: dict, roles: dict) -> None:
    g = groups.get(row["slug"])
    if g:
        for k in ("cluster", "cluster_name", "subgroup", "subgroup_name"):
            row[k] = g.get(k, "")
        row["title"] = row["title"] or g.get("title", "")
    elif not row["cluster"]:
        row["cluster"], row["cluster_name"], row["subgroup"], row["subgroup_name"] = _classify(row["slug"], row["title"])
    row["role"], row["hub"] = roles.get(row["slug"], ("", ""))


# ---------------------------------------------------------------- commands

def cmd_build(a) -> int:
    if REGISTRY.exists() and not a.force:
        print(f"{REGISTRY.relative_to(ROOT)} đã có — dùng `refresh`, hoặc --force để dựng lại từ file cũ (mất sửa tay).")
        return 1
    sitemap, groups, roles, titles = _sitemap(), _groups(), _taxonomy_roles(), _final_titles()
    live_titles = {s: g.get("title", "") for s, g in groups.items()}
    rows: dict[str, dict] = {}
    canon_cache: dict[str, str] = {}

    def canon(s: str, title: str = "") -> str:
        """Live slug for any legacy slug (file slug or old URL); itself when not published."""
        if s in groups:
            return s
        if s not in canon_cache:
            canon_cache[s] = _map_to_live(s, titles.get(s, "") or title, live_titles) or s
        return canon_cache[s]

    def row(slug: str) -> dict:
        return rows.setdefault(slug, {k: "" for k in FIELDS} | {"slug": slug})

    for s, g in groups.items():                                   # 1. every live article
        row(s)["status"], row(s)["title"] = "Live", g.get("title", "")
    for section, s, cells in _md_rows(LEGACY["anchor_index"]):     # 2. anchors + related terms
        r = row(canon(s, cells[2]))
        if r["slug"] != s:
            r["file_slug"] = r["file_slug"] or s
        r["anchor"] = r["anchor"] or cells[0]
        r["keywords"] = r["keywords"] or cells[2]
        r["legacy_cluster"] = r["legacy_cluster"] or section
    if LEGACY["anchor_keys"].exists():                            # 3. curated main/secondary keywords
        with LEGACY["anchor_keys"].open(encoding="utf-8-sig", newline="") as f:
            for k in csv.DictReader(f):
                r = row(canon(k["target"], k.get("title", "")))
                r["key_chinh"], r["key_phu"] = k.get("key_chinh", ""), k.get("key_phu", "")
                if k.get("ngu_nghia"):
                    r["note"] = f"ngữ nghĩa: {k['ngu_nghia']}"
    unmapped = []
    for section, s, cells in _md_rows(LEGACY["topic_clusters"]):  # 4. pipeline status (our file slugs)
        status, kw = cells[-1], cells[1].replace("**", "").replace("[HUB]", "").strip()
        target = canon(s, kw)
        if target == s and s not in groups:
            unmapped.append(s)
        r = row(target)
        r["file_slug"] = s
        if status.startswith("Merged"):
            r["status"], r["merged_into"] = "Merged", status.split("→")[-1].strip()
        else:
            r["status"] = status
        r["key_chinh"] = r["key_chinh"] or kw
        r["title"] = r["title"] or titles.get(s, "")
        r["legacy_cluster"] = r["legacy_cluster"] or section.split(":")[0]
    for r in rows.values():
        r["live"] = "yes" if r["slug"] in sitemap else "no"
        if not r["status"]:
            r["status"] = "Live" if r["live"] == "yes" else "Finalized"
        r["key_chinh"] = r["key_chinh"] or r["anchor"]
        _apply_structure(r, groups, roles)
    save(list(rows.values()))
    print(f"pages.csv: {len(rows)} dòng · live {sum(r['live'] == 'yes' for r in rows.values())} · "
          f"file slug chưa khớp live {len(unmapped)} (xem `registry.py check`)")
    return 0


def cmd_refresh(a) -> int:
    rows = load()
    by_slug = {r["slug"]: r for r in rows}
    sitemap, groups, roles = _sitemap(), _groups(), _taxonomy_roles()
    added = 0
    for s, g in groups.items():
        if s not in by_slug:
            by_slug[s] = {k: "" for k in FIELDS} | {"slug": s, "status": "Live", "title": g.get("title", "")}
            added += 1
    # an article published under a different slug: fold its pipeline row into the live row
    live_titles = {s: g.get("title", "") for s, g in groups.items()}
    merged = 0
    for r in list(by_slug.values()):
        if r["slug"] in sitemap or not r["file_slug"]:
            continue
        target = _map_to_live(r["file_slug"], r["title"], live_titles) or _content_target(r["file_slug"])
        t = by_slug.get(target)
        if t and t is not r and (not t["file_slug"] or t["file_slug"] == r["file_slug"]):
            t["file_slug"] = r["file_slug"]
            if t["status"] == "Live":
                t["status"] = r["status"]
            for k in ("anchor", "key_chinh", "key_phu", "keywords", "note"):
                t[k] = t[k] or r[k]
            del by_slug[r["slug"]]
            merged += 1
    for r in by_slug.values():
        r["live"] = "yes" if r["slug"] in sitemap else "no"
        if r["slug"] in groups:
            r["title"] = groups[r["slug"]].get("title", "") or r["title"]
        _apply_structure(r, groups, roles)
    save(list(by_slug.values()))
    print(f"refresh: {len(by_slug)} dòng · thêm {added} URL live mới · gộp {merged} bài đã publish khác slug")
    return 0


def cmd_check(a) -> int:
    rows, issues = load(), 0
    live_slugs = {r["slug"] for r in rows if r["live"] == "yes"}
    not_live = [r for r in rows if r["file_slug"] and r["live"] == "no" and r["status"] in ("Finalized", "Optimizing")]
    pending = [r for r in not_live if not final_path(r["file_slug"]).exists()]
    waiting = [r for r in not_live if r not in pending]
    print(f"## Finalized nhưng không có file Final ({len(pending)}) — sửa status, hoặc gộp vào dòng URL live")
    for r in pending[:40]:
        print(f"- {r['file_slug']} · {r['key_chinh'][:70]}")
    print(f"\n## Bài Final chờ đăng ({len(waiting)}) — không lỗi; refresh tự khớp URL khi thân bài có trên live")
    for r in waiting[:40]:
        print(f"- {r['file_slug']} · {r['title'][:70]}")
    dups: dict[str, list[str]] = {}
    for r in rows:
        if r["key_chinh"] and r["status"] != "Merged":
            dups.setdefault(unaccent(r["key_chinh"]).strip(), []).append(r["slug"])
    multi = {k: v for k, v in dups.items() if len(v) > 1}
    print(f"\n## Trùng key chính — nghi cannibalization ({len(multi)})")
    for k, v in list(multi.items())[:40]:
        print(f"- “{k}”: {', '.join(v)}")
    roles = _taxonomy_roles()
    missing = [s for s in roles if s not in live_slugs]
    print(f"\n## Slug trong taxonomy.json không live ({len(missing)})")
    for s in missing[:40]:
        print(f"- {s} ({roles[s][0]})")
    nocluster = [r["slug"] for r in rows if not r["cluster"]]
    print(f"\n## Chưa có cluster ({len(nocluster)}): {', '.join(nocluster[:20])}")
    strat = _check_topics(live_slugs)
    issues = len(pending) + len(multi) + len(missing) + len(nocluster) + len(strat)
    return 1 if issues else 0


def _topics() -> dict:
    return json.loads(TAXONOMY.read_text(encoding="utf-8")).get("topics", {})


def topic_problems(data: dict, live_slugs: set[str], facts: set[str]) -> list[str]:
    """Strategy fields in taxonomy.json topics + name drift between topics and link-group labels."""
    topics = data.get("topics", {})
    out = []
    folders = {}
    for s in data.get("site", {}).get("sections", []):
        if s.get("section") not in SITE_SECTIONS:
            out.append(f"khu vực site {s.get('id')}: section `{s.get('section')}` phải là {' / '.join(SITE_SECTIONS)}")
        for f in s.get("folders", []):
            if f in folders:
                out.append(f"thư mục {f} nằm ở 2 khu vực site: {folders[f]} và {s.get('id')}")
            folders[f] = s.get("id")
    for code, t in topics.items():
        if t.get("section") not in SECTIONS:
            out.append(f"cụm {code}: section `{t.get('section')}` phải là core / outer / off")
        b = t.get("bridge_to", "")
        if t.get("section") == "outer" and not b:
            out.append(f"cụm {code} (outer): thiếu bridge_to")
        if b and b not in live_slugs:
            out.append(f"cụm {code}: bridge_to `{b}` không live")
        for at in t.get("attributes", []):
            fid = at.get("fact", "")
            if fid and fid != "market" and fid not in facts:
                out.append(f"cụm {code}: thuộc tính “{at.get('name')}” trỏ fact `{fid}` không có trong brand-facts.json")
    subnames = {sg: n for t in topics.values() for sg, n in t.get("subgroups", {}).items()}
    for c in data.get("clusters", []):
        if c.get("topic") not in topics:
            out.append(f"cụm link {c['id']}: topic `{c.get('topic')}` không có trong topics")
        for g in c.get("groups", []):
            m = re.match(r"(\d+[a-z]) (.+)", g.get("name", ""))
            if m and m.group(1) in subnames and m.group(2) != subnames[m.group(1)]:
                out.append(f"tên nhóm lệch: link group “{g['name']}” ≠ topics {m.group(1)} “{subnames[m.group(1)]}”")
    return out


def _check_topics(live_slugs: set[str]) -> list[str]:
    data = json.loads(TAXONOMY.read_text(encoding="utf-8"))
    facts = {f["id"] for f in json.loads(BRAND_FACTS.read_text(encoding="utf-8"))["facts"]} if BRAND_FACTS.exists() else set()
    out = topic_problems(data, live_slugs, facts)
    print(f"\n## Chiến lược cụm (taxonomy.json topics) ({len(out)})")
    for x in out[:40]:
        print(f"- {x}")
    return out


def covered(attr: dict, rows: list[dict]) -> list[str]:
    """Articles whose title / keywords contain the attribute name or one of its aliases (accent-insensitive).
    Heuristic on registry text, not a content check."""
    keys = [unaccent(k).lower() for k in [attr["name"], *attr.get("aliases", [])]]
    return [r["slug"] for r in rows
            if any(k in unaccent(" ".join([r["title"], r["key_chinh"], r["key_phu"], r["keywords"]])).lower() for k in keys)]


def cmd_cluster(a) -> int:
    topics, rows = _topics(), [r for r in load() if r["status"] != "Merged"]
    if not a.code:
        print("| Mã | Cụm | Section | Thực thể | bridge_to | Bài | Qua pipeline | Thuộc tính phủ |")
        print("|---|---|---|---|---|---:|---:|---:|")
        for code, t in topics.items():
            rs = [r for r in rows if r["cluster"] == code]
            done = sum(1 for r in rs if r["status"] == "Finalized")
            at = t.get("attributes", [])
            cov = sum(1 for x in at if covered(x, rs))
            print(f"| {code} | {t['name']} | {t.get('section', '')} | {t.get('entity', '')} | {t.get('bridge_to', '') or '—'} | "
                  f"{len(rs)} | {round(100 * done / len(rs)) if rs else 0}% | {cov}/{len(at)} |")
        print('\nSửa section / entity / bridge_to / attributes: knowledge/3-seo/strategy/taxonomy.json → "topics".')
        return 0
    t = topics.get(a.code)
    if not t:
        print(f"Không có cụm `{a.code}`. Có: {', '.join(topics)}")
        return 1
    rs = [r for r in rows if r["cluster"] == a.code]
    print(f"# Cụm {a.code} — {t['name']}")
    print(f"section: {t.get('section')} · thực thể: {t.get('entity')} · bridge_to: {t.get('bridge_to') or '— (core)'}")
    print(f"bài: {len(rs)} · Finalized: {sum(1 for r in rs if r['status'] == 'Finalized')} · "
          f"Planned/đang làm: {sum(1 for r in rs if r['status'] not in ('Finalized', 'Live', 'Merged'))}")
    print("nhóm con: " + " · ".join(f"{k} {v}" for k, v in t.get("subgroups", {}).items()))
    at = t.get("attributes", [])
    if not at:
        print("\nChưa khai báo attributes cho cụm này (taxonomy.json → topics → attributes).")
        return 0
    print("\n| Thuộc tính | Nguồn giá trị | Bài đang phủ (theo tiêu đề/từ khoá) |\n|---|---|---|")
    gaps = []
    for x in at:
        hit = covered(x, rs)
        if not hit:
            gaps.append(x["name"])
        shown = (", ".join(hit[:3]) + (" …" if len(hit) > 3 else "")) if hit else "**chưa có**"
        print(f"| {x['name']} | {x.get('fact') or '—'} | {shown} |")
    if gaps:
        print(f"\nGap ({len(gaps)}): {', '.join(gaps)} → ứng viên bài mới cho /keyword-plan")
    return 0


def positioning() -> dict:
    """The two bold lines of profile.md §0 (single source for Định vị nội dung / Thực thể trung tâm)."""
    text = (ROOT / "knowledge/1-brand/profile.md").read_text(encoding="utf-8")
    out = {}
    for key, label in (("positioning", "Định vị nội dung"), ("entity", "Thực thể trung tâm")):
        m = re.search(rf"^- \*\*{label}:\*\*\s*(.+)$", text, re.M)
        out[key] = m.group(1).strip() if m else ""
    return out


def site_sections() -> dict:
    """Site-wide view: taxonomy.json `site.sections` joined with the latest gsc-site-folders.json snapshot.
    Folders not mapped to any area are returned as `unmapped` so the map never silently drops traffic."""
    import page_groups as pg
    day, snap = pg.latest_site_folders()
    groups = {g["group"]: g for g in snap.get("groups", [])}
    data = json.loads(TAXONOMY.read_text(encoding="utf-8")).get("site", {})
    out, used = [], set()
    for s in data.get("sections", []):
        gs = [groups[f] for f in s.get("folders", []) if f in groups]
        used.update(s.get("folders", []))
        out.append(dict(id=s["id"], name=s["name"], section=s.get("section", ""), note=s.get("note", ""),
                        folders=s.get("folders", []),
                        urls=sum(g.get("rows", 0) for g in gs), clicks=sum(g.get("clicks", 0) for g in gs),
                        prev=sum(g.get("prev_clicks", 0) for g in gs), impressions=sum(g.get("impressions", 0) for g in gs)))
    unmapped = [g for f, g in groups.items() if f not in used and g.get("clicks", 0) > 0]
    return dict(date=day, start=snap.get("start_date", ""), end=snap.get("end_date", ""),
                totals=snap.get("totals", {}), sections=out, unmapped=unmapped)


def suggest_section(share_k: float, rate: float, site_rate: float, sessions: float) -> str:
    """core when the cluster brings >= 15% of key events, or converts >= 2x the site rate on real traffic."""
    return "core" if share_k >= 0.15 or (rate >= 2 * site_rate and sessions >= 1000) else "outer"


def cmd_suggest_core(a) -> int:
    """Read-only: per cluster share of clicks and key events from page-audit.csv next to the declared section."""
    if not PAGE_AUDIT.exists():
        print("Chưa có page-audit.csv — chạy python scripts/page_groups.py report")
        return 3
    topics = _topics()
    with PAGE_AUDIT.open(encoding="utf-8-sig", newline="") as f:
        audit = list(csv.DictReader(f))
    agg: dict[str, list[float]] = {}
    for r in audit:
        v = agg.setdefault(r["cluster"], [0, 0.0, 0.0, 0.0, 0])
        v[0] += 1
        v[1] += float(r["clicks"] or 0)
        v[2] += float(r["key_events"] or 0)
        v[3] += float(r["sessions"] or 0)
        v[4] += r.get("pipeline") == "Finalized"
    tc, tk, ts = (sum(v[i] for v in agg.values()) or 1 for i in (1, 2, 3))
    site_rate = tk / ts
    print("Key events = tổng GA4 (xem trang MTK + điền form + gửi form), chưa tách theo event — trọng số trong "
          "kpi-definitions.md chưa áp được.\n")
    print("| Mã | Cụm | Section khai báo | % clicks | % key events | KE / 1.000 sessions | Qua pipeline | Gợi ý |")
    print("|---|---|---|---:|---:|---:|---:|---|")
    for code, t in topics.items():
        v = agg.get(code, [0, 0, 0, 0, 0])
        share_k, rate = v[2] / tk, (v[2] / v[3] if v[3] else 0)
        sug = suggest_section(share_k, rate, site_rate, v[3])
        decl = t.get("section", "")
        flag = "" if decl == sug or decl == "off" else " ⚠️ lệch"
        print(f"| {code} | {t['name']} | {decl} | {100 * v[1] / tc:.0f}% | {100 * share_k:.0f}% | {1000 * rate:.1f} | "
              f"{round(100 * v[4] / v[0]) if v[0] else 0}% | {sug}{flag} |")
    print("\nChỉ gợi ý (key events >= 15% tổng, hoặc tỷ lệ >= 2x trung bình site). Quyết định: sửa taxonomy.json → topics.")
    return 0


def cmd_show(a) -> int:
    hits = find(load(), a.slug)
    for r in hits:
        print("\n".join(f"{k:15} {v}" for k, v in r.items() if v))
        print("-")
    return 0 if hits else 1


def main() -> int:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--force", action="store_true"); b.set_defaults(fn=cmd_build)
    sub.add_parser("refresh").set_defaults(fn=cmd_refresh)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    s = sub.add_parser("show"); s.add_argument("slug"); s.set_defaults(fn=cmd_show)
    c = sub.add_parser("cluster"); c.add_argument("code", nargs="?"); c.set_defaults(fn=cmd_cluster)
    sub.add_parser("suggest-core").set_defaults(fn=cmd_suggest_core)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
