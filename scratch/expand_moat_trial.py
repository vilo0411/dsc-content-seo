"""One reviewed article, all configured channels; no external publishing."""
import sys,json,csv,shutil,html
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import quote
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import syndicate as s
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
cfg=json.loads((s.BASE/'config.json').read_text(encoding='utf-8'));sid=cfg['tabs']['Publishing']
session=AuthorizedSession(Credentials.from_service_account_file(str(s.ROOT/cfg['credentials_file']),scopes=['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']))
api='https://sheets.googleapis.com/v4/spreadsheets/'+cfg['spreadsheet_id']
def call(method,url,**kw):
    r=session.request(method,url,timeout=45,**kw)
    if not r.ok:raise RuntimeError(f'HTTP {r.status_code}: '+r.json().get('error',{}).get('message','Request failed'))
    return r.json()
meta=call('GET',api,params={'includeGridData':'true','ranges':"'Publishing'!A1:V5"})
def fetch():return call('GET',api+'/values/'+quote("'Publishing'!A1:V1000",safe='')).get('values',[])
before=fetch();headers=before[0]
assert headers==s.FIELDS or headers==s.FIELDS[:19], 'Unexpected headers; migration refused'
def decode(values):
    rows={}
    for line in values[1:]:
        if not any(line):continue
        row={k:'' for k in s.FIELDS};row.update(dict(zip(values[0],line)))
        if not row['id'] or row['id'] in rows:raise ValueError('Invalid IDs')
        rows[row['id']]=row
    return rows
remote=decode(before)
local=s.read(s.BASE/'ledger.csv')
base=json.loads((s.BASE/'sync-baseline.json').read_text(encoding='utf-8'))
merged,conflicts=s.merge(base,local,remote)
assert not conflicts, 'Resolve existing conflicts before expanding trial'
slug='con-hao-kinh-te-la-gi-cach-tao-ra-va-tam-quan-trong-cua-con-hao-kinh-te'
source='https://www.dsc.com.vn/kien-thuc/'+slug
payload=json.loads((s.ROOT/'scratch/moat_channel_content.json').read_text(encoding='utf-8'))
channels={r['channel']:r for r in csv.DictReader((s.BASE/'channels.csv').open(encoding='utf-8-sig'))}
asset_meta=json.loads((s.BASE/'assets/drive-asset.json').read_text(encoding='utf-8'))
asset=asset_meta['webViewLink']
# Folder move pending Editor access; keep the working asset link and disclose status.
composers={'x':'https://x.com/compose/post','mastodon':'https://mastodon.social/publish','pinterest':'https://www.pinterest.com/pin-creation-tool/','telegraph':'https://telegra.ph/','ameblo':'https://blog.ameba.jp/ucs/entry/srventryinsertinput.do','google-sites':'https://sites.google.com/','linkedin':'https://www.linkedin.com/feed/','medium':'https://medium.com/new-story'}
instructions={
'pinterest':'Dán tiêu đề vào Title, đoạn mô tả vào Description; Link dùng source_url, Alt: Năm nguồn lợi thế cạnh tranh: tài sản vô hình, chi phí chuyển đổi, hiệu ứng mạng, lợi thế chi phí, quy mô hiệu quả. Tải ảnh từ asset_url. Không dán URL vào mô tả nếu không cần.',
'telegraph':'Mở trang mới ở telegra.ph, điền tiêu đề và tác giả Chứng khoán DSC. Link tài khoản cũ là bài giới thiệu, không phải editor. Dán nội dung và chèn ảnh tại đầu bài.',
'ameblo':'Nội dung tiếng Việt cho độc giả Việt; kiểm tra phù hợp tệp người theo dõi trước đăng. Điền tiêu đề riêng, dán thân bài; ảnh tùy chọn.',
'pixbender':'Chưa xác minh chức năng đăng ảnh của tài khoản. Mở profile rồi chọn đăng/tải ảnh nếu có; bản này chỉ dùng khi nền tảng hỗ trợ caption và ảnh. Không coi link mở profile là composer đã xác minh.',
'google-sites':'Mở danh sách Sites bằng tài khoản có quyền, chọn site hiện có rồi tạo trang con hoặc thêm khối thư viện. URL công khai không phải URL editor. Chưa publish site tự động.',
'linkedin':'Chưa có URL tài khoản. Mở feed, chọn bắt đầu bài đăng bằng tài khoản cá nhân thật hoặc Page có quyền. Ảnh checklist tùy chọn.',
'medium':'Chưa có URL tài khoản. Mở new-story, điền title riêng, dán thân bài; ảnh checklist tùy chọn. Đây là bài chuyển thể, không mặc định gắn canonical về một bài có nội dung khác.',
'wakelet':'Mở profile rồi vào bộ sưu tập có quyền chỉnh sửa; thêm nguồn URL và mô tả. Mở link này không tự tạo bộ sưu tập.',
'band':'Mở kênh, chọn viết bài nếu có quyền; dán thân bài và tải ảnh checklist tùy chọn.',
'mastodon':'Mở trang đăng sau khi đăng nhập; nội dung dự kiến dưới 500 ký tự khi URL tính 23 ký tự.',
'x':'Mở compose sau khi đăng nhập; nội dung dự kiến dưới 280 ký tự khi URL tính 23 ký tự.'}
pack=s.BASE/'packs'/slug/'all-channels-v2';pack.mkdir(parents=True,exist_ok=True)
stamp=datetime.now(timezone.utc).isoformat()
for channel,item in payload.items():
    key=slug+'-'+channel+'-v1'
    row=merged.get(key)
    if row and row.get('status') in {'Approved','Posted'}:
        key=slug+'-'+channel+'-v2'
        if key in merged: raise ValueError('Protected version exists')
        row=None
    row=row or {k:'' for k in s.FIELDS}
    content=item['body']+'\n'+source
    if channel in {'x','mastodon'}:assert len(item['body'])+1+23<=({'x':280,'mastodon':500}[channel])
    row.update(id=key,slug=slug,source_url=source,channel=channel,format='image-pin' if channel=='pinterest' else ('long-article' if channel in {'medium','ameblo','telegraph'} else 'social-adaptation'),version=key.rsplit('-',1)[1],content=content,asset_path='knowledge/operations/syndication/assets/con-hao-kinh-te-pinterest-v1.png',target_url=source,utm_url='',anchor='Đọc bài nguồn tại Chứng khoán DSC',status='Draft',notes='TIÊU ĐỀ: '+item['title']+'\n'+instructions[channel]+'\nChờ duyệt; chưa đăng.',index_status='Unknown',channel_url=channels[channel]['url'],compose_url=composers.get(channel,channels[channel]['url']),asset_url=asset)
    merged[key]=row
    (pack/(channel+'.md')).write_text('# '+item['title']+'\n\n'+content+'\n\n---\nMở kênh: '+row['channel_url']+'\nMở đăng: '+row['compose_url']+'\nẢnh: '+asset+'\n\n'+instructions[channel],encoding='utf-8')
assert fetch()==before,'Remote changed; retry required'
positions={line[0]:i+2 for i,line in enumerate(before[1:]) if line and line[0]}
n=len(before)+1;patch=[]
if headers!=s.FIELDS:patch.append({'range':"'Publishing'!T1:V1",'values':[s.FIELDS[19:]]})
for key,row in merged.items():
    if key not in positions:positions[key]=n;n+=1
    if remote.get(key)!=row:patch.append({'range':f"'Publishing'!A{positions[key]}:V{positions[key]}",'values':[[row[k] for k in s.FIELDS]]})
call('POST',api+'/values:batchUpdate',json={'valueInputOption':'RAW','data':patch})
formatting=[{'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'COLUMNS','startIndex':9,'endIndex':10},'properties':{'hiddenByUser':True},'fields':'hiddenByUser'}},
{'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'COLUMNS','startIndex':6,'endIndex':7},'properties':{'pixelSize':560},'fields':'pixelSize'}},
{'repeatCell':{'range':{'sheetId':sid,'startRowIndex':1,'endRowIndex':n,'startColumnIndex':6,'endColumnIndex':7},'cell':{'userEnteredFormat':{'wrapStrategy':'WRAP','verticalAlignment':'TOP'}},'fields':'userEnteredFormat.wrapStrategy,userEnteredFormat.verticalAlignment'}},
{'repeatCell':{'range':{'sheetId':sid,'startRowIndex':0,'endRowIndex':1,'startColumnIndex':19,'endColumnIndex':22},'cell':{'userEnteredFormat':{'backgroundColor':{'red':.08,'green':.23,'blue':.35},'textFormat':{'bold':True,'foregroundColor':{'red':1,'green':1,'blue':1}}}},'fields':'userEnteredFormat'}}]
for key,row in merged.items():
    link=row.get('channel_url') or row.get('compose_url')
    if link:formatting.append({'repeatCell':{'range':{'sheetId':sid,'startRowIndex':positions[key]-1,'endRowIndex':positions[key],'startColumnIndex':3,'endColumnIndex':4},'cell':{'userEnteredFormat':{'textFormat':{'link':{'uri':link}}}},'fields':'userEnteredFormat.textFormat.link'}})
call('POST',api+':batchUpdate',json={'requests':formatting})
assert decode(fetch())==merged,'Remote verification failed; baseline unchanged'
shutil.copy2(s.BASE/'ledger.csv',pack/'ledger-before.csv')
s.write(s.BASE/'ledger.csv',merged)
(s.BASE/'sync-baseline.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2),encoding='utf-8')
call('POST',api+'/values/'+quote("'Sync Log'!A:C",safe='')+':append',params={'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS'},json={'values':[[stamp,'Success','11 channel drafts; plain source links; clickable channel/compose links; Drive infographic attached. Readback equals local.']]})
cards=[]
for channel,item in payload.items():
    row=next(r for r in merged.values() if r['channel']==channel and r['slug']==slug and r['status']=='Draft')
    esc=html.escape
    cards.append('<article><h2>'+esc(channel)+' — '+esc(item['title'])+'</h2><p><a target="_blank" rel="noopener" href="'+esc(row['compose_url'],quote=True)+'">Mở kênh để đăng</a> · <a target="_blank" rel="noopener" href="'+esc(asset,quote=True)+'">Tải ảnh trên Drive</a></p><pre>'+esc(row['content'])+'</pre><button onclick="navigator.clipboard.writeText(this.previousElementSibling.textContent).then(()=>this.textContent=\'Đã copy\').catch(()=>this.textContent=\'Hãy chọn và copy nội dung\')">Copy nội dung</button><p>'+esc(instructions[channel])+'</p></article>')
(pack/'preview.html').write_text('<!doctype html><meta charset="utf-8"><title>DSC — 11 bản chuyển thể</title><style>body{font:16px/1.65 system-ui;max-width:980px;margin:30px auto;background:#e8f8f2;color:#0d1b2a}article{background:white;padding:28px;margin:24px 0;border-radius:16px}pre{white-space:pre-wrap;font:inherit}button{padding:10px 20px;cursor:pointer}a{color:#007e15}</style><h1>Con hào kinh tế — 11 kênh</h1><p>Tất cả là Draft. Link nguồn thuần. Chưa đăng ra nền tảng.</p>'+''.join(cards),encoding='utf-8')
(pack/'README.md').write_text('# Bộ thử toàn kênh\n\nMở preview.html để xem 11 bản và copy nội dung. Cột channel trên Sheet có link bấm; T/U/V lần lượt là tài khoản, trang mở đăng, ảnh Drive. Tiêu đề đề xuất và hướng dẫn từng nền tảng nằm trong notes. Không có UTM. Mọi bản là Draft, chưa đăng; index Unknown.\n\nẢnh Drive: '+asset+'\n\nNguồn kiến thức: bài DSC trong source_url. Đối chiếu thuật ngữ: https://www.morningstar.com/investing-definitions/economic-moat\n\n```mermaid\nflowchart TD\n Social[X / Mastodon / BAND / LinkedIn] --> DSC[Bài nguồn DSC]\n Visual[Pinterest / Pixbender] --> DSC\n Long[Medium / Telegraph / Ameblo] --> DSC\n Hub[Wakelet / Google Sites] --> DSC\n```\n',encoding='utf-8')
s.dashboard()
print('Verified 11 drafts; no UTM; channel hyperlinks and Drive asset saved. No external publishing.')
