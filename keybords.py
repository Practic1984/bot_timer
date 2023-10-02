from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def menu_main():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Добавить", callback_data="add"),
        InlineKeyboardButton("Посмотреть", callback_data="look"),
        InlineKeyboardButton("Удалить", callback_data="del"),                
    )

    return markup
