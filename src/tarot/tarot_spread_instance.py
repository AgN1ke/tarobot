# tarot_spread_instance.py
import json
import random
from .tarot_spread import TarotSpread, SpreadCardSlot


class TarotCard:
    # Assuming you have a TarotCard class defined somewhere
    def __init__(self, name: str, reversed: bool):
        self.name = name
        self.reversed = reversed

    def __str__(self):
        return f"Card: {self.name}, Reversed: {'Yes' if self.reversed else 'No'}"


class TarotSpreadInstance:
    def __init__(self, spread: TarotSpread, card_file: str, reversal_chance: float = 0.08):
        self.spread = spread
        self.card_names = self._load_card_names(card_file)
        self.cards = self._generate_random_cards(reversal_chance)

    @staticmethod
    def _load_card_names(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def _generate_random_cards(self, reversal_chance):
        cards_map = {}
        for slot in self.spread.cards:
            card_name = random.choice(self.card_names)
            reversed = random.random() < reversal_chance
            cards_map[slot.slot_index] = TarotCard(card_name, reversed)
        return cards_map

    def get_slot_str(self, slot_index):
        try:
            slot = next(s for s in self.spread.cards if s.slot_index == slot_index)
            card = self.cards[slot_index]
            card_status = "Reversed" if card.reversed else "Upright"
            return f"Slot {slot_index} - {slot.meaning}: {card.name} ({card_status})"
        except StopIteration:
            return None

    def __str__(self):
        card_descriptions = "\n    ".join(
            f"Slot Index: {slot.slot_index}, Meaning: {slot.meaning}, Card: {self.cards[slot.slot_index]}"
            for slot in self.spread.cards
        )
        return (f"Spread ID: {self.spread.spread_id}, Name: {self.spread.name}, "
                f"Number of Cards: {self.spread.number_of_cards}, Cards:\n    {card_descriptions}")
