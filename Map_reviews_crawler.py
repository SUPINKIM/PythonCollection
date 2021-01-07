# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 10:34:25 2019


"""

from selenium import webdriver
#import csv
from bs4 import BeautifulSoup 
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import emoji

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

#driver = webdriver.Chrome('C:/Users/paprikastory/Downloads/chromedriver_win32/chromedriver')
driver.implicitly_wait(3)
driver.get('https://play.google.com/store/apps/details?id=com.skplanet.tmaptaxi.android.passenger&hl=ko')

req = driver.page_source
soup=BeautifulSoup(req, 'html.parser')

#구글 플레이 리뷰 화면창 띄움 

#---------------webdriver 연결

#리뷰 모두 보기 버튼 클릭
driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[6]/div/span/span').click()

driver.implicitly_wait(3)

body = driver.find_element_by_tag_name('body')

scroll_down=50
#페이지 스크롤 다운
while scroll_down:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    scroll_down-=1
    
    try:
        more = driver.find_element_by_class_name('U26fgb O0WRkf oG5Srb C0oVfc n9lfJ M9Bg4d') #더보기 버튼이 나오면 클릭
        driver.execute_script("arguments[0].click();", more)
    except:
        None
        
time.sleep(5)

f=open('C:/Users/paprikastory/.spyder-py3/Tmap_Taxi_review.txt','a')

all_button = driver.find_elements_by_xpath("//button[text()='전체 리뷰']")   #전체 리뷰 버튼 모두 찾기
for i in all_button:
    driver.implicitly_wait(4)
    #i.send_keys(Keys.ENTER)
    driver.execute_script("arguments[0].click();", i)
#fcxH9b > div.WpDbMd > c-wiz:nth-child(4) > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div:nth-child(2) > div > div:nth-child(10) > div > div.d15Mdf.bAhLNe > div.UD7Dzf > span:nth-child(1) > div > button
    


#페이지에 있는 리뷰 전체 긁어오기 
re = driver.find_elements_by_class_name('UD7Dzf')
dates = driver.find_elements_by_class_name('p2TkOb')  #리뷰 작성 날짜   
date=[] 
for j in date:
    date.append(j.text)

print(date)
d=0
for j in re:
    print(j.text)
    review=j.text.encode('utf-8')
    allchars = [str for str in review.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in review.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    #f.writelines(date[d])
    #d+=1
    print(type(clean_text))
    f.writelines(clean_text)


driver.close()
f.close()

#//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/span[1]/div/button
#//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[10]/div/div[2]/div[2]/span[1]/div/button
#fcxH9b > div.WpDbMd > c-wiz:nth-child(4) > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div:nth-child(2) > div > div:nth-child(10) > div > div.d15Mdf.bAhLNe > div.UD7Dzf > span:nth-child(1) > div > button
