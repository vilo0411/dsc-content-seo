"""Build the SEO work dashboard from local evidence; no network or source-status writes.

Usage: python scripts/build_work_dashboard.py
"""
from __future__ import annotations

import contextlib
import csv
from datetime import datetime
import html
import io
import json
from pathlib import Path
import re
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'knowledge/operations'
PIPE = ROOT / 'knowledge/3-pipeline'
CONTENT = ROOT / 'knowledge/4-content'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def rel(path):
    return path.relative_to(ROOT).as_posix()


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
    for spec in sorted((PIPE / 'internal-links/plans').glob('*.json')):
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

    task('Content audit: xóa / sửa / gộp', 'Content audit', PIPE / 'content-audit-2026-11-05-tracker.html',
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
    ledger = PIPE / 'publish-ledger.csv'
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
    for line in (CONTENT / 'topic-clusters.md').read_text(encoding='utf-8').splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if line.startswith('|') and len(cells) >= 4 and '/kien-thuc/' in cells[0]:
            primary.setdefault(normalize(cells[1]), set()).add(cells[-1])
    conflicts = []
    for line in (CONTENT / 'sprint-backlog.md').read_text(encoding='utf-8').splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if line.startswith('|') and len(cells) >= 3:
            statuses = primary.get(normalize(cells[1]), set())
            if statuses and cells[2] not in statuses:
                conflicts.append(f'{cells[1]}: backlog={cells[2]}; topic-clusters={", ".join(sorted(statuses))}')
    task('Backlog có trạng thái lệch nguồn chính', 'Dữ liệu tiến độ', CONTENT / 'sprint-backlog.md',
         'Cần đối chiếu' if conflicts else 'Không thấy lệch ở từ khóa khớp chính xác',
         f'{len(conflicts)} từ khóa khớp chính xác nhưng khác trạng thái. Nguồn trạng thái bài: topic-clusters.md.',
         'Tra trạng thái bằng python scripts/topic_status.py <slug>; backlog cũ chỉ để tham khảo.',
         details='\n'.join(conflicts))

    catalog = []
    for base, category in [(PIPE, 'Pipeline'), (CONTENT / 'audits', 'Audit'), (CONTENT / '4-cms', 'CMS')]:
        for path in sorted(base.rglob('*')):
            if path.is_file():
                catalog.append(dict(path=rel(path), name=path.name, group=category,
                                    archived='archive' in path.parts))
    for path in [CONTENT / 'topic-clusters.md', CONTENT / 'sprint-backlog.md', CONTENT / 'index.html']:
        catalog.append(dict(path=rel(path), name=path.name, group='Nội dung', archived=False))

    payload = dict(generated_at=datetime.now().astimezone().isoformat(timespec='seconds'),
                   snapshot=snapshot, snapshot_mode=meta.get('mode'), tasks=tasks, catalog=catalog)
    (OUT / 'status.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    template = (ROOT / 'scripts/templates/work-dashboard.html').read_text(encoding='utf-8')
    (OUT / 'index.html').write_text(template.replace('__PAYLOAD__', json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c')), encoding='utf-8')
    print(f'Work dashboard: {len(tasks)} workstreams, {len(catalog)} files, snapshot {snapshot}')
    return payload


if __name__ == '__main__':
    build()
