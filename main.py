from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import openai
import random
#import re
#import asyncio

openai.api_key = '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'
bot = Bot(token='6294843629:AAG_VbK-m_WoHCtb__okjwnuWgfWCwi_B9I')
dp = Dispatcher(bot)

# Список всех карт
tarot_cards = ["Дурак",
    "Маг",
    "Верховная жрица",
    "Императрица",
    "Император",
    "Верховный жрец",
    "Влюблённые",
    "Колесница",
    "Сила",
    "Отшельник",
    "Колесо фортуны",
    "Справедливость",
    "Повешенный",
    "Смерть",
    "Умеренность",
    "Дьявол",
    "Башня",
    "Звезда",
    "Луна",
    "Солнце",
    "Суд",
    "Мир",
    "Туз мечей",
    "2 меча",
    "3 меча",
    "4 меча",
    "5 мечей",
    "6 мечей",
    "7 мечей",
    "8 мечей",
    "9 мечей",
    "10 мечей",
    "Валет мечей",
    "Рыцарь мечей",
    "Королева мечей",
    "Король мечей",
    "Туз кубков",
    "2 кубка",
    "3 кубка",
    "4 кубка",
    "5 кубков",
    "6 кубков",
    "7 кубков",
    "8 кубков",
    "9 кубков",
    "10 кубков",
    "Валет кубков",
    "Рыцарь кубков",
    "Королева кубков",
    "Король кубков",
    "Туз пентаклей",
    "2 пентаклей",
    "3 пентаклей",
    "4 пентаклей",
    "5 пентаклей",
    "6 пентаклей",
    "7 пентаклей",
    "8 пентаклей",
    "9 пентаклей",
    "10 пентаклей",
    "Валет пентаклей",
    "Рыцарь пентаклей",
    "Королева пентаклей",
    "Король пентаклей",
    "Туз жезлов",
    "2 жезла",
    "3 жезла",
    "4 жезла",
    "5 жезлов",
    "6 жезлов",
    "7 жезлов",
    "8 жезлов",
    "9 жезлов",
    "10 жезлов",
    "Валет жезлов",
    "Рыцарь жезлов",
    "Королева жезлов",
    "Король жезлов",
]

#список карт + стикер ID
tarot_card_sticker_ids = {
    "Дурак": "CAACAgIAAxkBAAICxGRpNICJbDMl9tutPRZcmPGDji5qAALkMQAC0o9ISy57XY6zQPAZLwQ",
    "Маг": "CAACAgIAAxkBAAICxmRpNIPH2U8s6Z7D2CMjC6abzsULAAJ2LAACsE1ISz210jUQsrd_LwQ",
    "Верховная жрица": "CAACAgIAAxkBAAICyGRpNIXTTYYp9IORx9J1AAH4ntColAACRSgAAtt1SEvT-8hnuYJsIi8E",
    "Императрица": "CAACAgIAAxkBAAICymRpNIbg77dcSP-qJOvDo_cISvlqAAIoLAACfItJS6vTgjo9ZM4VLwQ",
    "Император": "CAACAgIAAxkBAAICzGRpNIfFR-vewAqbNgGaEbBHKFrtAAKIKgACkYxIS5Ig6QjMyvLoLwQ",
    "Верховный жрец": "CAACAgIAAxkBAAICzmRpNIgtoMyDa9UMZvIk-eKauGZBAAIUMgACaKFJS6FYP93ReJKyLwQ",
    "Влюблённые": "CAACAgIAAxkBAAIC0GRpNIgeQXTHIi2Cyjv8g0O98uPvAAIGKgACRgABUEvhuNAPkL8pBi8E",
    "Колесница": "CAACAgIAAxkBAAIC0mRpNIreXZ8enqZb6bdjKz41tLiNAAKvJwACPMhRS8NCcr73V9yiLwQ",
    "Сила": "CAACAgIAAxkBAAIC1GRpNIvoc0eVS_u4GjHVTRZ9tRXyAAJnMgACDttISxdONEBmn0xYLwQ",
    "Отшельник": "CAACAgIAAxkBAAIC1mRpNIwLpsHvCZPrcVHzlfCsGPybAALYLQACwqZISyleyJ3tVlyoLwQ",
    "Колесо фортуны": "CAACAgIAAxkBAAIC2GRpNI6T-pFW7gZRQzBgzTJoE_UfAAJ0LQACd91IS5zc385Z5d3NLwQ",
    "Справедливость": "CAACAgIAAxkBAAIC2mRpNI_46KILFkRdkvlwPkAPvj1HAALPLwACVCpISwk3E4LHlVFSLwQ",
    "Повешенный": "CAACAgIAAxkBAAIC3GRpNJBE5f-x__E_QMnK1ShzDCY3AAKaLwAC86pIS1V53Tmfr9F3LwQ",
    "Смерть": "CAACAgIAAxkBAAIC3mRpNJHEczlQGCJgbCYUFlWcTk3QAAL2KAACVdpRS4CJcFLXHQhiLwQ",
    "Умеренность": "CAACAgIAAxkBAAIC4GRpNJISB9z7nNzFA8JrJFI_g_NAAAK9MgAC9LNIS3zxHUWuEdxRLwQ",
    "Дьявол": "CAACAgIAAxkBAAIC4mRpNJR0Ek5yMIKi-IivBif1gXUqAALvLgACqWlIS9Ra0psB02yZLwQ",
    "Башня": "CAACAgIAAxkBAAIC5GRpNJe_Bftvc2sjVDFRZjX56XiBAALgLwAC85pIS91f2jgth25NLwQ",
    "Звезда": "CAACAgIAAxkBAAIC5mRpNJgWPMjCzo4wX0-did_zLemQAAIxMQACeQdJSzwmWpHPa4K8LwQ",
    "Луна": "CAACAgIAAxkBAAIC6GRpNJodWPsommt5nQtm-7Qf53wZAAKULAACvBtIS7tcbbdkSp4HLwQ",
    "Солнце": "CAACAgIAAxkBAAIC6mRpNJv56eTWZjlGgyKx_7EnEsBbAAIpMQACV8dISzXKyQtBwlYOLwQ",
    "Суд": "CAACAgIAAxkBAAIC7GRpNJx2PunLqxka-fV9Mu7aYHJqAALsKAAC5cxIS5ake1TthWBZLwQ",
    "Мир": "CAACAgIAAxkBAAIC7mRpNJ1Evvvhqb4XgZWYa9JojH5XAAKXKQACp2NRSwdf4B2G83FGLwQ",
    "Туз мечей": "CAACAgIAAxkBAAIC8GRpNJ4ZL8BIuHDs9HrBNUuxF_1rAAJBMgACArxISy3-llZ5hXiHLwQ",
    "2 меча": "CAACAgIAAxkBAAIC8mRpNJ-aeB-VESh0wqOATbZmDqn3AALxKQACYBVRS0V4JuGhIh7ZLwQ",
    "3 меча": "CAACAgIAAxkBAAIC9GRpNKEP3i-okjQd897wtgQ5qjTzAAKuKQACZlhQS0saDhO1Qq36LwQ",
    "4 меча": "CAACAgIAAxkBAAIC9mRpNKNk_1FhmNG4biF7IYfs1Ma3AAICLQACmVZISzBKWILhI8tMLwQ",
    "5 мечей": "CAACAgIAAxkBAAIC-GRpNKQ1IPAwkG4nENw7V2Qfl4xCAAKOMAAC3EBJS38AAS9r5ZhFcy8E",
    "6 мечей": "CAACAgIAAxkBAAIC-mRpNKWphIyp811Z38GHhBY30xFHAAJrMwACBxhJS1sXEocAAfJBSC8E",
    "7 мечей": "CAACAgIAAxkBAAIC_GRpNKeQQ6cgBHX0rM9raIUAAXg7zAACsiYAAvAXUEtqqaJxXI_OOC8E",
    "8 мечей": "CAACAgIAAxkBAAIC_mRpNKjrGcyiaH5eY2oSv1N-0N0EAAKELQACDDJQS0n9Q2A9LRUsLwQ",
    "9 мечей": "CAACAgIAAxkBAAIDAAFkaTSp9mw2ATQbm8cSKZ91slEyZQAC9CwAAhuESUsnhIwKN34ITC8E",
    "10 мечей": "CAACAgIAAxkBAAIDAmRpNKr8xN6fvc45tjPdqjZE0UzRAAKBKgACreRQSx8C--u3amYsLwQ",
    "Валет мечей": "CAACAgIAAxkBAAIDBGRpNKsaAAG595bhj4LrSr9c6cntwgACkSgAAnyXUUt9OAABTsiE5C8vBA",
    "Рыцарь мечей": "CAACAgIAAxkBAAIDBmRpNKxOUFqzxsiQTxdQ-YqvjOsMAALjLwACtdxIS-VegZctnHJ9LwQ",
    "Королева мечей": "CAACAgIAAxkBAAIDCGRpNK1Z8xfislcq-tPd-okZY6RQAALTIwAC-S5QSwj7RWqR08C1LwQ",
    "Король мечей": "CAACAgIAAxkBAAIDCmRpNK95-lF0J3TkTnyyu-zVFfEeAAJALwACsh5JS5Aj-TQVSi5-LwQ",
    "Туз кубков": "CAACAgIAAxkBAAIDDGRpNLF1rivxMruQiereBdvI3t4TAALcLAACWH5JS8RHxex0JRTALwQ",
    "2 кубка": "CAACAgIAAxkBAAIDDmRpNLIwmC1o-I6OLz1r7akBVDYDAAJ6KgACI3BISxkaGOTgF5D9LwQ",
    "3 кубка": "CAACAgIAAxkBAAIDEGRpNLM3ie4-hT-IdWHaX-sfoGF-AALfJgACuvFRS2Fvv6PV6bcoLwQ",
    "4 кубка": "CAACAgIAAxkBAAIDEmRpNLT_oTPn_6uciPq-nL939I5_AAIcKwACbPxIS8IddrxElr16LwQ",
    "5 кубков": "CAACAgIAAxkBAAIDFGRpNLXjaASUNssQXoRJrUwqjsDPAAKNMQACzF5JSwe4T8x0HV7KLwQ",
    "6 кубков": "CAACAgIAAxkBAAIDFmRpNLZ-LKjUH_qmDnFGk4fKFmv0AALlLAAC4ilISzhXcSxQC0J8LwQ",
    "7 кубков": "CAACAgIAAxkBAAIDGGRpNLc7qg5JnQHtNYKgQKmhvN95AAJMMAACn51IS8sAAUka_J3bAAEvBA",
    "8 кубков": "CAACAgIAAxkBAAIDGmRpNLhUR_tRZZQVfNASvtpxTksQAAIGMQACfHNIS91KnpDvUgJnLwQ",
    "9 кубков": "CAACAgIAAxkBAAIDHGRpNLlYgQABvc4Lb2N9LiHUS2equAACHjkAAkiySUvdKIOlRdrfTC8E",
    "10 кубков": "CAACAgIAAxkBAAIDHmRpNLst7vXVU4KB5Ju96p-Rqz3eAALsLgACKxhJS04FZzK2kxIAAS8E",
    "Валет кубков": "CAACAgIAAxkBAAIDIGRpNL0JejRa_ePpa4cyizHX_NOpAAKALwACRA1JS-QmT0Az13-aLwQ",
    "Рыцарь кубков": "CAACAgIAAxkBAAIDImRpNL69gCvcZQ77-2J_u3zce06-AAK7JgAC61VRSzvbE0Ki4klMLwQ",
    "Королева кубков": "CAACAgIAAxkBAAIDJGRpNL8wyW4ISPpnkBBjghq8FBSiAAJAPQACopFJS7FT23KmtAmbLwQ",
    "Король кубков": "CAACAgIAAxkBAAIDJmRpNMAkvctl0G8CCpgJqDFjWZJbAAI7MAACaIFIS5Z7ekaTJDK3LwQ",
    "Туз пентаклей": "CAACAgIAAxkBAAIDKGRpNMFQ-CH7XBPiAlNi6yOm4pZMAAKZKgACzPhJS5zJxo-qEd0NLwQ",
    "2 пентаклей": "CAACAgIAAxkBAAIDKmRpNMMG5J0XPjIj7ki06_4AASgH6QAC3zgAAkRZSUulZZFb4oYlgS8E",
    "3 пентаклей": "CAACAgIAAxkBAAIDLGRpNMM9V2smPWrcnZnnpWCFG9ByAALQLwACR31JS6Bjpyn7Rf2_LwQ",
    "4 пентаклей": "CAACAgIAAxkBAAIDLmRpNMVWSOhRIwMNC73WKAUXno3rAAK3LgACvlBIS8Ttl50drsSwLwQ",
    "5 пентаклей": "CAACAgIAAxkBAAIDMGRpNMV1qFJoqNodnlZ6Za-2iodqAALrLgACFMFJS7IME3p4l3zQLwQ",
    "6 пентаклей": "CAACAgIAAxkBAAIDMmRpNMbaz3Ohks9oSwHJNUBb6eTLAALxNQACs8tISxRVzBNDVJcnLwQ",
    "7 пентаклей": "CAACAgIAAxkBAAIDNGRpNMjb0Cn7MA3kcHPh1YbP3maPAAJTMQACmYFIS8qb1NuAy9sFLwQ",
    "8 пентаклей": "CAACAgIAAxkBAAIDNmRpNMlgLztXbZJYMLZqLiFTCWtoAALEJwACx_5IS36O85OJ8l06LwQ",
    "9 пентаклей": "CAACAgIAAxkBAAIDOGRpNMoeFZDoO5i1GkwgpBIGz09PAAKBLAACBjVIS3PFqfzbvMGwLwQ",
    "10 пентаклей": "CAACAgIAAxkBAAIDOmRpNMv2m_f_Rb0cpaoo0EiXGoyAAAIZMAACEGhIS6yHeNoQfDmHLwQ",
    "Валет пентаклей": "CAACAgIAAxkBAAIDPGRpNMwEFD_coizoYnx7SBThvboyAALwLQAC-LFIS3DSec2HM8lnLwQ",
    "Рыцарь пентаклей": "CAACAgIAAxkBAAIDPmRpNM1eKDxg-B4YPLOh6s2lSyusAAKsNAACfwJJSwmYmt03CAwULwQ",
    "Королева пентаклей": "CAACAgIAAxkBAAIDQGRpNM5MLFoHl4Or44Cl5pyT9xGQAAK1MAACxbtJS3ZtmQnwO4plLwQ",
    "Король пентаклей": "CAACAgIAAxkBAAIDQmRpNM__9d9EnORWbGNUFtgR1njUAAJ8MAACcAZJS10ZN0AaOBOrLwQ",
    "Туз жезлов": "CAACAgIAAxkBAAIDRGRpNNAJ8Z4oY7chgKoSoc-NYevuAAKCMQACaWtJS441UNEkKGBDLwQ",
    "2 жезла": "CAACAgIAAxkBAAIDRmRpNNH_uzUD5LyhpJFyDJ_4qAaIAAJULAACBgdJSwuYesNVxd_CLwQ",
    "3 жезла": "CAACAgIAAxkBAAIDSGRpNNJDSq8O_NOH-IDZ0bp19FolAAK7LgACCP9IS3hamLAHHGv6LwQ",
    "4 жезла": "CAACAgIAAxkBAAIDSmRpNNOGpr4JWwwupyjHelJfpiAvAAK4NwACSpBJS733j61yZI0lLwQ",
    "5 жезлов": "CAACAgIAAxkBAAIDTGRpNNQQ1nw_Q0bZ2GwarRYHbgqyAAKgKwACn2ZRS30vjbVNX897LwQ",
    "6 жезлов": "CAACAgIAAxkBAAIDTmRpNNhcylMFTtje-1v0Noq9wMsAA2QyAALSB0lLS_oZmxs3iIcvBA",
    "7 жезлов": "CAACAgIAAxkBAAIDUGRpNNq2pGdGAAHCdctrel-Af52iMAACDDYAAlyWSUuR7hUXqE431y8E",
    "8 жезлов": "CAACAgIAAxkBAAIDUmRpNNuLn3IN9KVBHMg6C23_lSxlAALaNgACHHxIS1uvpm6BDqkGLwQ",
    "9 жезлов": "CAACAgIAAxkBAAIDVGRpNNxWofUq-YBkdNVOKZNGiAXNAAKGLwACuuxIS4ejTEOhlx5wLwQ",
    "10 жезлов": "CAACAgIAAxkBAAIDVmRpNN2rh0kGVMyV3fIgy5JwGP87AAIvLQACKj5JS0PNmBd2v4_vLwQ",
    "Валет жезлов": "CAACAgIAAxkBAAIDWGRpNN7gyBMkNf3GJ7jR1fRKrZutAAIDLwACIL9JS-uifJOcNh9fLwQ",
    "Рыцарь жезлов": "CAACAgIAAxkBAAIDWmRpNN96A-HugseC2f1Ani6nX1j_AAJ6NQAC6NVJS9p8paKvkFM5LwQ",
    "Королева жезлов": "CAACAgIAAxkBAAIDXGRpNODlnk3j_2XYR-DBXE8NuxdHAAL0LwACVcZIS3OoSPgnKd6wLwQ",
    "Король жезлов": "CAACAgIAAxkBAAIDXmRpNOHD5j_susewWcy99exltLiaAAKTMgACFQhIS6nfa7q5qGvyLwQ",
}

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



