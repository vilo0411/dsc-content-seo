import csv,json,sys,shutil
from pathlib import Path
from urllib.parse import quote
from datetime import datetime,timezone,timedelta
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import syndicate as s
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
cfg=json.loads((s.BASE/'config.json').read_text(encoding='utf-8'))
session=AuthorizedSession(Credentials.from_service_account_file(str(s.ROOT/cfg['credentials_file']),scopes=['https://www.googleapis.com/auth/spreadsheets']))
api='https://sheets.googleapis.com/v4/spreadsheets/'+cfg['spreadsheet_id']
def call(method,url,**kw):
    r=session.request(method,url,timeout=40,**kw)
    if not r.ok:raise RuntimeError(f'Sheets HTTP {r.status_code}')
    return r.json()
call('GET',api,params={'fields':'sheets.properties'})
def fetch(tab,area):
    return call('GET',api+'/values/'+quote(f"'{tab}'!{area}",safe=''),params={'valueRenderOption':'UNFORMATTED_VALUE','dateTimeRenderOption':'SERIAL_NUMBER'}).get('values',[])
before=fetch('Publishing','A1:X1000');assert before[0]==s.FIELDS
remote={}
for line in before[1:]:
    if not any(line):continue
    r=s.from_sheet_row(before[0],line);assert r['id'] not in remote;remote[r['id']]=r
local=s.read(s.BASE/'ledger.csv');baseline=json.loads((s.BASE/'sync-baseline.json').read_text(encoding='utf-8'))
rows,conflicts=s.merge(baseline,local,remote);assert not conflicts
original='https://extgw.dsc.com.vn/eback/uploads/con_hao_kinh_te_la_gi_32a2fa962f.jpg'
import requests
image=requests.get(original,timeout=30);assert image.ok and image.headers.get('content-type','').startswith('image/')
new_image={'pinterest','pixbender'}
positions={line[0]:i+2 for i,line in enumerate(before[1:]) if line and line[0]}
patch=[]
for key,row in rows.items():
    needed=row['channel'] in new_image
    row['asset_path']='' if needed else original
    row['asset_url']=row['asset_path']
    notes=[line for line in row['notes'].splitlines() if not any(term in line for term in ['Ảnh bắt buộc:','Ảnh tùy chọn: để trống','Ảnh đang chờ thiết kế','Ảnh trong asset_url','Ảnh gốc là ảnh ngang','chưa sẵn sàng đăng khi chưa có ảnh','Tải ảnh từ asset_url.'])]
    notes.append('ẢNH MỚI: chờ thiết kế/duyệt/upload; asset_path và asset_url để trống. Chưa sẵn sàng đăng định dạng ảnh.' if needed else 'DÙNG ẢNH DSC CÓ SẴN: asset_path và asset_url là URL ảnh gốc online. Không yêu cầu thiết kế mới; có thể dùng cùng ảnh này làm ảnh kèm/ảnh bìa.')
    row['notes']='\n'.join(notes)
    for col,field in [('H','asset_path'),('V','asset_url'),('P','notes')]:
        if row[field]!=remote[key][field]:patch.append({'range':f"'Publishing'!{col}{positions[key]}",'values':[[row[field]]]})
formats_before=fetch('Formats','A1:I100')
format_updates=[]
for i,line in enumerate(formats_before[1:],start=2):
    channel=line[1].lower().replace(' ','-')
    label='Cần tạo ảnh mới; chờ duyệt; để trống asset_path/asset_url' if channel in new_image else 'Dùng ảnh gốc DSC online có sẵn; không cần tạo mới'
    if len(line)>6 and line[6]!=label:format_updates.append({'range':f"'Formats'!G{i}",'values':[[label]]})
assert fetch('Publishing','A1:X1000')==before and fetch('Formats','A1:I100')==formats_before,'Remote changed'
call('POST',api+'/values:batchUpdate',json={'valueInputOption':'RAW','data':patch+format_updates})
readback=fetch('Publishing','A1:X1000')
verified={r['id']:r for r in [s.from_sheet_row(readback[0],line) for line in readback[1:] if line and line[0]]}
assert verified==rows
shutil.copy2(s.BASE/'ledger.csv',s.BASE/'assets/ledger-before-selective-images.csv')
s.write(s.BASE/'ledger.csv',rows)
(s.BASE/'sync-baseline.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (s.BASE/'formats.csv').open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f).writerows(fetch('Formats','A1:I100'))
with (s.BASE/'image-plan.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['channel','image_mode','asset_url'])
    for row in rows.values():w.writerow([row['channel'],'create-new-pending' if row['channel'] in new_image else 'reuse-dsc',row['asset_url']])
today=datetime.now(timezone(timedelta(hours=7))).date().isoformat()
call('POST',api+'/values/'+quote("'Sync Log'!A:C",safe='')+':append',params={'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS'},json={'values':[[s.date_to_serial(today),'Success','Image policy: 9 channels reuse verified DSC source image; Pinterest/Pixbender pending new designs with blank asset fields.']]})
s.dashboard()
print('Verified: 9 DSC source-image references; 2 pending new-image rows blank. Content and dates preserved.')
