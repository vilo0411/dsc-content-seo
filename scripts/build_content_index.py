"""Build the local searchable catalog of CMS exports and audit artifacts."""
from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[1] / 'knowledge/4-content'


def build():
    rows = []
    for folder, kind in [('4-cms', 'CMS'), ('audits', 'Audit')]:
        for path in sorted((BASE / folder).rglob('*')):
            if not path.is_file() or path.name == 'README.md':
                continue
            relative = path.relative_to(BASE).as_posix()
            rows.append({'kind': kind, 'name': path.name,
                         'path': relative, 'href': relative,
                         'group': path.parent.relative_to(BASE).as_posix()})
    data = json.dumps(rows, ensure_ascii=False).replace('<', '\\u003c')
    page = '''<!doctype html><html lang="vi"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tra cứu HTML CMS và audit</title>
<style>body{font:16px system-ui;max-width:1200px;margin:40px auto;padding:0 20px;color:#172b4d}input,select{font:inherit;padding:10px;margin:0 8px 16px 0}input{width:min(600px,80%)}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:12px;border-bottom:1px solid #ddd;overflow-wrap:anywhere}a{color:#0758ab}small{color:#526278}tr[hidden]{display:none}</style>
<h1>Tra cứu HTML CMS và audit</h1>
<p><a href="../operations/index.html">Bảng điều hành: internal link, stale, audit và tiến độ</a></p>
<p><b>CMS:</b> HTML thân bài để dán vào CMS. <b>Audit:</b> báo cáo, bản xem trước, so sánh và dữ liệu kiểm tra.</p>
<input id="query" type="search" aria-label="Tìm tài liệu" placeholder="Tìm slug, tên file, đợt audit…">
<select id="kind" aria-label="Loại tài liệu"><option value="">Tất cả</option><option>CMS</option><option>Audit</option></select>
<p id="count" aria-live="polite"></p><table><thead><tr><th>Loại</th><th>Tài liệu</th><th>Thư mục / phiên bản</th></tr></thead><tbody id="rows"></tbody></table>
<script>
const data=DATA;
const normalize=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/đ/g,'d').toLowerCase();
const tbody=document.getElementById('rows'),query=document.getElementById('query'),kind=document.getElementById('kind');
function render(){
 tbody.replaceChildren();
 const terms=normalize(query.value).split(/\\s+/).filter(Boolean);
 const matches=data.filter(r=>(!kind.value||r.kind===kind.value)&&terms.every(t=>normalize(r.path).includes(t)));
 for(const r of matches){const tr=document.createElement('tr');
 const type=document.createElement('td');type.textContent=r.kind;
 const name=document.createElement('td'),a=document.createElement('a');a.href=r.href;a.textContent=r.name;name.append(a);
 const group=document.createElement('td');group.textContent=r.group;tr.append(type,name,group);tbody.append(tr);}
 document.getElementById('count').textContent=matches.length+' / '+data.length+' tài liệu';
}
query.addEventListener('input',render);kind.addEventListener('change',render);render();
</script></html>'''.replace('DATA', data)
    (BASE / 'index.html').write_text(page, encoding='utf-8')
    print(f'Indexed {len(rows)} artifacts: {BASE / "index.html"}')
    from build_work_dashboard import build as build_dashboard
    build_dashboard()
    return rows


if __name__ == '__main__':
    build()
