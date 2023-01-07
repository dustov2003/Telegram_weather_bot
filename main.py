import telebot
from telebot import types
import requests

bot = telebot.TeleBot('Your ')
api="Your API-key from https://openweathermap.org/"

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/start')


@bot.message_handler(commands=['start'])
def start(message):
    buts = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buts.add(types.KeyboardButton('/Русский'), types.KeyboardButton('/English'))
    bot.send_message(message.chat.id, "Выберите язык:\nРусский\nEnglish", reply_markup=buts)
    lang = 'en'
    @bot.message_handler(commands=['Русский', 'English'])
    def gettext(message):
        global lang
        if message.text == '/English':
            lang = 'en'
            bot.send_message(message.chat.id, 'Please input cityname:', reply_markup=types.ReplyKeyboardRemove())
        elif message.text == '/Русский':
            lang = 'ru'
            bot.send_message(message.chat.id, 'Введите название города:', reply_markup=types.ReplyKeyboardRemove())
        def help(message):
            url = "https://api.openweathermap.org/data/2.5/weather?lang=" + lang + "&units=metric&q=" + message.text + "&appid="+api
            response = requests.get(url)
            data = response.json()
            if (len(data) < 3):
                bot.send_message(message.chat.id,
                                 'Такой город не найден в базе данных, начните сначала:/start\nSuch a city is not found in the database, start over:/start',
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
                                     types.KeyboardButton('/start')))
            else:
                cityname = data['name']
                temp = str(data['main']['temp'])
                feels = str(data['main']['feels_like'])
                speed = str(data['wind']['speed'])
                press = str(data['main']['pressure'])
                desc = data['weather'][0]['description']
                if lang == 'ru':
                    bot.send_message(message.chat.id,
                                     'Город: '+ cityname + '\nТемпература: ' + temp + '\nОщущается как: ' + feels + '\nСкорость ветра: ' + speed + '\nДавление: ' + press + '\nПогода: ' + desc)
                else:
                    bot.send_message(message.chat.id,
                                     'City: '+ cityname + '\nTemperature: ' + temp + '\nFeels like: ' + feels + '\nWind speed: ' + speed + '\nPressure: ' + press + '\nWeather: ' + desc)

bot.polling(none_stop=True)
