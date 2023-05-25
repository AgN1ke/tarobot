from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import openai
import random
import json

openai.api_key = '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'
bot = Bot(token='6294843629:AAG_VbK-m_WoHCtb__okjwnuWgfWCwi_B9I')
dp = Dispatcher(bot)

with open('tarot_cards.json', 'r', encoding='utf-8') as f:
    tarot_cards = json.load(f)

with open('tarot_card_sticker_ids.json', 'r', encoding='utf-8') as f:
    tarot_card_sticker_ids = json.load(f)

def card_with_orientation():
    return random.random() <= 0.01

def draw_celtic_cross():
    cards = random.sample(tarot_cards, 10)
    positions = ['Текущее положение',
                 'Непосредственное влияние',
                 'Основания',
                 'Прошлое',
                 'Возможное будущее',
                 'Немедленное будущее',
                 'Страхи и препятствия',
                 'Внешняя ситуация',
                 'Надежды и стремления',
                 'Исход']
    cards_with_orientations = [(card + ' (перевёрнута)' if card_with_orientation() else card) for card in cards]
    return list(zip(cards_with_orientations, positions))

def draw_tree_of_life():
    cards = random.sample(tarot_cards, 10)
    positions = ['Я',
                 'Моя подсознательность',
                 'Мое сознание',
                 'Моя жизненная сила',
                 'Моя мораль',
                 'Мои привязанности',
                 'Мое "Я"',
                 'Мое окружение',
                 'Мои страхи',
                 'Мой путь']
    cards_with_orientations = [(card + ' (перевёрнута)' if card_with_orientation() else card) for card in cards]
    return list(zip(cards_with_orientations, positions))

def draw_wheel_of_fortune():
    cards = random.sample(tarot_cards, 7)
    positions = ['Прошлое',
                 'Настоящее',
                 'Будущее',
                 'Причина текущей ситуации',
                 'Препятствие',
                 'Внешнее влияние',
                 'Результат']
    cards_with_orientations = [(card + ' (перевёрнута)' if card_with_orientation() else card) for card in cards]
    return list(zip(cards_with_orientations, positions))

def draw_life_path():
    cards = random.sample(tarot_cards, 9)
    positions = ['Прошлое',
                 'Настоящее',
                 'Будущее',
                 'Что помогает',
                 'Что мешает',
                 'Что следует изучить',
                 'Что следует принять',
                 'Что следует отпустить',
                 'Что ждет в будущем']
    cards_with_orientations = [(card + ' (перевёрнута)' if card_with_orientation() else card) for card in cards]
    return list(zip(cards_with_orientations, positions))

layout_functions = {
    '1': draw_celtic_cross,
    '2': draw_tree_of_life,
    '3': draw_wheel_of_fortune,
    '4': draw_life_path,
}

layout_names = {
    '1': "Крест Кельтов",
    '2': "Дерево жизни",
    '3': "Колесо судьбы",
    '4': "Путь жизни",
}

user_data = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    print(f"User ID: {user_id}")
    user_data[user_id] = {}
    await bot.send_message(chat_id=message.chat.id, text='Пожалуйста, введите ваше имя:')

@dp.message_handler(lambda message: not user_data[message.from_user.id])
async def ask_name(message: types.Message):
    user_data[message.from_user.id]['name'] = message.text
    await bot.send_message(chat_id=message.chat.id, text='Пожалуйста, введите вашу дату рождения:')

@dp.message_handler(lambda message: 'name' in user_data[message.from_user.id] and
                                    'age' not in user_data[message.from_user.id])
async def ask_age(message: types.Message):
    user_data[message.from_user.id]['age'] = message.text
    await bot.send_message(chat_id=message.chat.id, text='Пожалуйста, укажите ваш пол:')

@dp.message_handler(lambda message: 'name' in user_data[message.from_user.id] and
                                    'age' in user_data[message.from_user.id] and
                                    'gender' not in user_data[message.from_user.id])
async def ask_gender(message: types.Message):
    user_data[message.from_user.id]['gender'] = message.text
    await bot.send_message(chat_id=message.chat.id, text='Пожалуйста, расскажите о вашей текущей проблеме:')

@dp.message_handler(lambda message: 'name' in user_data[message.from_user.id] and
                                    'age' in user_data[message.from_user.id] and
                                    'gender' in user_data[message.from_user.id] and
                                    'issue' not in user_data[message.from_user.id])
async def ask_issue(message: types.Message):
    user_data[message.from_user.id]['issue'] = message.text
    await send_layout_keyboard(message)


async def send_layout_keyboard(message: types.Message):
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
    await bot.send_message(chat_id=message.chat.id, text='Пожалуйста выберите расклад:', reply_markup=reply_markup)

chat_histories = {}

@dp.callback_query_handler(lambda c: c.data and c.data in ['1', '2', '3', '4'])
async def process_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    chat_id = callback_query.message.chat.id

    if chat_id not in chat_histories:
        chat_histories[chat_id] = []

    layout_name = layout_names[callback_query.data]
    user_data[chat_id]['layout_name'] = layout_name

    layout_func = layout_functions[callback_query.data]
    drawn_cards_with_positions = layout_func()

    user_data[chat_id]['drawn_cards_with_positions'] = drawn_cards_with_positions
    user_data[chat_id]['current_card_index'] = 0

    cards_positions_text = '\n'.join(f"{pos}: {card}" for card, pos in drawn_cards_with_positions)

    await bot.send_message(chat_id=callback_query.message.chat.id, text=cards_positions_text)

    await ask_question_about_card(chat_id)

async def ask_question_about_card(chat_id):
    user_name = user_data.get(chat_id, {}).get('name', '')
    user_age = user_data.get(chat_id, {}).get('age', '')
    user_gender = user_data.get(chat_id, {}).get('gender', '')
    user_issue = user_data.get(chat_id, {}).get('issue', '')
    layout_name = user_data[chat_id]['layout_name']
    drawn_cards_with_positions = user_data[chat_id]['drawn_cards_with_positions']
    current_card_index = user_data[chat_id]['current_card_index']

    card, pos = drawn_cards_with_positions[current_card_index]

    cards_positions_text = '\n'.join(f"{pos}: {card}" for card, pos in drawn_cards_with_positions)

    prompt = f"Ты сделал расклад для клиента по имени {user_name}, дата рождения {user_age}, " \
             f"пол {user_gender}, проблема {user_issue}. " \
             f"Расклад '{layout_name}':\n{cards_positions_text}\n" \
             f"Предложи наводящий вопрос к карте {card} в контексте '{pos}'."

    await gpt_request(chat_id, prompt, 200)

async def interpret_card(chat_id):
    user_response = user_data[chat_id].get('user_response', '')

    user_name = user_data.get(chat_id, {}).get('name', '')
    user_age = user_data.get(chat_id, {}).get('age', '')
    layout_name = user_data[chat_id]['layout_name']
    drawn_cards_with_positions = user_data[chat_id]['drawn_cards_with_positions']
    current_card_index = user_data[chat_id]['current_card_index']

    card, pos = drawn_cards_with_positions[current_card_index]

    cards_positions_text = '\n'.join(f"{pos}: {card}" for card, pos in drawn_cards_with_positions)

    prompt = f"Ты таролог и только что сделал расклад для клиента по имени {user_name}, {user_age} лет. " \
             f"Расклад '{layout_name}':\n{cards_positions_text}\n" \
             f"Клиент ответил на ваш вопрос о карте {card} в контексте '{pos}': '{user_response}'. " \
             f"Интерпретируй карту {card} в контексте '{pos}' от моего лица обращаясь по имени. "

    await gpt_request(chat_id, prompt, 2000)

    user_data[chat_id]['current_card_index'] += 1
    user_data[chat_id]['user_response'] = ''

    if user_data[chat_id]['current_card_index'] < len(drawn_cards_with_positions):
        await ask_question_about_card(chat_id)
    else:
        await bot.send_message(chat_id=chat_id, text="Интерпретация расклада завершена.")

@dp.message_handler(content_types=['text'])
async def process_user_input(message: types.Message):
    chat_id = message.chat.id

    if chat_id not in chat_histories:
        print("Ошибка: нет истории чата для этого chat_id.")
        return

    chat_history = chat_histories[chat_id]

    user_input = message.text
    chat_history.append({"role": "user", "content": user_input})

    user_data[chat_id]['user_response'] = user_input
    await interpret_card(chat_id)

async def gpt_request(chat_id, prompt, max_tokens):
    print(f"Запрос к GPT: {prompt}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты - ассистент, обученный интерпретировать расклады карт таро."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )

        bot_response = response['choices'][0]['message']['content']
        chat_histories[chat_id].append({"role": "assistant", "content": bot_response})
        print(f"Bot: {bot_response}")

        await bot.send_message(chat_id=chat_id, text=bot_response)
    except Exception as e:
        print(f"Произошла ошибка при запросе к OpenAI: {e}")

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Press /start to start.")

def main():
    start_polling(dp)

if __name__ == '__main__':
    main()



