import pandas as pd 
import numpy as np 
import os 
import math 

# list of store names. 
stores = ['Coop-Extra', 'KIWI', 'Bunnpris', 
          'Coop-Mega', 'Coop-Prix', 'Joker', 'Europris', 
          'Matkroken', 'MENY', 'Naerbutikken', 
          'REMA-1000', 'SPAR', 'oda', 'Coop-Marked', 'Obs', 'Gigaboks'] 

def is_valid_item(item:str, product:str) -> bool:
    product = product.split(" ") 
    if len(product) > 1 and item not in product[0]:
        return False 
    return True

# checks if a element is a subword / subpart of the word word. 
def is_part_of_word(element, word):
    if len(element) < len(word) and element in word:
        return True 
    return False 

# checks if food item is contained in the store item. 
def check_food_item(food_item:str, store_item:str):
    # is_contained = False   
    # store_item_lst = store_item.split(" ") 
    store_item_lst = store_item.split(" ")
    for element in store_item_lst:
        if food_item in element or food_item.upper() in element or food_item.lower() in element:
            return True 
    return False  

# compares the prices of all the store 
# for the given item. 
def compare_prices(item:str):
    prices = {}
    stores = os.listdir("Stores")
    print(stores)
    for store in stores:
        # load the data from this store. 
        # case sensitive titles.  
        df = pd.read_csv(store) 
        store_data = [] 
        # loop over all the titles. 
        for indx, food_item in enumerate(df["title"].values):
            # food_item_lst = food_item.split(" ") 
            if check_food_item(item, food_item):
                # price = df.loc[df["title"] == food_item]
                # adding the price. 
                # adding the actual title of the product. 
                store_data.append(df.iloc[indx]["title"])
                # adding the price. 
                store_data.append(df.iloc[indx]["price"]) 
                # adding the price per unit (kg price)
                store_data.append(df.iloc[indx]["kg price"]) 
                # adding the expiration that of the sale. 
                store_data.append(df.iloc[indx]["time"])
                
        if len(store_data) > 0:
            prices[store] = store_data 
    return prices 

# returns a list of products containing the name item, from the given store name. 
def find_items(item:str, store:str) -> list:
    df = pd.read_csv("Stores/" + store) 
    items = []
    for title in df["title"].values:
        if item == title:
            items.append(title) 
        elif item.upper()[0] + item[1:] in title or item.upper() in title or item.lower() in title:
            items.append(title) 
    return items

# returns a list of all the stores having the item. 
def find_all_store_items(item:str) -> list: 
    stores = os.listdir(os.getcwd() + "/Stores")
    all_items = []
    for store in stores:
        items = find_items(item, store) 
        if len(items) > 0:
            all_items.append((store, items))  
    return all_items 

# returns the prices of the list of the items from the given store. 
def get_prices(items:list, store:list) -> list:
    df = pd.read_csv("Stores/" + store)
    prices = []
    for item in items:
        if item in df["title"].values:
            price = df[df["title"] == item]["price"].values.item() 
            prices.append((item, price)) 
    return prices  

# returns the prices for all the items for all the stores. 
def get_all_store_prices(stores_and_items:list) -> list:
    data = {}
    # iterate over each store. 
    for store, items in stores_and_items:
        df = pd.read_csv("Stores/" + store)
        prices = []
        for item in items:
            if item in df["title"].values: 
                price = df[df["title"] == item]["price"].values[0]
                # kg price. 
                price_kg = df[df["title"] == item]["kg price"].values[0]
                prices.append((item, price, price_kg)) 
        data[store] = prices  
    return data    

# select the cheapest one of the prices. 
def select_cheapest(prices:dict):
    cheapest = None 
    best_stores = [] 
    product_names = []
    for store in prices.keys():
        data = prices[store] 
        product_name = data[0] 
        price = data[1]
        if cheapest is None:
            cheapest = price 
            best_stores.append(store)
            product_names.append(product_name)
        elif cheapest == price:
            cheapest = price 
            best_stores.append(store)
            product_names.append(product_name)
        elif cheapest > price:
            cheapest = price 
            # empty all previous best stores. 
            while len(best_stores) > 0:
                best_stores.pop() 
            while len(product_names) > 0:
                product_names.pop()
            best_stores.append(store) 
            product_names.append(product_name)
    return cheapest, best_stores, product_names

def compare_prices_other_stores(store:str):
    df = pd.read_csv(store + ".csv") 
    store_prices = {}
    for other_store in stores:
        if other_store == store:
            pass 
        else:
            df_store = pd.read_csv(other_store + ".csv") 
            similar_items = []
            for indx, item_title in enumerate(df["title"].values):
                if item_title in df_store["title"].values:
                    print(df_store[df_store["title"] == item_title]["title"], 1)
                    # similar_items.append(df_store[df_store["title"] == item_title]["title"].value)
            store_prices[other_store] = similar_items 
    return store_prices

def get_nonempty_dict(data:dict) -> dict:
    new_dict = {}
    for store, products in data.items():
        if len(products) > 0:
            new_dict[store] = products 
    return new_dict  

def apply_filter(items:list, store_prices:dict):
    updated_store_prices = {} 
    for item in items:
        data = []
        for store, product in store_prices.items():
            if is_valid_item(item, product[0]):
                data.append(product) 
        updated_store_prices[store] = data 
    return updated_store_prices  

# input a list of ingredients / items, return a dict with keys as the stores and the values containing a 
# list of all the items, where each list item is a tuple of the type (item, price, price_per_unit). 
def get_food_items(items:list) -> dict:
    data = {}
    stores = os.listdir("Stores")
    for store in stores:
        data[store] = [] 
    for item in items:
        all_items = find_all_store_items(item)  
        store_prices = get_all_store_prices(all_items)
        print(store_prices)
        store_prices = apply_filter(items, store_prices)
        for store, product_data in store_prices.items():
            for product in product_data:
                data[store].append(product) 
    data = get_nonempty_dict(data)
    return data

def select_cheapest_combination(items:list, data:dict) -> list:
    combination = [] 
    for item in items:
        min_price = math.inf 
        cheapest_product = None 
        cheapest_store = None 
        for store, products in data.items():
            for product in products:
                if item in product[0] or item.upper() in product[0] or item.lower() in product[0]:
                    price = product[1].split(" ")[1].split(",") 
                    if len(price) > 1:
                        price = float(price[0]) + float(price[1])/100 
                    else:
                        price = float(price[0])
                    if price < min_price:
                        min_price = price 
                        cheapest_product = product    
                        cheapest_store = store    
                      
        combination.append((cheapest_store, cheapest_product)) 
    return combination 

def is_exact_name(item:str, product:str) -> bool:
    if item == product or item.upper() == product or item.lower() == product:
        return True 

def is_part_expression(item_name:str, product_name:str) -> bool:
    pass 

def contains_full_item_name(item_name:str, product_name:str) -> bool:
    product_lst1 = product_name.split(item_name)
    product_lst2 = product_name.split(item_name.upper()) 
    product_lst3 = product_name.split(item_name.lower()) 
    if "" in product_lst1 or "" in product_lst2 or "" in product_lst3:
        return True 
    return False 

def is_basic_item(item:str):
    with open("Basic_items.txt") as file:
        for f in file.readlines():
            f = f.strip("\n") 
            if item.upper() == f or item.lower() == f or item == f:
                return True 
    return False  

def remove_symbols(item_name:str) -> str:
    pass 

# filter the items. 
def filter_products(data:dict) -> dict:
    product_filter = {"Melk":["Lett", "Hel", "Skummet"], 
                      "Smør":[""]}  
    for key, names in product_filter.items():
        valid_product_names = [name + key for name in names]
        # update product list. 
        for store, products in data.items():
            updated_list = [] 
            for product in products:
                for valid_prod in valid_product_names:
                    if valid_prod.upper() in product[0] or valid_prod.lower() in product[0] or valid_prod in product[0]:
                        updated_list.append(product) 
            if len(updated_list) > 0:
                data[store] = updated_list

def display_store_prices(store_prices:dict) -> None:
    for store, data in store_prices.items():
        print()
        print(f"Store {store} selection: ")
        for val in data:
            print(f"Item: {val[0]}, Price: {val[1]}, Price per unit: {val[2]}") 
        print("**"*50)


