import telebot
from telebot import types

import logging
import msg
import os
import keybords
from config import TOKEN
from sqliteormmagic import SQLiteDB
from datetime import datetime
import pytz

db_users = SQLiteDB('users.db')

def get_msk_time() -> datetime:
    time_now = datetime.now(pytz.timezone("Europe/Moscow"))
    time_now = time_now.strftime('%Y-%m-%d %H:%M:%S')
    return time_now

bot = telebot.TeleBot(token=TOKEN, parse_mode='HTML', skip_pending=True) 

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "Запуск бота"),
    ],)


def main():
    @bot.message_handler(commands=['start'])
    def start_fnc(message):
        db_users.create_table('users', [
            ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
            ('from_user_id', 'INTEGER'), 
            ('task', 'TEXT'),
            ('reg_time', 'TEXT'),
        ])

        bot.send_message(chat_id=message.from_user.id, text=msg.start_msg,reply_markup=keybords.menu_main())
              
    
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        print(f"call {call.data}")

        if call.data=='add':
            m = bot.send_message(chat_id=call.from_user.id, text=msg.add_txt)
            bot.register_next_step_handler(m, get_text)

        elif call.data=='look':
            task_list = db_users.find_elements_in_column(table_name='users', column_name='from_user_id', key_name=call.from_user.id)
            text = ''
            for task in task_list:
                text += f"""
ID: {task[0]}
Время: {task[3]}
Текст: {task[2]}
"""

            bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=keybords.menu_main())

        elif call.data=='del':
            print(f"call {call.data}")
            m = bot.send_message(chat_id=call.from_user.id, text=msg.del_txt)
            bot.register_next_step_handler(m, del_task)

    @bot.message_handler(content_types=['text'])
    def get_text(message):
        print(f"message {message.text}")
        bot.send_message(chat_id=message.from_user.id, text=msg.add_txt_sucess, reply_markup=keybords.menu_main())
        db_users.ins_unique_row('users', [
            ('from_user_id', message.from_user.id),
            ('task', message.text),
            ('reg_time', get_msk_time()),
        ])

    def del_task(message):
        print(f"message {message.text}") 
        db_users.del_row(table_name='users', column='id', key_name=message.text)
        bot.send_message(chat_id=message.from_user.id, text=msg.del_txt_sucess, reply_markup=keybords.menu_main())
        
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    main()

    