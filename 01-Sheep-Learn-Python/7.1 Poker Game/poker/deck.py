from typing import List
import random
from card import Card, Suit, Value


class Deck:
    def __init__(self, cards: List[Card] = None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards

    def add_one(self, card: Card) -> Card:
        self.cards.append(card)
        return card

    def deal_one(self) -> Card:
        return self.cards.pop()

    def deal_one_to(self, deck: 'Deck') -> Card:
        card = self.deal_one()
        deck.add_one(card)
        return card

    def deal_many_to(self, deck: 'Deck', n: int) -> List[Card]:
        if len(self) < n:
            raise ValueError("it doesn't has {} cards to deal!".format(n))
        cards = [
            self.deal_one_to(deck)
            for _ in range(n)
        ]
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def __add__(self, other):
        return Deck(cards=self.cards + other.cards)

    def __str__(self):
        return "{}(cards=[{}])".format(
            self.__class__.__name__,
            ", ".join([
                "'%s'" % card
                for card in self.cards[::-1]
            ])
        )

    def __repr__(self):
        return "{}(cards=[{}])".format(
            self.__class__.__name__,
            ", ".join([
                repr(card)
                for card in self.cards[::-1]
            ])
        )

    @classmethod
    def new_shuffled_deck(cls) -> 'Deck':
        deck = cls(cards=[])
        for suit_code in Suit._valid_suit:
            for value_code in Value._valid_value:
                deck.add_one(Card(suit=suit_code, value=value_code))
                deck.shuffle()
        return deck

    def __len__(self):
        return len(self.cards)


if __name__ == "__main__":
    new_deck = Deck.new_shuffled_deck()
    print(len(new_deck))

    print(new_deck.deal_one())
    print(len(new_deck))

    small_deck = Deck()
    new_deck.deal_many_to(small_deck, 5)
    print(small_deck)
    print(repr(small_deck))
