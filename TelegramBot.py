
import telebot
from configBot import keys ,TOKEN
from utilsBot2 import ConversionException, CryyptoConverter, CountTB

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start','help'])
def help(message):
    text = 'чтобы начать работу введите команду боту в следующем формате: \n\
    <количество вводимой валюты>\
    <название конвертируемой валюты>\
    <в какую валюту перевести>\n\
    Увидеть список всех доступных валют /values'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def availble_types(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types='text')
def conversion(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversionException('Несоответствие количеста параметров (должно быть 3)')
        amount, quote, base = values
        middle_base = CryyptoConverter.convert(quote, base, amount)
        total_base = CountTB.multi(amount, middle_base) # Класс со статическим методом из задания добавлен)
    except ConversionException as e:
        bot.reply_to(message,f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}' )
    else:
        text = f'Количество {amount} {quote} это {total_base} в {base}(ах)'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)

