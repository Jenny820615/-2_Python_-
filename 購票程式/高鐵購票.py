import requests
import time
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

url='https://irs.thsrc.com.tw/IMINT/?locale=tw'
# 開啟瀏覽器
driver = webdriver.Chrome()
driver.get(url)

# 同意cookies
driver.implicitly_wait(3)
element=driver.find_element(By.CSS_SELECTOR,"#cookieAccpetBtn")
element.click()

# 出發站:依出發站的value
driver.implicitly_wait(3)
select_Start=Select(driver.find_element(By.NAME,"selectStartStation"))
select_Start.select_by_value('2')
# 抵達站:依抵達站的value
driver.implicitly_wait(3)
select_Destination=Select(driver.find_element(By.NAME,"selectDestinationStation"))
select_Destination.select_by_value('12')

# 選出發日期:依日期的XPATH
driver.implicitly_wait(3)
element=driver.find_element(By.XPATH,"//*[@id=\"BookingS1Form\"]/div[3]/div[2]/div/div[1]/div[1]/input[2]")
element.click()
driver.implicitly_wait(3)
element=driver.find_element(By.XPATH,"//*[@id=\"mainBody\"]/div[9]/div[2]/div/div[2]/div[1]/span[33]")
element.click()

# 選擇出發時間:依時間的value
driver.implicitly_wait(3)
select_Destination=Select(driver.find_element(By.XPATH,"//*[@id=\"BookingS1Form\"]/div[3]/div[2]/div/div[2]/div[1]/select"))
select_Destination.select_by_value('630A')

# 選擇全票張數:依張數的value
driver.implicitly_wait(3)
select_Destination=Select(driver.find_element(By.XPATH,"//*[@id=\"BookingS1Form\"]/div[4]/div[1]/div[1]/div/select"))
select_Destination.select_by_value('3F')


# # 輸入驗證碼欄位
# element=driver.find_element(By.ID,"securityCode")
# element.click()
# verifyCode=input('請輸入驗證碼')
# element.send_keys(verifyCode)

# driver.find_element(By.ID,'SubmitButton').click()
# driver.implicitly_wait(10)