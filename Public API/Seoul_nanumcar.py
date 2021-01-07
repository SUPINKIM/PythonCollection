import csv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

f = open('seoul_nanumcar.csv')
data = csv.reader(f)
header = next(data)  #header : 데이터 파일에서 여러 가지 값들이 어떤 의미를 갖는지 표시한 행
#print(header)

x = [] #x축 데이터 : 구분(연월)
y = [] #y축 데이터 : 차량 대수
for row in data:
    print(row)
    x.append(row[0])
    num = str.split(row[-1],',') #,가 있는 str이라 ,로 먼저 쪼개준 다음 하나의 str로 합친 후 int로 형 변환
    #print(num)
    row_y = num[0]+num[-1]
    #print("row_y : "+row_y)
    car_num = int(row_y)
    y.append(car_num)

print(x)
print(y)

plt.figure()  #그래프를 위한 액자 생성

#font_location = 'C:/Windows/Fonts/NanumGothic.ttf'
plt.rc('font',family='Malgun Gothic')
#plt.rcParams["font.family"] = 'NanumGothic'
#plt.rcParams['axes.unicode_minus'] = False  (축에서 -기호가 깨질 때 사용하는 코드)


plt.title('서울특별시 연도별 나눔카 차량대수 현황')
plt.xlabel('월')
plt.ylabel('차량대수')

plt.ylim(1000,6000)
plt.plot(y,marker='o', color='skyblue') #차량대수 값 넣음.

x_label = list(range(0, len(x)))
print(x_label)
plt.xticks(x_label,x)

fig = plt.gcf()
plt.show()
fig.savefig('seoul_nanumcar.png')   # 그래프 저장 확장자 : png
f.close()
