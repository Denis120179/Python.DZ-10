# СОЗДАНИЕ КАЛЬКУЛЯТОРА НА БОТЕ

import telebot
from telebot import types
import logging

logging.basicConfig(
    level=logging.INFO,
    filename = "mylog.log", encoding="utf-8",
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%H:%M:%S',
    )
logger = logging.getLogger(__name__)

typeNums = 0
res = 0

#bot = telebot.TeleBot("Напишите свой TOKEN")  
bot = telebot.TeleBot("6189994125:AAFnR-h49T-KtfMkJXUvhuBYAT0QAlpaB7c")

@bot.message_handler(commands = ["start"])

def calculator(message): 
    user = message.from_user
    logger.info("Старт: %s: %s", user.first_name, message.text)   
    #logger.info("Выбор чисел: %s: %s", user.first_name, message.text)   
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    but1 = types.KeyboardButton("Рациональные числа")
    but2 = types.KeyboardButton("Комплексные числа")
    markup.add(but1) 
    markup.add(but2) 
    bot.send_message(message.chat.id, "Выбери числа", reply_markup=markup)

@bot.message_handler(content_types = "text")

def buttons(message): 
    user = message.from_user
    logger.info("Выбор чисел: %s: %s", user.first_name, message.text)  
    #logger.info("Ввод выражения: %s: %s", user.first_name, message.text) 
    global typeNums  
    a = types.ReplyKeyboardRemove() 
    if message.text == "Рациональные числа":
        bot.send_message(message.chat.id, "Введите выражение, разделяя знаки пробелами")                
        bot.register_next_step_handler(message, controller) 
        typeNums = 0

    elif message.text == "Комплексные числа":
        bot.send_message(message.chat.id, "Введите выражение, разделяя знаки пробелами")                
        bot.register_next_step_handler(message, controller) 
        typeNums = 1

def controller(message):
    user = message.from_user
    #logger.info("Результат: %s: %s", user.first_name, message.text)   
    logger.info("Ввод выражения: %s: %s", user.first_name, message.text) 
    global res
    line = message.text.split()
    znak = line[1]
    if typeNums == 0:
        a = int(line[0])    
        b = int(line[2])
    if typeNums == 1:
        a = complex(line[0])    
        b = complex(line[2])
    if znak == '+':
        res = a+b
    elif znak == '-':
        res = a-b
    elif znak == '*':
        res = a*b
    elif znak == '/':
        res = a/b
    elif znak == '//' and typeNums == 0:
        res = a//b
    elif znak == '%' and typeNums == 0:
        res = a%b
    elif typeNums == 1 and znak == '//' or znak == '%':
        bot.send_message(message.chat.id, "Неверный ввод или недопустимая операция, проверьте выражение")
        bot.register_next_step_handler(message, controller)
        return
    bot.send_message(message.chat.id, str(res)) 

bot.infinity_polling()