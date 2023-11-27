# test_tarot_spread_instance.py
import unittest

from src.tarot.tarot_spread import TarotSpreadParser
from src.tarot.tarot_spread_instance import TarotSpreadInstance


class TestTarotSpreadInstance(unittest.TestCase):
    def test_spread_instances(self):
        # Load spreads from file
        parser = TarotSpreadParser('../../data/spreads_sample.json')
        spreads = parser.parse_spreads()

        # Iterate over each spread and create an instance
        for spread in spreads:
            spread_instance = TarotSpreadInstance(spread, '../../data/tarot_cards.json')
            print(spread_instance)

            # Check if the spread instance is correctly initialized
            self.assertEqual(len(spread_instance.cards), spread.number_of_cards)

    def test_print_slot(self):
        # Load a single spread for testing
        parser = TarotSpreadParser('../../data/spreads_sample.json')
        spreads = parser.parse_spreads()
        spread_instance = TarotSpreadInstance(spreads[0], '../../data/tarot_cards.json')

        slot_str = spread_instance.get_slot_str(1)  # Replace 1 with an actual slot index from your spread
        print(slot_str)
        # Check if the output contains expected strings
        self.assertIn("Slot 1", slot_str)
        self.assertIn(spreads[0].cards[0].meaning, slot_str)


if __name__ == '__main__':
    unittest.main()
