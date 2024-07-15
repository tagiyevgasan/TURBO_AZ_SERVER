import requests
from bs4 import BeautifulSoup
from turbo_parser.models import Order, SendedLink
from users.models import User
import time
from datetime import datetime
import random
import telebot
token = "5575363607:AAHsn2NL_uHZj5zwaASWu53zmggDQM3sTPU"
bot = telebot.TeleBot(token)

headers = {"user-agent": 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

# function which returns soups of pages
# --------------------------------------------------------------------------------------------------------
def get_soup(ordered_link):

    next_page = 0
    i = 1

    while next_page != None:
        numeric_page_url = ordered_link.replace("https://turbo.az/autos?", f"https://turbo.az/autos?page={i}")
        time.sleep(random.randint(3,7))
        response = requests.get(numeric_page_url)
        soup = BeautifulSoup(response.text, "lxml")
        next_page = soup.find("nav", class_="pagination")
        if next_page != None:
            next_page = next_page.find("span", class_="next")
        i+=1
        yield soup
# ----------------------------------------------------------------------------------------------

# function which returns exchange rate
def exchange_rate(currency_code):

    t = datetime.now().strftime("%d.%m.%Y")
    responce = requests.get(f'https://cbar.az/currencies/{t}.xml')
    soup = BeautifulSoup(responce.text, 'xml')

    currency_info = soup.find("Valute", Code = currency_code)

    rate = float(currency_info.Value.text)
    return rate
# ----------------------------------------------------------------------------------------------

# function which checks prices of cars and sends notification if car price meets requirement
# ----------------------------------------------------------------------------------------------
def get_car_info(chat_id, order_id, threshold, ordered_link, exchange_rates):

    for page_soup in get_soup(ordered_link):

        data = page_soup.find_all("div", class_="products")

        
        data1 = []

        for p_i in data:
            a = p_i.find_all("div", class_="products-i")
            for i in a:
                data1.append(i)


        for d in data1:

            if d.find("div", class_="product-price") == None:
                continue

            price = d.find("div", class_="product-price").text

            dollar = price.find("$")
            evro = price.find("€")
            manat = price.find("AZN")
            
            price = price.replace(" ", "").replace("$", "").replace("AZN", "").replace("€", "")

            if (dollar==evro==-1):
                price = float(price)/exchange_rates[0]

            if (dollar==manat==-1):
                price = float(price)*exchange_rates[1]/exchange_rates[0]

            price = float(price)
            get_link = 0
            if float(price) <= threshold:
                get_link = "https://turbo.az" + d.find("a", class_="products-i__link").get("href")

                order = Order.objects.get(pk=order_id)
                sended_links = order.sendedlink_set.all()

                sended_links_list = [obj.sended_link for obj in sended_links]

                if (get_link in sended_links_list):
                    continue
            
                bot.send_message(chat_id, f"Istediyiniz avtomobil {round(price, 2)} dollara movcuddur:");
                bot.send_message(chat_id, get_link);
                bot.send_message(chat_id, "---------------------------------------------------------------------");

                SendedLink.objects.create(sended_link=get_link,order_id=order_id)
                
# ------------------------------------------------------------------------------------------------------------


def orders_check():

    orders = Order.objects.all()
    
    exchange_rates = (exchange_rate("USD"), exchange_rate("EUR"))

    for o in orders:
        user = User.objects.get(pk=o.user_id)
        
        chat_id = user.telegram_chat_id
        order_id = o.id
        threshold = o.threshold
        ordered_link = o.ordered_link

        if len(o.sendedlink_set.all()) >= 10:
            continue
        
        
        get_car_info(chat_id, order_id, threshold, ordered_link, exchange_rates)
        time.sleep(random.randint(10,20))



