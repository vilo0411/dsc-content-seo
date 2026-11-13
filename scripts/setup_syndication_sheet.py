"""Initialize missing syndication tabs using the user-supplied service account."""
import csv
import json
from pathlib import Path
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
from syndicate import BASE, FIELDS, dashboard

ROOT = Path(__file__).resolve().parents[1]
TARGET = '1urr2pvtQRWof_uC-X3RA_D6EMUvHLRhZJbx1PS1TBY0'

def main():
    credentials = Credentials.from_service_account_file(
        str(ROOT/'gen-lang-client-0863794209-385c2ddf2422.json'),
        scopes=['https://www.googleapis.com/auth/spreadsheets'])
    session = AuthorizedSession(credentials)
    endpoint = f'https://sheets.googleapis.com/v4/spreadsheets/{TARGET}'
    def call(method, url, **kwargs):
        response = session.request(method, url, timeout=45, **kwargs)
        if not response.ok:
            # Never dump credentials, request headers or access tokens.
            raise RuntimeError(f'Sheets returned HTTP {response.status_code}: ' + response.json().get('error',{}).get('message','Request failed'))
        return response.json()
    meta = call('GET', endpoint, params={'fields':'spreadsheetId,sheets.properties'})
    existing = {s['properties']['title']:s['properties']['sheetId'] for s in meta.get('sheets',[])}
    names = ['Dashboard','Channels','Publishing','Checks','Sync Log']
    requests = [{'addSheet':{'properties':{'title':name,'gridProperties':{'frozenRowCount':1,'rowCount':1000,'columnCount':26}}}} for name in names if name not in existing]
    created = []
    if requests:
        reply=call('POST',endpoint+':batchUpdate',json={'requests':requests})
        for result in reply['replies']:
            props=result['addSheet']['properties']; existing[props['title']]=props['sheetId']; created.append(props['title'])
    channels=list(csv.reader((BASE/'channels.csv').open(encoding='utf-8-sig',newline='')))
    data={'Dashboard':[['Metric','Value'],['Posted','=COUNTIF(Publishing!L2:L1000,"Posted")'],['Approved','=COUNTIF(Publishing!L2:L1000,"Approved")']],
          'Channels':channels,'Publishing':[FIELDS],
          'Checks':[['id','publishing_id','checked_at','url','http_status','backlink','robots','canonical','index_status','method','evidence','next_check']],
          'Sync Log':[['time','result','details']]}
    for name in names:
        observed=call('GET',endpoint+'/values/'+requests_quote(name+'!A1:S12'))
        if observed.get('values'):
            if name!='Dashboard' and observed['values'][0]!=data[name][0]:
                raise RuntimeError(f'Existing {name} has incompatible headers; left unchanged')
            continue
        rows=data[name]
        call('PUT',endpoint+'/values/'+requests_quote(name+'!A1'),params={'valueInputOption':'USER_ENTERED' if name=='Dashboard' else 'RAW'},json={'values':rows})
    formatting=[]
    for name in created:
        sid=existing[name]; width=len(data[name][0])
        formatting += [{'repeatCell':{'range':{'sheetId':sid,'startRowIndex':0,'endRowIndex':1,'startColumnIndex':0,'endColumnIndex':width},'cell':{'userEnteredFormat':{'backgroundColor':{'red':.08,'green':.23,'blue':.35},'textFormat':{'bold':True,'foregroundColor':{'red':1,'green':1,'blue':1}},'wrapStrategy':'WRAP'}},'fields':'userEnteredFormat'}},
                       {'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'COLUMNS','startIndex':0,'endIndex':width},'properties':{'pixelSize':180},'fields':'pixelSize'}}]
    if 'Publishing' in created:
        formatting.append({'setDataValidation':{'range':{'sheetId':existing['Publishing'],'startRowIndex':1,'endRowIndex':1000,'startColumnIndex':11,'endColumnIndex':12},'rule':{'condition':{'type':'ONE_OF_LIST','values':[{'userEnteredValue':v} for v in ['Draft','Approved','Posted','Skipped','Needs-fix','Archived']]},'strict':True,'showCustomUi':True}}})
    if formatting: call('POST',endpoint+':batchUpdate',json={'requests':formatting})
    for name in names:
        result=call('GET',endpoint+'/values/'+requests_quote(name+'!A1:S12'))
        assert result.get('values'), f'{name}: readback empty'
    config=json.loads((BASE/'config.json').read_text(encoding='utf-8'))
    config.update(spreadsheet_id=TARGET,tabs={n:existing[n] for n in names},auth_mode='service_account',credentials_file='gen-lang-client-0863794209-385c2ddf2422.json')
    (BASE/'config.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
    for path in [BASE/'playbook.md']:
        path.write_text(path.read_text(encoding='utf-8').replace('1nWu0TSVzChCOtW57z4OLZxHidJzDJqwLS08XA2drGUk',TARGET),encoding='utf-8')
    dashboard()
    print('Verified target Sheet; local config updated. Existing tabs and rows preserved.')

def requests_quote(value):
    from urllib.parse import quote
    return quote("'"+value.split('!')[0]+"'!"+value.split('!')[1],safe='')

if __name__=='__main__': main()
