# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 15:16:25 2021

@author: Hong Sung Uk
"""
import pandas as pd
import urllib
import urllib.request
import json
from datetime import datetime
import datetime as dt

#코드 자동 실행은 스케쥴러 이용하여 설정할 것 https://hogni.tistory.com/11
#if datetime.today().strftime("%Y-%m-%d %H:%M:%S") =='2021-06-01 16:00:00' :
 #   아래 코드 실행
# 코드는 20시와 23시에 실행되어야 하고 그때의 i값을 찾아내야함

ServiceKey = 'kijRO03tVUYGoIzqTygxmXi0JW8qCK8HynpR+4KAw/FNFSsB1ctzr480mZbyF8E41JiJUJHiJVYg5Y4NlYv+Bw=='
url = ' http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst'

# 울산
queryParams = '?' + urllib.parse.urlencode(
    {
        urllib.parse.quote_plus('ServiceKey') : ServiceKey,
        urllib.parse.quote_plus('numOfRows') : '113', # 총 14개의 항목을 3시간 단위로 순차적으로 불러옵니다. 다음날 24시간예보에 필요한 만큼만 가져왔습니다.
        urllib.parse.quote_plus('dataType') : 'JSON', # JSON, XML 두가지 포멧을 제공합니다.
        urllib.parse.quote_plus('base_date') : datetime.today().strftime("%Y%m%d"), # 예보 받을 날짜를 입력합니다. 최근 1일간의 자료만 제공합니다.
        urllib.parse.quote_plus('base_time') : '2000', # 예보 시간을 입력합니다. 2시부터 시작하여 3시간 단위로 입력 가능합니다.
        urllib.parse.quote_plus('nx') : '102', # 울산 태양광 발전소 x 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
        urllib.parse.quote_plus('ny') : '83' # 울산 태양광 발전소 y 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
    }
)

response = urllib.request.urlopen(url + queryParams).read()
response = json.loads(response, encoding="UTF-8")

fcst_df = pd.DataFrame()
date = datetime.today().strftime("%Y-%m-%d")
date = str(pd.to_datetime(date)+dt.timedelta(days=1))[0:10]
fcst_df['Forecast_time'] = [f'{date} {hour}:00' for hour in range(24)]
row_idx = 0

for i, data in enumerate(response['response']['body']['items']['item']):
    if i > 0:
        if data['category']=='REH':
            fcst_df.loc[row_idx, 'Humidity'] = float(data['fcstValue'])
            print('category:Humidity,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='T3H':
            fcst_df.loc[row_idx, 'Temperature'] = float(data['fcstValue'])
            print('category:Temperature,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='SKY':
            fcst_df.loc[row_idx, 'Cloud'] = float(data['fcstValue'])
            print('category:Cloud,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='VEC':
            fcst_df.loc[row_idx, 'WindDirection'] = float(data['fcstValue'])
            print('category:WindDirection,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='WSD':
            fcst_df.loc[row_idx, 'WindSpeed'] = float(data['fcstValue'])
            print('category:WindSpeed,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'], '\n')
            row_idx+=3
fcst_df = fcst_df.loc[0:23]
fcst_df.to_csv(datetime.today().strftime("%Y%m%d")+'_20h.csv', index=False)

queryParams = '?' + urllib.parse.urlencode(
    {
        urllib.parse.quote_plus('ServiceKey') : ServiceKey,
        urllib.parse.quote_plus('numOfRows') : '113', # 총 14개의 항목을 3시간 단위로 순차적으로 불러옵니다. 다음날 24시간예보에 필요한 만큼만 가져왔습니다.
        urllib.parse.quote_plus('dataType') : 'JSON', # JSON, XML 두가지 포멧을 제공합니다.
        urllib.parse.quote_plus('base_date') : datetime.today().strftime("%Y%m%d"), # 예보 받을 날짜를 입력합니다. 최근 1일간의 자료만 제공합니다.
        urllib.parse.quote_plus('base_time') : '2300', # 예보 시간을 입력합니다. 2시부터 시작하여 3시간 단위로 입력 가능합니다.
        urllib.parse.quote_plus('nx') : '102', # 울산 태양광 발전소 x 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
        urllib.parse.quote_plus('ny') : '83' # 울산 태양광 발전소 y 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
    }
)

response = urllib.request.urlopen(url + queryParams).read()
response = json.loads(response, encoding="UTF-8")

fcst_df_23 = pd.DataFrame()
date = datetime.today().strftime("%Y-%m-%d")
date = str(pd.to_datetime(date)+dt.timedelta(days=1))[0:10]
fcst_df_23['Forecast_time'] = [f'{date} {hour}:00' for hour in range(3,24)]
row_idx = 0

for i, data in enumerate(response['response']['body']['items']['item']):
    if i > 0:
        if data['category']=='REH':
            fcst_df_23.loc[row_idx, 'Humidity'] = float(data['fcstValue'])
            print('category:Humidity,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='T3H':
            fcst_df_23.loc[row_idx, 'Temperature'] = float(data['fcstValue'])
            print('category:Temperature,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='SKY':
            fcst_df_23.loc[row_idx, 'Cloud'] = float(data['fcstValue'])
            print('category:Cloud,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='VEC':
            fcst_df_23.loc[row_idx, 'WindDirection'] = float(data['fcstValue'])
            print('category:WindDirection,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='WSD':
            fcst_df_23.loc[row_idx, 'WindSpeed'] = float(data['fcstValue'])
            print('category:WindSpeed,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'], '\n')
            row_idx+=3
fcst_df_23 = fcst_df_23.loc[0:23]
fcst_df_23.to_csv(datetime.today().strftime("%Y%m%d")+'_23h.csv', index=False)

# 당진
queryParams = '?' + urllib.parse.urlencode(
    {
        urllib.parse.quote_plus('ServiceKey') : ServiceKey,
        urllib.parse.quote_plus('numOfRows') : '113', # 총 14개의 항목을 3시간 단위로 순차적으로 불러옵니다. 다음날 24시간예보에 필요한 만큼만 가져왔습니다.
        urllib.parse.quote_plus('dataType') : 'JSON', # JSON, XML 두가지 포멧을 제공합니다.
        urllib.parse.quote_plus('base_date') : datetime.today().strftime("%Y%m%d"), # 예보 받을 날짜를 입력합니다. 최근 1일간의 자료만 제공합니다.
        urllib.parse.quote_plus('base_time') : '2000', # 예보 시간을 입력합니다. 2시부터 시작하여 3시간 단위로 입력 가능합니다.
        urllib.parse.quote_plus('nx') : '53', # 당진 태양광 발전소 x 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
        urllib.parse.quote_plus('ny') : '114' # 당진 태양광 발전소 y 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
    }
)

response = urllib.request.urlopen(url + queryParams).read()
response = json.loads(response, encoding="UTF-8")

fcst_df_dangjin = pd.DataFrame()
date = datetime.today().strftime("%Y-%m-%d")
date = str(pd.to_datetime(date)+dt.timedelta(days=1))[0:10]
fcst_df_dangjin['Forecast_time'] = [f'{date} {hour}:00' for hour in range(24)]
row_idx = 0

for i, data in enumerate(response['response']['body']['items']['item']):
    if i > 0:
        if data['category']=='REH':
            fcst_df_dangjin.loc[row_idx, 'Humidity'] = float(data['fcstValue'])
            print('category:Humidity,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='T3H':
            fcst_df_dangjin.loc[row_idx, 'Temperature'] = float(data['fcstValue'])
            print('category:Temperature,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='SKY':
            fcst_df_dangjin.loc[row_idx, 'Cloud'] = float(data['fcstValue'])
            print('category:Cloud,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='VEC':
            fcst_df_dangjin.loc[row_idx, 'WindDirection'] = float(data['fcstValue'])
            print('category:WindDirection,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='WSD':
            fcst_df_dangjin.loc[row_idx, 'WindSpeed'] = float(data['fcstValue'])
            print('category:WindSpeed,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'], '\n')
            row_idx+=3            
fcst_df_dangjin = fcst_df_dangjin.loc[0:23]
fcst_df_dangjin.to_csv(datetime.today().strftime("%Y%m%d")+'_20h_dang.csv', index=False)

queryParams = '?' + urllib.parse.urlencode(
    {
        urllib.parse.quote_plus('ServiceKey') : ServiceKey,
        urllib.parse.quote_plus('numOfRows') : '113', # 총 14개의 항목을 3시간 단위로 순차적으로 불러옵니다. 다음날 24시간예보에 필요한 만큼만 가져왔습니다.
        urllib.parse.quote_plus('dataType') : 'JSON', # JSON, XML 두가지 포멧을 제공합니다.
        urllib.parse.quote_plus('base_date') : datetime.today().strftime("%Y%m%d"), # 예보 받을 날짜를 입력합니다. 최근 1일간의 자료만 제공합니다.
        urllib.parse.quote_plus('base_time') : '2300', # 예보 시간을 입력합니다. 2시부터 시작하여 3시간 단위로 입력 가능합니다.
        urllib.parse.quote_plus('nx') : '53', # 당진 태양광 발전소 x 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
        urllib.parse.quote_plus('ny') : '114' # 당진 태양광 발전소 y 좌표입니다. '기상청18_동네예보 조회서비스_오픈API활용가이드.zip'에 포함 된 excel파일을 통해 확인 가능합니다.
    }
)

response = urllib.request.urlopen(url + queryParams).read()
response = json.loads(response, encoding="UTF-8")

fcst_df_dangjin_23 = pd.DataFrame()
date = datetime.today().strftime("%Y-%m-%d")
date = str(pd.to_datetime(date)+dt.timedelta(days=1))[0:10]
fcst_df_dangjin_23['Forecast_time'] = [f'{date} {hour}:00' for hour in range(3,24)]
row_idx = 0

for i, data in enumerate(response['response']['body']['items']['item']):
    if i > 0:
        if data['category']=='REH':
            fcst_df_dangjin_23.loc[row_idx, 'Humidity'] = float(data['fcstValue'])
            print('category:Humidity,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='T3H':
            fcst_df_dangjin_23.loc[row_idx, 'Temperature'] = float(data['fcstValue'])
            print('category:Temperature,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='SKY':
            fcst_df_dangjin_23.loc[row_idx, 'Cloud'] = float(data['fcstValue'])
            print('category:Cloud,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='VEC':
            fcst_df_dangjin_23.loc[row_idx, 'WindDirection'] = float(data['fcstValue'])
            print('category:WindDirection,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'])
        elif data['category']=='WSD':
            fcst_df_dangjin_23.loc[row_idx, 'WindSpeed'] = float(data['fcstValue'])
            print('category:WindSpeed,',data['category'], 'baseTime:',data['baseTime'], ', fcstTime:', data['fcstTime'], ', fcstValue:', data['fcstValue'], '\n')
            row_idx+=3            
fcst_df_dangjin_23 = fcst_df_dangjin_23.loc[0:23]
fcst_df_dangjin_23.to_csv(datetime.today().strftime("%Y%m%d")+'_23h_dang.csv', index=False)