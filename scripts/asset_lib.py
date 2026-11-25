#!/usr/bin/env python3
"""Thư viện asset dựng ảnh: nền KV, motif tách nền, texture, ảnh thật (Unsplash/Pexels) — tạo 1 lần, dùng lại nhiều lần.

Dùng:
    python scripts/asset_lib.py plan                          # spec + trạng thái (đã có / chưa)
    python scripts/asset_lib.py build [--only id,id] [--kind bg|motif|texture] [--source codex|unsplash] [--limit N] [--dry-run]
    python scripts/asset_lib.py find --theme emerald --side right --aspect 4:5 [--tags "Tết,hoa mai"] [--kind bg] [--season tet]
    python scripts/asset_lib.py add <file> --id <id> --kind bg --theme emerald --side right --master tall [--tags …] [--season …]
    python scripts/asset_lib.py sheet                         # ảnh tổng hợp + preview.html để duyệt thư viện
    python scripts/asset_lib.py reject <id> --ly-do "…"       # loại asset xấu (giữ file, không được chọn nữa)

Thư mục: knowledge/1-brand/assets/library/{bg,motif,texture}/<id>.png · spec.json (danh sách muốn có) · index.json (đã có, thẻ, nguồn, lượt dùng).
- Codex: `creative.codex_generate` (tài khoản ChatGPT đã đăng nhập, không cần API key), tuần tự, mỗi asset 1 lần.
- Motif/texture có nền: vẽ trên nền magenta #FF00FF đặc → tách nền bằng chroma key (không cần rembg) → PNG trong suốt.
- Unsplash: khoá UNSPLASH_ACCESS_KEY trong .env; gọi download_location theo yêu cầu API; lưu tác giả + link để ghi công khi cần.
- `side` = phía CHỪA TRỐNG cho chữ (left/right/top/center). master tall = 9:16 (cắt được 4:5, 1:1), wide = 16:9 (cho 1.91:1).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, setup_utf8  # noqa: E402

LIB = ROOT / "knowledge/1-brand/assets/library"
SPEC = LIB / "spec.json"
INDEX = LIB / "index.json"
MASTER = {"tall": (1080, 1920), "wide": (1920, 1080), "square": (1440, 1440)}
ASPECT_MASTER = {"4:5": "tall", "1:1": "tall", "9:16": "tall", "1.91:1": "wide", "16:9": "wide"}
MAGENTA = (255, 0, 255)


def _ssl_ctx():
    import ssl
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:  # Python từ python.org trên macOS thiếu kho chứng chỉ → cần certifi
        return ssl.create_default_context()


def http_get(url: str, headers: dict | None = None, timeout: int = 30) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=timeout, context=_ssl_ctx()).read()

STYLE = {
    "emerald": ("premium cinematic 3D render, deep emerald green (#0B331E to #226435) palette, polished metallic gold "
                "(#EFD786 to #A57D3F) accents with fine engraved Vietnamese patterns, soft volumetric light, shallow depth of "
                "field, luxurious and calm"),
    "ivory": ("elegant contemporary Vietnamese silk-and-watercolor painting, warm ivory paper (#F9F4EB), jade green "
              "(#6CB298) tones, thin gold (#C9A24A) linework, airy and refined"),
}
NO = ("Absolutely NO text, NO letters, NO numbers, NO logos, NO watermarks, NO brand marks, NO people or faces, "
      "NO coins, NO banknotes, NO price arrows or profit symbols.")


def load_json(p: Path, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def save_index(idx: dict) -> None:
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")


def index() -> dict:
    return load_json(INDEX, {"version": 1, "assets": {}})


def env_key(name: str) -> str | None:
    if os.environ.get(name):
        return os.environ[name]
    envf = ROOT / ".env"
    if envf.exists():
        for line in envf.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


# ─────────────────────────── prompts ───────────────────────────

def prompt_for(a: dict) -> str:
    w, h = MASTER[a["master"]]
    ratio = {"tall": "9:16 vertical", "wide": "16:9 horizontal", "square": "1:1 square"}[a["master"]]
    style = STYLE.get(a["theme"], STYLE["emerald"])
    if a.get("allow_red") and a.get("season") == "national":
        red = "Red is allowed only for the Vietnamese flag silk; everything else follows the palette. "
    elif a.get("allow_red"):
        red = "Touches of soft lotus/peach pink are fine; no saturated red. "
    else:
        red = "No red anywhere. "
    if a["kind"] == "bg":
        space = {"right": "keep the right 45% of the frame calm, dark-to-mid toned and uncluttered",
                 "left": "keep the left 45% of the frame calm and uncluttered",
                 "top": "keep the top 45% of the frame calm and uncluttered (sky / soft gradient)",
                 "center": "keep the central area calm and uncluttered, details only near the edges"}[a["side"]]
        return " ".join([
            f"Background plate for premium social media visuals of a Vietnamese securities company. Subject: {a['subject']}.",
            f"Details: {', '.join(a.get('motifs', []))}." if a.get("motifs") else "",
            f"Mood: {a['mood']}." if a.get("mood") else "",
            f"Style: {style}.",
            f"Composition: {space} as negative space for text added later; the subject sits on the opposite side.",
            f"Aspect ratio {ratio}, about {w}x{h}px, high detail.", red, NO])
    if a["kind"] == "overlay":
        return " ".join([
            f"Light overlay element for compositing in screen blend mode: {a['subject']}.",
            "The background must be perfectly pure black (#000000) everywhere except the light itself; no scenery, no objects, no gradient haze.",
            f"Aspect ratio {ratio}, about {w}x{h}px.", NO])
    if a["kind"] == "motif":
        return " ".join([
            f"Single isolated object for compositing: {a['subject']}.",
            f"Style: {style}.",
            "Centered, fully visible with generous margin, nothing cropped. Background: a perfectly flat, uniform, solid pure "
            "magenta (#FF00FF) color filling the entire canvas, no gradient, no shadow on the background, no floor, no other objects.",
            "The object itself must not contain magenta or pink.",
            f"Aspect ratio {ratio}.", red, NO])
    # texture
    if a.get("keyed"):
        return " ".join([
            f"{a['subject']}.", f"Style: {style}.",
            "Lines only, on a perfectly flat, uniform, solid pure magenta (#FF00FF) background filling the canvas, no gradient, no shadow.",
            f"Aspect ratio {ratio}.", NO])
    return " ".join([f"{a['subject']}.", f"Style: {style}.", f"Aspect ratio {ratio}, evenly lit, seamless feel.", NO])


# ─────────────────────────── image ops ───────────────────────────

def chroma_key(src: Path, dst: Path, key=MAGENTA, t0: float = 60, t1: float = 140, pad: int = 24) -> tuple[int, int]:
    """Tách nền magenta → RGBA; khử ám màu ở mép; cắt sát vật + lề."""
    import numpy as np
    from PIL import Image
    im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    k = np.array(key, np.float32)
    dist = np.sqrt(((im - k) ** 2).sum(-1))
    alpha = np.clip((dist - t0) / (t1 - t0), 0, 1)
    a = np.maximum(alpha, 1e-3)[..., None]
    rgb = np.clip((im - (1 - alpha[..., None]) * k) / a, 0, 255)
    # khử ám magenta còn lại: kéo R,B về không vượt G nhiều ở vùng mép
    edge = (alpha > 0) & (alpha < 1)
    m = np.minimum(rgb[..., 0], rgb[..., 2]) - rgb[..., 1]
    spill = np.clip(m, 0, None) * edge
    rgb[..., 0] -= spill
    rgb[..., 2] -= spill
    out = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")
    bbox = img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox:
        x0, y0, x1, y1 = bbox
        img = img.crop((max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad)))
    img.save(dst)
    return img.size


def fit_master(src: Path, dst: Path, master: str) -> tuple[int, int]:
    from creative import cover_crop
    w, h = MASTER[master]
    cover_crop(src, dst, w, h)
    return w, h


# ─────────────────────────── sources ───────────────────────────

def build_codex(a: dict, dry: bool) -> dict:
    from creative import codex_generate, lint_prompt
    prompt = prompt_for(a)
    errs = [e for e in lint_prompt(prompt) if "negative space" not in e or a["kind"] == "bg"]
    if errs:
        return {"status": "prompt lỗi: " + "; ".join(errs)}
    if dry:
        return {"status": "dry-run ok", "prompt": prompt}
    folder = LIB / a["kind"]
    folder.mkdir(parents=True, exist_ok=True)
    raw = folder / f"{a['id']}.raw.png"
    res = codex_generate(prompt, raw)
    if not res["status"].startswith("ok"):
        return res
    dst = folder / f"{a['id']}.png"
    if a["kind"] == "motif" or a.get("keyed"):
        size = chroma_key(raw, dst)
    elif a["kind"] == "overlay":
        size = fit_master(raw, dst, a["master"])
    elif a["kind"] == "texture":
        size = fit_master(raw, dst, "square")
    else:
        size = fit_master(raw, dst, a["master"])
    res.update(file=str(dst.relative_to(ROOT)), size=list(size), prompt=prompt,
               source={"type": "codex", "license": "tạo bởi AI cho DSC"})
    return res


def build_unsplash(a: dict, dry: bool) -> dict:
    key = env_key("UNSPLASH_ACCESS_KEY")
    if not key:
        return {"status": "thiếu UNSPLASH_ACCESS_KEY trong .env"}
    q = urllib.parse.urlencode({"query": a["query"], "orientation": a.get("orientation", "portrait"),
                                "per_page": 10, "content_filter": "high"})
    hdr = {"Authorization": f"Client-ID {key}", "Accept-Version": "v1"}
    data = json.loads(http_get(f"https://api.unsplash.com/search/photos?{q}", hdr))
    results = [r for r in data.get("results", []) if not r.get("premium") and not r.get("plus")]
    if not results:
        return {"status": "Unsplash không có kết quả"}
    taken = {v.get("source", {}).get("photo_id") for v in index()["assets"].values()}
    if a.get("photo_id"):
        pick = next((r for r in results if r["id"] == a["photo_id"]), None) or json.loads(
            http_get(f"https://api.unsplash.com/photos/{a['photo_id']}", hdr))
    else:
        pick = next((r for r in sorted(results, key=lambda r: -r.get("likes", 0)) if r["id"] not in taken), results[0])
    info = {"photo_id": pick["id"], "author": pick["user"]["name"], "author_url": pick["user"]["links"]["html"],
            "photo_url": pick["links"]["html"], "license": "Unsplash License (dùng thương mại, không bắt buộc ghi công)"}
    if dry:
        return {"status": "dry-run ok", "source": info}
    # theo API guidelines: báo lượt tải
    http_get(pick["links"]["download_location"], hdr)
    w, h = MASTER[a["master"]]
    url = pick["urls"]["raw"] + "&" + urllib.parse.urlencode({"w": max(w, h) * 2 // 2, "fit": "max", "fm": "jpg", "q": 85})
    folder = LIB / a["kind"]
    folder.mkdir(parents=True, exist_ok=True)
    raw = folder / f"{a['id']}.raw.jpg"
    raw.write_bytes(http_get(url, timeout=60))
    dst = folder / f"{a['id']}.png"
    fit_master(raw, dst, a["master"])
    return {"status": "ok", "file": str(dst.relative_to(ROOT)), "size": [w, h], "source": {"type": "unsplash", **info}}


def stock_preview(aid: str, query: str | None = None, n: int = 8) -> Path:
    """Tải ảnh nhỏ của n ứng viên Unsplash cho 1 asset → 1 ảnh tổng hợp để chọn; ghi photo_id đã chọn vào spec.json."""
    from PIL import Image, ImageDraw
    import io
    spec = {s["id"]: s for s in load_json(SPEC, {"assets": []})["assets"]}
    a = spec[aid]
    key = env_key("UNSPLASH_ACCESS_KEY")
    hdr = {"Authorization": f"Client-ID {key}", "Accept-Version": "v1"}
    q = urllib.parse.urlencode({"query": query or a["query"], "orientation": a.get("orientation", "portrait"),
                                "per_page": n, "content_filter": "high"})
    res = [r for r in json.loads(http_get(f"https://api.unsplash.com/search/photos?{q}", hdr)).get("results", [])
           if not r.get("premium") and not r.get("plus")]
    cell = 260
    S = Image.new("RGB", (len(res) * (cell + 10) + 10, cell + 40), (228, 230, 229))
    d = ImageDraw.Draw(S)
    for i, r in enumerate(res):
        im = Image.open(io.BytesIO(http_get(r["urls"]["small"]))).convert("RGB")
        im.thumbnail((cell, cell))
        S.paste(im, (10 + i * (cell + 10), 10))
        d.text((10 + i * (cell + 10), cell + 16), f"{i}: {r['id']}", fill=(0, 0, 0))
    out = LIB / f"preview-{aid}.jpg"
    S.save(out, quality=85)
    (LIB / f"preview-{aid}.json").write_text(json.dumps([r["id"] for r in res]), encoding="utf-8")
    return out


def pin_stock(aid: str, photo_id: str, query: str | None = None) -> None:
    data = load_json(SPEC, {"assets": []})
    for s in data["assets"]:
        if s["id"] == aid:
            s["photo_id"] = photo_id
            if query:
                s["query"] = query
    SPEC.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build(only=None, kind=None, source=None, limit=None, dry=False, force=False) -> list[dict]:
    spec = load_json(SPEC, {"assets": []})["assets"]
    idx = index()
    out, n = [], 0
    for a in spec:
        if only and a["id"] not in only:
            continue
        if kind and a["kind"] != kind or source and a["source"] != source:
            continue
        if a["id"] in idx["assets"] and (ROOT / idx["assets"][a["id"]]["file"]).exists() and not force:
            continue
        if limit and n >= limit:
            break
        n += 1
        try:
            res = build_codex(a, dry) if a["source"] == "codex" else build_unsplash(a, dry)
        except Exception as e:  # noqa: BLE001
            res = {"status": f"lỗi: {e}"}
        out.append({"id": a["id"], **res})
        print(f"{a['id']:<22} {res['status']}" + (f"  ({res['seconds']}s)" if "seconds" in res else ""), flush=True)
        if res["status"].startswith("ok") and not dry:
            idx["assets"][a["id"]] = {k: a.get(k) for k in ("kind", "theme", "side", "master", "season", "tags", "blend")} | {
                "file": res["file"], "size": res["size"], "source": res["source"], "prompt": res.get("prompt"),
                "created": datetime.now().isoformat(timespec="seconds"), "used": [], "status": "active"}
            save_index(idx)
    return out


# ─────────────────────────── find / use / add / reject ───────────────────────────

def find(theme=None, side=None, aspect=None, tags=None, kind="bg", season=None, limit=5) -> list[tuple[str, dict, int]]:
    """Xếp hạng: khớp theme/side/master bắt buộc; điểm theo thẻ trùng + mùa; ít dùng & lâu chưa dùng lên trước."""
    master = ASPECT_MASTER.get(aspect) if aspect else None
    want = {t.strip().lower() for t in (tags or []) if t.strip()}
    rows = []
    for aid, v in index()["assets"].items():
        if v.get("status") != "active" or v["kind"] != kind:
            continue
        if theme and v.get("theme") != theme or side and v.get("side") != side or master and v.get("master") != master:
            continue
        if season and v.get("season") not in (season, "all"):
            continue
        score = 10 * len(want & {t.lower() for t in v.get("tags", [])}) + (5 if season and v.get("season") == season else 0)
        score -= 3 * len(v.get("used", []))
        last = max((u["date"] for u in v.get("used", [])), default="")
        rows.append((aid, v, score, last))
    rows.sort(key=lambda r: (-r[2], r[3]))
    return [(r[0], r[1], r[2]) for r in rows[:limit]]


def record_use(aid: str, job: str, creative_id: str) -> None:
    idx = index()
    if aid in idx["assets"]:
        idx["assets"][aid].setdefault("used", []).append({"job": job, "creative": creative_id, "date": date.today().isoformat()})
        save_index(idx)


def path_of(aid: str) -> Path | None:
    v = index()["assets"].get(aid)
    return ROOT / v["file"] if v and (ROOT / v["file"]).exists() else None


def add(file: Path, aid: str, kind: str, theme: str, side: str, master: str, tags: list[str], season: str) -> Path:
    folder = LIB / kind
    folder.mkdir(parents=True, exist_ok=True)
    dst = folder / f"{aid}.png"
    size = fit_master(file, dst, master) if kind == "bg" else chroma_key(file, dst)
    idx = index()
    idx["assets"][aid] = {"kind": kind, "theme": theme, "side": side, "master": master, "season": season, "tags": tags,
                          "file": str(dst.relative_to(ROOT)), "size": list(size),
                          "source": {"type": "import", "from": str(file)}, "created": datetime.now().isoformat(timespec="seconds"),
                          "used": [], "status": "active"}
    save_index(idx)
    return dst


def reject(aid: str, reason: str) -> None:
    idx = index()
    idx["assets"][aid].update(status="rejected", reject_reason=reason)
    save_index(idx)


def sheet() -> Path:
    from PIL import Image, ImageDraw
    items = [(k, v) for k, v in index()["assets"].items() if v.get("status") == "active"]
    cell, cols = 260, 6
    rows = (len(items) + cols - 1) // cols or 1
    S = Image.new("RGB", (cols * (cell + 10) + 10, rows * (cell + 34) + 10), (228, 230, 229))
    d = ImageDraw.Draw(S)
    for i, (k, v) in enumerate(items):
        im = Image.open(ROOT / v["file"])
        if im.mode == "RGBA":
            bg = Image.new("RGBA", im.size, (40, 48, 44, 255))
            bg.alpha_composite(im)
            im = bg
        im = im.convert("RGB")
        im.thumbnail((cell, cell))
        x, y = 10 + (i % cols) * (cell + 10), 10 + (i // cols) * (cell + 34)
        S.paste(im, (x + (cell - im.width) // 2, y))
        d.text((x, y + cell + 4), f"{k}", fill=(0, 0, 0))
        d.text((x, y + cell + 18), f"{v['kind']} · {v.get('theme')} · chừa {v.get('side')} · dùng {len(v.get('used', []))}", fill=(70, 70, 70))
    out = LIB / "library-sheet.jpg"
    S.save(out, quality=85)
    return out


def main(argv=None) -> int:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan")
    p = sub.add_parser("build")
    p.add_argument("--only")
    p.add_argument("--kind")
    p.add_argument("--source")
    p.add_argument("--limit", type=int)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true", help="tạo lại asset đã có (tốn quota nếu là Codex)")
    p = sub.add_parser("stock-preview")
    p.add_argument("id")
    p.add_argument("--query")
    p = sub.add_parser("stock-pin")
    p.add_argument("id")
    p.add_argument("photo_id")
    p.add_argument("--query")
    p = sub.add_parser("find")
    for f in ("--theme", "--side", "--aspect", "--tags", "--season"):
        p.add_argument(f)
    p.add_argument("--kind", default="bg")
    p = sub.add_parser("add")
    p.add_argument("file")
    for f in ("--id", "--kind", "--theme", "--side", "--master"):
        p.add_argument(f, required=True)
    p.add_argument("--tags", default="")
    p.add_argument("--season", default="all")
    p = sub.add_parser("reject")
    p.add_argument("id")
    p.add_argument("--ly-do", required=True)
    sub.add_parser("sheet")
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        idx = index()["assets"]
        spec = load_json(SPEC, {"assets": []})["assets"]
        for s in spec:
            st = "✓" if s["id"] in idx else "·"
            print(f"{st} {s['id']:<22} {s['kind']:<8} {s['source']:<9} {s['theme']:<8} chừa {s['side']:<7} {s['master']:<6} {s['season']}")
        print(f"\n{sum(s['id'] in idx for s in spec)}/{len(spec)} đã có")
    elif a.cmd == "build":
        res = build(a.only.split(",") if a.only else None, a.kind, a.source, a.limit, a.dry_run, a.force)
        return 1 if any(r["status"].startswith(("lỗi", "prompt lỗi", "Codex", "thiếu")) for r in res) else 0
    elif a.cmd == "stock-preview":
        print(stock_preview(a.id, a.query))
    elif a.cmd == "stock-pin":
        pin_stock(a.id, a.photo_id, a.query)
        print(f"{a.id} → {a.photo_id}. Chạy: python scripts/asset_lib.py build --only {a.id} --force")
    elif a.cmd == "find":
        for aid, v, sc in find(a.theme, a.side, a.aspect, (a.tags or "").split(","), a.kind, a.season):
            print(f"{aid:<22} điểm {sc:>3}  {v['file']}  dùng {len(v.get('used', []))}")
    elif a.cmd == "add":
        print(add(Path(a.file), a.id, a.kind, a.theme, a.side, a.master, [t.strip() for t in a.tags.split(",") if t.strip()], a.season))
    elif a.cmd == "reject":
        reject(a.id, a.ly_do)
        print(f"{a.id} → rejected")
    elif a.cmd == "sheet":
        print(sheet())
    return 0


if __name__ == "__main__":
    sys.exit(main())
