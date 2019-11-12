# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 00:38:55 2019

@author: Abner
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

def SelectData(data,key):
    for j in data:
        if key in j.text:
            return j.text.split('：')[1]
    return 'N'
def SelectDataClass(data,key,recolumns):
    for j in data:
        if key in j['class']:
            return j[recolumns]

def SelectDataId(data,key,recolumns):
    for j in data:
        if key in j['id']:
            return j[recolumns]
        
def SelectData2(data,key):
    for j in data:
        if key in j.text.replace("\xa0", ""):
            return j.text.replace("\xa0", "")
    return '現況:N'
        
options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
#options.add_argument('--headless')
driver= webdriver.Chrome(chrome_options = options)
driver.get('https://rent.591.com.tw/?kind=0&region=1')
for dd in driver.find_elements_by_tag_name("dd") : #找到縣市案紐並點擊
    if dd.get_attribute('data-id')=='3':
        dd.click()
        break
time.sleep(3)
df=pd.DataFrame(columns=['_id','city','name','grnder','cellPhone',
                         'tel','mail','objType','size','Types','situation','claim','price']) #自訂蒐集資料欄位

while 1:
    getData=[]
    obj=driver.find_elements_by_class_name('listInfo') #取得頁面中所有房屋物件
    fhand = driver.window_handles[0]
    for o in obj:
        time.sleep(1)
        situation=BeautifulSoup(o.find_element_by_css_selector("p.lightBox").get_attribute('innerHTML'), 
                                'html.parser').text.replace("\n", "").replace("\xa0", "").replace(" ", "").split('|')[0] #取得指定物件內容
        if situation!='車位': 
            o.click()
            
            time.sleep(1)
            driver.implicitly_wait(30)
            handles = driver.window_handles      #網頁所有分頁
            driver.switch_to.window(handles[1])  #切換控制頁
            try:                                 #因有些物件會移除或連結失敗 為了讓程式繼續順利執行做錯誤判斷
                detail=driver.find_elements_by_class_name('detailInfo')[0].get_attribute('innerHTML')
                detailSoup = BeautifulSoup(detail, 'html.parser')
                #situation = SelectData2(detailSoup.find_all('li'),'現況').split(':')[1]
             
                dataid=driver.find_element_by_id('propNav').find_element_by_tag_name('i').get_attribute('innerHTML')[1:-1]
                city=driver.find_element_by_id('propNav').find_elements_by_tag_name('a')[2].get_attribute('innerHTML')
                size = re.sub("\D", "",SelectData2(detailSoup.find_all('li'),'坪數'))
                Type = SelectData2(detailSoup.find_all('li'),'型態').split(':')[1]
                
                price = int(re.sub("\D", "",detailSoup.find('i').text))
                
                userInfo = driver.find_element_by_css_selector("div.userInfo").get_attribute('innerHTML')
                userInfoSoup = BeautifulSoup(userInfo, 'html.parser')
                a = userInfoSoup.find_all('span')
                name=SelectDataClass(a,'kfCallName','data-name')
                if '先生' in name:
                    gender = 'M'
                elif '小姐' in name:
                    gender = 'F'
                else:
                    gender = 'N'
                    
                mobile=SelectDataClass(a,'dialPhoneNum','data-value')
                
                b = userInfoSoup.find_all('input')
                tel = SelectDataId(b,'hid_tel','value')
                mail = SelectDataId(b,'hid_email','value')
                
                if '（屋主' in userInfoSoup.find('div', {'class': 'avatarRight'}).find_all('div')[0].text:
                    objType = '屋主'
                elif '(仲介' in userInfoSoup.find('div', {'class': 'avatarRight'}).find_all('div')[0].text:
                    objType = '仲介'
                elif '（代理人）' in userInfoSoup.find('div', {'class': 'avatarRight'}).find_all('div')[0].text:
                    objType = '代理人'
                else:
                    objType = -1
                    print(userInfoSoup.find('div', {'class': 'avatarRight'}).find_all('div')[0].text)
                   
                labelList = driver.find_element_by_css_selector("ul.labelList-1").get_attribute('innerHTML')
                lableSoup = BeautifulSoup(labelList, 'html.parser')
                claim=SelectData(lableSoup.find_all('li'),'性別要求')
                getData.append([dataid,city,name,gender,mobile,tel,mail,objType,size,Type,situation,claim,price])
            
                driver.close()
                driver.switch_to.window(fhand)
                driver.implicitly_wait(30)
                time.sleep(2)
            except IndexError:  #如果頁面是沒有物件的關閉頁面轉換控制頁面 繼續迴圈
                driver.close()
                driver.switch_to.window(fhand)
                driver.implicitly_wait(30)
                time.sleep(2)
            
        
    if driver.find_elements_by_class_name('pageNext')[0].get_attribute('href')=='javascript:;':  #程式碼判斷 下一頁是否有href='javascript:;' 因最後一頁是沒有的 當執行到最後一頁就是程式結束的時候
        driver.find_elements_by_class_name('pageNext')[0].click()
        time.sleep(5)
        df2=pd.DataFrame(data=getData,columns=['_id','city','name','grnder','cellPhone','tel','mail','objType','size','Types','situation','claim','price'])
        df=df.append(df2, ignore_index = True)  #資料儲存至Dataframe
    else:
        break

# rent591=pd.read_csv('rent591.csv',encoding='utf-8')
# rent591=rent591.append(df, ignore_index = True) 
# rent591.to_csv('rent591.csv',index=False,encoding='utf-8')

# rent591.groupby('_id').size().sort_values()
# rent591=rent591.drop_duplicates('_id','first',inplace=True)
# rent591.to_csv('rent591.csv',index=False,encoding='utf-8')