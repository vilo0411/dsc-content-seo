import json
from pathlib import Path
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
from urllib.parse import quote
root=Path.cwd()
cfg=json.loads((root/'knowledge/operations/syndication/config.json').read_text())
s=AuthorizedSession(Credentials.from_service_account_file(str(root/cfg['credentials_file']),scopes=['https://www.googleapis.com/auth/spreadsheets']))
url='https://sheets.googleapis.com/v4/spreadsheets/'+cfg['spreadsheet_id']
def api(method,path='',**kw):
 r=s.request(method,url+path,timeout=45,**kw); r.raise_for_status(); return r.json()
meta=api('GET',params={'fields':'spreadsheetId,sheets.properties'})
p=next(x['properties'] for x in meta['sheets'] if x['properties']['title']=='Publishing')
rng="'Publishing'!A1:X1000"
def read():
 return api('GET','/values/'+quote(rng,safe=''),params={'valueRenderOption':'UNFORMATTED_VALUE','dateTimeRenderOption':'SERIAL_NUMBER'}).get('values',[])
rows=read(); headers=rows[0]
print(json.dumps({'properties':p,'headers':headers,'populated_rows':len(rows)},ensure_ascii=False))
(root/'scratch').mkdir(exist_ok=True)
(root/'scratch/publishing-before-column-move.json').write_text(json.dumps({'metadata':meta,'values':rows},ensure_ascii=False),encoding='utf-8')
# Read cell structure before native moves; moveDimension preserves cell metadata.
cells=api('GET',params={'ranges':"'Publishing'!A1:X13",'includeGridData':'true','fields':'sheets(data(startRow,startColumn,rowData(values(userEnteredValue,userEnteredFormat,dataValidation)),columnMetadata(pixelSize,hiddenByUser)),basicFilter)'} )
(root/'scratch/publishing-before-column-move-structure.json').write_text(json.dumps(cells,ensure_ascii=False),encoding='utf-8')
assert read()==rows, 'Sheet changed; inspect again before moving columns'
block=['title','content','hashtags','compose_url','channel_url','asset_url']
order=headers[:6]+block+[h for h in headers[6:] if h not in block]
working=list(headers); requests=[]
for dest,name in enumerate(order):
 src=working.index(name)
 if src==dest: continue
 requests.append({'moveDimension':{'source':{'sheetId':p['sheetId'],'dimension':'COLUMNS','startIndex':src,'endIndex':src+1},'destinationIndex':dest if src>dest else dest+1}})
 working.insert(dest,working.pop(src))
if requests: api('POST',':batchUpdate',json={'requests':requests})
after=read()
assert after[0]==order
normalize=lambda data: [{h:(row[i] if i<len(row) else '') for i,h in enumerate(data[0])} for row in data[1:]]
assert normalize(rows)==normalize(after), 'Readback values differ'
layout=api('GET',params={'ranges':"'Publishing'!G1:L3",'includeGridData':'true','fields':'sheets(data(columnMetadata(pixelSize,hiddenByUser),rowData(values(formattedValue,userEnteredFormat))),properties.gridProperties)'})
print(json.dumps({'verified_headers':after[0],'unchanged_records':len(after)-1,'layout':layout},ensure_ascii=False))
