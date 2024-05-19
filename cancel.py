from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add('Актуальная стоимость ваших акций')
main_menu.add('Добавить отслеживание акций')
main_menu.add('Посмотреть список отслеживания')
main_menu.add('Удалить акции из отслеживания')


all_stocks = ReplyKeyboardMarkup(resize_keyboard=True)
all_stocks.add('ЛУКОЙЛ', 'Сбербанк')
all_stocks.add('Газпром', 'ГМК Норникель')
all_stocks.add('ВК (ранее VK)', 'Ростелеком')
all_stocks.add('Яндекс', 'Аэрофлот')
all_stocks.add('РУСАЛ', 'ТКС Холдинг (TCS)')
all_stocks.add('X5 Group', 'OZON адр (Мосбиржа)')
all_stocks.add('Сургутнефтегаз', 'АФК Система')
all_stocks.add('Сургутнефтегаз ап', 'ММК')
all_stocks.add('Роснефть', 'Полюс')
all_stocks.add('Софтлайн', 'Башнефть ап')
all_stocks.add('Назад в главное меню')

