from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

email = "max.brodeur@mail.mcgill.ca"
passwd = "kingofthepirates"

def click(driver, elem):
	driver.execute_script("return arguments[0].click()",elem)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://mycourses2.mcgill.ca/d2l/loginh/?target=%2fd2l%2fhome')

time.sleep(1)
Xpath = '//*[@id="link1"]'
mcgill_btn = driver.find_element(By.XPATH, Xpath)
click(driver, mcgill_btn)

time.sleep(1)
Xpath = '//*[@id="i0116"]'
email_txt = driver.find_element(By.XPATH, Xpath)
email_txt.send_keys(email)

Xpath = '//*[@id="idSIButton9"]'
next_btn = driver.find_element(By.XPATH, Xpath)
click(driver, next_btn)

time.sleep(3)
Xpath = '//*[@id="passwordInput"]'
passwd_txt = driver.find_element(By.XPATH, Xpath)
passwd_txt.send_keys(passwd)

Xpath = '//*[@id="submitButton"]'
submit_btn = driver.find_element(By.XPATH, Xpath)
click(driver, submit_btn)

#AUTHENTIFICATOR!!!!
time.sleep(2)
Xpath = '//*[@id="idDiv_SAOTCAS_Title"]'
authentificator = driver.find_element(By.XPATH, Xpath)
print(authentificator.text)


time.sleep(5)
driver.close()