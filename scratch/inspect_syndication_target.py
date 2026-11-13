import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import syndicate as s
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
cfg=json.loads((s.BASE/'config.json').read_text())
session=AuthorizedSession(Credentials.from_service_account_file(str(s.ROOT/cfg['credentials_file']),scopes=['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']))
api='https://sheets.googleapis.com/v4/spreadsheets/'+cfg['spreadsheet_id']
r=session.get(api+'/values/Publishing!A1:V30',timeout=40);r.raise_for_status()
print(json.dumps(r.json().get('values',[]),ensure_ascii=False))
folder='1MYywLSKvXCyIxbNin6s9aio4WhnEOaR9'
r=session.get('https://www.googleapis.com/drive/v3/files/'+folder,params={'fields':'id,name,mimeType,capabilities','supportsAllDrives':'true'},timeout=40)
print('SERVICE_ACCOUNT_FOLDER',r.status_code, r.json())
if r.ok and r.json().get('capabilities',{}).get('canAddChildren'):
    path=s.BASE/'assets/con-hao-kinh-te-pinterest-v1.png'
    with path.open('rb') as f:
        upload=session.post('https://www.googleapis.com/upload/drive/v3/files',params={'uploadType':'multipart','supportsAllDrives':'true','fields':'id,name,webViewLink,parents'},files={'metadata':('metadata',json.dumps({'name':'DSC-con-hao-kinh-te-pinterest-v1.png','parents':[folder]}),'application/json'),'file':(path.name,f,'image/png')},timeout=60)
    print('UPLOAD',upload.status_code,upload.json())
    if upload.ok: (s.BASE/'assets/drive-asset.json').write_text(json.dumps(upload.json(),indent=2),encoding='utf-8')
