from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import Select

options=Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

driver.get('https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login')
time.sleep(1)
# manager login
driver.find_element('xpath','//button[text()="Bank Manager Login"]').click()
time.sleep(1)
driver.find_element('xpath','//button[@ng-click="addCust()"]')
# do rest quickly

driver.find_element('xpath','//button[@ng-click="addCust()"]').click()
driver.find_element('xpath','//input[@ng-model="fName"]').send_keys('John')
driver.find_element('xpath','//input[@ng-model="lName"]').send_keys('Doe')
driver.find_element('xpath','//input[@ng-model="postCd"]').send_keys('12345')
driver.find_element('xpath','//button[text()="Add Customer"]').click()
al=driver.switch_to.alert
al.accept()

driver.find_element('xpath','//button[@ng-click="openAccount()"]').click()
Select(driver.find_element('id','userSelect')).select_by_visible_text('John Doe')
Select(driver.find_element('id','currency')).select_by_visible_text('Dollar')
driver.find_element('xpath','//button[text()="Process"]').click()
al=driver.switch_to.alert
al.accept()

driver.find_element('xpath','//button[text()="Home"]').click()
driver.find_element('xpath','//button[text()="Customer Login"]').click()
Select(driver.find_element('id','userSelect')).select_by_visible_text('John Doe')
driver.find_element('xpath','//button[text()="Login"]').click()

drivers=driver

# deposit and withdraw

wait_time=1

driver.find_element('xpath','//button[@ng-click="deposit()"]').click()
driver.find_element('xpath','//input[@ng-model="amount"]').send_keys('1000')
driver.find_element('xpath','//button[text()="Deposit"]').click()

driver.find_element('xpath','//button[@ng-click="withdrawl()"]').click()
amt_field = driver.find_element('xpath','//input[@ng-model="amount"]')
amt_field.clear(); amt_field.send_keys('200')
driver.find_element('xpath','//button[text()="Withdraw"]').click()

print('---strong tags---')
for el in driver.find_elements('xpath','//strong'):
    print(repr(el.text))

print('---page source snippet---')
p=driver.page_source
print(p[p.find('<strong'):p.find('Balance')+50])

print('---full page source---')
#write source to file for later
with open('page.html','w',encoding='utf8') as f:
    f.write(driver.page_source)

print('saved page.html')

driver.quit()
