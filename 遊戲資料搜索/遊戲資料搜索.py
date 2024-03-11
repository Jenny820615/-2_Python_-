import csv
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import chardet

fn = "armors_jp.csv"

# 使用chardet套件自動檢測編碼
with open(fn, 'rb') as f:
    result = chardet.detect(f.read())
encoding = result['encoding']

# 指定header=None，表示將所有行都當作資料，不將第一行視為索引
df = pd.read_csv(fn, usecols=[1], encoding=encoding, header=None)
search_page = df[1].values.tolist()

# 建立list存放網址
addresses=[]

driver=webdriver.Chrome()
driver.implicitly_wait(3)
driver.get("https://w.atwiki.jp/rockyou11")

# 輸入期別進行查詢
for i in search_page:    
    element=driver.find_element(By.NAME,"keyword")
    element.click()
    element.clear()
    element.send_keys(i)
    element.send_keys(Keys.RETURN)
    
    html=driver.page_source 
    soup=bs(html,"lxml")
    try:
        address=soup.find('div',id='wikibody').find('li').find('a')
        addresses.append('https:'+address.get('href'))
    except AttributeError:
        addresses.append('検索条件にあてはまる結果はありませんでした。')
driver.quit()

# 儲存回CSV檔案，指定header=False，表示不將第一行當作列索引寫入
df = pd.read_csv(fn,sep=',', encoding=encoding, header=None)
df.insert(2, '新欄位', addresses)
df.to_csv('armors_jp.csv', index=False, encoding=encoding, header=False)
