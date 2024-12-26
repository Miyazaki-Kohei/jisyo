import os
import requests
import csv
from dotenv import load_dotenv

load_dotenv()
# カレントディレクトリのパスを取得
current_directory = os.getcwd()

url = 'https://api.lanscopean.com/v1/devices'
access_token =  os.getenv('ACCESS_TOKEN')
headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
params = {'limit': 1000}  # ページごとのデータ数の制限

fieldnames = ['serial', 'fj_manage_number', 'user_name', 'apple_ID', 'manager_name', 'phone_number', 'install']

# CSV ファイルを書き出すための準備
csv_file_path = os.path.join(current_directory, 'DeviceData1.csv')

with open(csv_file_path, 'w', newline='', errors='ignore') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    while True:
        # API のリクエストを送る
        response = requests.get(url, headers=headers, params=params, verify=False)  # 本番環境ではverify=Trueに設定すること

        # データを Json 形式に変換
        data = response.json()
        log_file_path = os.path.join(current_directory, 'test.txt')

        with open(log_file_path, 'a', encoding='UTF-8') as file: 
            file.write(response.text)

        # 各デバイスの情報を CSV ファイルに書き出す
        for device in data['data']:
            asset_no = device.get('asset_no', '')
            login_user_name = device.get('login_user_name', '')
            apple_id = device.get('apple_id', '')
            managed_device_name = device.get('managed_device_name', '')
            manager_name = device.get('user_name', '')
            serial = device.get('serial', '')
            phone_number = device.get('phone_number', '')

            # 新しい列を追加し、値を設定する
            install_value = '1'

            writer.writerow({'fj_manage_number': asset_no, 'user_name': login_user_name, 'apple_ID': apple_id,
                             'serial': serial, 'phone_number': phone_number, 'install': install_value})

        # 次のページがある場合は、next_token を取得してパラメータに追加する
        if 'next_token' in data:
            next_token = data['next_token']
            params['next_token'] = next_token
        else:
            break