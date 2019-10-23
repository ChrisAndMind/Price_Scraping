import pickle
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import tkinter as tk

#This needs to be dynamic to work on other laptops...
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
products = []
URL_LIST = []

class product():
    def __init__(self, brand, desc, price, link, past_prices):
        self.brand = brand
        self.desc = desc
        self.price = price
        self.link = link
        self.past_prices = past_prices
    


def addURL(url):
    URL_LIST = getURL()

    #check if link already exists
    if(checkIfLinkExists(url)):
        URL_LIST.append(url)
        pickle_out = open("URL_LIST.pickle", "wb")
        pickle.dump(URL_LIST, pickle_out)
        pickle_out.close()
        #add new product to list:
        p = gatherProductFromURL(url)
        addProduct(p)
        print("new product added")
    else:
        print("Link already exists")


def getURL():
    pickle_in = open("URL_LIST.pickle", "rb")
    URL_LIST_01 = pickle.load(pickle_in)
    return URL_LIST_01


def getProductsList():
    pickle_in = open("products.pickle", "rb")
    products_01 = pickle.load(pickle_in)
    return products_01

def addProduct(product):
    products = getProductsList()
    products.append(product)
    pickle_out = open("products.pickle", "wb")
    pickle.dump(products, pickle_out)
    pickle_out.close()

def saveProductList(product_list):
    pickle_out = open("products.pickle", "wb")
    pickle.dump(product_list, pickle_out)
    pickle_out.close()

def gatherProductFromURL(url):
    #Gets the product from the website and returns the created product
    #if sportscheck:
        if str(url).startswith("https://www.sportscheck"):
            page_Sportscheck = requests.get(url, headers=headers)
            soup_sportscheck = BeautifulSoup(page_Sportscheck.content, 'html.parser')
    
            product_brand = soup_sportscheck.find("span", {"class":"product__brand"}).get_text()
            product_desc = soup_sportscheck.find("span", {"class":"product__desc"}).get_text()
            product_price = list(soup_sportscheck.find("span", itemprop="price").get_text())
            product_link = url
            
            #For the ',' in the price instead of '.'
            for counter in range(len(product_price)):
                if product_price[counter] == ',':
                    product_price[counter] = "."

            product_price= "".join(product_price)
            price_converted = float(product_price[0:(len(product_price)-2)])
            past_prices = []
            product_ret = product(product_brand, product_desc, price_converted, product_link, past_prices)
            return product_ret
        #if BergZeit
        if str(url).startswith("https://www.bergzeit"):
            page_bergZeit = requests.get(url, headers=headers)
            soup_bergZeit = BeautifulSoup(page_bergZeit.content, 'html.parser')
    
            product_brand = soup_bergZeit.find("span", {"class":"brand__name"}).get_text()
            product_desc = soup_bergZeit.find("h1", {"class":"headline"}).get_text()
            product_price = list(soup_bergZeit.find("span", {"class":"price"}).get_text())
            product_link = url

            #For the , in the price instead of .
            for counter in range(len(product_price)):
                if product_price[counter] == ',':
                    product_price[counter] = "."

            product_price= "".join(product_price)
            price_converted = float(product_price[0:(len(product_price)-2)])
            past_prices = []
            product_ret = product(product_brand, product_desc, price_converted, product_link, past_prices)
            return product_ret
           
       
def getCurrentPrice(url):
    #returns current price of the products url. input is product[i].url or so...
    #if sportscheck.
    if str(url).startswith("https://www.sportscheck"):
        page_Sportscheck = requests.get(url, headers=headers)
        soup_sportscheck = BeautifulSoup(page_Sportscheck.content, 'html.parser')
        product_price = list(soup_sportscheck.find("span", itemprop="price").get_text())
        #For the , in the price instead of .
        for counter in range(len(product_price)):
            if product_price[counter] == ',':
                product_price[counter] = "."

        product_price= "".join(product_price)
        price_converted = float(product_price[0:(len(product_price)-2)])
        return price_converted
    #if BergZeit
    if str(url).startswith("https://www.bergzeit"):
        page_bergZeit = requests.get(URL, headers=headers)
        soup_bergZeit = BeautifulSoup(page_bergZeit.content, 'html.parser')
        product_price = list(soup_bergZeit.find("span", {"class":"price"}).get_text())
        #For the , in the price instead of .
        for counter in range(len(product_price)):
            if product_price[counter] == ',':
                product_price[counter] = "."

        product_price= "".join(product_price)
        price_converted = float(product_price[0:(len(product_price)-2)])
        return price_converted


    
def updatePrices(products):
    # call getURL and all that? or do that in the main before calling this method?
    #here, we loop through all products (their link) and check if the price of that link is equal to the currently saved price. if not, append the current price to past_prices and change current_price to new price.
    #for this, we have a function which has url as input and price of product as output.
    #products = getProductsList()
    
    for p in products:
        temp_price = getCurrentPrice(p.link)
        if temp_price != p.price:
            p.past_prices = p.price
            a = p.price
            p.price = temp_price
         
    saveProductList(products)

def checkIfLinkExists(link):
    links = getURL()

    for i in links:
        if i == link:
            return False
    return True



def deleteAllLists():
    #leaves the .pickle file with an empty list slot..
    for i in range(0, len(URL_LIST)):
        URL_LIST.remove(i)

    for i in range(0, len(products)):
        products.remove(i)

    pickle_out = open("products.pickle", "wb")
    pickle.dump(products, pickle_out)
    pickle_out.close()

    pickle_out = open("URL_LIST.pickle", "wb")
    pickle.dump(URL_LIST, pickle_out)
    pickle_out.close()

def deleteProduct(location):
    products = getProductsList()
    products.remove(location)
    saveProductList(products)

def printPrices(products):
    for p in products:
        print(p.brand + " - " + p.desc + " | PRICE: " + str(p.price) + " | PAST: [" + str(p.past_prices) + " ]")




def GUI():
    win = tk.Tk()
    win.title("Price Follower")
    win.geometry("370x100")
    win.resizable(False, False)

    def link_adder():
        link1 = str(entry1.get())
        addURL(link1)
        

    def print_prices():
        p= getProductsList()
        updatePrices(p)
        p= getProductsList()
        printPrices(p)


    # ------ Widgets ------
    label1 = tk.Label(text = "Welcome")
    label1.grid(row = 0, column = 0)

    label2 = tk.Label(text = "Insert Link")
    label2.grid(row = 1, column = 0)

    entry1 = tk.Entry(win, width = 40)
    entry1.grid(row = 2, column=0)

    button1 = tk.Button(text = "Click here to add Link" , command = link_adder)
    button1.grid(row = 2, column = 1)

    button2 = tk.Button(text = "Show Prices", command = print_prices)
    button2.grid(row = 3  , column = 1 )
    # ------ END widgets -------
    win.mainloop()

# ============= MAIN =================
GUI()




"""
deleteAllLists()
addURL("https://www.sportscheck.com/burton/burton-reserve-bib-snowboardhose-herren-p330011-F040/true-black/")
addURL("https://www.sportscheck.com/burton/burton-covert-snowboardhose-herren-p298017-F040/true-black/")
addURL("https://www.sportscheck.com/volcom/volcom-articulated-snowboardhose-herren-p301580-F040/black/")


product1 = getProductsList()
product1[0].price = 60.0

for p in product1:
    print(p.desc + "price: " + str(p.price))

updatePrices(product1)
for p in product1:
    print(p.desc + "price: " + str(p.price))

print(product1[0].past_prices)


pickle_out = open("URL_LIST.pickle", "wb")
pickle.dump([], pickle_out)
pickle_out.close()

pickle_out1 = open("products.pickle", "wb")
pickle.dump([], pickle_out1)
pickle_out1.close()
"""