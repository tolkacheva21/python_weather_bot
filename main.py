import telebot
import requests
import json

bot_API = '7947122100:AAFcZAk44pw6xjMh2OoBZDiaegLjFk235yQ'
bot = telebot.TeleBot(bot_API)
weather_API = 'a519c4cf4a1b7de7b0c6ed85b7fb0018'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Вас приветствует погодный бот')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Мои команды:\n/start\n/help\n/weather')

@bot.message_handler(commands=['weather'])
def com_weather(message):
    bot.send_message(message.chat.id, 'Введите город, в котором хотите узнать погоду')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_API}&units=metric'
                       f'&lang=ru')
    if res.status_code == 200 and city != 'false' and city != 'true':
        data = json.loads(res.text)
        descrip = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        pressure = data["main"]["pressure"] * 0.75
        wind_speed = data["wind"]["speed"]

        icon_code = data["weather"][0]["icon"]
        icon_url = f'https://openweathermap.org/img/wn/{icon_code}@2x.png'

        bot.reply_to(message, f'Температура сейчас:  {temp} C°, {descrip}\n'
                              f'Ощущается как: {feels_like} C°\n'
                              f'Минимальная температура: {temp_min}  C°\n'
                              f'Максимальная температура: {temp_max}  C°\n'
                              f'Давление: {pressure} мм рт.ст\n'
                              f'Скорость ветра: {wind_speed} м/с')
        bot.send_photo(message.chat.id, icon_url)
    else:
        bot.reply_to(message, f'Город указан неверно')

bot.polling(non_stop=True)
