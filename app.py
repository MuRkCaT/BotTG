import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<Имя валюты>\<в какую валюту перевести>\<количчество валюты>\nУвидеть список всех валют:/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(massage: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(massage, text)

@bot.message_handler(content_types=['text',])
def convert(massage: telebot.types.Message):
    global text
    try:
           values = massage.text.split(' ')

           if len(values) != 3:
               raise ConvertionException('Слишком много параметров')

           quote, base, amount = values
           total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(massage, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(massage, f'Не удалось обработать команду\n{e}')
    else:
          text = f'Цена {amount} {quote} в {base} - {total_base}'



          bot.send_message(massage.chat.id, text)




bot.polling(
)
