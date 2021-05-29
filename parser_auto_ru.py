import requests
from datetime import datetime
import csv



# ТЗ
# Выгрузить данные о новых автомобилях марки BMW с сайта https://auto.ru.
# Данные должны быть представлены в виде .csv таблицы с полями:
# 'current_date', 'mark_info', 'model_info', 'year', 'rur', 'usd', 'eur', 'city', 'seller_name', 'transmission', 'power', 'engine_type', 'owners_number'

FILE_CSV = 'auto_ru_bmw_list.csv'
FILE_XLSX = 'auto_ru_bmw_list.xlsx'
URL = 'https://auto.ru/-/ajax/desktop/listing/'  # POST
HEADERS = '''Host: auto.ru
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://auto.ru/moskva/cars/bmw/all/?page=2
x-client-app-version: 03c316d6011
x-page-request-id: 7eeebe7c09fb2b3126b4e5dbc5e896af
x-client-date: 1622274239397
x-csrf-token: c501a3e91feec36f7dff4c4aec9f9f6e4407582dcfe0bc77
x-requested-with: fetch
content-type: application/json
Origin: https://auto.ru
Content-Length: 110
Connection: keep-alive
Cookie: autoru_sid=a%3Ag60b1e7912go45b2fn7d9ae0s09n1ntm.239a427b8e260fbaf6c998ce1b198f3d%7C1622271889958.604800.JxmJFUEhgKT9br28y-4WZw.F72JZNpTWT8J7R6u-PgUa031adX6ffslBY6q1v6JZYE; autoruuid=g60b1e7912go45b2fn7d9ae0s09n1ntm.239a427b8e260fbaf6c998ce1b198f3d; suid=e24601a2695ec1fad0fc4eecbc188fd8.4e752b7d9a2f8f04de81d56acc4f1ff1; X-Vertis-DC=sas; yuidlt=1; yandexuid=1867712871621071502; counter_ga_all7=2; crookie=F3r1zq9y6swK5QBnVQsApLEw47gVSjihEIC2ahqPl2QTo3u+iQWSzKrFkkAwGay37E5K+GE9tZGU0NCirPY/ICcwfig=; cmtchd=MTYyMjI3MTg5MDg2MQ==; _ym_isad=2; _ym_uid=1622271897170726580; _ym_d=1622274234; cycada=Z57WjoZ2yXLnJFtx235QWLE0IsBFgWMK+CoRvqvTxAc=; _ga=GA1.2.715204751.1622271908; _gid=GA1.2.1706153147.1622271908; listing_view=%7B%22output_type%22%3A%22table%22%2C%22version%22%3A1%7D; _csrf_token=c501a3e91feec36f7dff4c4aec9f9f6e4407582dcfe0bc77; from_lifetime=1622274234516; from=direct; _gat_fixprocent=1; gdpr=0'''
HEADERS_DICT = {}
for header in HEADERS.split('\n'):
    key, value = header.split(': ')
    HEADERS_DICT[key] = value

page_count = 0
data_list = []

while True:
    page_count += 1
    param = {
        "catalog_filter": [{"mark": "BMW"}],
        "category": "cars",
        "geo_id": [213],
        "geo_radius": 200,
        "page": page_count,
        "section": "all",
    }
    response = requests.post(URL, json=param, headers=HEADERS_DICT)
    if response.status_code != 200:
        break

    data = response.json()
    print(f'Page: {page_count} ...')

    for i in range(0, len(data['offers'])):

        mark_info = str(data['offers'][i]['vehicle_info']['mark_info'].get('name'))  # marka auto
        model_info = str(data['offers'][i]['vehicle_info']['model_info'].get('name'))  # model auto
        year = str(data['offers'][i]['documents'].get('year'))  # god
        rur = str(data['offers'][i]['price_info'].get('RUR'))
        usd = str(data['offers'][i]['price_info'].get('USD'))
        eur = str(data['offers'][i]['price_info'].get('EUR'))
        city = str(data['offers'][i]['seller']['location']['region_info'].get('name'))  # gorod
        seller_name = str(data['offers'][i]['seller'].get('name'))  # prodavets
        transmission = str(data['offers'][i]['vehicle_info']['tech_param'].get('transmission'))  # korobka peredach
        power = str(data['offers'][i]['vehicle_info']['tech_param'].get('power'))  # loshadinyh sil
        engine_type = str(data['offers'][i]['vehicle_info']['tech_param'].get('engine_type'))  # toplivo
        owners_number = str(data['offers'][i]['documents'].get('owners_number'))  # kolichestvo vladeltsev

        data_list.append({
            'current_date': str(datetime.now().date()),
            'mark_info': mark_info,
            'model_info': model_info,
            'year': year,
            'rur': rur,
            'usd': usd,
            'eur': eur,
            'city': city,
            'seller_name': seller_name,
            'transmission': transmission,
            'power': power,
            'engine_type': engine_type,
            'owners_number': owners_number,
        })

with open(FILE_CSV, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['current_date', 'mark_info', 'model_info', 'year', 'rur', 'usd', 'eur', 'city', 'seller_name', 'transmission', 'power', 'engine_type', 'owners_number'])
        for item in data_list:
            writer.writerow([item['current_date'], item['mark_info'], item['model_info'], item['year'], item['rur'], item['usd'], item['eur'], item['city'], item['seller_name'], item['transmission'], item['power'], item['engine_type'], item['owners_number']])
