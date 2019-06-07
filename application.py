import requests
from bs4 import BeautifulSoup
import telebot
import array

token = "823847912:AAG2XZky17saQ4Tyb0mp4ftaXUNbbzkxBTI"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])

def handle_start(message):
    bot.send_message(message.from_user.id,"Добро пожаловать в news чат Телеграмм.")
    bot.send_message(message.from_user.id,"Для обновления новостей - /update.")

@bot.message_handler(commands=['update'])

def handle_update(message):
    global array
    url = "https://strana.ua/news"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = soup.find_all(class_ = "article")
    #strana-adate
    result_t = soup.find_all(class_ = "date")
    temp1 = 0
    temp2 = True
    pem = ''
    for i in result:
        url = "https://strana.ua"+i["href"]
        if array != url and temp2==True:
            temp2=False
            pem = url
            
        if array == url:
            print("Yes")
            break
        S = ''
        S+=i.get_text()+'\n'
        S+=url+'\n'
        exl = list(result_t[temp1].get_text().split("\n"))
        S+="Время - "
        for k in exl:
            S+=k
        S+='\n'
        temp1+=1
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        result_page = soup.find_all(id = "article-body")
        temp = 0
        for j in result_page[0].get_text():
            if temp>150:
                S+="..."
                break
            temp+=1
            S+=j
        bot.send_message(message.from_user.id,S)
        print(array)
    array = pem
bot.polling(none_stop=True)
