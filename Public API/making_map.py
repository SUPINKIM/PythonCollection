import urllib.request 
import pprint as pp
import json
import sys
import io
from json import JSONDecodeError

import folium


#json을 활용한 지도 그리기(국문관광정보서비스)
ServiceKey = "" #개인 인증키
url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaCode?ServiceKey='+ServiceKey+'&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=TestApp&_type=json' #지역코드 조회
url2 = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey='+ServiceKey+'&numOfRows=10&pageNo=3&MobileOS=ETC&MobileApp=TestApp&_type=json&areaCode=1&cat1=A02&listYN=Y' #지역기반 관광정보 조회(인문/문화/역사)

request = urllib.request.Request(url2)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    #print(response_body.decode('utf-8'))
    try:
        dict1 = json.loads(response_body.decode('utf-8')) #utf-8로 파싱
        pp.pprint(dict1)
        #print(len(dict1['response']['body']['items']['item']))
        
        map_osm=folium.Map(location=[37.4922691511,126.8634058253], zoom_start=11) #기본 포커스 
        
        #print(dict1['response']['body']['items']['item'][0]['addr1']) # 각 addr1를 뽑기 위해서는 n차원 배열처럼 인덱싱을 해줘야 함. 바로 addr1로 접근 불가.
        for i in range(len(dict1['response']['body']['items']['item'])) : 
            mapx= dict1['response']['body']['items']['item'][i]['mapx']  #x좌표
            mapy= dict1['response']['body']['items']['item'][i]['mapy']  #y좌표
            title = dict1['response']['body']['items']['item'][i]['title'] #장소 이름
            addr = dict1['response']['body']['items']['item'][i]['addr1']  #장소 주소
            
            popup = folium.Popup('<b>'+title+'</b>\n'+addr,max_width=125) #팝업창 텍스트 및 크기
            folium.Marker([mapy,mapx], popup=popup, icon=folium.Icon(color='lightgreen')).add_to(map_osm) #마커 위치 및 팝업스타일 지정
            map_osm.save('map8.html')
            
    except JSONDecodeError as e: 
        dict1 = response_body #그대로 출력
        print(dict1)
    #pprint(dict)
else:
    print("Error Code:" + rescode)
