import itertools
from typing import List, Dict
from deck import Suit, Value, Card, Deck


class Board(Deck):
    pass

class PlayerHand(Deck):
    pass


hand_type_power = 10 ** 6 # one million

class HandType:
    royal_flush = 9
    straight_flush = 8
    four_of_a_kind = 7
    full_house = 6
    flush = 5
    straight = 4
    three_of_a_kind = 3
    two_pairs = 2
    pair = 1
    high_card = 0

    _hand_type_code_mapper = dict()


for hand_name, hand_code in HandType.__dict__.items():
    if not hand_name.startswith("_"):
        HandType._hand_type_code_mapper[hand_name] = hand_code
        HandType._hand_type_code_mapper[hand_code] = hand_name


def product(a_list):
    res = 1
    for v in a_list:
        res *= v
    return res


class Hand(Deck):
    """
    a 5 cards deck
    """
    @classmethod
    def random_hand(cls):
        hand = cls()
        deck = cls.new_shuffled_deck()
        deck.deal_many_to(hand, 5)
        return hand

    @property
    def suits(self) -> List[int]:
        return [card.suit for card in self.cards]

    @property
    def values(self) -> List[int]:
        return [card.value for card in self.cards]

    @property
    def counter(self) -> Dict:
        dct = dict()
        for value in self.values:
            try:
                dct[value] += 1
            except KeyError:
                dct[value] = 1
        return dct

    def is_flush(self) -> bool:
        return len(set(self.suits)) == 1

    def is_straight(self) -> bool:
        if sum(self.values) == 28 and product(self.values) == 1680:
            return True

        if len(set(self.values)) == 5 and (max(self.values) - min(self.values) == 4):
            return True

        return False

    def is_royal_flush(self):
        return self.is_straight_flush() and max(self.values) == Value.ace

    def is_straight_flush(self):
        return (self.is_flush() and self.is_straight())

    def is_four_of_a_kind(self):
        return set(self.counter.values()) == {1, 4}

    def is_full_house(self):
        return set(self.counter.values()) == {2, 3}

    def is_three_of_a_kind(self):
        return set(self.counter.values()) == {1, 3}

    def is_two_pairs(self):
        return set(self.counter.values()) == {1, 2} and len(self.counter) == 3

    def is_pairs(self):
        return len(self.counter) == 4

    _hand_type = None
    _hand_power = None

    def get_hand_type_and_power(self):
        if len(self) != 5:
            raise ValueError("A valid hand can only and only has 5 cards")

        if self.is_royal_flush():
            self._hand_type = HandType.royal_flush
            self._hand_power = 0
        elif self.is_straight_flush():
            self._hand_type = HandType.straight_flush
            if sum(self.values) == 28:
                self._hand_power = Value.five
            else:
                self._hand_power = max(self.values)
        elif self.is_four_of_a_kind():
            self._hand_type = HandType.four_of_a_kind
            values = [
                value
                for value, counts in self.counter.items() if counts == 4
            ]
            self._hand_power = values[0]
        elif self.is_full_house():
            self._hand_type = HandType.full_house
            values = [
                value
                for value, _ in
                sorted(
                    self.counter.items(),
                    key=lambda pair: pair[1],
                    reverse=True
                )
            ]
            self._hand_power = values[-1] * 100 + values[-2]
        elif self.is_flush():
            self._hand_type = HandType.flush
            self._hand_power = 0
        elif self.is_straight():
            self._hand_type = HandType.straight
            if sum(self.values) == 28:
                self._hand_power = Value.five
            else:
                self._hand_power = max(self.values)
        elif self.is_three_of_a_kind():
            self._hand_type = HandType.three_of_a_kind
            values = [
                value
                for value, counts in self.counter.items() if counts == 3
            ]
            self._hand_power = values[0]
        elif self.is_two_pairs():
            self._hand_type = HandType.two_pairs
            values = [
                value
                for value, counts in self.counter.items() if counts == 2
            ]
            values.sort()
            self._hand_power = values[-1] * 100 + values[-2]
        elif self.is_pairs():
            self._hand_type = HandType.pair
            values = [
                value
                for value, counts in self.counter.items() if counts == 2
            ]
            self._hand_power = values[0]
        else:
            self._hand_type = HandType.high_card
            self._hand_power = max(self.values)
        self._hand_power += self._hand_type * hand_type_power

    @property
    def hand_type(self) -> int:
        if self._hand_type is None:
            self.get_hand_type_and_power()
        return self._hand_type

    @property
    def hand_type_for_human(self) -> str:
        return HandType._hand_type_code_mapper[self.hand_type]

    @property
    def hand_power(self) -> int:
        if self._hand_power is None:
            self.get_hand_type_and_power()
        return self._hand_power

    @classmethod
    def i_am_feeling_lucky(cls, n_games, best_n):
        """
        print ``best_n`` hand out of random ``n_games`` hands
        """
        hands = [
            cls.random_hand()
            for _ in range(n_games)
        ]
        hands_sorted = list(
            sorted(
                hands,
                key=lambda hand: hand.hand_power,
                reverse=True,
            )
        )
        for hand in hands_sorted[:best_n]:
            print(hand, hand.hand_type_for_human, hand.hand_power)


if __name__ == "__main__":
    # hand = Hand.random_hand()
    # print(hand)
    # print(hand.hand_type_for_human)
    # print(hand.hand_power)

    # a fun method
    Hand.i_am_feeling_lucky(100, 5)


    def test():
        # four of a kind
        hand = Hand(cards=[
            Card(suit=Suit.diamond, value=Value.ace),
            Card(suit=Suit.spade, value=Value.two),
            Card(suit=Suit.diamond, value=Value.two),
            Card(suit=Suit.heart, value=Value.two),
            Card(suit=Suit.club, value=Value.two),
        ])
        print(hand, hand.hand_type_for_human, hand.hand_power)

        # full house
        hand = Hand(cards=[
            Card(suit=Suit.diamond, value=Value.seven),
            Card(suit=Suit.spade, value=Value.seven),
            Card(suit=Suit.diamond, value=Value.seven),
            Card(suit=Suit.heart, value=Value.jack),
            Card(suit=Suit.club, value=Value.jack),
        ])
        print(hand, hand.hand_type_for_human, hand.hand_power)

        # flush
        hand = Hand(cards=[
            Card(suit=Suit.diamond, value=Value.ace),
            Card(suit=Suit.diamond, value=Value.ace),
            Card(suit=Suit.diamond, value=Value.six),
            Card(suit=Suit.diamond, value=Value.four),
            Card(suit=Suit.diamond, value=Value.king),
        ])
        print(hand, hand.hand_type_for_human, hand.hand_power)

        # straight
        hand = Hand(cards=[
            Card(suit=Suit.spade, value=Value.ace),
            Card(suit=Suit.diamond, value=Value.two),
            Card(suit=Suit.heart, value=Value.three),
            Card(suit=Suit.club, value=Value.four),
            Card(suit=Suit.diamond, value=Value.five),
        ])
        print(hand, hand.hand_type_for_human, hand.hand_power)

        # straight
        hand = Hand(cards=[
            Card(suit=Suit.spade, value=Value.five),
            Card(suit=Suit.diamond, value=Value.four),
            Card(suit=Suit.heart, value=Value.eight),
            Card(suit=Suit.club, value=Value.seven),
            Card(suit=Suit.diamond, value=Value.six),
        ])
        print(hand, hand.hand_type_for_human, hand.hand_power)

        # three of a kind
        hand = Hand(cards=[
            Card(suit=Suit.diamond, value=Value.six),
            Card(suit=Suit.spade, value=Value.ace),
            Card(suit=Suit.diamond, value=Value.six),
            Card(suit=Suit.heart, value=Value.six),
            Card(suit=Suit.club, value=Value.king),
        ])
        print(hand, hand.hand_type_for_human, hand.hand_power)

        # two pairs
        hand = Hand(cards=[
            Card(suit=Suit.diamond, value=Value.ace),
            Card(suit=Suit.spade, value=Value.ace),
            Card(suit=Suit.diamond, value=Value.six),
            Card(suit=Suit.heart, value=Value.six),
            Card(suit=Suit.club, value=Value.king),
        ])
        print(hand, hand.hand_type_for_human, hand.hand_power)

        # pair
        hand = Hand(cards=[
            Card(suit=Suit.diamond, value=Value.jack),
            Card(suit=Suit.spade, value=Value.ace),
            Card(suit=Suit.diamond, value=Value.ten),
            Card(suit=Suit.heart, value=Value.six),
            Card(suit=Suit.club, value=Value.ten),
        ])
        print(hand, hand.hand_type_for_human, hand.hand_power)

        # high card
        hand = Hand(cards=[
            Card(suit=Suit.diamond, value=Value.jack),
            Card(suit=Suit.spade, value=Value.ace),
            Card(suit=Suit.diamond, value=Value.ten),
            Card(suit=Suit.heart, value=Value.six),
            Card(suit=Suit.club, value=Value.king),
        ])
        print(hand, hand.hand_type_for_human, hand.hand_power)

    # test()
