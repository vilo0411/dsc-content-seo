#!/usr/bin/env python3
"""Print one persona section from personas.md instead of loading all 4 (~14.5 KB).

    python scripts/persona.py P2                         # whole P2 section (~3 KB)
    python scripts/persona.py P2 --part "Product Bridge" # only matching ### subsection(s)
    python scripts/persona.py --matrix                   # quick persona → writing-adjustment matrix + usage rules
    python scripts/persona.py --list                     # persona names
"""
from __future__ import annotations

import argparse
import re
import sys

from _common import ROOT, setup_utf8, unaccent

PERSONAS = ROOT / "knowledge/1-brand/personas.md"


def sections(lines: list[str], level: str):
    """Return [(title, start, end)] for headings of exactly this level."""
    pat = re.compile(rf"^{re.escape(level)} (?!#)(.+)$")
    heads = [(m.group(1).strip(), i) for i, l in enumerate(lines) if (m := pat.match(l))]
    out = []
    for k, (t, s) in enumerate(heads):
        e = len(lines)
        # section ends at the next heading of the same or higher level
        for j in range(s + 1, len(lines)):
            h = re.match(r"^(#+) ", lines[j])
            if h and len(h.group(1)) <= len(level):
                e = j
                break
        out.append((t, s, e))
    return out


def main() -> int:
    setup_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("persona", nargs="?", help="P1–P4")
    ap.add_argument("--part", help="filter ### subsections by title (accent-insensitive substring)")
    ap.add_argument("--matrix", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    lines = PERSONAS.read_text(encoding="utf-8").splitlines()
    h2 = sections(lines, "##")

    if a.list:
        for t, _, _ in h2:
            if re.match(r"P\d", t):
                print(t)
        return 0
    if a.matrix:
        for t, s, e in h2:
            if unaccent(t).startswith(("ma tran", "quy tac")):
                print("\n".join(lines[s:e]).rstrip() + "\n")
        return 0
    if not a.persona:
        ap.error("cần P1–P4, --matrix hoặc --list")

    key = a.persona.upper().strip()
    hit = next(((t, s, e) for t, s, e in h2 if t.upper().startswith(key)), None)
    if not hit:
        print(f"Không có persona {key}. Có: " + ", ".join(t for t, _, _ in h2 if re.match(r"P\d", t)), file=sys.stderr)
        return 1
    t, s, e = hit
    body = lines[s:e]
    if a.part:
        q = unaccent(a.part)
        subs = [(st, ss, se) for st, ss, se in sections(body, "###") if q in unaccent(st)]
        if not subs:
            print(f"{t}: không có mục ### khớp '{a.part}'", file=sys.stderr)
            return 1
        print(f"## {t}\n")
        for _, ss, se in subs:
            print("\n".join(body[ss:se]).rstrip() + "\n")
        return 0
    print("\n".join(body).rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
