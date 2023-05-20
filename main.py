from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


import openai
import asyncio
import random

# Настройка OpenAI
openai.api_key = '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'

bot = Bot(token='6294843629:AAG_VbK-m_WoHCtb__okjwnuWgfWCwi_B9I')
dp = Dispatcher(bot)

# Список всех карт
tarot_cards = ["Шут", "Маг", "Верховная жрица", "Императрица", "Император", "Верховный священник",
               "Влюблённые", "Колесница", "Справедливость", "Повешенный", "Смерть", "Умеренность",
               "Дьявол", "Башня", "Звезда", "Луна", "Солнце", "Суд", "Мир", "Туз жезлов", "2 жезлов",
               "3 жезлов", "4 жезлов", "5 жезлов", "6 жезлов", "7 жезлов", "8 жезлов", "9 жезлов", "10 жезлов",
               "Валет жезлов", "Рыцарь жезлов", "Королева жезлов", "Король жезлов", "Туз кубков", "2 кубка",
               "3 кубка", "4 кубка", "5 кубков", "6 кубков", "7 кубков", "8 кубков", "9 кубков", "10 кубков", "Валет кубков", "Рыцарь кубков",
               "Королева кубков", "Король кубков", "Туз мечей", "2 мечей", "3 мечей", "4 мечей", "5 мечей", "6 мечей",
               "7 мечей", "8 мечей", "9 мечей", "10 мечей", "Валет мечей", "Рыцарь мечей", "Королева мечей",
               "Король мечей", "Туз пентаклей", "2 пентаклей", "3 пентаклей", "4 пентаклей", "5 пентаклей",
               "6 пентаклей", "7 пентаклей", "8 пентаклей", "9 пентаклей", "10 пентаклей", "Валет пентаклей",
               "Рыцарь пентаклей", "Королева пентаклей", "Король пентаклей"]



def draw_celtic_cross():
    cards = random.sample(tarot_cards, 10)
    positions = ['Текущее положение', 'Непосредственное влияние', 'Основания', 'Прошлое', 'Возможное будущее',
                 'Немедленное будущее', 'Страхи и препятствия', 'Внешняя ситуация', 'Надежды и стремления', 'Исход']
    return list(zip(cards, positions))

def draw_tree_of_life():
    cards = random.sample(tarot_cards, 10)
    positions = ['Я', 'Моя подсознательность', 'Мое сознание', 'Моя жизненная сила', 'Моя мораль',
                 'Мои привязанности', 'Мое "Я"', 'Мое окружение', 'Мои страхи', 'Мой путь']
    return list(zip(cards, positions))

def draw_wheel_of_fortune():
    cards = random.sample(tarot_cards, 7)
    positions = ['Прошлое', 'Настоящее', 'Будущее', 'Причина текущей ситуации', 'Препятствие', 'Внешнее влияние',
                 'Результат']
    return list(zip(cards, positions))

def draw_life_path():
    cards = random.sample(tarot_cards, 9)
    positions = ['Прошлое', 'Настоящее', 'Будущее', 'Что помогает', 'Что мешает', 'Что следует изучить',
                 'Что следует принять', 'Что следует отпустить', 'Что ждет в будущем']
    return list(zip(cards, positions))

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
    # Выводим ID пользователя при вызове команды /start
    user_id = message.from_user.id
    print(f"User ID: {user_id}")
    user_data[user_id] = {}  # создаем словарь для пользователя
    await bot.send_message(chat_id=message.chat.id, text='Пожалуйста, введите ваше имя:')


@dp.message_handler(lambda message: not user_data[message.from_user.id])
async def ask_name(message: types.Message):
    user_data[message.from_user.id]['name'] = message.text  # сохраняем имя
    await bot.send_message(chat_id=message.chat.id, text='Пожалуйста, введите ваш возраст:')


@dp.message_handler(
    lambda message: 'name' in user_data[message.from_user.id] and 'age' not in user_data[message.from_user.id])
async def ask_age(message: types.Message):
    user_data[message.from_user.id]['age'] = message.text  # сохраняем возраст
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


@dp.callback_query_handler(lambda c: c.data and c.data in ['1', '2', '3', '4'])
async def process_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    user_id = callback_query.from_user.id

    layout_name = layout_names[callback_query.data]
    user_data[user_id]['layout_name'] = layout_name  # сохраняем layout_name в данные пользователя

    # Выберем функцию для расклада в зависимости от выбора пользователя
    layout_func = layout_functions[callback_query.data]
    drawn_cards_with_positions = layout_func()

    # Форматируем каждую карточку на новой строке
    cards_positions_text = '\n'.join(f"{pos}: {card}" for card, pos in drawn_cards_with_positions)
    user_data[user_id][
        'cards_positions_text'] = cards_positions_text  # сохраняем cards_positions_text в данные пользователя

    # Отправляем расклад пользователю перед интерпретацией
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text=f"Ваш расклад '{layout_name}':\n{cards_positions_text}")

    # Сообщение пользователю о начале обработки расклада OpenAI
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Пожалуйста, подождите...')

    # Добавьте имя и возраст в запрос к GPT
    user_name = user_data.get(user_id, {}).get('name', '')
    user_age = user_data.get(user_id, {}).get('age', '')

    prompt_prefix = f"Я таролог и только что сделал расклад для клиента по имени {user_name}, возраст {user_age}. Расклад "
    prompt_postfix = f"'{layout_name}':\n{cards_positions_text}\n" \
                     f"Интерпретируй этот расклад для клиента от моего лица кратко. Делай отступы между картами."

    prompt = prompt_prefix + prompt_postfix

    print(f"Запрос к GPT: {prompt}")

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1500
        )

        if 'choices' in response and response['choices'] and 'text' in response['choices'][0]:
            await send_long_message(callback_query, response['choices'][0]['text'].strip())
        print(f"Ответ от GPT: {response.choices[0].text.strip()}")
    except Exception as e:
        print(f"Произошла ошибка при запросе к OpenAI: {e}")


async def send_long_message(callback_query, text):
    while text:
        if len(text) > 4096:
            pos = text.rfind(' ', 0, 4096)
        else:
            pos = len(text)
        await bot.send_message(chat_id=callback_query.message.chat.id, text=text[:pos])
        text = text[pos:]
        await asyncio.sleep(0.1)  # добавьте задержку, чтобы избежать ограничения скорости отправки сообщений

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Use /start to test this bot.")

def main():
    start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
