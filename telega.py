# -*- coding: utf-8 -*-

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from rasklady import layout_functions, layout_names


class TarotBot:
    def __init__(self, token, bd, gpt):
        self.bot = Bot(token=token)
        self.dp = Dispatcher(self.bot)
        self.user_data = {}
        self.gpt = gpt
        self.bd = bd

        self.setup_handlers()

    def setup_handlers(self):
        self.dp.message_handler(commands=['start'])(self.start)
        self.dp.message_handler(lambda message: not self.user_data[message.from_user.id])(self.ask_name)
        self.dp.message_handler(lambda message: 'name' in self.user_data[message.from_user.id] and
                                                'age' not in self.user_data[message.from_user.id])(self.ask_age)
        self.dp.message_handler(lambda message: 'name' in self.user_data[message.from_user.id] and
                                                'age' in self.user_data[message.from_user.id] and
                                                'gender' not in self.user_data[message.from_user.id])(self.ask_gender)
        self.dp.message_handler(lambda message: 'name' in self.user_data.get(message.from_user.id, {}) and
                                                'age' in self.user_data.get(message.from_user.id, {}) and
                                                'gender' in self.user_data.get(message.from_user.id, {}) and
                                                'issue' not in self.user_data.get(message.from_user.id, {}))(
            self.ask_issue)
        self.dp.callback_query_handler(lambda c: c.data and c.data in ['1', '2', '3', '4'])(self.process_callback)
        self.dp.message_handler(content_types=['text'])(self.process_user_input)

    async def start(self, message: types.Message):
        user_id = message.from_user.id
        print(f"Telegram Name: {message.from_user.first_name} {message.from_user.last_name} ID: {user_id}")
        self.user_data[user_id] = {}
        await self.bot.send_message(chat_id=message.chat.id, text='Пожалуйста, введите ваше имя:')

    async def ask_name(self, message: types.Message):
        self.user_data[message.from_user.id]['name'] = message.text
        print(f"User's name: {message.text}")
        await self.bot.send_message(chat_id=message.chat.id, text='Пожалуйста, введите вашу дату рождения:')

    async def ask_age(self, message: types.Message):
        self.user_data[message.from_user.id]['age'] = message.text
        print(f"User's age: {message.text}")
        await self.bot.send_message(chat_id=message.chat.id, text='Пожалуйста, укажите ваш пол:')

    async def ask_gender(self, message: types.Message):
        self.user_data[message.from_user.id]['gender'] = message.text
        print(f"User's gender: {message.text}")
        await self.bot.send_message(chat_id=message.chat.id, text='Пожалуйста, расскажите о вашей текущей проблеме:')

    async def ask_issue(self, message: types.Message):
        user_id = message.from_user.id

        self.user_data.setdefault(user_id, {})

        existing_user = self.bd.user_exists(user_id)

        if not existing_user:
            self.bd.add_user(user_id, message.from_user.first_name, message.from_user.last_name,
                             self.user_data[user_id]['name'],
                             self.user_data[user_id]['age'],
                             self.user_data[user_id]['gender'])

        self.bd.add_issue(user_id, message.text)
        self.user_data[user_id]['issue'] = message.text

        await self.send_layout_keyboard(message)

    async def send_layout_keyboard(self, message: types.Message):
        keyboard = [
            [
                InlineKeyboardButton("Крест Кельтов", callback_data='1'),
                InlineKeyboardButton("Дерево жизни", callback_data='2')
            ],
            [
                InlineKeyboardButton("Колесо судьбы", callback_data='3'),
                InlineKeyboardButton("Путь жизни", callback_data='4')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await self.bot.send_message(chat_id=message.chat.id, text='Пожалуйста выберите расклад:',
                                    reply_markup=reply_markup)

    async def process_callback(self, callback_query: types.CallbackQuery):
        await self.bot.answer_callback_query(callback_query.id)

        chat_id = callback_query.message.chat.id

        if chat_id not in self.user_data:
            self.user_data[chat_id] = {}

        layout_name = layout_names[callback_query.data]
        self.user_data[chat_id]['layout_name'] = layout_name

        layout_func = layout_functions[callback_query.data]
        drawn_cards_with_positions = layout_func()

        self.user_data[chat_id]['drawn_cards_with_positions'] = drawn_cards_with_positions
        self.user_data[chat_id]['current_card_index'] = 0

        cards_positions_text = '\n'.join(f"{pos}: {card}" for card, pos in drawn_cards_with_positions)

        await self.bot.send_message(chat_id=callback_query.message.chat.id, text=cards_positions_text)

        await self.ask_question_about_card(chat_id)

    async def ask_question_about_card(self, chat_id):
        user_name = self.user_data.get(chat_id, {}).get('name', '')
        user_age = self.user_data.get(chat_id, {}).get('age', '')
        user_gender = self.user_data.get(chat_id, {}).get('gender', '')
        user_issue = self.user_data.get(chat_id, {}).get('issue', '')
        layout_name = self.user_data[chat_id]['layout_name']
        drawn_cards_with_positions = self.user_data[chat_id]['drawn_cards_with_positions']
        current_card_index = self.user_data[chat_id]['current_card_index']

        card, pos = drawn_cards_with_positions[current_card_index]

        cards_positions_text = '\n'.join(f"{pos}: {card}" for card, pos in drawn_cards_with_positions)

        prompt = f"Ты сделал расклад для клиента по имени {user_name}, дата рождения {user_age}, " \
                 f"пол {user_gender}, проблема {user_issue}. " \
                 f"Расклад: '{layout_name}':\n{cards_positions_text}\n" \
                 f"Предложи наводящий вопрос, который нужен для трактовки карты {card} в контексте '{pos}' " \
                 f"и личных данных человека. Но не задавай очень сложные абстрактные вопросы." \
                 f"Будь как психолог." \
                 f"Обращайся от моего лица по имени на вы." \
                 f"Не здоровайся, не пиши ничего лишнего кроме вопроса."

        bot_response = self.gpt.gpt_request(chat_id, prompt, 500)
        await self.bot.send_message(chat_id=chat_id, text=bot_response)

    async def interpret_card(self, chat_id):
        user_response = self.user_data[chat_id].get('user_response', '')

        user_name = self.user_data.get(chat_id, {}).get('name', '')
        user_age = self.user_data.get(chat_id, {}).get('age', '')
        layout_name = self.user_data[chat_id]['layout_name']
        user_gender = self.user_data.get(chat_id, {}).get('gender', '')
        user_issue = self.user_data.get(chat_id, {}).get('issue', '')
        drawn_cards_with_positions = self.user_data[chat_id]['drawn_cards_with_positions']
        current_card_index = self.user_data[chat_id]['current_card_index']

        card, pos = drawn_cards_with_positions[current_card_index]

        cards_positions_text = '\n'.join(f"{pos}: {card}" for card, pos in drawn_cards_with_positions)

        prompt = f"Ты только что сделал расклад для клиента по имени {user_name}, дата рождения {user_age}. " \
                 f"пол {user_gender}, проблема {user_issue}. " \
                 f"Расклад '{layout_name}':\n{cards_positions_text}\n" \
                 f"Клиент ответил на ваш вопрос о карте {card} в контексте '{pos}': '{user_response}'. " \
                 f"Интерпретируй карту {card} в контексте '{pos}' от моего лица обращаясь по имени и на вы. "

        bot_response = self.gpt.gpt_request(chat_id, prompt, 2000)
        await self.bot.send_message(chat_id=chat_id, text=bot_response)

        self.user_data[chat_id]['current_card_index'] += 1
        self.user_data[chat_id]['user_response'] = ''

        if self.user_data[chat_id]['current_card_index'] < len(drawn_cards_with_positions):
            await self.ask_question_about_card(chat_id)
        else:
            await self.bot.send_message(chat_id=chat_id, text="Интерпретация расклада завершена.")

    async def process_user_input(self, message: types.Message):
        chat_id = message.chat.id

        if chat_id not in self.user_data:
            print("Ошибка: нет истории чата для этого chat_id.")
            return

        user_input = message.text

        self.user_data[chat_id]['user_response'] = user_input
        await self.interpret_card(chat_id)

    def main(self):
        start_polling(self.dp)
