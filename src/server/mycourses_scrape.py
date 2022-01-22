from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

email = "max.brodeur@mail.mcgill.ca"
passwd = "kingofthepirates"
term = "Winter 2022"
course = "MATH 340"

def click(driver, elem):
	driver.execute_script("return arguments[0].click()",elem)

def get_to_courses(driver):
	Xpath = '//*[@id="link1"]'
	mcgill_btn = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	click(driver, mcgill_btn)

	Xpath = '//*[@id="i0116"]'
	email_txt = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	email_txt.send_keys(email)

	Xpath = '//*[@id="idSIButton9"]'
	next_btn = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	click(driver, next_btn)

	Xpath = '//*[@id="passwordInput"]'
	passwd_txt = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	passwd_txt.send_keys(passwd)

	Xpath = '//*[@id="submitButton"]'
	submit_btn = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	click(driver, submit_btn)

	#AUTHENTIFICATOR!!!!
	Xpath = '//*[@id="idDiv_SAOTCAS_Title"]'
	authentificator = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	print("AUTHENTIFICATOR")
	Xpath = '//*[@id="idChkBx_SAOTCAS_TD"]'
	chkbx = driver.find_element(By.XPATH, Xpath)
	click(driver,chkbx)
	Xpath = '//*[@id="lightbox"]/div[3]/div/div[2]/div/div[1]'
	element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	print("HERE!")
	Xpath = '//*[@id="idBtn_Back"]'
	no_btn = driver.find_element(By.XPATH, Xpath)
	click(driver,no_btn)

def get_to_tabs(driver):
	Xpath = '//*[@id="d2l_1_12_602"]'
	#root1 = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	no_btn = driver.find_element(By.XPATH, Xpath)
	print(no_btn)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://mycourses2.mcgill.ca/d2l/loginh/?target=%2fd2l%2fhome')

get_to_courses(driver)
#get_to_tabs(driver)
#GET TERM TAB


#tabs = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))






time.sleep(5)
driver.close()