import sys,json,csv,html,re,shutil
from pathlib import Path
from datetime import datetime,date,timezone,timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import syndicate as s
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
cfg=json.loads((s.BASE/'config.json').read_text(encoding='utf-8'))
session=AuthorizedSession(Credentials.from_service_account_file(str(s.ROOT/cfg['credentials_file']),scopes=['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']))
api='https://sheets.googleapis.com/v4/spreadsheets/'+cfg['spreadsheet_id']
def call(method,url,**kw):
    r=session.request(method,url,timeout=45,**kw)
    if not r.ok:raise RuntimeError(str(r.status_code)+': '+r.json().get('error',{}).get('message','Failed'))
    return r.json()
meta=call('GET',api,params={'fields':'sheets.properties,properties'})
tabs={t['properties']['title']:t['properties'] for t in meta['sheets']}
def fetch(name,area='A1:X1000'):
    return call('GET',api+'/values/'+quote("'"+name+"'!"+area,safe=''),params={'valueRenderOption':'UNFORMATTED_VALUE','dateTimeRenderOption':'SERIAL_NUMBER'}).get('values',[])
before=fetch('Publishing');oldhead=before[0]
assert oldhead in (s.FIELDS,s.FIELDS[:22])
def decode(data):
    out={}
    for line in data[1:]:
        if not any(line):continue
        r=s.from_sheet_row(data[0],line)
        assert r['id'] and r['id'] not in out
        out[r['id']]=r
    return out
remote=decode(before);local=s.read(s.BASE/'ledger.csv')
base=json.loads((s.BASE/'sync-baseline.json').read_text(encoding='utf-8'))
rows,conflicts=s.merge(base,local,remote);assert not conflicts,'Resolve sync conflicts first'
payload=json.loads((s.ROOT/'scratch/moat_channel_content.json').read_text(encoding='utf-8'))
heading_map={
'telegraph':['Lợi thế phải có cơ chế cụ thể','Đối chiếu câu chuyện với dữ liệu','Theo dõi điều có thể làm lợi thế mất đi'],
'ameblo':['1. Khách hàng chọn doanh nghiệp vì điều gì?','2. Điều gì khiến khách hàng khó rời đi?','3. Kết quả kinh doanh có phù hợp với lập luận không?'],
'medium':['Chi phí ngoài bảng giá','Từ mô tả đến bằng chứng','Lợi thế có thể suy giảm'],
'google-sites':['Nội dung nên đọc','Cách sử dụng checklist']}
tags={'x':'#ConHaoKinhTe #DSC','mastodon':'#ConHaoKinhTe #DauTuGiaTri #DSC','band':'#ConHaoKinhTe #PhanTichDoanhNghiep #DSC','pinterest':'#ConHaoKinhTe #KienThucChungKhoan #DSC','pixbender':'#ConHaoKinhTe #Infographic #DSC','linkedin':'#ConHaoKinhTe #PhanTichDoanhNghiep #DSC'}
formats=[
['short-post','X','Một ý chính','Câu mở → một luận điểm → link nguồn → 1–2 hashtag','Không H1/H2 trong caption','Đề xuất 180–250 ký tự kể cả hashtag; URL được rút gọn theo nền tảng','Ảnh tùy chọn','1–2 hashtag, không nhồi từ khóa','Dán content vào compose; kiểm tra bộ đếm trước đăng'],
['short-post','Mastodon','Một luận điểm có ngữ cảnh','Mở vấn đề → giải thích ngắn → link → hashtag','Đoạn ngắn, không heading kiểu Markdown','Bản thử dưới 500 ký tự theo cách tính URL rút gọn; kiểm tra giao diện thực tế','Ảnh tùy chọn, thêm alt text khi dùng','2–3 hashtag','Dán content, không dán tiêu đề riêng nếu đã có câu mở'],
['community-discussion','BAND','Thảo luận cộng đồng','Tình huống → giải thích → câu hỏi thảo luận → nguồn','Tiêu đề ở title nếu editor hỗ trợ; thân bài ngắt đoạn','Đề xuất 150–250 từ','Ảnh checklist tùy chọn','2–3 hashtag nếu cộng đồng cho phép','Không ép đăng nếu cộng đồng không nhận quảng bá'],
['image-pin','Pinterest','Ảnh lưu tham khảo','Title → Description → Link → Alt text','Title riêng; mô tả súc tích','Title khoảng 40–70 ký tự; mô tả khoảng 250–450 ký tự là mục tiêu biên tập','Ảnh dọc 2:3; alt text diễn giải nội dung','Tối đa 3 hashtag liên quan; không thay thế mô tả tự nhiên','Dán target_url vào Link; hashtag trong Description; dùng ảnh đã upload đúng tài khoản'],
['resource-curation','Wakelet','Tuyển chọn nguồn','Tên bộ sưu tập → nguồn → vì sao nên đọc → cách dùng','Tiêu đề tài nguyên; bullet chỉ dẫn','Đề xuất 100–180 từ','Ảnh bìa tùy chọn','Dùng nhãn chủ đề thay hashtag rời','Thêm URL nguồn làm item; dán mô tả vào description'],
['explain-article','Telegraph','Bài giải thích','Title → mở bài → 3 H2 → kết luận → nguồn','Title dùng ô tiêu đề; H2 dùng Heading trong editor, H3 khi cần','Đề xuất 350–600 từ','Ảnh đầu bài hoặc sau đoạn mở','Không thêm hashtag kiểu social','Markdown ## trong Sheet biểu thị H2; đặt lại kiểu Heading nếu dán plain text; kiểm tra link trước publish'],
['learning-article','Ameblo','Bài học theo câu hỏi','Title → mở bài → 3 H2 câu hỏi → kết luận → nguồn','H2 cho câu hỏi, H3 chỉ khi có nhánh phụ','Đề xuất 350–600 từ','Ảnh đầu bài tùy chọn','Có thể dùng tag của nền tảng; không nhồi hashtag vào thân bài','Bản HTML local giữ h1/h2; nếu paste plain text cần định dạng lại Heading'],
['image-caption','Pixbender','Caption gắn ảnh','Title → điều ảnh thể hiện → nguồn → hashtag','Tiêu đề riêng nếu có; caption ngắn','Đề xuất 80–150 từ','Ảnh là nội dung chính; alt text nếu hỗ trợ','2–3 hashtag','Chưa xác minh composer/khả năng caption; kiểm tra tài khoản trước đăng'],
['resource-hub','Google Sites','Trang tài nguyên','Title → giới thiệu → H2 tài nguyên → H2 cách dùng → CTA','Title trang + H2 cho các nhóm; tránh sao chép nguyên bài','Đề xuất 150–300 từ','Ảnh minh họa + nút mở nguồn','Không dùng hashtag','Chọn site có quyền, tạo trang con; đặt Heading trong editor; không dán ## như ký tự thường'],
['professional-post','LinkedIn','Góc nhìn chuyên môn','Câu mở → luận điểm → ví dụ → bullet kiểm chứng → nguồn → hashtag','Không Heading HTML trong bài post ngắn; phân đoạn rõ','Đề xuất 180–300 từ','Infographic tùy chọn','2–3 hashtag','Tài khoản chưa cung cấp; mở feed và chọn đúng profile/Page'],
['analysis-article','Medium','Phân tích một góc hẹp','Title → mở bài → 3 H2 → kết luận → nguồn','Title ô riêng, H2 cho ba phần, H3 khi thật sự cần','Đề xuất 400–700 từ','Ảnh đầu bài tùy chọn','Tag của Medium điền khi publish; không dùng hashtag trong thân bài','Dán title riêng; dùng Heading của Medium cho các dòng ##; không gắn canonical mặc định cho bài chuyển thể khác nội dung']]
by_channel={r[1].lower():r[0] for r in formats};by_channel['google-sites']='resource-hub'
online='https://extgw.dsc.com.vn/eback/uploads/con_hao_kinh_te_la_gi_32a2fa962f.jpg'
pack=s.BASE/'packs'/next(iter(rows.values()))['slug']/'all-channels-v3';pack.mkdir(parents=True,exist_ok=True)
def rich_content(content):
    blocks=[]
    for block in content.split('\n\n'):
        if block.startswith('## '):blocks.append('<h2>'+html.escape(block[3:])+'</h2>')
        elif block.startswith('# '):blocks.append('<h1>'+html.escape(block[2:])+'</h1>')
        else:blocks.append('<p>'+html.escape(block).replace('\n','<br>')+'</p>')
    return '\n'.join(blocks)
for key,row in rows.items():
    ch=row['channel']
    if ch not in payload or row['status']!='Draft':continue
    # Preserve current wording and user edits; add structure rather than regenerating body.
    text=row['content']
    for heading in heading_map.get(ch,[]):
        text=re.sub(r'(?m)^(?:## )?'+re.escape(heading)+r'$', '## '+heading,text)
    title=payload[ch]['title']
    if ch in heading_map and not text.startswith('# '):text='# '+title+'\n\n'+text
    if ch=='x':text='Khách hàng có dễ đổi nhà cung cấp? Chi phí chuyển đổi là một nguồn tạo con hào kinh tế. Tìm hiểu cùng DSC:\n'+row['source_url']
    hashtag=tags.get(ch,'')
    if hashtag and hashtag not in text:text+='\n\n'+hashtag
    if ch in {'x','mastodon'}:
        weighted=len(text)-len(row['source_url'])+23
        assert weighted<=({'x':280,'mastodon':500}[ch]),f'{ch}: {weighted}'
    row.update(content=text,title=title,hashtags=hashtag,format=by_channel.get(ch,row['format']),asset_path=online,asset_url=online)
    row['notes']=re.sub(r'Ảnh trên Drive; đang chờ quyền chuyển vào folder đích\.?','',row['notes'])
    row['notes']+='\nẢnh trong asset_url là ảnh gốc DSC online. Infographic mới chưa upload được đúng tài khoản do storageQuotaExceeded; không dùng bản lưu ở dscnews8386.\n'+next(f[-1] for f in formats if f[1].lower().replace(' ','-')==ch)
    if ch=='pinterest':row['notes']+='\nẢnh gốc là ảnh ngang tham khảo; bản dọc 2:3 hiện chỉ có local, chờ phương án Drive phù hợp trước đăng.'
    (pack/(ch+'.md')).write_text(text,encoding='utf-8')
    (pack/(ch+'.html')).write_text('<!doctype html><meta charset="utf-8">'+rich_content(text),encoding='utf-8')
assert fetch('Publishing')==before,'Remote changed; retry'
patch=[]
if oldhead!=s.FIELDS:patch.append({'range':"'Publishing'!W1:X1",'values':[s.FIELDS[22:]]})
positions={line[0]:i+2 for i,line in enumerate(before[1:]) if line and line[0]}
for key,row in rows.items():
    assert key in positions,'Unexpected new record'
    if row!=remote.get(key):patch.append({'range':f"'Publishing'!A{positions[key]}:X{positions[key]}",'values':[s.sheet_row(row)]})
call('POST',api+'/values:batchUpdate',json={'valueInputOption':'RAW','data':patch})
if 'Formats' not in tabs:
    added=call('POST',api+':batchUpdate',json={'requests':[{'addSheet':{'properties':{'title':'Formats','gridProperties':{'rowCount':100,'columnCount':12,'frozenRowCount':1}}}}]})
    tabs['Formats']=added['replies'][0]['addSheet']['properties']
format_headers=['format_id','channel','purpose','structure','headings','editorial_length','image','hashtags','manual_publish']
existing_formats=fetch('Formats','A1:I30')
if existing_formats:assert existing_formats[0]==format_headers,'Existing Formats has a different structure; preserve it'
call('PUT',api+'/values/'+quote("'Formats'!A1:I12",safe=''),params={'valueInputOption':'RAW'},json={'values':[format_headers]+formats})
requests=[{'updateSpreadsheetProperties':{'properties':{'timeZone':'Asia/Bangkok'},'fields':'timeZone'}}]
for name,col in [('Publishing',13),('Publishing',17),('Checks',2),('Checks',11),('Sync Log',0)]:
    props=tabs[name];sheetid=props['sheetId'];end=props['gridProperties']['rowCount']
    values=fetch(name,f'{chr(65+col)}2:{chr(65+col)}{min(end,1000)}')
    for offset,line in enumerate(values):
        if not line or line[0] in ('',None) or isinstance(line[0],(int,float)):continue
        try: serial=s.date_to_serial(line[0])
        except ValueError:raise ValueError(f'Invalid date at {name} row {offset+2}; refusing to coerce')
        requests.append({'updateCells':{'start':{'sheetId':sheetid,'rowIndex':offset+1,'columnIndex':col},'rows':[{'values':[{'userEnteredValue':{'numberValue':serial}}]}],'fields':'userEnteredValue'}})
    requests.append({'repeatCell':{'range':{'sheetId':sheetid,'startRowIndex':1,'endRowIndex':end,'startColumnIndex':col,'endColumnIndex':col+1},'cell':{'userEnteredFormat':{'numberFormat':{'type':'DATE','pattern':'dd/MM/yyyy'}}},'fields':'userEnteredFormat.numberFormat'}})
fid=tabs['Formats']['sheetId'];pid=tabs['Publishing']['sheetId']
requests += [{'repeatCell':{'range':{'sheetId':fid,'startRowIndex':0,'endRowIndex':12,'startColumnIndex':0,'endColumnIndex':9},'cell':{'userEnteredFormat':{'wrapStrategy':'WRAP','verticalAlignment':'TOP'}},'fields':'userEnteredFormat.wrapStrategy,userEnteredFormat.verticalAlignment'}},
{'updateDimensionProperties':{'range':{'sheetId':fid,'dimension':'COLUMNS','startIndex':0,'endIndex':9},'properties':{'pixelSize':260},'fields':'pixelSize'}}]
for sheetid,start,end in [(fid,0,9),(pid,22,24)]:
    requests.append({'repeatCell':{'range':{'sheetId':sheetid,'startRowIndex':0,'endRowIndex':1,'startColumnIndex':start,'endColumnIndex':end},'cell':{'userEnteredFormat':{'backgroundColor':{'red':.08,'green':.23,'blue':.35},'textFormat':{'bold':True,'foregroundColor':{'red':1,'green':1,'blue':1}}}},'fields':'userEnteredFormat'}})
call('POST',api+':batchUpdate',json={'requests':requests})
assert decode(fetch('Publishing'))==rows,'Readback mismatch'
assert fetch('Formats','A1:I12')==[format_headers]+formats
cfg['tabs']['Formats']=fid;cfg['drive_folder_id']='1MYywLSKvXCyIxbNin6s9aio4WhnEOaR9';cfg['asset_auth_policy']='service_account_only_no_connected_account_fallback'
(s.BASE/'config.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
shutil.copy2(s.BASE/'ledger.csv',pack/'ledger-before.csv');s.write(s.BASE/'ledger.csv',rows)
(s.BASE/'sync-baseline.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (s.BASE/'formats.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerows([format_headers]+formats)
now=datetime.now(timezone(timedelta(hours=7))).date().isoformat()
call('POST',api+'/values/'+quote("'Sync Log'!A:C",safe='')+':append',params={'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS'},json={'values':[[s.date_to_serial(now),'Success','Headings, hashtags, Formats, native DATE cells; replaced local/other-account asset links with online DSC source. New infographic upload blocked by service account quota.']]})
cards=[]
for row in rows.values():
    content=rich_content(row['content']);esc=html.escape
    cards.append('<article><h2>'+esc(row['channel'])+'</h2><p>'+esc(row['notes'])+'</p><a href="'+esc(row['compose_url'],quote=True)+'" target="_blank" rel="noopener">Mở đăng</a> · <a href="'+online+'" target="_blank">Ảnh gốc online</a><div class="copy-source">'+content+'</div><button onclick="copyRich(this)">Copy có định dạng</button></article>')
js='''<script>async function copyRich(b){let n=b.previousElementSibling;try{await navigator.clipboard.write([new ClipboardItem({'text/html':new Blob([n.innerHTML],{type:'text/html'}),'text/plain':new Blob([n.innerText],{type:'text/plain'})})]);b.textContent='Đã copy; kiểm tra Heading trong editor'}catch(e){const r=document.createRange();r.selectNodeContents(n);const s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Đã chọn nội dung: nhấn Ctrl+C'}};</script>'''
(pack/'preview.html').write_text('<!doctype html><meta charset="utf-8"><title>DSC: Heading và hashtag</title><style>body{font:16px/1.65 system-ui;max-width:980px;margin:30px auto;background:#e8f8f2;color:#0d1b2a}article{background:white;padding:28px;margin:24px 0;border-radius:16px}p{white-space:pre-line}button{padding:12px;cursor:pointer}.copy-source{border-top:1px solid #ddd;margin-top:20px}a{color:#007e15}</style><h1>11 bản nháp: Heading và hashtag</h1><p>Long form: H1/H2. Social: hashtag có chủ đích. Chưa đăng. Ảnh infographic mới chờ cách upload đúng tài khoản.</p>'+''.join(cards)+js,encoding='utf-8')
s.dashboard()
print('Verified 11 Publishing rows, 11 format guides; native date formatting applied; no local asset paths or rejected account links in Publishing.')
print('Formats gid:',fid)
