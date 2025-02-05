# Cryptobot
### Как работает код оплаты через CryptoBot API (для чат-бота Telegram на основе моего примера)

**Принцип работы:**
1. Пользователь запускает бота командой `/start` и нажимает кнопку "Получить за 0.1$".
2. Бот создает счет через CryptoBot API и отправляет пользователю ссылку на оплату.
3. После оплаты пользователь нажимает "Проверить оплату". Бот проверяет статус платежа через API.
4. Если оплата успешна — бот отправляет документ `qw.docx`.

---

### Пример работы с CryptoBot API
**1. Создание счета:**  
Код вызывает метод `createInvoice`, чтобы получить ссылку на оплату:
```python
def get_pay_link(amount):
    headers = {"Crypto-Pay-API-Token": API_TOKEN}
    data = {"asset": "USDT", "amount": amount}
    response = requests.post('https://pay.crypt.bot/api/createInvoice', headers=headers, json=data)
    ...
    return pay_url, invoice_id
```

**2. Проверка оплаты:**  
Код запрашивает список всех счетов через `getInvoices` и ищет нужный `invoice_id`:
```python
def check_payment_status(invoice_id):
    response = requests.post('https://pay.crypt.bot/api/getInvoices', ...)
    ...
    for inv in response.json()['result']['items']:
        if inv['invoice_id'] == invoice_id:
            return inv['status']
```

---

### 💡 Как перейти на тестовую сеть CryptoBot
**Шаг 1: Получить тестовый API-токен**  
1. Напишите боту [@CryptoTestnetBot](https://t.me/CryptoTestnetBot) и создайте тестовое приложение.
2. Получите тестовый `API_TOKEN` (он будет начинаться с `testnet:`).

**Шаг 2: Заменить URL API на тестовые**  
Замените все URL в коде с основной сети на тестовую:

| **Тип сети** | **Метод API**          | **URL основной сети**                  | **URL тестовой сети**                          |
|--------------|------------------------|----------------------------------------|------------------------------------------------|
| Основная     | Создание счета         | `https://pay.crypt.bot/api/createInvoice` | `https://testnet-pay.crypt.bot/api/createInvoice` |
| Основная     | Проверка счетов        | `https://pay.crypt.bot/api/getInvoices`   | `https://testnet-pay.crypt.bot/api/getInvoices`   |

**Пример изменения в коде:**
```python
# Было (основная сеть):
response = requests.post('https://pay.crypt.bot/api/createInvoice', ...)

# Стало (тестовая сеть):
response = requests.post('https://testnet-pay.crypt.bot/api/createInvoice', ...)
```

**Шаг 3: Использовать тестовые платежи**  
- В тестовой сети используйте **USDT-TRC20** (Tron testnet) или другие тестовые активы.
- Для оплаты подключите кошелек, поддерживающий тестовые транзакции (например, [@TestCryptoBot](https://t.me/TestCryptoBot)).

---

### Важные замечания
- Тестовые платежи **не списывают реальные деньги**.
- Убедитесь, что в коде используется **тестовый API-токен** (начинается с `testnet:`).
- Если код выдает ошибки, проверьте:
  - Правильность URL.
  - Активность тестового токена.
  - Наличие файла `qw.docx` в директории бота.

Пример тестового токена:
```python
API_TOKEN = 'testnet:123456:ABC...DEF'  # Тестовый токен из @CryptoTestnetBot
```

### Установка необходимых библиотек

Для работы с данным кодом вам нужно установить несколько библиотек. Вот команды для их установки:

```bash
pip install telebot requests
```

- **`telebot`**: Библиотека для работы с Telegram Bot API.
- **`requests`**: Библиотека для выполнения HTTP-запросов к CryptoPay API.

---

### Документация и ссылки

1. **CryptoPay API**:
   - Официальная документация: [CryptoPay API Docs](https://help.crypt.bot/crypto-pay-api)
   - Репозиторий с примерами: [Foile/crypto-pay-api](https://github.com/Foile/crypto-pay-api)
   - В репозитории вы найдете примеры использования API, включая создание счетов, проверку платежей и работу с вебхуками.

2. **Telegram Bot API**:
   - Официальная документация: [Telegram Bot API](https://core.telegram.org/bots/api)
   - Библиотека `pyTelegramBotAPI`: [pyTelegramBotAPI Docs](https://github.com/eternnoir/pyTelegramBotAPI)

---

### Пример использования CryptoPay API

Вот пример кода для создания счета и проверки платежа, основанный на репозитории [Foile/crypto-pay-api](https://github.com/Foile/crypto-pay-api):
