from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

#driver = webdriver.Chrome(ChromeDriverManager().install())

#사파리로 web crawling하기 
driver = webdriver.Safari(executable_path = '/usr/bin/safaridriver')
driver.implicitly_wait(3)

driver.get('http://gs25.gsretail.com/gscvs/ko/products/event-goods#;')
html = driver.page_source 
soup = BeautifulSoup(html,'html.parser')

temporary = [] #임시 배열
pagenumber_array = [] #페이지 숫자 담는 배열
gift_array = [] # 덤증정 

           
def extraction(tabButton): #필요한 정보를 긁어오기 위한 함수
    time.sleep(3)
    p_name = [] #상품명
    p_price = [] #상품가격
    p_promotion = [] #상품 프로모션 종류
    product_images_array = [] # 상품 이미지 배열
        
    p_names = driver.find_elements_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div['+str(tabButton)+']/ul/li/div/p[2]')
    p_prices = driver.find_elements_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div['+str(tabButton)+']/ul/li/div/p[3]/span')
    p_promotions = driver.find_elements_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div['+str(tabButton)+']/ul/li/div/div/p/span')
    
    for n in p_names:
        p_name.append(n.text)

    for n in p_prices:
        p_price.append(n.text)
        
    for n in p_promotions:
        p_promotion.append(n.text)
    
    i=0
    while i < len(p_price):
        a = p_price[i]  #임시 저장
        a = a[:-1] #원 제거
        string = "".join(a) #스트링 변환
        try:
            b = string.index(',') #위치값 리턴
            c = a[b+1:] #콤마 이후부터
            a = a[:b] #콤마 전까지
            p_price[i] = a+c #자른 문자열 합치기
        
        except ValueError as e:
            p_price[i] = a #1000 이하 가격의 제품일 때
        
        finally:
            i=i+1
        
    j = 0
    while j < len(p_name):
        print(p_name[j])
        print(p_price[j])
        print(p_promotion[j])
        j=j+1
        
    product_images_all = driver.find_elements_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div['+str(tabButton)+']/ul/li/div/p[1]/img')
    product_img_count = len(product_images_all) #전체 상품 개수가 8개 미만인 페이지의 경우
    
    if (product_img_count == len(p_name)):
        total = product_img_count
    else:
        total = len(p_name)

    for n in range(1,9):
        try:
            product_images = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div['+str(tabButton)+']/ul/li['+str(n)+']/div/p[1]/img')
            img_one = product_images.get_property('src')
            product_images_array.append(img_one)
            print(img_one)
            
            if (product_img_count < 8 and n == total):
                break
        except:
            product_images_array.append('이미지 준비중')
            print('이미지 준비중')
              
    driver.implicitly_wait(10)

def setbutton(promotionbutton,numberbutton): # 숫자(페이지) 버튼을 눌러 다음 페이지로 이동
    driver.implicitly_wait(20)
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div['+str(promotionbutton)+']/div/span/a['+str(numberbutton)+']').click()
    time.sleep(1)
                                           
    
def promotionTab(tabButton): # 1+1,2+1,덤증정 이동하는 함수
    driver.implicitly_wait(20)
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/ul/li['+str(tabButton)+']/span').click()
    time.sleep(1)
    
def gift_product_extraction(): #덤증정 상품 이미지와 이름을 뽑는 메소드(가격은 text가 None으로 계속 나와서 못 뽑음:( )
    driver.implicitly_wait(20)
    d_img = driver.find_elements_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div[3]/ul/li/div/div[2]/div[2]/p[2]/img')
    
    d_names=[] #덤 상품 이름
    d_imgs=[] #덤 상품 이미지 


    for n in d_img:
        img_one=n.get_attribute('src') #속성 src
        img_n = n.get_attribute('alt') #속성 alt
        d_imgs.append(img_one)
        d_names.append(img_n)


    i=0
    while i < len(d_imgs):
        print(d_imgs[i])
        gift_array.append(d_imgs[i])
        print(d_names[i])
        gift_array.append(d_names[i])
        i=i+1
        
    return gift_array
              
def next_extraction(tabButton): #next버튼 누르기 
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div['+str(tabButton)+']/div/a[3]').click() #next 버튼 누르기
    time.sleep(2)

    
def page_number_ext(tabButton): #페이지 넘버 추출한 뒤 extraction() 을 호출해 해당 페이지 추출하는 메소드 
    time.sleep(1)
    pages = driver.find_elements_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div['+str(tabButton)+']/div/span')    
    p_tem = [] #한 페이지에 보이는 숫자 페이지 리스트
    
    for i in pages:
        p_tem.append(i.text)
    p_tem = p_tem[0]
    p_tem = p_tem.split(' | ') # 한 페이지에 보이는 숫자 저장
    print(p_tem)
    count = len(p_tem) #next 버튼을 누른 이후에 페이지 개수 세는 변수(왜냐하면 10이 넘어가면 11,12..73..이런 식으로 뽑히는데 어차피 필요한 건 1부터 10까지임. 동일하게 1-10으로 들어감)
    
    i = 1
    while i <= count:
        try:
            time.sleep(4)
            driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div['+str(tabButton)+']/div/span/a['+str(i)+']').click()
            time.sleep(2)
            
            if(tabButton == 3): #덤증정 탭일 경우, 덤 증정 상품을 크롤링하는 함수 호출
                gift_product_extraction()
            
            now_page = driver.find_element_by_css_selector('div.tblwrap.mt50 > div.paging > span.num > a.on') # 현재 보여지고 있는 페이지 값 저장
            extraction(tabButton)
            

            
        except TimeoutException as e:
            print(e)
        finally:
            i=i+1
    
    next_extraction(tabButton)
    next_page =driver.find_element_by_css_selector('div.tblwrap.mt50 > div.paging > span.num > a.on') # next버튼 누른 후에 보여지고 있는 페이지 값 저장
    
    if (now_page == next_page):
        finish = True
    else: 
        finish = False
        page_number_ext(tabButton)
    
    if (finish == True):  #끝페이지까지 크롤링이 완료되었다면 함수 종료
        return 0    
    
    
def GS_ONEplusONE():  
    time.sleep(2)
    promotionTab(1)
    page_number_ext(1)


def GS_TWOplusONE():
    time.sleep(2)
    promotionTab(2)
    page_number_ext(2)

def GS_Dum():
    time.sleep(2) 
    promotionTab(3)
    page_number_ext(3)


#GS_ONEplusONE()
#time.sleep(5)
GS_TWOplusONE()
time.sleep(5)
GS_Dum()
