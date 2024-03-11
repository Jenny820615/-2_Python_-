# -*- coding: utf-8 -*-

import time
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

web=input('請輸入拓元售票訂購網址(有立即訂購之頁面)：')
account_number=input('請輸入FB會員帳號：')
password=input('請輸入FB會員密碼：')
start_time=input('請輸入開放搶票時間(ex：13:00:00)時/分/秒：')
sessions=str(input('請輸入第幾場次(若只有一場請輸入0)：'))
price=str(input('請輸入欲購買的區域&票價(ex:2樓2F區3800，若不分區域票價請填0)：'))
tickets=input('請輸入欲購買張數(1~4)：')


driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(web)

# 會員登入
element=driver.find_element(By.CLASS_NAME,"justify-content-center").click()
driver.implicitly_wait(10)
# facebook登入，要關閉雙重驗證
element=driver.find_element(By.ID,"facebook").click()
# 輸入帳號
element=driver.find_element(By.ID,"email")
element.click()
element.send_keys(account_number)
element=driver.find_element(By.ID,"pass")
element.click()
element.send_keys(password)
element=driver.find_element(By.ID,"loginbutton").click()
driver.implicitly_wait(10)
# 接受所有cookie
element=driver.find_element(By.ID,"onetrust-accept-btn-handler").click()
# 等時間到了再執行
current_time = datetime.now().time()
target_time = datetime.strptime(start_time, "%H:%M:%S").time()
while current_time < target_time:
    time.sleep(0.0001)  # 每0.0001秒檢查一次
    current_time = datetime.now().time()

driver.implicitly_wait(10)
# 立即訂購(上)-各場次都一樣     
element=driver.find_element(By.XPATH,"//*[@id=\"tab-func\"]/li[1]/a/div")
# selenium無法點可能是元素重疊或隱藏，透過執行JavaScript來點擊元素。
# arguments[0] 代表傳遞給 execute_script()方法的第一個參數，即我們要點擊的element物件。等於click()
driver.execute_script("arguments[0].click();", element)

# 立即訂購(下):tr[第幾場(從1開始)]，若只有一場就沒有索引
if sessions=='0':
    session='//*[@id=\"gameList\"]/table/tbody/tr/td[4]/button'
else:
    session='//*[@id=\"gameList\"]/table/tbody/tr['+sessions+']/td[4]/button'
driver.implicitly_wait(360)
element=driver.find_element(By.XPATH,session)
driver.execute_script("arguments[0].click();", element)

# 選區域票價:部份票價在<li>、部份在<a>。部份是均一票價不用選擇，就需直接跳過此段。
# 先尋找所有符合條件的 <a> 元素和 <li> 元素
if price != '0':
    elements = driver.find_elements(By.XPATH, "//a[contains(.,'"+price+"')]")
    # if not elements是條件判斷，檢查elements是否為空或False。如果是則進入if區塊中的程式碼。
    if not elements:
        elements = driver.find_elements(By.XPATH, "//li[contains(.,'"+price+"')]")
    # 找到第一個符合條件的元素，然後點選。預防售完的票價無法點選，導致整個程式需從頭輸入資料重新跑。
    for element in elements:
        try:
            driver.execute_script("arguments[0].click();", element)
            break  # 成功找到並點選元素後，跳出迴圈，繼續往下執行
        except:
            pass  # 如果點選失敗，繼續尋找下一個符合條件的元素

# 選擇張數-用select函數建立物件
select_ticket=Select(driver.find_element(By.CLASS_NAME,'form-select'))
select_ticket.select_by_value(str(tickets))

# 我已詳細閱讀，有的訂購網頁即便ID或XPATH無誤仍無法正常點選導致頁面關閉
# 故用try except若點不到即跳過，不會導致頁面關閉無法手動輸入相關資料
driver.implicitly_wait(360)
driver.find_element(By.ID,'TicketForm_agree')
try:
    element.click()
except:
    pass
print('...請回到網頁填寫驗證碼及後續相關付款資料!!...')

# 點選輸入驗證碼欄位，有的訂購網頁即便ID或XPATH無誤仍無法正常點選導致頁面關閉
# 故用try except若點不到即跳過，不會導致頁面關閉無法手動輸入相關資料
driver.implicitly_wait(360)
element=driver.find_element(By.ID,"TicketForm_verifyCode")
try:
    element.click()
except:
    pass
# For匯出的執行檔不要關閉
input()

# verifyCode=input('請輸入驗證碼')
# element.send_keys(verifyCode)

# # 確認訂購
# element=driver.find_element(By.XPATH,"//*[@id=\"form-ticket-ticket\"]/div[4]/button[2]")
# element.click()