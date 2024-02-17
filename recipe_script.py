import numpy as np 
import selenium
import bs4 
from bs4 import BeautifulSoup
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
import random 

# url = "https://www.adamsmatkasse.no/menyen" 
# op = webdriver.ChromeOptions()
# op.add_argument('headless')
# driver = webdriver.Chrome(options=op)

def accept_cookies(driver):
    driver.find_element(By.XPATH, "//span[contains(text(), 'Godta alle cookies')]").click()
    time.sleep(1) 

def contains_recipe(content:str) -> bool:
    key_word = "oppskrift" 
    content_lst = content.split("/")
    if key_word in content_lst:
        return True 
    return False

def scroll_down(driver):
    driver.execute_script('window.scrollBy(0, 1000)') 
    time.sleep(2) 

def reached_bottom_page(driver) -> bool:
    if driver.execute_script('return window.innerHeight + window.pageYOffset >= document.body.offsetHeight'):
        return True 
    return False

def get_recipe_links(driver, recipes:list, recipes_clicks:list):
    # driver.get(url) 
    elems = driver.find_elements(By.XPATH, "//a[@href]")
    for elem in elems:
        content = elem.get_attribute("href")
        if contains_recipe(content) and content not in recipes: 
            recipes.append(content) 
            recipes_clicks.append(elem)

def get_recipe_data(driver, recipe_link):
    recipes = [] 
    while True:
        get_recipe_links(driver, recipes)  
        if recipe_link in recipes:
            break 
        else:
            scroll_down() 
            time.sleep(1)
    # click the link 
    driver


# fetches ingredients from random recipe. 
def get_ingredients(driver, recipes, recipes_clicks, url):
    driver.get(url)
    time.sleep(3)
    driver.maximize_window()
    accept_cookies(driver) 
    get_recipe_links(driver, recipes, recipes_clicks) 
    number = random.randint(0, len(recipes) - 1)
    link = recipes_clicks[number] 
    link.click() 
    time.sleep(2)
    title = driver.find_elements(By.TAG_NAME, "h1")[1].text
    portions = driver.find_elements(By.CSS_SELECTOR, ".flex.items-center.justify-between.w-full.pb-2.border-b.border-black")[0].text
    amounts = driver.find_elements(By.CSS_SELECTOR, ".col-span-3.text-right")
    items = driver.find_elements(By.CSS_SELECTOR, ".flex.items-center.col-span-7.gap-2") 
    portions = portions.split("\n")[1]
    items_lst = [item.text for item in items] 
    amount_lst = [amount.text for amount in amounts] 
    ingredients = [] 
    for item, amount in zip(items_lst, amount_lst):
        ingredients.append((item, amount))
    return ingredients, portions, title, recipes[number] 

def click_first_link(driver, recipes, recipes_clicks):
    get_recipe_links(driver, recipes, recipes_clicks)
    link = recipes_clicks[0] 
    link.click() 
    time.sleep(3)
    tags = driver.find_elements(By.TAG_NAME, 'h3') 
    title = driver.find_elements(By.TAG_NAME, "h1")[1].text
    # basis_items = driver.find_elements(By.TAG_NAME, "li") 
    portions = driver.find_elements(By.CSS_SELECTOR, ".flex.items-center.justify-between.w-full.pb-2.border-b.border-black")[0].text
    food_items = driver.find_elements(By.CSS_SELECTOR, "w-10.h-10.shrink-0") 
    # element = driver.find_element(By.CSS_SELECTOR, "[data-testid='pluggable-input-body']")
    # basis_items = driver.find_elements(By.CSS_SELECTOR, "flex.flex-wrap.gap-1.pb-4.mt-2")
    amount_items = driver.find_elements(By.CSS_SELECTOR, ".col-span-3.text-right") 
    # elements = driver.find_elements(By.TAG_NAME, "span")
    amounts = driver.find_elements(By.CSS_SELECTOR, ".col-span-3.text-right")
    items = driver.find_elements(By.CSS_SELECTOR, ".flex.items-center.col-span-7.gap-2") 
    items_lst = [item.text for item in items] 
    amount_lst = [amount.text for amount in amounts] 
    portions = portions.split("\n")[1]
    # print([amount.text for amount in amounts])
    print(len(amount_lst), len(items_lst), title, portions)  
    # print(amount_portions)

# click_first_link()
# ingredients, portions, title, link = get_ingredients()

def get_random_recipe(driver, recipes, recipes_clicks, url):
    ingredients, portions, title, link = get_ingredients(driver, recipes, recipes_clicks, url) 
    items = [ing[0] for ing in ingredients]
    amount = [ing[1] for ing in ingredients]
    return items, amount, title, link 

# print(f"Title: {title}") 
# print(f"Link for the recipe: {link}")
# print(f"Amount of portions: {portions}")
# print(f"Ingredients: ") 
# for ing in ingredients:
#     print(f"{ing[0]}, {ing[1]}")

# # only the ingredients. 
# items = [ing[0] for ing in ingredients] 
# amount = [ing[1] for ing in ingredients]
# print(items)
# print(amount)

