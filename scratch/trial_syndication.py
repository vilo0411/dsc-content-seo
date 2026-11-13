import sys,json,csv,shutil
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import quote,urlencode
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import syndicate as s
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession

root=s.ROOT; cfg=json.loads((s.BASE/'config.json').read_text())
session=AuthorizedSession(Credentials.from_service_account_file(str(root/cfg['credentials_file']),scopes=['https://www.googleapis.com/auth/spreadsheets']))
api='https://sheets.googleapis.com/v4/spreadsheets/'+cfg['spreadsheet_id']
def call(method,url,**kw):
    r=session.request(method,url,timeout=45,**kw)
    if not r.ok: raise RuntimeError('Request failed: HTTP '+str(r.status_code))
    return r.json()
meta=call('GET',api,params={'fields':'sheets.properties'})
assert any(x['properties']['title']=='Publishing' for x in meta['sheets'])
range_url=api+'/values/'+quote("'Publishing'!A1:S1000",safe='')
before=call('GET',range_url).get('values',[])
assert before[0]==s.FIELDS
remote={}
for line in before[1:]:
    if not any(line): continue
    row=dict(zip(s.FIELDS,line+['']*(len(s.FIELDS)-len(line))))
    if not row['id'] or row['id'] in remote: raise ValueError('Invalid remote ID')
    remote[row['id']]=row
slug='con-hao-kinh-te-la-gi-cach-tao-ra-va-tam-quan-trong-cua-con-hao-kinh-te'
source='https://www.dsc.com.vn/kien-thuc/'+slug
import requests
live=requests.get(source,timeout=40)
assert live.status_code==200 and 'con h' in live.text.lower(), 'Source live verification failed'
pack=s.BASE/'packs'/slug/'v1'; pack.mkdir(parents=True,exist_ok=True)
stamp=datetime.now(timezone.utc).isoformat()
asset='https://extgw.dsc.com.vn/eback/uploads/con_hao_kinh_te_la_gi_32a2fa962f.jpg'
texts={
'x':'Con hào kinh tế là lợi thế giúp doanh nghiệp bảo vệ vị thế trước đối thủ. Khi đọc báo cáo, hãy hỏi: khách hàng có dễ chuyển sang nhà cung cấp khác không?\n\nTìm hiểu cùng DSC:',
'mastodon':'Một doanh nghiệp bán chạy chưa chắc đã có con hào kinh tế.\n\nCon hào nằm ở lợi thế có thể duy trì trước cạnh tranh, chẳng hạn chi phí chuyển đổi: khách hàng phải tốn thời gian, tiền bạc hoặc gián đoạn quy trình khi đổi nhà cung cấp.\n\nKhi phân tích, cần tìm bằng chứng lợi thế đó còn tồn tại, thay vì chỉ nhìn doanh thu một kỳ.\n\nDSC giải thích các nguồn lợi thế cạnh tranh:',
'wakelet':'Con hào kinh tế: đọc lợi thế cạnh tranh của doanh nghiệp\n\nTài nguyên dành cho người đang học phân tích doanh nghiệp. Bài viết của Chứng khoán DSC giải thích con hào kinh tế và các nguồn hình thành lợi thế cạnh tranh.\n\nGợi ý khi đọc:\n• Phân biệt sức hút của sản phẩm trong một giai đoạn với lợi thế có thể duy trì.\n• Xem khách hàng phải đánh đổi gì nếu chuyển sang nhà cung cấp khác.\n• Đối chiếu lập luận với kết quả kinh doanh qua nhiều kỳ.\n\nThêm vào bộ sưu tập “Kiến thức phân tích doanh nghiệp”. Đọc bài gốc:'}
local=s.read(s.BASE/'ledger.csv')
for channel,text in texts.items():
    ident=slug+'-'+channel+'-v1'
    if ident in local or ident in remote: raise ValueError('Trial already exists; refusing overwrite')
    url=source
    content=text+'\n'+url
    if channel=='x': assert len(text)+1+23<=280
    if channel=='mastodon': assert len(text)+1+23<=500
    row={k:'' for k in s.FIELDS}; row.update(id=ident,slug=slug,source_url=source,channel=channel,format='curation' if channel=='wakelet' else 'short-post',version='v1',content=content,asset_path=asset if channel=='wakelet' else '',target_url=source,utm_url='',anchor='Đọc bài gốc tại Chứng khoán DSC',status='Draft',notes='Chờ duyệt; chưa đăng. Live source HTTP 200 verified '+stamp,index_status='Unknown')
    local[ident]=row
    (pack/(channel+'.md')).write_text(content,encoding='utf-8')
base=json.loads((s.BASE/'sync-baseline.json').read_text())
merged,conflicts=s.merge(base,local,remote)
assert not conflicts, 'Sync conflict; no writes applied'
assert call('GET',range_url).get('values',[])==before, 'Remote changed; retry required'
patch=[]
positions={line[0]:i+2 for i,line in enumerate(before[1:]) if line and line[0]}
nextrow=len(before)+1
for ident,row in merged.items():
    if remote.get(ident)==row: continue
    if ident in positions: n=positions[ident]
    else: n=nextrow;nextrow+=1
    patch.append({'range':f"'Publishing'!A{n}:S{n}",'values':[[row[k] for k in s.FIELDS]]})
if patch: call('POST',api+'/values:batchUpdate',json={'valueInputOption':'RAW','data':patch})
after=call('GET',range_url).get('values',[])
verified={line[0]:dict(zip(s.FIELDS,line+['']*(len(s.FIELDS)-len(line)))) for line in after[1:] if line and line[0]}
assert verified==merged,'Readback mismatch; baseline not advanced'
shutil.copy2(s.BASE/'ledger.csv',pack/'ledger-before.csv')
s.write(s.BASE/'ledger.csv',merged)
(s.BASE/'sync-baseline.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2),encoding='utf-8')
(pack/'README.md').write_text('# Gói thử: Con hào kinh tế\n\nTrạng thái: Draft — cần duyệt trước đăng.\n\nNguồn live: '+source+'\n\nHTTP 200 xác minh '+stamp+'. Không xác nhận index. Không dùng các nhận định về mã cổ phiếu hoặc giá thị trường. Ảnh là ảnh gốc hiện có, tùy chọn cho Wakelet; X/Mastodon dùng bài chữ.\n\n```mermaid\nflowchart TD\n X[X] --> D[Bài gốc DSC]\n M[Mastodon] --> D\n W[Wakelet] --> D\n```\n\nĐăng tay sau duyệt, nhập URL thực tế vào Publishing; kiểm tra ở ngày 7/14/28 tính từ ngày đăng.\n',encoding='utf-8')
call('POST',api+'/values/'+quote("'Sync Log'!A:C",safe='')+':append',params={'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS'},json={'values':[[stamp,'Success','Trial: 3 Draft variants; local and remote readback equal']]})
s.dashboard()
print('Source live verified. Created 3 Draft variants; synced and read back successfully. No social posts published.')
