# -*- coding: utf-8 -*-
import random
import json

with open('../data/tarot_cards.json', 'r', encoding='utf-8') as f:
    tarot_cards = json.load(f)

with open('../data/tarot_card_sticker_ids.json', 'r', encoding='utf-8') as f:
    tarot_card_sticker_ids = json.load(f)


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


with open('../data/tarot_cards.json', 'r', encoding='utf-8') as f:
    tarot_cards = json.load(f)

with open('../data/tarot_card_sticker_ids.json', 'r', encoding='utf-8') as f:
    tarot_card_sticker_ids = json.load(f)


def card_with_orientation():
    return random.random() <= 0.01


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
