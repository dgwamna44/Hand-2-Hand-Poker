import unittest
from hand2handpoker import *
from poker_hands import *
from poker_database import *
from datetime import date

class MyTestClass(unittest.TestCase):
    """Ensure there's 52 cards in a new deck"""
    def test_52_cards(self):
        new_deck = Deck() 
        expected = 52
        actual = len(new_deck.cards)
        self.assertEqual(expected, actual)

    """Ensure face card is converted to correct rank"""
    def test_face_card_to_rank(self):
        ace_of_spades = Card("Ace", "spade", "path")
        expected = 14
        actual = face_card_to_rank(ace_of_spades.value)
        self.assertEqual(expected, actual)

    """Ensure rank is converted to correct face card"""
    def test_rank_to_face_card(self):
        king_rank = 13
        expected = "King"
        actual = rank_to_face_card(king_rank)
        self.assertEqual(expected, actual)
    
    def test_find_matches_two_pair(self):
        """Ensure that the Two Pair result is provided entering a given hand"""
        card1 = Card(7, "spade", None)
        card2 = Card(7, "diamond", None)
        card3 = Card(8, "spade", None)
        card4 = Card(8, "heart", None)
        card5 = Card("Ace", "club", None)
        hand = [card1, card2, card3, card4, card5]
        result = find_matches(hand)
        expected = "Two Pair"
        actual = result[0]
        self.assertEqual(expected, actual)

    def test_find_matches_full_house(self):
        """Ensure that the full_house result is provided entering a given hand"""
        card1 = Card(5, "spade", None)
        card2 = Card(5, "diamond", None)
        card3 = Card(5, "spade", None)
        card4 = Card("Queen", "heart", None)
        card5 = Card("Queen", "club", None)
        hand = [card1, card2, card3, card4, card5]
        result = find_matches(hand)
        expected = "Full House"
        actual = result[0]
        self.assertEqual(expected, actual)

        
    def test_find_straight_points(self):
        """Ensure the correct number of points are awarded for the straight hand"""
        card1 = Card(7, "spade", None)
        card2 = Card(8, "diamond", None)
        card3 = Card(9, "spade", None)
        card4 = Card(10, "heart", None)
        card5 = Card("Jack", "club", None)
        hand = [card1, card2, card3, card4, card5]
        result = find_matches(hand)
        expected = 60
        actual = result[1] # second item of tuple contains the point value for hand
        self.assertEqual(expected, actual)

    def test_royal_flush(self):
        """Ensure royal flush is detected (values == 10, "Jack", "Queen", "King" and "Ace", and all the same suit"""
        card1 = Card(10, "spade", None)
        card2 = Card("Jack", "spade", None)
        card3 = Card("Queen", "spade", None)
        card4 = Card("King", "spade", None)
        card5 = Card("Ace", "spade", None)
        hand = [card1, card2, card3, card4, card5]
        result = find_matches(hand)
        expected = "Royal Flush"
        actual = result[0]
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
