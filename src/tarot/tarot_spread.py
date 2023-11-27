# tarot_spread.py
import json


class SpreadCardSlot:
    def __init__(self, slot_index, meaning):
        self.slot_index = slot_index
        self.meaning = meaning

    def __str__(self):
        return f"Slot Index: {self.slot_index}, Meaning: {self.meaning}"


class TarotSpread:
    def __init__(self, spread_id, number_of_cards, name, cards):
        self.spread_id = spread_id
        self.number_of_cards = number_of_cards
        self.name = name
        self.cards = [SpreadCardSlot(card['slot_index'], card['meaning']) for card in cards]

    def __str__(self):
        card_descriptions = "\n    ".join(str(card) for card in self.cards)
        return f"Spread ID: {self.spread_id}, Name: {self.name}, Number of Cards: {self.number_of_cards}, " \
               f"Cards:\n    {card_descriptions}"


class TarotSpreadParser:
    def __init__(self, json_file):
        self.json_file = json_file

    def parse_spreads(self):
        spreads = []
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            for spread_data in data:
                spread = TarotSpread(
                    spread_data['spread_id'],
                    spread_data['number_of_cards'],
                    spread_data['name'],
                    spread_data['cards']
                )
                spreads.append(spread)
        return spreads
