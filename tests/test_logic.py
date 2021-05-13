from copy import deepcopy
from typing import List

import pytest

from player import Player, top
from thegame import Stack, TheGame, Direction


@pytest.fixture()
def setup_game():
    game = TheGame()
    game.mix_cards()
    game.serve_cards()
    return game


def stack_consistency(stacks: List[Stack]):
    for stack in stacks:
        test_stack = deepcopy(stack)
        test_stack.clear()
        for element in stack:
            test_stack.append(element)
    return True


@pytest.mark.parametrize("player_cards ,expected_stacks", [
    ([2, 3, 4, 5, 6, 7, 8], [[1, 2, 3], [1], [100], [100]]),
    ([3, 5, 51, 6, 7, 8, 99], [[1, 3], [1], [100, 99], [100]]),
    ([2, 10, 12, 51, 11, 81, 99], [[1, 12, 2], [1], [100], [100]]),
    ([4, 5, 12, 51, 11, 89, 99], [[1], [1], [100, 89, 99], [100]]),
])
def test_logic_from_start(player_cards, expected_stacks):
    stacks = [Stack(), Stack(), Stack(direction=Direction.down), Stack(direction=Direction.down)]

    player = Player("test_player")
    player.cards = player_cards
    new_stacks = player.play(stacks)
    assert stack_consistency(new_stacks)
    assert new_stacks == expected_stacks


def test_play(setup_game):
    game = setup_game

    game_round = 1
    while game.remaining_cards():
        print("=" * 20, str(game_round), "=" * 20)
        for player in game.players:
            new_stacks = player.play(game.stacks, single_cards_allowed=not game.deck)
            assert new_stacks == None or stack_consistency(new_stacks)
            if new_stacks:
                game.stacks = new_stacks
            else:
                return False

            for i in range(2):
                if len(game.deck) > 0:
                    player.cards.append(game.deck.pop(-1))
        game_round += 1
