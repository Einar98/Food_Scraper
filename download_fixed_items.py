from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
import time 
from bs4 import BeautifulSoup 
import pandas as pd 

def scroll_to_bottom(driver):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)

def reached_bottom_page(driver) -> bool:
    if driver.execute_script('return window.innerHeight + window.pageYOffset >= document.body.offsetHeight'):
        return True 
    return False

def accept_cookies(driver):
    driver.find_element(By.XPATH, "//span[contains(text(), 'Godta alle cookies')]").click()
    time.sleep(1) 

def get_offerings_from_kiwi_page(data, driver, offerings:list):
    # driver.get(url)
    # time.sleep(3) 
    # driver.maximize_window() 
    # get the links. 
    links = driver.find_elements(By.XPATH, "//a[@href]") 
    # filter the links 
    for i in range(len(links)):
        content = links[i].text 
        # data = get_data(content) 
        if data is None:
            pass 
        else:
            if data in offerings:
                print("already in list") 
            else:
                offerings.append(data)  

def scrape_kiwi(): 
    url = "https://kiwi.no/aktuelt/dagligvarer/prissjekk/"
    driver = webdriver.Chrome() 
    driver.get(url=url)
    time.sleep(3)
    driver.maximize_window() 
    offerings = [] 
    print("Start fetching prices ...")
    while True:
        # get_offerings_from_page(url, driver, offerings)  
        if reached_bottom_page(driver):
            print("Reached bottom of page.")
            break
        # scroll down. 
        driver.execute_script('window.scrollBy(0, 1000)') 
        # wait for loading. 
        time.sleep(3) 

    print("Done scraping.") 
    driver.quit()
    return offerings

def open_page(driver, url):
    driver.get(url=url)
    time.sleep(2)
    driver.maximize_window()
    time.sleep(2) 

def get_pre_price(content:str) -> float:
    left_space = False 
    right_space = False 
    for letter in content:
        pass 

def strip_spaces(data:list) -> list:
    new_data = [] 
    for content in data:
        new_data.append(content.replace(" ", "")) 
    return new_data

def remove_spaces(data:list) -> list:
    new_data = [] 
    for content in data:
        if content == " ":
            pass 
        else:
            new_data.append(content) 
    return new_data

def contains_price(string:str) -> bool:
    numbers = "1234567890" 
    numbers_true = False 
    if "," not in string:
        return False 
    else:
        for element in string:
            if element not in numbers:
                return False 
        return True

def contains_text(content:str):
    abc = "abcdefghijklmnopqrstuvwxyz" 
    ABC = abc.upper() 
    for small_letter, big_letter in zip(abc, ABC):
        if small_letter in content or big_letter in content:
            return True
    return False 

def get_date(data:str) -> str:
    data = data.split("T.O.M. ") 
    return data[len(data) - 1]

driver = webdriver.Chrome() 
url = "https://kiwi.no/aktuelt/dagligvarer/prissjekk/"
open_page(driver, url)
elems = driver.find_elements(By.TAG_NAME, "tr") 

def fetch_prices():
    for elem in elems:
        if elem.text == " "*len(elem.text):
            pass 
        elif "    " in elem.text:
            content = elem.text.split(" "*15)
            content = remove_spaces(content)
            # content = strip_spaces(content)
            print(content) 
        else:
            date = get_date(elem.text)
            data = elem.text.split(" ") 
            print(date)

fetch_prices()
