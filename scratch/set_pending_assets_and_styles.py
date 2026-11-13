import sys,json,shutil,csv
from pathlib import Path
from datetime import datetime,timezone,timedelta
from urllib.parse import quote
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import syndicate as s
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
cfg=json.loads((s.BASE/'config.json').read_text(encoding='utf-8'))
session=AuthorizedSession(Credentials.from_service_account_file(str(s.ROOT/cfg['credentials_file']),scopes=['https://www.googleapis.com/auth/spreadsheets']))
api='https://sheets.googleapis.com/v4/spreadsheets/'+cfg['spreadsheet_id']
def call(method,url,**kw):
    r=session.request(method,url,timeout=40,**kw)
    if not r.ok:raise RuntimeError(f'HTTP {r.status_code}')
    return r.json()
meta=call('GET',api,params={'fields':'sheets.properties'})
tabs={t['properties']['title']:t['properties'] for t in meta['sheets']}
def fetch(name,area):
    return call('GET',api+'/values/'+quote("'"+name+"'!"+area,safe=''),params={'valueRenderOption':'UNFORMATTED_VALUE','dateTimeRenderOption':'SERIAL_NUMBER'}).get('values',[])
before=fetch('Publishing','A1:X1000');assert before[0]==s.FIELDS
remote={}
for line in before[1:]:
    if not any(line):continue
    row=s.from_sheet_row(before[0],line);assert row['id'] and row['id'] not in remote;remote[row['id']]=row
local=s.read(s.BASE/'ledger.csv');baseline=json.loads((s.BASE/'sync-baseline.json').read_text(encoding='utf-8'))
merged,conflicts=s.merge(baseline,local,remote);assert not conflicts
style_for={'pinterest':'S02','pixbender':'S02','linkedin':'S01 hoặc S03','band':'S01','x':'S01','mastodon':'S01','wakelet':'S03','telegraph':'S02','ameblo':'S03','medium':'S02','google-sites':'S03'}
for row in merged.values():
    row['asset_path']='';row['asset_url']=''
    lines=[line for line in row['notes'].splitlines() if not any(term in line for term in ['Ảnh trong asset_url','Ảnh gốc là ảnh ngang tham khảo','Ảnh trên Drive;'])]
    required=row['channel'] in {'pinterest','pixbender'}
    lines.append(('Ảnh bắt buộc: chờ chọn style, tạo và duyệt ảnh.' if required else 'Ảnh tùy chọn: để trống; có thể triển khai bài chữ nếu kênh hỗ trợ.')+' Mẫu đề xuất: '+style_for.get(row['channel'],'S01')+'. Chưa có asset online đã duyệt; không dùng ảnh thay thế. Xem tab Visual Styles.')
    row['notes']='\n'.join(lines)
style_headers=['style_id','name','content_job','composition','palette','typography','proposed_sizes','best_channels','moat_example','production_status']
styles=[
['S01','Luận điểm lớn','Nêu một ý hoặc hiểu lầm','Navy; chữ lớn lệch trái; nhấn một cụm xanh; một điểm tựa hình học','Navy #0D1B2A / xanh #2BE841 / trắng','3 cấp chữ; tiêu đề 8–14 từ, tối đa 3 dòng','1080×1350 hoặc 1080×1080','LinkedIn / BAND / X / Mastodon','Lợi nhuận cao chưa đủ chứng minh con hào','Bản bố cục local; chưa duyệt, chưa tạo asset đăng'],
['S02','Sơ đồ giải thích','Làm rõ một cơ chế','Một tâm điểm, 2–3 nhánh có nghĩa; nhãn ngắn; đường dẫn rõ','Mint #E8F8F2 / navy / xanh #00AD14','Tên cơ chế lớn; nhãn nhánh ngắn; chú thích nhỏ','1000×1500 bản dọc; 1200×900 bản ngang','Pinterest / Pixbender nếu hỗ trợ / bài dài','Chi phí chuyển đổi: dữ liệu, nhân sự, vận hành','Bản bố cục local; bản dọc chưa xuất, chưa tạo asset đăng'],
['S03','Đối chiếu bằng chứng','So sánh nhận định và câu hỏi kiểm chứng','Hai cột đối xứng; 3–4 hàng; một dải nhấn; không xếp 5 ô giống nhau','Trắng hoặc ngà / navy / xanh #00AD14','Tiêu đề lớn; tên cột rõ; nội dung hai cột cùng cấp','1080×1350 hoặc 1080×1080','LinkedIn / bài dài / tài nguyên','Dấu hiệu ban đầu / bằng chứng cần tìm','Bản bố cục local; chưa duyệt, chưa tạo asset đăng'],
['S04','Chuỗi câu hỏi','Giải thích theo nhiều bước','5 slide: bìa, cơ chế, bằng chứng, phản biện, nguồn; thay bố cục theo ý','Navy hoặc trắng; nhấn xanh; nhận diện thống nhất','Mỗi slide một luận điểm; số trang và tiến trình nhỏ','Bộ 5 ảnh 1080×1350','Chỉ kênh hỗ trợ bộ ảnh/carousel; xác minh tài khoản trước','Khách hàng ở lại vì điều gì?','Mới có bố cục slide bìa; chưa sản xuất đủ bộ']]
assert fetch('Publishing','A1:X1000')==before,'Remote changed'
positions={line[0]:i+2 for i,line in enumerate(before[1:]) if line and line[0]}
updates=[]
for key,row in merged.items():
    n=positions[key]
    for column,field in [('H','asset_path'),('V','asset_url'),('P','notes')]:
        if remote[key][field]!=row[field]:updates.append({'range':f"'Publishing'!{column}{n}",'values':[[row[field]]]})
if updates:call('POST',api+'/values:batchUpdate',json={'valueInputOption':'RAW','data':updates})
if 'Visual Styles' not in tabs:
    added=call('POST',api+':batchUpdate',json={'requests':[{'addSheet':{'properties':{'title':'Visual Styles','gridProperties':{'rowCount':100,'columnCount':12,'frozenRowCount':1}}}}]})
    tabs['Visual Styles']=added['replies'][0]['addSheet']['properties']
existing=fetch('Visual Styles','A1:J10');assert not existing or existing[0]==style_headers
call('PUT',api+'/values/'+quote("'Visual Styles'!A1:J5",safe=''),params={'valueInputOption':'RAW'},json={'values':[style_headers]+styles})
sid=tabs['Visual Styles']['sheetId']
call('POST',api+':batchUpdate',json={'requests':[
{'repeatCell':{'range':{'sheetId':sid,'startRowIndex':0,'endRowIndex':5,'startColumnIndex':0,'endColumnIndex':10},'cell':{'userEnteredFormat':{'wrapStrategy':'WRAP','verticalAlignment':'TOP'}},'fields':'userEnteredFormat.wrapStrategy,userEnteredFormat.verticalAlignment'}},
{'repeatCell':{'range':{'sheetId':sid,'startRowIndex':0,'endRowIndex':1,'startColumnIndex':0,'endColumnIndex':10},'cell':{'userEnteredFormat':{'backgroundColor':{'red':.05,'green':.11,'blue':.16},'textFormat':{'bold':True,'foregroundColor':{'red':1,'green':1,'blue':1}}}},'fields':'userEnteredFormat'}},
{'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'COLUMNS','startIndex':0,'endIndex':10},'properties':{'pixelSize':240},'fields':'pixelSize'}}]})
check=fetch('Publishing','A1:X1000')
verified={r['id']:r for r in [s.from_sheet_row(check[0],line) for line in check[1:] if line and line[0]]}
assert verified==merged and all(not r['asset_path'] and not r['asset_url'] for r in verified.values())
assert fetch('Visual Styles','A1:J5')==[style_headers]+styles
backup=s.BASE/'assets/ledger-before-pending-assets.csv';shutil.copy2(s.BASE/'ledger.csv',backup)
s.write(s.BASE/'ledger.csv',merged)
(s.BASE/'sync-baseline.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2),encoding='utf-8')
cfg['tabs']['Visual Styles']=sid
(s.BASE/'config.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
with (s.BASE/'visual-styles.csv').open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f).writerows([style_headers]+styles)
now=datetime.now(timezone(timedelta(hours=7))).date().isoformat()
call('POST',api+'/values/'+quote("'Sync Log'!A:C",safe='')+':append',params={'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS'},json={'values':[[s.date_to_serial(now),'Success','Blanked pending asset fields, removed fallback images; added 4 Visual Styles. No image generated or uploaded.']]})
s.dashboard()
print('Verified blank asset fields for '+str(len(merged))+' rows. Visual Styles gid: '+str(sid))
