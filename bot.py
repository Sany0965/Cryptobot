import telebot
from telebot import types
import requests
import os

TOKEN = 'token_botFather'
API_TOKEN = 'token_api_pay'

bot = telebot.TeleBot(TOKEN)

invoices = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    get_button = types.InlineKeyboardButton(text="Получить за 0.1$", callback_data='get_0.1')
    markup.add(get_button)
    bot.send_message(message.chat.id, "Добро пожаловать! Нажмите кнопку ниже, чтобы получить документ.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'get_0.1')
def get_invoice(call):
    chat_id = call.message.chat.id
    pay_link, invoice_id = get_pay_link('0.1')
    if pay_link and invoice_id:
        invoices[chat_id] = invoice_id  # Store the invoice id associated with the chat_id
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Оплатить 0.1$", url=pay_link))
        markup.add(types.InlineKeyboardButton(text="Проверить оплату", callback_data=f'check_payment_{invoice_id}'))
        bot.send_message(chat_id, "Перейдите по этой ссылке для оплаты и нажмите 'Проверить оплату'", reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, 'Ошибка: Не удалось создать счет на оплату.')

@bot.callback_query_handler(func=lambda call: call.data.startswith('check_payment_'))
def check_payment(call):
    chat_id = call.message.chat.id
    invoice_id = call.data.split('check_payment_')[1]
    payment_status = check_payment_status(invoice_id)
    if payment_status and payment_status.get('ok'):
        if 'items' in payment_status['result']:
            invoice = next((inv for inv in payment_status['result']['items'] if str(inv['invoice_id']) == invoice_id), None)
            if invoice:
                status = invoice['status']
                if status == 'paid':
                    bot.send_message(chat_id, "Оплата прошла успешно!✅")
                    # Убедитесь, что файл 'qw.docx' находится в той же директории
                    with open('qw.docx', 'rb') as document:
                        bot.send_document(chat_id, document)
                    # Чтобы избежать дублирования счетов, удалим его из списка
                    del invoices[chat_id]
                    bot.answer_callback_query(call.id)
                else:
                    bot.answer_callback_query(call.id, 'Оплата не найдена❌', show_alert=True)
            else:
                bot.answer_callback_query(call.id, 'Счет не найден.', show_alert=True)
        else:
            print(f"Ответ от API не содержит ключа 'items': {payment_status}")
            bot.answer_callback_query(call.id, 'Ошибка при получении статуса оплаты.', show_alert=True)
    else:
        print(f"Ошибка при запросе статуса оплаты: {payment_status}")
        bot.answer_callback_query(call.id, 'Ошибка при получении статуса оплаты.', show_alert=True)

def get_pay_link(amount):
    headers = {"Crypto-Pay-API-Token": API_TOKEN}
    data = {"asset": "USDT", "amount": amount}
    response = requests.post('https://pay.crypt.bot/api/createInvoice', headers=headers, json=data)
    if response.ok:
        response_data = response.json()
        return response_data['result']['pay_url'], response_data['result']['invoice_id']
    return None, None

def check_payment_status(invoice_id):
    headers = {
        "Crypto-Pay-API-Token": API_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.post('https://pay.crypt.bot/api/getInvoices', headers=headers, json={})
    
    if response.ok:
        return response.json()
    else:
        print(f"Ошибка при запросе к API: {response.status_code}, {response.text}")
        return None

if __name__ == '__main__':
    bot.polling(non_stop=True)
