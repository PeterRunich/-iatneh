from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ...database.db import Sqlite
"""Создаёт и возвращает inline панель с жанрами и pagination"""

# current_page_number - аргументы указывающий на какой странице находится пользователь
# current_page_number - аргументы указывающий количество элементов на одной странице
async def filter_kb_builder(current_page_number, limit, genres=[]):
    last_page_number = int(Sqlite().count_genres() / limit) # расчёт последней страницы

    if current_page_number > last_page_number: # если текущая станица больше возможного то ставим последнюю возможную
        current_page_number = last_page_number
    elif current_page_number < 1: # если текущая станица меньше 1 то ставим 1
        current_page_number = 1

    kb = InlineKeyboardMarkup(row_width=3) # базовый элемент inline клавиатуры который будет наполняться дальше (row_width - количество элементов на одной строке)
    offset = (current_page_number - 1) * limit # расчёт смещения для запроса к бд
    data = Sqlite().get_genres(limit, offset)

    if current_page_number > 1: # расчёт номера предыдущий страницы
        prev_page_number = current_page_number - 1
    else:
        prev_page_number = 1

    if current_page_number < last_page_number: # расчёт номера следующей страницы
        next_page_number = current_page_number + 1
    else:
        next_page_number = last_page_number

    # формируем кнопки pagination
    btns = [
        InlineKeyboardButton("<", callback_data=f"cq1:move_to:{prev_page_number}"),
        InlineKeyboardButton(f"{current_page_number}/{last_page_number}", callback_data='cq1:no_action:'),
        InlineKeyboardButton(">", callback_data=f"cq1:move_to:{next_page_number}")
    ]

    kb = await highlight_selected_genres(kb, data, genres) # добавляем жанры в базовый элемент клавиатуры (чтобы работоло ограничение row_width нужно заполнять базовый элемент методом insert)

    kb.row(*btns) # добавляем кнопки pagination в базовый элемент клавиатуры
    kb.add(InlineKeyboardButton('Перейти на страницу по номеру', callback_data="cq1:go_to_page:"))
    kb.add(InlineKeyboardButton('Поиск 🔎', callback_data="cq1:search:"))

    return kb # возвращаем готовую панель

async def highlight_selected_genres(kb, data, genres):
    for genre_data in data:
        text = genre_data[1]

        if str(genre_data[0]) in genres:
            text += " ✅"

        kb.insert(InlineKeyboardButton(text, callback_data=f"cq1:add_to_filter:{genre_data[0]}"))

    return kb
