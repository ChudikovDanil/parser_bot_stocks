from aiogram import Dispatcher, Bot, executor, types
import cancel as kb
import json
import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By


########################################################################################################################
# Функция для сохранения данных в JSON-файл
def save_data_to_json(data):
    with open('stocks_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Функция для получения данных о ценах акций
def get_stocks_data():
    while True:
        # Создаем и открываем браузер
        browser = webdriver.Edge()
        browser.get('https://bcs.ru/markets?refid=16625&utm_source=yandex&utm_medium=cpc&utm_campaign=104685997~BCS_StocksBUY_RF_Poisk&utm_content=5376858046~49346496724~15646715788~desktop~39~premium~none&yclid=12001303311098576895')

        # Название акций
        infas = browser.find_elements(By.CLASS_NAME, 'qhaJj')

        # Создаем словарь для хранения данных
        stocks_data = {}

        # Итерируемся по индексам с шагом 3
        for i in range(0, len(infas), 3):
            # Получаем название акции и цены
            stock_name = infas[i].text
            initial_price_text = infas[i + 1].text.replace(' ₽', '').replace(',', '.').replace(' ', '')
            last_price_text = infas[i + 2].text.replace(' ₽', '').replace(',', '.').replace(' ', '')

            # Обработка случая с отсутствующей ценой
            initial_price = float(initial_price_text) if initial_price_text != '—' else None
            last_price = float(last_price_text) if last_price_text != '—' else None

            # Добавляем данные в словарь
            stocks_data[stock_name] = last_price

        # Сохраняем данные в JSON-файл
        save_data_to_json(stocks_data)

        # Выводим словарь данных
        for key, value in stocks_data.items():
            print(f"{key}: {value}")

        # Закрываем браузер
        browser.quit()

        # Ждем 60 секунд перед обновлением данных
        time.sleep(85)


# Запускаем поток для получения данных о ценах акций
Thread(target=get_stocks_data).start()
########################################################################################################################


token = '7104747317:AAH6k_THAegoppioIXKvK-mRbEvJUUhi1fQ'
bot = Bot(token)
dp = Dispatcher(bot=bot)


# Функция для загрузки данных из JSON файла
def load_user_data():
    try:
        with open('user_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Функция для загрузки данных из JSON-файла с актуальными ценами акций
def load_stocks_data():
    try:
        with open('stocks_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Функция для сохранения данных в JSON файл
def save_user_data(user_data):
    with open('user_data.json', 'w', encoding='utf-8') as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)


# Функция для обработки команды /start
@dp.message_handler(commands=['start'])
async def start_function(message: types.Message):
    # Отправляем приветственное сообщение пользователю
    await message.answer(f'{message.from_user.first_name}, привет, здесь ты можешь следить за падением своих акций',
                         reply_markup=kb.main_menu)

    # Получаем идентификатор пользователя
    user_id = str(message.from_user.id)

    # Загружаем данные пользователя из JSON файла
    user_data = load_user_data()

    # Если данные о пользователе отсутствуют, создаем новую запись
    if user_id not in user_data:
        user_data[user_id] = {'stocks': []}
        save_user_data(user_data)


# Функция для обработки команды "Добавить отслеживание акций"
@dp.message_handler(text='Добавить отслеживание акций')
async def add_stocks(message: types.Message):
    await message.answer('Выберите акцию ниже:', reply_markup=kb.all_stocks)


# Список всех акций
all_stock_names = [
    'ЛУКОЙЛ', 'Сбербанк', 'Газпром', 'ГМК Норникель', 'ВК (ранее VK)', 'Ростелеком',
    'Яндекс', 'Аэрофлот', 'РУСАЛ', 'ТКС Холдинг (TCS)', 'X5 Group', 'OZON адр (Мосбиржа)',
    'Сургутнефтегаз', 'АФК Система', 'Сургутнефтегаз ап', 'ММК', 'Роснефть', 'Полюс',
    'Софтлайн', 'Башнефть ап'
]


# Функция для обработки выбора акции пользователем
@dp.message_handler(lambda message: message.text in all_stock_names)
async def add_stock(message: types.Message):
    # Получаем идентификатор пользователя и выбранную акцию
    user_id = str(message.from_user.id)
    stock_name = message.text

    # Загружаем данные пользователя из JSON файла
    user_data = load_user_data()

    # Если пользователя нет в файле, добавляем его
    if user_id not in user_data:
        user_data[user_id] = {'stocks': []}

    # Добавляем акцию в список акций пользователя, если ее там еще нет
    if stock_name not in user_data[user_id]['stocks']:
        user_data[user_id]['stocks'].append(stock_name)
        # Сохраняем изменения в JSON файл
        save_user_data(user_data)
        await message.answer(f'Акция "{stock_name}" добавлена в список отслеживания.')
    else:
        await message.answer(f'Акция "{stock_name}" уже есть в списке отслеживания.')


# Функция для обработки команды "Удалить акции из отслеживания"
@dp.message_handler(text='Удалить акции из отслеживания')
async def delete_stocks_confirmation(message: types.Message):
    # Отправляем запрос на подтверждение удаления
    confirm_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    confirm_kb.add('Да', 'Нет')
    await message.answer('Вы уверены, что хотите удалить все акции из отслеживания?', reply_markup=confirm_kb)


# Функция для обработки подтверждения удаления акций
@dp.message_handler(lambda message: message.text in ['Да', 'Нет'])
async def confirm_delete_stocks(message: types.Message):
    user_id = str(message.from_user.id)
    user_data = load_user_data()

    if message.text == 'Да':
        if user_id in user_data and user_data[user_id]['stocks']:
            user_data[user_id]['stocks'] = []
            save_user_data(user_data)
            await message.answer('Все акции удалены из списка отслеживания.', reply_markup=kb.main_menu)
        else:
            await message.answer('У вас нет отслеживаемых акций, чтобы удалить.', reply_markup=kb.main_menu)
    else:
        await message.answer('Удаление отменено.', reply_markup=kb.main_menu)


# Функция для обработки команды "Посмотреть список отслеживания"
@dp.message_handler(text='Посмотреть список отслеживания')
async def browse_stocks(message: types.Message):
    # Получаем идентификатор пользователя
    user_id = str(message.from_user.id)

    # Загружаем данные пользователя из JSON файла
    user_data = load_user_data()

    # Проверяем наличие акций в списке пользователя
    if user_id in user_data and user_data[user_id]['stocks']:
        stocks_list = '\n'.join(f'{idx+1}. {stock}' for idx, stock in enumerate(user_data[user_id]['stocks']))
        await message.answer(f'Ваши отслеживаемые акции:\n{stocks_list}')
    else:
        await message.answer('У вас нет отслеживаемых акций.')


@dp.message_handler(text='Актуальная стоимость ваших акций')
async def get_price_stocks(message: types.Message):
    # Получаем идентификатор пользователя
    user_id = str(message.from_user.id)

    # Загружаем данные пользователя из JSON файла
    user_data = load_user_data()

    # Проверяем, есть ли данные о пользователе
    if user_id in user_data:
        # Загружаем данные о ценах акций
        stocks_data = load_stocks_data()

        # Формируем сообщение о ценах акций пользователя
        response = ''
        for stock in user_data[user_id]['stocks']:
            if stock in stocks_data:
                response += f'{stock}: {stocks_data[stock]} ₽\n'
            else:
                response += f'{stock}: Цена не доступна\n'

        # Отправляем сообщение пользователю
        await message.answer(response)
    else:
        await message.answer('Вы еще не добавили акции для отслеживания.')



# Функция для обработки команды "Назад в главное меню"
@dp.message_handler(text='Назад в главное меню')
async def back_to_main_menu(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, Вы вернулись в главное меню', reply_markup=kb.main_menu)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)