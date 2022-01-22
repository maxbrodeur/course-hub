from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

#HELPERS

def delayed_send_keys(element, keys):
	for key in keys:
		element.send_keys(key)
		time.sleep(0.1)

def auth(username_txt, password_txt, email, passwd):
	count = 4
	trying = True
	while trying and count>0:
		try:
			username_txt.send_keys(email)
			password_txt.send_keys(passwd)
			trying = False
		except selenium.common.exceptions.UnexpectedAlertPresentException:
			count -= 1
			username_txt.clear()
			password_txt.clear()
			time.sleep(0.5)

	if trying: exit(-1)

EMAIL = ""
PASSWD = ""

driver = webdriver.Safari()
driver.get('https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin')
time.sleep(3) #	wait for load

Xpath = "//input[@id='mcg_un']"
username_txt = driver.find_element(By.XPATH, Xpath)


Xpath = "//input[@id='mcg_pw']"
password_txt = driver.find_element(By.XPATH, Xpath)

auth(username_txt, password_txt, EMAIL, PASSWD)

password_txt.send_keys(Keys.RETURN)

# BREACHED THE MAINFRAME
time.sleep(2)

Xpath = "/html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a"
student_menu = driver.find_element(By.XPATH, Xpath)
print(student_menu.get_attribute('text'))
student_menu.click()



time.sleep(5)
driver.close()