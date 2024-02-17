from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
import time 
from bs4 import BeautifulSoup 
import pandas as pd 
import os 

""" This script fetches the store offerings from etilbudsavis.no from a given store """

# url = "https://www.rema.no/kampanjevarer/1000-fryste-priser/"

# driver.get(url=url)

# time.sleep(3) 

# this one works. 
# <a id="CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll" class="CybotCookiebotDialogBodyButton" href="#" tabindex="0" lang="nb" style="width: 210px; display: block;">Kun nødvendige </a>
# <a id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll" class="CybotCookiebotDialogBodyButton" href="#" tabindex="0" lang="nb" style="width: 210px; display: block;">Godta alle</a>
# driver.find_element(By.XPATH, "//span[contains(text(), 'Godta cookies')]").click()

# this one works for rema 100. 
# driver.find_element(By.XPATH, "//a[contains(text(),'Godta alle')]").click()

# retrieves the data for each link. 
def get_data(content:str) -> bool:
    data = content.split("\n") 
    if len(data) == 4:
        return {"title":data[0], "kg price":data[1], "price":data[2], "time":data[3]}
    return None 

def scroll_to_bottom(driver):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)

def get_offerings_from_page(url, driver, offerings:list):
    # driver.get(url)
    # time.sleep(3) 
    # driver.maximize_window() 
    # get the links. 
    links = driver.find_elements(By.XPATH, "//a[@href]") 
    # filter the links 
    for i in range(len(links)):
        content = links[i].text 
        data = get_data(content) 
        if data is None:
            pass 
        else:
            if data in offerings:
                print("already in list") 
            else:
                offerings.append(data)  

def reached_bottom_page(driver) -> bool:
    if driver.execute_script('return window.innerHeight + window.pageYOffset >= document.body.offsetHeight'):
        return True 
    return False

def get_kiwi_offerings():
    url = "https://etilbudsavis.no/KIWI/tilbud"
    driver = webdriver.Chrome()
    driver.get(url=url)
    time.sleep(3)
    driver.maximize_window() 

# get_kiwi_offerings()

def scrape_store_offerings(store:str): 
    url = "https://etilbudsavis.no/" + store + "/tilbud" 
    op = webdriver.ChromeOptions() 
    op.add_argument("headless")
    driver = webdriver.Chrome(options=op) 
    driver.get(url=url)
    time.sleep(3)
    driver.maximize_window() 
    offerings = [] 
    print("Start fetching prices ...")
    while True:
        get_offerings_from_page(url, driver, offerings)  
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

# transforms the data to pandas dataframe. 
def transform_to_df(offerings:list):
    # create and save a dataframe containing the data. 
    df = pd.DataFrame(columns=list(offerings[0].keys())) 
    # loop through each dictionary. 
    for data in offerings:
        offering_data = list(data.values())  
        df.loc[len(df)] = offering_data 
    # returns the dataframe.   
    return df 

def save_as_csv(df, title) -> None:
    root = os.getcwd() + "/Stores/"
    df.to_csv(root + title + ".csv")

# store names. 
stores = ['Coop-Extra', 'KIWI', 'Bunnpris', 
          'Coop-Mega', 'Coop-Prix', 'Joker', 'Europris', 
          'Matkroken', 'MENY', 'Naerbutikken', 
          'REMA-1000', 'SPAR', 'oda', 'Coop-Marked', 'Obs', 'Gigaboks'] 

# main. 
def get_updated_offers(stores):
    # get the offerings from the store. 
    size = len(stores)
    for indx, store in enumerate(stores):
        offerings = scrape_store_offerings(store) 
        # save only if there are any offers available. 
        if len(offerings) > 0:
            # transform it to a dataframe. 
            df = transform_to_df(offerings) 
            # save as csv. 
            save_as_csv(df, store) 
            # print progress. 
            print(f"Progress: {100*round((indx + 1)/size, 2)}%")
        else:
            print(f"Error, {store} has no offers available.")
            print(f"Progress: {100*round((indx + 1)/size, 2)}%")

if __name__ == "__main__":
    pass 

