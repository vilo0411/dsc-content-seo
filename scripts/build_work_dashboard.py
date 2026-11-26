"""Build the SEO work dashboard from local evidence; no network or source-status writes.

Usage: python scripts/build_work_dashboard.py
"""
from __future__ import annotations

import contextlib
import csv
from collections import Counter
from datetime import datetime, timedelta
import html
import io
import json
from pathlib import Path
import re
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'knowledge/0-dashboard'
PIPE = ROOT / 'knowledge/3-seo'
CONTENT = ROOT / 'knowledge/3-seo/content'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def rel(path):
    return path.relative_to(ROOT).as_posix()


NEXT_BY_STATUS = {
    'Planned': '/outlining <keyword> (hoặc /write)', 'Outlining': 'Hoàn tất outline → outline_lint → trình Gate 1',
    'Outline-Pending': 'Hoàn tất outline → trình Gate 1', 'In Progress': 'Kiểm tra lại trạng thái thật (topic_status --set)',
    'Outline-Approved': '/drafting <slug>', 'Optimizing': 'Hoàn tất /optimize → /approve',
}


def workflow_tasks(task) -> dict:
    """Workflow-level rows: articles in progress, registry health, competitor watch, monthly report, channel drafts."""
    import registry
    today = datetime.now().date()
    stats = {}
    rows = registry.load() if registry.REGISTRY.exists() else []
    doing = [r for r in rows if r['status'] in NEXT_BY_STATUS]
    stats['in_progress'] = len(doing)
    for st, nxt in NEXT_BY_STATUS.items():
        hit = [r for r in doing if r['status'] == st]
        if hit:
            task(f'Bài ở bước {st}', 'Bài SEO', registry.REGISTRY, f'{len(hit)} bài',
                 'Nguồn: registry pages.csv (topic_status.py).', nxt,
                 details='\n'.join(f"{r['file_slug'] or r['slug']} · {r['key_chinh']}" for r in hit))
    if rows:
        live = {r['slug'] for r in rows if r['live'] == 'yes'}
        not_live = [r for r in rows if r['file_slug'] and r['live'] == 'no' and r['status'] in ('Finalized', 'Optimizing')]
        # Final file exists but no live page matches its body → simply not published yet (publish queue, not an error)
        waiting = [r for r in not_live if registry.final_path(r['file_slug']).exists()]
        nofile = [r for r in not_live if r not in waiting]
        keys = Counter(unaccent_key(r['key_chinh']) for r in rows if r['key_chinh'] and r['status'] != 'Merged')
        dup = [k for k, n in keys.items() if n > 1]
        nocl = [r['slug'] for r in rows if not r['cluster']]
        bad = len(nofile) + len(dup) + len(nocl)
        task('Registry bài viết', 'Dữ liệu', registry.REGISTRY, 'Cần đối chiếu' if bad else 'Đạt trong snapshot',
             f'{len(rows)} URL · {len(live)} live · {len(waiting)} bài Final chờ đăng · {len(nofile)} Finalized không có file Final · '
             f'{len(dup)} key chính trùng · {len(nocl)} chưa có cluster.',
             'Chờ đăng: xem mục "Chờ publish" của weekly_review.py. Lỗi dữ liệu: python scripts/registry.py check → '
             'sửa slug / status / cluster; trùng key → cân nhắc gộp (301).',
             details='\n'.join([*(f'không có file Final: {r["file_slug"]}' for r in nofile), *(f'trùng key: {k}' for k in dup),
                                *(f'chưa cluster: {s}' for s in nocl), *(f'chờ đăng: {r["file_slug"]}' for r in waiting)]))
    watch = sorted((ROOT / 'knowledge/2-market/competitors/watch').glob('*.md'))
    y, w, _ = today.isocalendar()
    this_week = f'{y}-W{w:02d}'
    vel = ROOT / 'knowledge/2-market/competitors/velocity.csv'
    new_posts = 0
    if vel.exists():
        with vel.open(encoding='utf-8', newline='') as fh:
            new_posts = sum(int(r['new'] or 0) for r in csv.DictReader(fh) if r['week'] == this_week)
    stats['competitor_new'] = new_posts
    latest = watch[-1] if watch else ROOT / 'knowledge/2-market/competitors/competitors.json'
    task('Theo dõi đối thủ', 'Đối thủ', latest,
         'Đạt trong snapshot' if watch and watch[-1].stem == this_week else 'Chưa chạy tuần này',
         f'Báo cáo gần nhất: {watch[-1].stem if watch else "chưa có"} · {new_posts} bài mới của đối thủ tuần {this_week}.',
         '/competitor-watch (competitor_watch.py run → report), rồi đưa chủ đề "DSC chưa có" vào /keyword-plan.')
    prev = (today.replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
    rep = ROOT / f'knowledge/5-analytics/reports/{prev}.md'
    due = today.day >= 5
    task(f'Báo cáo tháng {prev}', 'Đo lường', rep if rep.exists() else ROOT / 'knowledge/5-analytics/kpi-definitions.md',
         'Đạt trong snapshot' if rep.exists() else ('Đến hạn' if due else 'Chưa đến hạn (GSC trễ 2–4 ngày)'),
         'Lead, CPL SEO, CPA Ads theo kpi-definitions.md.', f'/analytics-report {prev}')
    drafts = []
    for p in sorted((ROOT / 'knowledge/4-channels').rglob('*.md')):
        if p.name != 'README.md' and re.search(r'^Status:\s*Draft', p.read_text(encoding='utf-8', errors='replace')[:600], re.M):
            drafts.append(p)
    stats['channel_drafts'] = len(drafts)
    task('Bản nháp kênh khác chờ duyệt', 'Kênh khác', ROOT / 'knowledge/4-channels/README.md' if not drafts else drafts[0],
         'Đạt trong snapshot' if not drafts else f'{len(drafts)} bản nháp',
         'Ads / email / landing / social có Status: Draft.', 'Duyệt → đổi Status: Approved; agent không tự đăng / gửi.',
         details='\n'.join(rel(p) for p in drafts))
    return stats


PENDING = {'Optimizing', 'Outline-Pending', 'Outlining', 'Outline-Approved', 'In Progress'}
KIND = [('Proposal-', 'Proposal'), ('Optimize-', 'Bản viết lại'), ('Draft-', 'Draft'), ('', 'Outline')]


def md_preview(path: Path) -> str:
    """Render a working markdown file for in-dashboard reading (fenced blocks kept as <pre>)."""
    import md_to_cms_html as m
    text = path.read_text(encoding='utf-8', errors='replace')
    fm, lines = m.split_frontmatter(text)
    out = []
    if fm:
        out.append('<table class="fm">' + ''.join(f'<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>'
                                                  for k, v in fm.items()) + '</table>')
    chunk, fence = [], None
    for ln in lines + ['']:
        if ln.strip().startswith('```'):
            if fence is None:
                out.append(m.convert(chunk)[1] if chunk else '')
                chunk, fence = [], []
            else:
                out.append('<pre>' + html.escape('\n'.join(fence)) + '</pre>')
                fence = None
            continue
        (fence if fence is not None else chunk).append(ln)
    if fence:
        out.append('<pre>' + html.escape('\n'.join(fence)) + '</pre>')
    h1, body = m.convert(chunk)
    out.append(body)
    if h1:
        out.insert(1 if fm else 0, f'<h1>{html.escape(h1)}</h1>')
    doc = '\n'.join(out)

    # Images are relative to the markdown file; re-point them at the dashboard folder.
    def fix(mt):
        src = mt.group(2)
        if re.match(r'(https?:|/|data:)', src):
            return mt.group(0)
        target = (path.parent / src).resolve()
        try:
            return f'{mt.group(1)}../../{target.relative_to(ROOT).as_posix()}"'
        except ValueError:
            return mt.group(0)
    return re.sub(r'(<img[^>]*?src=")([^"]+)"', fix, doc)


def approval_queue() -> list[dict]:
    """Articles waiting at a gate, with their working files rendered inline (Gate 1 = outline/proposal, Gate 2 = draft)."""
    import registry
    rows = registry.load() if registry.REGISTRY.exists() else []
    by_slug = {}
    for r in rows:
        for s in {r['slug'], r['file_slug']} - {''}:
            by_slug.setdefault(s, r)
    waves = {}
    for tr in (CONTENT / 'audits').glob('*/tracker.csv'):
        with tr.open(encoding='utf-8-sig', newline='') as fh:
            for r in csv.DictReader(fh):
                if r.get('slug') and r.get('wave'):
                    waves[r['slug']] = f"{tr.parent.name} · đợt {r['wave']}"
    files = {}
    for folder in (CONTENT / '1-outlines', CONTENT / '2-drafts'):
        for p in folder.glob('*.md'):
            for prefix, kind in KIND:
                if p.name.startswith(prefix):
                    files.setdefault(p.stem[len(prefix):], {})[kind] = p
                    break
    queue = []
    for slug, fs in files.items():
        r = by_slug.get(slug)
        status = r['status'] if r else 'Không có trong registry'
        if (r and status not in PENDING) or (not r and 'Proposal' not in fs):
            continue   # not waiting, or a stray note file (Rollback-*, *-image-prompts) outside the registry
        snap = CONTENT / 'archive' / slug / 'gate2.md'
        work = fs.get('Bản viết lại') or fs.get('Draft')
        newest = max(p.stat().st_mtime for p in fs.values())
        plan = [p.stat().st_mtime for k, p in fs.items() if k in ('Proposal', 'Outline')]
        # Gate 2 = a gate2 snapshot taken after the plan file was last touched.
        if work and snap.exists() and snap.stat().st_mtime >= max(plan, default=0):
            gate = 'Gate 2 · duyệt bài'
        elif 'Proposal' in fs:
            gate = 'Gate 1 · duyệt Proposal'
        elif 'Outline' in fs and status in ('Outline-Pending', 'Outlining'):
            gate = 'Gate 1 · duyệt Outline'
        else:
            gate = 'Đang làm'
        final = CONTENT / '3-finalized' / f'Final-{slug}.md'
        order = ['Proposal', 'Outline', 'Bản viết lại', 'Draft']
        created, updated = file_dates(list(fs.values()))
        queue.append(dict(
            slug=slug, status=status, gate=gate, wave=waves.get(slug, ''),
            keyword=r['key_chinh'] if r else '', title=r['title'] if r else '',
            created=created, updated=updated,
            final=rel(final) if final.exists() else '',
            final_date=datetime.fromtimestamp(final.stat().st_mtime).strftime('%Y-%m-%d') if final.exists() else '',
            docs=[dict(kind=k, path=rel(fs[k]), html=md_preview(fs[k])) for k in order if k in fs]))
    queue.sort(key=lambda q: q['updated'], reverse=True)
    return queue


def file_dates(paths: list[Path]) -> tuple[str, str]:
    """(Created, Updated) of an article's working files: YAML fields first (AGENTS.md rule 8), file time as fallback."""
    from _common import read_text, split_frontmatter
    created, updated = [], []
    for p in paths:
        fm = split_frontmatter(read_text(p)[0])[0]
        mt = datetime.fromtimestamp(p.stat().st_mtime).strftime('%Y-%m-%d')
        created.append(fm.get('Created') or mt)
        updated.append(fm.get('Updated') or mt)
    return (min(created) if created else ''), (max(updated) if updated else '')


ACTION_CMD = {'refresh': '/optimize {slug}', 'bridge': '/cro {slug}', 'prune?': 'xem lại: gộp / 301 / giữ — {slug}'}


def _num(x) -> float:
    try:
        return float(x or 0)
    except ValueError:
        return 0.0


def today_view(approvals: list[dict]) -> dict:
    """Home screen data: today's tasks, metric changes, site-level queue, strategy map. Read-only."""
    import campaign
    import page_groups
    import registry
    import topic_status
    import weekly_review as wr
    from _common import working_files

    today = datetime.now().date()
    rows = registry.load() if registry.REGISTRY.exists() else []
    audit_path = registry.PAGE_AUDIT
    audit = []
    if audit_path.exists():
        with audit_path.open(encoding='utf-8-sig', newline='') as fh:
            audit = list(csv.DictReader(fh))
    audit_dir = page_groups.latest_audit_dir()
    site = registry.site_sections()
    serp = sorted((ROOT / 'knowledge/raw/serp').glob('*.json'), key=lambda p: p.stat().st_mtime)
    fresh = dict(
        audit=audit_dir.name if audit_dir else '', site=site['date'],
        audit_built=datetime.fromtimestamp(audit_path.stat().st_mtime).strftime('%Y-%m-%d') if audit_path.exists() else '',
        serp=datetime.fromtimestamp(serp[-1].stat().st_mtime).strftime('%Y-%m-%d') if serp else '')

    # 1. Today's tasks
    doing = []
    for r in rows:
        if r['status'] in NEXT_BY_STATUS:
            slug = r['file_slug'] or r['slug']
            created, updated = file_dates(working_files(slug) or working_files(r['slug']))
            doing.append(dict(slug=slug, keyword=r['key_chinh'], status=r['status'], next=NEXT_BY_STATUS[r['status']],
                              created=created, updated=updated))
    leftovers, mismatch = topic_status.find_stale()
    cleanup = dict(
        leftovers=[dict(file=rel(p), slug=sl, updated=file_dates([p])[1]) for p, sl in leftovers],
        mismatch=[dict(file=rel(p), slug=sl, status=st) for p, sl, st in mismatch])
    ledger = wr.snap.read_ledger()
    unpublished = [s for s, r in ledger.items() if r['final'] and not r['first_live'] and r['note'] != 'seed']
    backfill = [s for s, r in ledger.items() if wr.d(r['first_live']) and not r['backfill_done']]
    gsc_due = [s for s, r in ledger.items()
               if wr.d(r['first_live']) and not r['gsc_checked'] and (today - wr.d(r['first_live'])).days >= wr.GSC_FROM]
    jobs = [j for j in campaign.summary() if j['status'] not in ('Đóng',)]
    todo = dict(
        gate1=[a['slug'] for a in approvals if a['gate'].startswith('Gate 1')],
        gate2=[a['slug'] for a in approvals if a['gate'].startswith('Gate 2')],
        doing=doing, cleanup=cleanup, weekly=dict(unpublished=unpublished, backfill=backfill, gsc_due=gsc_due),
        campaigns=[dict(id=j['id'], status=j['status']) for j in jobs])

    # 2. Metric changes (offline snapshot from page_groups.py report)
    topics = registry._topics()
    by = {}
    for r in audit:
        v = by.setdefault(r['cluster'], dict(clicks=0.0, prev=0.0, impr=0.0, ke=0.0, sess=0.0, n=0, final=0))
        v['clicks'] += _num(r['clicks'])
        v['prev'] += _num(r['prev_clicks'])
        v['impr'] += _num(r['impressions'])
        v['ke'] += _num(r['key_events'])
        v['sess'] += _num(r['sessions'])
        v['n'] += 1
        v['final'] += r.get('pipeline') == 'Finalized'
    tot = {k: sum(v[k] for v in by.values()) for k in ('clicks', 'prev', 'impr', 'ke', 'sess')}
    drops = sorted((r for r in audit if 'rank-drop' in r['labels']), key=lambda r: _num(r['click_change']))[:5]
    metrics = dict(total=tot, drops=[dict(slug=r['slug'], clicks=_num(r['clicks']), change=_num(r['click_change']),
                                          cluster=r['cluster']) for r in drops])

    # 3. Site-level queue
    queue = sorted((r for r in audit if r.get('action') in ACTION_CMD), key=lambda r: -_num(r['priority']))
    counts = Counter(r.get('action', '') for r in audit)
    queue_rows = [dict(slug=r['slug'], action=r['action'], priority=_num(r['priority']), labels=r['labels'],
                       cluster=r['cluster'], section=r.get('section', ''), pipeline=r.get('pipeline', ''),
                       cmd=ACTION_CMD[r['action']].format(slug=r['slug'])) for r in queue[:15]]

    # 4. Strategy map
    site_rate = tot['ke'] / tot['sess'] if tot['sess'] else 0
    live = {r['slug'] for r in rows if r['live'] == 'yes'}
    facts = {f['id'] for f in read_json(registry.BRAND_FACTS)['facts']}
    warnings = registry.topic_problems(read_json(registry.TAXONOMY), live, facts)
    clusters = []
    reg_rows = [r for r in rows if r['status'] != 'Merged']
    for code, t in topics.items():
        v = by.get(code, dict(clicks=0, prev=0, impr=0, ke=0, sess=0, n=0, final=0))
        share_k = v['ke'] / tot['ke'] if tot['ke'] else 0
        sug = registry.suggest_section(share_k, v['ke'] / v['sess'] if v['sess'] else 0, site_rate, v['sess'])
        if t.get('section') not in (sug, 'off'):
            warnings.append(f"cụm {code} khai báo {t.get('section')}, dữ liệu gợi ý {sug} (key events {share_k:.0%})")
        rs = [r for r in reg_rows if r['cluster'] == code]
        at = t.get('attributes', [])
        clusters.append(dict(
            code=code, name=t['name'], section=t.get('section', ''), suggested=sug, entity=t.get('entity', ''),
            bridge_to=t.get('bridge_to', ''), pages=v['n'], clicks=v['clicks'], prev=v['prev'],
            clicks_share=v['clicks'] / tot['clicks'] if tot['clicks'] else 0, ke=v['ke'], ke_share=share_k,
            pipeline=v['final'] / v['n'] if v['n'] else 0,
            attrs=len(at), attrs_covered=sum(1 for x in at if registry.covered(x, rs)),
            actions=dict(Counter(r.get('action', '') for r in audit if r['cluster'] == code))))
    strategy = dict(**registry.positioning(), clusters=clusters, warnings=warnings, site=site)
    return dict(fresh=fresh, todo=todo, metrics=metrics, queue=queue_rows, queue_counts=dict(counts), strategy=strategy)


# ─────────────────────────── activity log + channels (all marketing domains) ───────────────────────────

STAGE_RE = re.compile(r'^(?:Stage|Status):\s*(.+)$', re.M)
CAMPAIGN_CH = {'social': 'social', 'ads': 'ads-meta', 'landing': 'landing', 'seo': 'seo', 'email': 'email'}
IN_PROGRESS = {'Planned', 'Outlining', 'Outline-Pending', 'In Progress', 'Outline-Approved', 'Optimizing'}


def _head(path, n=800):
    return path.read_text(encoding='utf-8', errors='replace')[:n]


def _mdate(path):
    return datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d')


def activity_view(days=180, cap=2000):
    """Events for the "Hoạt động" tab: last N days (newest first) + per-domain counts for 7 / 30 days."""
    import activity_log as al
    ev = al.read_events(days=days)
    today = datetime.now().date()
    cut7, cut30 = (today - timedelta(days=7)).isoformat(), (today - timedelta(days=30)).isoformat()
    counts = {}
    for e in ev:
        c = counts.setdefault(e.get('domain', '?'), {'d7': 0, 'd30': 0, 'last': ''})
        ts = e.get('ts', '')
        c['d7'] += ts >= cut7
        c['d30'] += ts >= cut30
        c['last'] = max(c['last'], ts)
    return dict(events=list(reversed(ev))[:cap], counts=counts, labels=al.DOMAIN_LABEL, total=len(ev))


def channels_view(approvals, act):
    """One card per channel: what is in progress, what waits for approval, latest activity.
    pending[] = non-SEO drafts waiting for a human (fed into "Cần làm" on the Hôm nay tab)."""
    import campaign
    import registry
    counts = act['counts']
    cards, pending = [], []

    def card(domain, items, metrics, cmd=''):
        c = counts.get(domain, {})
        cards.append(dict(domain=domain, label=act['labels'].get(domain, domain), metrics=metrics, items=items[:12],
                          more=max(0, len(items) - 12), d7=c.get('d7', 0), d30=c.get('d30', 0),
                          last=c.get('last', '')[:16].replace('T', ' '), cmd=cmd))

    def draft_item(dom, f, stage, job=''):
        return dict(domain=dom, job=job, file=rel(f), name=f.name, stage=stage, updated=_mdate(f))

    # SEO
    rows = registry.load()
    in_prog = [r for r in rows if r['status'] in IN_PROGRESS]
    g1 = sum(a['gate'].startswith('Gate 1') for a in approvals)
    g2 = sum(a['gate'].startswith('Gate 2') for a in approvals)
    card('seo', [f"{r['status']} · {r['slug']}" for r in in_prog],
         [('Đang làm', len(in_prog)), ('Chờ duyệt outline', g1), ('Chờ duyệt bài', g2),
          ('Live', sum(r['live'] == 'yes' for r in rows))], '/write · /approve')

    # Campaign jobs + drafts inside each job (Stage: PREVIEW / not yet copied to approved/)
    jobs = campaign.summary()
    by_dom = {d: [] for d in ('social', 'ads-meta', 'landing', 'seo', 'email')}
    for j in jobs:
        job = campaign.CAMPAIGNS_DIR / j['id']
        approved = {f.stem for f in (job / 'approved').glob('*')} if (job / 'approved').is_dir() else set()
        for ch, dom in CAMPAIGN_CH.items():
            if not (job / ch).is_dir():
                continue
            for f in sorted((job / ch).glob('*.md')):
                m = STAGE_RE.search(_head(f))
                stage = m.group(1).strip() if m else ''
                if f.stem in approved or re.match(r'(?i)approved|live', stage):
                    continue
                item = draft_item(dom, f, stage.split('—')[0].strip() or 'Nháp', j['id'])
                by_dom[dom].append(item)
                pending.append(item)
    card('campaign', [f"{j['status']} · {j['id']} · " + ' '.join(f'{k}:{v}' for k, v in j['files'].items())
                      + f" · approved:{j['approved']}" + (' · report ✓' if j['report'] else '') for j in jobs],
         [('Job', len(jobs)), ('Chờ duyệt', sum(j['status'] == 'Chờ duyệt' for j in jobs)),
          ('Live', sum(j['status'] == 'Live' for j in jobs)), ('Nháp trong job', len(pending))],
         '/campaign-brief · /mkt-status')

    # Meta Ads: drafts in jobs + review files
    reviews = sorted(ROOT.glob('knowledge/6-campaigns/CMP-*/ads/review-*.md')) + sorted(ROOT.glob('knowledge/raw/ads/review-*.md'))
    card('ads-meta', [f"{i['stage']} · {i['job']} · {i['name']}" for i in by_dom['ads-meta']]
         + [f"Review · {rel(p)}" for p in reviews[-3:]],
         [('Nháp chờ duyệt', len(by_dom['ads-meta'])), ('Review', len(reviews))], '/ads-brief → /meta-ads-copy · /ads-review')

    # Channels with their own folder in 4-channels (Status: Draft in frontmatter)
    def chan_files(sub):
        out = []
        for f in sorted((ROOT / 'knowledge/4-channels' / sub).glob('*.md')):
            if f.name != 'README.md':
                m = STAGE_RE.search(_head(f))
                out.append((m.group(1).strip() if m else '?', f))
        return out

    for sub, dom, cmd in (('ads', 'ads-google', '/ads-audit · /ads-copy'), ('email', 'email', '/email-sequence'),
                          ('landing', 'landing', '/landing · /copy-landing')):
        fs = chan_files(sub)
        jd = by_dom.get(dom, []) if dom != 'ads-google' else []
        n_draft = sum(s.startswith('Draft') for s, _ in fs)
        card(dom, [f"{s} · {f.name}" for s, f in fs] + [f"{i['stage']} · {i['job']} · {i['name']}" for i in jd],
             [('File kênh', len(fs)), ('Nháp', n_draft + len(jd))], cmd)
        pending += [draft_item(dom, f, 'Draft') for s, f in fs if s.startswith('Draft')]

    # Social: syndication ledger + campaign posts
    ledger = ROOT / 'knowledge/4-channels/social/ledger.csv'
    srows = list(csv.DictReader(ledger.open(encoding='utf-8-sig', newline=''))) if ledger.exists() else []
    st = Counter(r.get('status', '') for r in srows)
    card('social', [f"{i['stage']} · {i['job']} · {i['name']}" for i in by_dom['social']]
         + [f"{r.get('status')} · {r.get('channel')} · {r.get('slug')}" for r in srows if r.get('status') != 'Posted'],
         [('Syndication', len(srows))] + [(f'Syndication {k or "?"}', v) for k, v in st.most_common(2)]
         + [('Post trong job', len(by_dom['social']))], '/social-post · /syndicate')

    # Creative: design.json per channel in each job
    items, n_sets, n_appr = [], 0, 0
    for design in sorted(ROOT.glob('knowledge/6-campaigns/CMP-*/*/creatives/design.json')):
        try:
            d = read_json(design)
        except Exception:
            continue
        v = d.get('version', '?')
        qa = design.parent / f'v{v}' / 'qa.json'
        qs = Counter(c.get('status', '?') for c in read_json(qa).get('creatives', {}).values()) if qa.exists() else Counter()
        n_appr += len(d.get('approved') or [])
        n_sets += 1
        job, ch = design.relative_to(ROOT / 'knowledge/6-campaigns').parts[:2]
        items.append(f"{job} · {ch} v{v} · " + (', '.join(f'{k} {c}' for k, c in qs.items()) or 'chưa QA')
                     + f" · đã duyệt {len(d.get('approved') or [])} lần")
    card('creative', items, [('Bộ creative', n_sets), ('Lần duyệt', n_appr)], '/creative')

    # Analytics + market
    reps = sorted((ROOT / 'knowledge/5-analytics/reports').glob('20*.md'))
    weekly = sorted((ROOT / 'knowledge/5-analytics/weekly').glob('20*.md'))
    card('analytics', [f"Báo cáo tháng · {p.stem}" for p in reversed(reps)][:4] + [f"Weekly · {p.stem}" for p in reversed(weekly)][:4],
         [('Báo cáo tháng mới nhất', reps[-1].stem if reps else '—'), ('Weekly mới nhất', weekly[-1].stem if weekly else '—')],
         '/analytics-report · /weekly')
    mk = ROOT / 'knowledge/2-market'
    watch = sorted((mk / 'competitors/watch').glob('20*.md'))
    profiles = sorted((mk / 'competitors/profiles').glob('*.md'))
    research = sorted((mk / 'research').glob('*.md'))
    card('market', [f"Watch · {p.stem}" for p in reversed(watch)][:3] + [f"Profile · {p.stem}" for p in profiles]
         + [f"Research · {p.stem}" for p in research],
         [('Watch mới nhất', watch[-1].stem if watch else '—'), ('Profile', len(profiles)), ('Research', len(research))],
         '/competitor-watch · /market-research')
    return dict(cards=cards, pending=pending)


def unaccent_key(s: str) -> str:
    import unicodedata
    s = s.replace('đ', 'd').replace('Đ', 'D')
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()


def build():
    import link_plan

    OUT.mkdir(parents=True, exist_ok=True)
    tasks = []
    meta = read_json(ROOT / 'knowledge/raw/live/_meta.json')
    snapshot = meta.get('last_run', 'Không rõ')

    def task(name, group, source, state, evidence, next_step, **extra):
        tasks.append(dict(name=name, group=group, source=rel(source), state=state,
                          evidence=evidence, next_step=next_step, **extra))

    # Reuse the established verifier, including anchor and full-paragraph rules.
    for spec in sorted((PIPE / 'links/plans').glob('*.json')):
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                link_plan.cmd_verify(SimpleNamespace(spec=str(spec)))
            match = re.search(r'Đã lên live: (\d+)/(\d+)', capture.getvalue())
            if not match:
                raise ValueError('Verifier không trả số lượng')
            done, total = map(int, match.groups())
            state = 'Đạt trong snapshot' if done == total else 'Còn mục chưa xác nhận'
            evidence = f'{done}/{total} thay đổi đạt kiểm tra; không cộng các đợt vì có thể trùng nhau.'
            task(spec.stem, 'Internal link', spec.with_suffix('.html') if spec.with_suffix('.html').exists() else spec,
                 state, evidence, 'Xem mục chưa đạt; đối chiếu CMS rồi sync và kiểm tra lại.',
                 done=done, total=total, details=capture.getvalue(), spec=rel(spec))
        except Exception as exc:
            task(spec.stem, 'Internal link', spec, 'Không kiểm tra được', str(exc), 'Kiểm tra spec và snapshot.')

    # Separate unknown/meta edits from body edits which can be checked locally.
    for spec in sorted((CONTENT / 'audits/edits').glob('*.json')):
        done = pending = unknown = 0
        details = []
        for edit in read_json(spec).get('edits', []):
            page = ROOT / 'knowledge/raw/live/html' / (edit['slug'] + '.html')
            before, after = edit.get('find', ''), edit.get('replace', '')
            if edit.get('field') or not page.exists() or not before or not after:
                unknown += 1
                result = 'Cần xác minh riêng (field/thiếu snapshot)'
            else:
                doc = page.read_text(encoding='utf-8')
                if after in doc and before not in doc:
                    done += 1
                    result = 'Đạt trong snapshot'
                elif before in doc:
                    pending += 1
                    result = 'Còn đoạn cũ trong snapshot'
                else:
                    unknown += 1
                    result = 'Nội dung đã đổi; chưa khớp bản đề xuất'
            details.append(f"{edit['slug']}: {result}")
        total = done + pending + unknown
        task(spec.stem, 'Stale', CONTENT / 'audits/stale-content-refresh-2026-11-04.html',
             'Đạt trong snapshot' if total and done == total else 'Còn mục chưa xác nhận',
             f'{done}/{total} đạt; {pending} còn đoạn cũ; {unknown} cần xác minh riêng.',
             'Mở bộ sửa stale; kiểm tra từng mục, title/meta cần đối chiếu CMS.',
             done=done, total=total, details='\n'.join(details), spec=rel(spec))

    task('Content audit: xóa / sửa / gộp', 'Content audit', CONTENT / 'audits/content-audit-2026-11-05/tracker.html',
         'Tiến độ ở trình duyệt', 'Tracker lưu localStorage và có Xuất/Nhập tiến độ; chưa có bản xuất chung trong repo.',
         'Mở tracker trên trình duyệt đã dùng; xuất tiến độ để đối chiếu. Chưa suy ra hoàn tất từ file báo cáo.')

    # Record saved QA results as historical evidence, never as publication proof.
    for check in sorted((CONTENT / 'audits').rglob('*validation*.json')):
        task(check.parent.name + ' / ' + check.stem, 'QA / SERP', check,
             'Có kết quả kiểm tra đã lưu', 'Kết quả tại thời điểm tạo file; chưa chứng minh bản hiện tại đã publish.',
             'Xem báo cáo và kiểm tra lại bản cuối trước khi xuất bản.')
    for monitor in sorted((CONTENT / 'audits').rglob('monitoring.csv')):
        with monitor.open(encoding='utf-8-sig', newline='') as f:
            records = list(csv.DictReader(f))
        measured = sum(bool(r.get('actual_date', '').strip()) for r in records)
        task(monitor.parent.name + ' / đo lường', 'Theo dõi GSC', monitor,
             'Chưa ghi nhận đo lường' if not measured else 'Đã có dữ liệu đo',
             f'{measured}/{len(records)} dòng có actual_date; không có nghĩa là đã đặt lịch tự động.',
             'Điền ngày publish thực tế và số đo ở các mốc trong file.')

    # Ledger is authoritative for recorded milestones, not exact CMS version parity.
    ledger = PIPE / 'logs/publish-ledger.csv'
    with ledger.open(encoding='utf-8-sig', newline='') as f:
        records = list(csv.DictReader(f))
    for label, field, prerequisite, step in [
        ('Bản Final chưa ghi nhận live', 'first_live', 'final', 'Đối chiếu CMS, publish rồi sync; Finalized chưa có nghĩa là đã lên web.'),
        ('Bài live chưa ghi nhận backfill', 'backfill_done', 'first_live', 'Gom backfill bằng /weekly, xác minh rồi ghi nhận vào ledger.'),
        ('Bài live chưa ghi nhận kiểm tra GSC', 'gsc_checked', 'first_live', 'Chạy /weekly để lọc bài đến hạn 28–56 ngày; danh sách này gồm cả bài chưa đến hạn.')]:
        pending = [r['slug'] for r in records if r.get(prerequisite) and not r.get(field)]
        task(label, 'Sau publish', ledger, 'Có việc cần đối chiếu' if pending else 'Không có mục thiếu mốc',
             f'{len(pending)} bài thiếu mốc {field} trong ledger; seed là mốc nhập lịch sử.', step,
             details='\n'.join(pending))

    # Detect contradictory backlog statuses without rewriting legacy records.
    normalize = lambda s: re.sub(r'\s+', ' ', s.replace('**', '').replace('`', '').strip().lower())
    primary = {}
    with (PIPE / 'strategy/pages.csv').open(encoding='utf-8-sig', newline='') as fh:
        for r in csv.DictReader(fh):
            if r.get('key_chinh'):
                primary.setdefault(normalize(r['key_chinh']), set()).add(r['status'])
    conflicts = []
    for line in (PIPE / 'strategy/sprint-backlog.md').read_text(encoding='utf-8').splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if line.startswith('|') and len(cells) >= 3:
            statuses = primary.get(normalize(cells[1]), set())
            if statuses and cells[2] not in statuses:
                conflicts.append(f'{cells[1]}: backlog={cells[2]}; registry={", ".join(sorted(statuses))}')
    task('Backlog có trạng thái lệch nguồn chính', 'Dữ liệu tiến độ', PIPE / 'strategy/sprint-backlog.md',
         'Cần đối chiếu' if conflicts else 'Không thấy lệch ở từ khóa khớp chính xác',
         f'{len(conflicts)} từ khóa khớp chính xác nhưng khác trạng thái. Nguồn trạng thái bài: strategy/pages.csv (topic_status.py).',
         'Tra trạng thái bằng python scripts/topic_status.py <slug>; backlog cũ chỉ để tham khảo.',
         details='\n'.join(conflicts))

    stats = workflow_tasks(task)

    catalog = []
    for base, category in [(PIPE / 'strategy', 'SEO strategy'), (PIPE / 'links', 'Internal link'), (PIPE / 'logs', 'Log'),
                           (CONTENT / 'audits', 'Audit'), (CONTENT / '4-cms', 'CMS'),
                           (ROOT / 'knowledge/2-market', 'Thị trường & đối thủ'), (ROOT / 'knowledge/4-channels', 'Kênh khác'),
                           (ROOT / 'knowledge/5-analytics', 'Đo lường'),
                           (ROOT / 'knowledge/6-campaigns', 'Chiến dịch'), (ROOT / 'knowledge/logs', 'Log')]:
        if not base.exists():
            continue
        for path in sorted(base.rglob('*')):
            if path.is_file() and not (category == 'Chiến dịch' and (
                    path.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp') or re.search(r'/creatives/v\d+/', path.as_posix()))):
                catalog.append(dict(path=rel(path), name=path.name, group=category,
                                    archived='archive' in path.parts))
    for path in [PIPE / 'strategy/pages.csv', PIPE / 'strategy/sprint-backlog.md', OUT / 'cms.html']:
        catalog.append(dict(path=rel(path), name=path.name, group='Nội dung', archived=False))

    order = ['Bài SEO', 'Đối thủ', 'Đo lường', 'Kênh khác', 'Internal link', 'Sau publish', 'Stale', 'Content audit',
             'QA / SERP', 'Theo dõi GSC', 'Dữ liệu', 'Dữ liệu tiến độ']
    tasks.sort(key=lambda t: order.index(t['group']) if t['group'] in order else len(order))
    approvals = approval_queue()
    stats['approvals'] = sum(q['gate'].startswith('Gate') for q in approvals)
    act = activity_view()
    channels = channels_view(approvals, act)
    stats['channel_pending'] = len(channels['pending'])
    payload = dict(generated_at=datetime.now().astimezone().isoformat(timespec='seconds'),
                   snapshot=snapshot, snapshot_mode=meta.get('mode'), tasks=tasks, catalog=catalog, stats=stats,
                   activity_recent=act['events'][:50], activity_counts=act['counts'],
                   channels=[{k: c[k] for k in ('domain', 'label', 'metrics', 'd7', 'd30', 'last')} for c in channels['cards']],
                   channel_pending=channels['pending'])
    (OUT / 'status.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    # Rendered documents go into index.html only; status.json stays small.
    payload['approvals'] = approvals
    payload['today'] = today_view(approvals)
    payload['activity'] = act
    payload['channels'] = channels['cards']
    template = (ROOT / 'scripts/templates/work-dashboard.html').read_text(encoding='utf-8')
    (OUT / 'index.html').write_text(template.replace('__PAYLOAD__', json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c')), encoding='utf-8')
    print(f'Work dashboard: {len(tasks)} workstreams, {len(catalog)} files, snapshot {snapshot}')
    return payload


if __name__ == '__main__':
    import argparse
    argparse.ArgumentParser(description=__doc__).parse_args()  # --help prints usage instead of rebuilding
    build()
