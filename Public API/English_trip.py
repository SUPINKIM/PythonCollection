import urllib.request 
#import xmltodict
import json
import sys
import io
from json import JSONDecodeError


ServiceKey = "개인 API 인증키" 

url = "http://api.visitkorea.or.kr/openapi/service/rest/EngService/detailIntro?ServiceKey="+ServiceKey+"&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=TestApp&&contentId=621155&contentTypeId=78&introYN=Y"
#요청 파라미터 넣어서 호출(api 가이드 문서의 예제와 동일한 파라미터 사용)

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
    try:
        dict = json.loads(response_body.decode('utf-8'))
    except JSONDecodeError as e:  
        dict = response_body #그대로 출력
    print(dict)
else:
    print("Error Code:" + rescode)
