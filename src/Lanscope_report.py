import requests
import csv
from datetime import datetime, timedelta
import pytz

url = 'https://api.lanscopean.com/v1/reports/devices/activity_time'
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb21wYW55X2lkIjoiODdFODg2RjU5QjEwNDM4Q0E5RjMxRUY4NkNEODQxOTIiLCJhcGlfa2V5X2lkIjoiaW9lcEdTdkRUZjVmMWp3TXZaS09BOFY0V2tjSjZhanp0ckdXME9wZyIsImFwaV9rZXlfdmFsdWUiOiJpb2VwR1N2RFRmNWYxandNdlpLT0E4VjRXa2NKNmFqenRyR1cwT3BnIiwidXVpZCI6IjNjNDBiZWFlLTkxMDEtNGRhNi05ZTlhLWM3Y2E4ZGE0OTIyMiJ9.1LeThayYupN-Prlgr48A1Um_OXfX7qq7jJ-6a96AVsM'
headers = {'Authorization':f'Bearer {access_token}','Content-Type':'application/json'}
params = {
    'start_date': '2024-04-04',
    'end_date': '2024-05-01',
    'asset_no': '1042'
}
# headers = {
#     'Accept': 'application/json'
# }

response = requests.get(url, params=params, headers=headers)



if response.status_code == 200:
    data = response.json()
        # 日本時間（JST）に変換
    for entry in data['data']:
        start_datetime = datetime.strptime(entry['start_datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        start_datetime = pytz.utc.localize(start_datetime).astimezone(pytz.timezone('Asia/Tokyo'))
        entry['start_datetime'] = start_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        
        end_datetime = datetime.strptime(entry['end_datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        end_datetime = pytz.utc.localize(end_datetime).astimezone(pytz.timezone('Asia/Tokyo'))
        entry['end_datetime'] = end_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    # 応答データの処理
    # CSVファイルへの書き込み
    with open('C:\\Lanscope作業\\report.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data['data'][0].keys())
        writer.writeheader()
        writer.writerows(data['data'])
        
    print('CSVファイルへの出力が完了しました。')
else:
    print('Error: HTTP request failed with status code', response.status_code)



