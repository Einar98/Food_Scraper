import numpy as np 
import selenium
import bs4 
from bs4 import BeautifulSoup
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
import random  
import os 

# import from other scripts. 
import recipe_script 
import compare_prices 
import food_prices 
import compare_prices 

# returns a random recipe from adams matkasse. 
def adams_matkasse():
    url = "https://www.adamsmatkasse.no/menyen" 
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op) 
    recipes = []
    recipes_clicks = []
    items, amount, title, link = recipe_script.get_random_recipe(driver, recipes, recipes_clicks, url)
    return items, amount, title, link

def display_items(items:list) -> None:
    print("Required items: ") 
    print("**"*23)
    for item in items:
        if "\n" in item:
            print(item.split("\n")[0])  
        else:
            print(item)

def get_adams_matkasse_recipe():
    running = True 
    items = None 
    amount = None 
    title = None 
    link = None 
    while running:
        print(f"Fetching a random recipe ...") 
        items, amount, title, link = adams_matkasse() 
        print()
        print(f"Recipe:") 
        print("**"*23) 
        print(title)
        print()
        display_items(items) 
        response = input("Proceed (q) or Fetch different Recipe (Enter): ")
        if response == "q":
            running = False 
    return items, amount, title, link 

# scrapes and updates csv files with offerings. 
def update_offerings(stores):
    food_prices.get_updated_offers(stores)

# list of store names. 
stores = ['Coop-Extra', 'KIWI', 'Bunnpris', 
          'Coop-Mega', 'Coop-Prix', 'Joker', 'Europris', 
          'Matkroken', 'MENY', 'Naerbutikken', 
          'REMA-1000', 'SPAR', 'oda', 'Coop-Marked', 'Obs', 'Gigaboks'] 

def get_shopping_list() -> list:
    shopping_lst = []
    print("Enter the items for the shopping list: ")
    running = True 
    while running:
        item = input("item name (q to quit): ")  
        if item == "q":
            running = False  
        else:
            print(f"{item} added to the list.")
            shopping_lst.append(item) 
    print(f"Shopping items: {shopping_lst}")
    return shopping_lst

def menu() -> int:
    print("Select an option from the list below: ")
    while True:
        print("Option 1 - Adams Matkasse")
        print("Option 2 - Custom Shopping List")
        ans = input("(q to quit): ") 
        if ans == "1":
            items, amount, title, link = get_adams_matkasse_recipe()
            items = [item.split("\n")[0] if "\n" in item else item for item in items]
            food_prices = compare_prices.get_food_items(items) 
            print(food_prices)
            cheapest_prods = compare_prices.select_cheapest_combination(items, food_prices)
            print(cheapest_prods)
            break 
        elif ans == "2":
            shopping_lst = get_shopping_list() 
            food_prices = compare_prices.get_food_items(shopping_lst) 
            compare_prices.filter_products(food_prices)
            print(food_prices)
            break 
        elif ans == "q":
            break
        else:
            print("Error, option not available.")
# user interface. 
def ui():
    pass 

menu()

