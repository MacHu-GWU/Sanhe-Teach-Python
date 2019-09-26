from player import Deck, Board, Player

def play_a_game():
    deck = Deck.new_shuffled_deck()

    players = [
        Player(name="Alice"),
        Player(name="Bob"),
        Player(name="Cathy"),
    ]  # type: List[Player]

    board = Board()

    deck.deal_many_to(board, 5)

    print(board)

    for player in players:
        player.fetch_n_cards(deck, 2)
        print("- ", player.name, player.player_hand)

    hand_power_to_players_mapper = dict()
    """
    {
        best_hand_power: [
            {
                "player": player,
                "best_hand": best_hand,
            }
        ]
    }
    """
    for player in players:
        best_hand = player.find_best_hand(board)
        data = {
            "player": player,
            "best_hand": best_hand,
        }
        try:
            hand_power_to_players_mapper[best_hand.hand_power].append(data)
        except:
            hand_power_to_players_mapper[best_hand.hand_power] = [data,]

    hand_power_and_players_list_sorted = list(sorted(
        hand_power_to_players_mapper.items(),
        key=lambda pair: pair[0],
        reverse=True
    ))

    for data in hand_power_and_players_list_sorted[0][1]:
        player, best_hand = data["player"], data["best_hand"]
        print("Winner is {}, with {} - {}".format(
            player.name,
            best_hand,
            best_hand.hand_type_for_human,
        ))

if __name__ == "__main__":
    play_a_game()
