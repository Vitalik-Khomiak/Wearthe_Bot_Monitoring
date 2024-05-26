import requests
import datetime
import telebot
import openai
import logging
from os import environ

from config import open_weather_token, openai_api_key

tg_bot_token = environ.get("TG_BOT_TOKEN2","define me")

FORMAT = '%(asctime)-15s %(name)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger()

# try:
    # Призначаємо змінні для open_weather_token і openai_api_key
    bot = telebot.TeleBot(tg_bot_token)
    openai.api_key = openai_api_key
    # print(tg_bot_token)
    # while True:
    #     continue
# except:
    print(tg_bot_token)
    # while True:
    #     continue


# print
logger.info('Bot Started')

#Після команди start запитуємо в якому місті користувач хоче взнати погоду
@bot.message_handler(commands=["start"])
def start_command(message):
    bot.reply_to(message, "Місто?")

#відправляємо open weather запит про погоду в обраному місті
@bot.message_handler(func=lambda message: True)
def get_weather(message):
    code_to_smile = {
        "Clear": "Ясненько ☀️",
        "Clouds": "Хмарно ☁️",
        "Rain": "Дощ ☔",
        "Drizzle": "Дощ ☔",
        "Thunderstorm": "Гроза ⚡",
        "Snow": "Сніг ❄️",
        "Mist": "Туман 🌫️"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        country = data["sys"]["country"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        wd = code_to_smile.get(weather_description, "виглянь у вікно!")

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        bot.reply_to(message, f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                               f"Погода в місті: {city},{country}\nТемпература: {cur_weather}C° {wd}\n"
                               f"Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\nВітер: {wind} м/с\n"
                               f"Схід сонця: {sunrise_timestamp}\nЗахід сонця: {sunset_timestamp}\nТривалість дня: {length_of_the_day}\n"
                               f"\nЧудового дня!"
                      )

        # Отримуємо текст повідомлення від користувача і передаємо штучному інтелекту
        user_message = f"Що мені одягнути в таку погоду {cur_weather} {wd}? дай мені коротку відповідь до 50 символів"
        
        # print
        logger.info(city)
        # Викликаємо модель GPT для генерації відповіді
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=user_message,
            max_tokens=50,
            temperature=0.7,
            n=1,
            stop=None,
            timeout=None

        )

        # Відправляємо відповідь користувачеві від штучного інтелекту
        bot.send_message(message.chat.id, f"Порада від штучного інтелекту, що краще одягнути:\n\n"
                                          f"{response.choices[0].text.strip()}\n\n"
                                          f"Чудового дня!")


    except Exception as e:
        logger.error("\U00002620  Перевірте назву міста \U00002620")
        bot.reply_to(message, "\U00002620 Перевірте назву міста \U00002620")



bot.polling(none_stop=True)