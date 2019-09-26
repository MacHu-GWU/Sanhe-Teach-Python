class Suit:
    spade = 1
    heart = 2
    club = 3
    diamond = 4

    _suit_code_mapper = dict()
    _symbol_mapper = {
        "spade": "♠",
        "heart": "♥",
        "club": "♦",
        "diamond": "♣",
    }
    _valid_suit = set()


for suit_name, suit_code in Suit.__dict__.items():
    if not suit_name.startswith("_"):
        Suit._suit_code_mapper[suit_name] = suit_code
        Suit._suit_code_mapper[suit_code] = suit_name

        Suit._symbol_mapper[suit_code] = Suit._symbol_mapper[suit_name]

        Suit._valid_suit.add(suit_code)


class Value:
    ace = 14
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13

    _value_code_mapper = dict()
    _symbol_mapper = {
        "ace": "A",
        "jack": "J",
        "queen": "Q",
        "king": "K",
    }
    _valid_value = set()


for value_name, value_code in Value.__dict__.items():
    if not value_name.startswith("_"):
        Value._value_code_mapper[value_name] = value_code
        Value._value_code_mapper[value_code] = value_name

        Value._symbol_mapper.setdefault(value_name, str(value_code))
        Value._symbol_mapper[value_code] = Value._symbol_mapper[value_name]

        Value._valid_value.add(value_code)


if __name__ == "__main__":
    from pprint import pprint

    pprint(Suit._suit_code_mapper)
    pprint(Suit._symbol_mapper)
    pprint(Suit._valid_suit)

    pprint(Value._value_code_mapper)
    pprint(Value._symbol_mapper)
    pprint(Value._valid_value)

    print(type(Suit))
    print(type(Value))
