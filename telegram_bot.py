import random
import telebot
from telebot import types

# Токен от @BotFather
TOKEN = "8558667216:AAFhwQLPOQoXMOqehFf-_-7QEcbDCYBgmCM"

bot = telebot.TeleBot(TOKEN)

RESPONSES = ["ого", "нафиг мне лень читать", "Ты упрямый чтоль?"]


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    response = random.choice(RESPONSES)
    
    # Создаём кнопку с ссылкой
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Перейти на сайт", url="https://griin.ru")
    markup.add(btn)
    
    bot.reply_to(message, response, reply_markup=markup)


if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
