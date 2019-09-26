from card_suit_and_value import Suit, Value


class Card:
    def __init__(self, suit: int, value: int):
        self.suit = suit
        self.value = value

    @property
    def name(self) -> str:
        return "{} of {}".format(
            Value._value_code_mapper[self.value].title(),
            Suit._suit_code_mapper[self.suit].title(),
        )

    def __repr__(self):
        return "Card(suit={}, value={})".format(self.suit, self.value)

    def __str__(self):
        return "{} {}".format(
            Suit._symbol_mapper[self.suit],
            Value._symbol_mapper[self.value],
        )

    def __hash__(self):
        return hash("{}-{}".format(self.suit, self.value))

    def __eq__(self, other: 'Card'):
        return (self.suit == other.suit) and (self.value == other.value)

    def __gt__(self, other: 'Card'):
        return self.value > other.value

    def __ge__(self, other: 'Card'):
        return self.value >= other.value

    def __ne__(self, other: 'Card'):
        return not (self == other)

    def __lt__(self, other: 'Card'):
        return not (self >= other)

    def __le__(self, other: 'Card'):
        return not (self > other)


if __name__ == "__main__":
    print(Card(suit=Suit.heart, value=Value.ace))  # Card('Ace of Heart')

    print([ # [Card(suit=2, value=14), Card(suit=2, value=14), Card(suit=2, value=14)]
        Card(suit=Suit.heart, value=Value.ace),
        Card(suit=Suit.heart, value=Value.ace),
        Card(suit=Suit.heart, value=Value.ace),
    ])

    print(Card(suit=Suit.club, value=Value.ace) > Card(suit=Suit.diamond, value=Value.king))
