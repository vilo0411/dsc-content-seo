"""Article registry - ONE row per article URL: cluster, link role, pipeline status, anchors.

Single source for internal linking and article status (replaces anchor-index.md, anchor-keys.csv
and the status table in topic-clusters.md). File: knowledge/3-seo/strategy/pages.csv
Link architecture (pillar / hub / spoke, pillar anchors) stays in strategy/taxonomy.json.

    python scripts/registry.py build [--force]   # one-time: merge the legacy files into pages.csv
    python scripts/registry.py refresh           # after page_groups.py build / sync_live: add new live
                                                  # URLs, update title/cluster/role; never touches status/anchors
    python scripts/registry.py check             # unmapped file slugs, duplicate main keywords, taxonomy gaps
    python scripts/registry.py show <slug>       # one row, all fields

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
    if not SITEMAP_CACHE.exists():
        return set()
    return {u.rstrip("/").rsplit("/", 1)[-1] for u in json.loads(SITEMAP_CACHE.read_text(encoding="utf-8")).get("urls", [])}


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
        target = _map_to_live(r["file_slug"], r["title"], live_titles)
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
    pending = [r for r in rows if r["file_slug"] and r["live"] == "no" and r["status"] in ("Finalized", "Optimizing")]
    print(f"## Bài Finalized chưa khớp URL live ({len(pending)}) — đã publish thì sửa cột `slug` thành slug live")
    for r in pending[:40]:
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
    issues = len(pending) + len(multi) + len(missing) + len(nocluster)
    return 1 if issues else 0


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
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
