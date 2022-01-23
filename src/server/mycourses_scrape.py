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

def click(driver, elem):
	driver.execute_script("return arguments[0].click()",elem)

def getShadowRoot(driver, host):
    shadowRoot = driver.execute_script("return arguments[0].shadowRoot", host)
    return shadowRoot

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

def get_to_course(driver, course):
	
	time.sleep(7)
	Xpath = '/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/d2l-expand-collapse-content/div/d2l-my-courses'
	root = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath))).shadow_root
	root = root.find_element(By.CSS_SELECTOR, 'd2l-my-courses-container').shadow_root #CHROME DRIVER SHADOWROOTS ONLY WORK WITH CSS
	root = root.find_element(By.CSS_SELECTOR, 'd2l-tabs') 
	root = root.find_element(By.CSS_SELECTOR, 'd2l-tab-panel')
	root = root.find_element(By.CSS_SELECTOR, 'd2l-my-courses-content').shadow_root 
	root = root.find_element(By.CSS_SELECTOR, 'd2l-my-courses-card-grid').shadow_root 
	tabs = root.find_elements(By.CSS_SELECTOR, 'd2l-enrollment-card')

	cards = [tab.shadow_root.find_element(By.CSS_SELECTOR, 'd2l-card') for tab in tabs]
	card = (card for card in cards if course in card.get_attribute('text')).__next__()
	
	click(driver, card.shadow_root.find_element(By.CSS_SELECTOR, 'div > a'))

def get_to_content(driver):

	Xpath = '/html/body/header/nav/d2l-navigation/d2l-navigation-main-footer/div/div/div[1]/a'
	root = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))
	click(driver, root)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://mycourses2.mcgill.ca/d2l/loginh/?target=%2fd2l%2fhome')

try:
	get_to_courses(driver)
except selenium.common.exceptions.TimeoutException:
	print("Took too long to authentificate")

get_to_course(driver, "MATH-340")
get_to_content(driver)
#GET TERM TAB


#tabs = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, Xpath)))


time.sleep(5)
driver.close()