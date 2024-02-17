from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
import time 
from bs4 import BeautifulSoup 
import pandas as pd 

website = "https://www.adamsmatkasse.no/menyen"
driver = webdriver.Chrome()

# auto accept cookies. 
def accept_cookies(driver):
    driver.find_element(By.XPATH, "//span[contains(text(), 'Godta alle cookies')]").click()
    time.sleep(1) 



