"""Local syndication ledger and three-way merge for agent-mediated Sheets sync."""
import argparse, csv, html, json
from pathlib import Path
from datetime import date, datetime, timedelta

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'knowledge/operations/syndication'
FIELDS = ['id','slug','source_url','channel','format','version','content','asset_path','target_url','utm_url','anchor','status','posted_url','posted_at','minutes','notes','index_status','checked_at','evidence','channel_url','compose_url','asset_url','title','hashtags']
DATE_FIELDS = {'posted_at', 'checked_at'}

def date_to_serial(value):
    """Store actual Sheets date values; keep blank dates empty."""
    if value in ('', None): return ''
    if isinstance(value, (int, float)): return value
    return (date.fromisoformat(str(value)[:10]) - date(1899, 12, 30)).days

def date_from_serial(value):
    if value in ('', None): return ''
    if isinstance(value, (int, float)):
        return (date(1899, 12, 30) + timedelta(days=int(value))).isoformat()
    return str(value)

def sheet_row(row):
    return [date_to_serial(row.get(k,'')) if k in DATE_FIELDS else row.get(k,'') for k in FIELDS]

def from_sheet_row(headers, values):
    row = {k:'' for k in FIELDS}
    row.update(dict(zip(headers,values)))
    for k in DATE_FIELDS: row[k] = date_from_serial(row[k])
    return row

def read(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    ids = [r['id'] for r in rows]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError('Missing or duplicate ID')
    return {r['id']: r for r in rows}

def merge(base, local, remote):
    result, conflicts = {}, []
    for key in sorted(local.keys() | remote.keys()):
        row = {}
        for field in FIELDS:
            b = base.get(key, {}).get(field, '')
            l = local.get(key, {}).get(field, b)
            r = remote.get(key, {}).get(field, b)
            if l != r and l != b and r != b:
                conflicts.append(dict(id=key, field=field, base=b, local=l, remote=r))
            row[field] = r if l == b else l
        result[key] = row
    return result, conflicts

def write(path, rows):
    with Path(path).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader(); w.writerows(rows.values())

def dashboard():
    rows = read(BASE / 'ledger.csv')
    sheet_id = html.escape(json.loads((BASE/'config.json').read_text(encoding='utf-8'))['spreadsheet_id'], quote=True)
    def cell(k, value):
        safe=html.escape(value, quote=True)
        if k in {'channel_url','compose_url','asset_url','source_url','posted_url'} and value.startswith('https://'):
            return '<td><a href="'+safe+'" target="_blank" rel="noopener noreferrer">'+safe+'</a></td>'
        return '<td>'+safe+'</td>'
    body = ''.join('<tr>' + ''.join(cell(k,r.get(k,'')) for k in FIELDS if k != 'utm_url')+'</tr>' for r in rows.values())
    (BASE/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>DSC Syndication</title><style>body{font:14px system-ui;margin:24px}table{border-collapse:collapse}td,th{padding:8px;border:1px solid #ddd;max-width:360px;white-space:pre-wrap}th{background:#153d59;color:white;position:sticky;top:0}</style><h1>DSC Syndication</h1><p>Edit ledger.csv or Google Sheets; sync through agent. Index status requires evidence.</p><a href="https://docs.google.com/spreadsheets/d/'+sheet_id+'/edit">Open Google Sheets</a><table><thead><tr>'+''.join('<th>'+k+'</th>' for k in FIELDS if k != 'utm_url')+'</tr></thead><tbody>'+body+'</tbody></table>',encoding='utf-8')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('build')
    m=sub.add_parser('merge'); m.add_argument('remote',type=Path)
    c=sub.add_parser('checkpoint'); c.add_argument('verified_remote',type=Path)
    args=p.parse_args()
    baseline=BASE/'sync-baseline.json'
    if args.command=='build': dashboard(); return
    local=read(BASE/'ledger.csv')
    remote=read(args.remote if args.command=='merge' else args.verified_remote)
    if args.command=='checkpoint':
        if local != remote: raise ValueError('Remote readback differs; checkpoint refused')
        baseline.write_text(json.dumps(local,ensure_ascii=False,indent=2),encoding='utf-8'); return
    base=json.loads(baseline.read_text(encoding='utf-8')) if baseline.exists() else {}
    merged, conflicts=merge(base,local,remote)
    (BASE/'conflicts.json').write_text(json.dumps(conflicts,ensure_ascii=False,indent=2),encoding='utf-8')
    write(BASE/'sync-proposal.csv',merged)
    print(f'Proposal only: {len(merged)} records; {len(conflicts)} conflicts. Source ledger unchanged.')

if __name__=='__main__': main()
