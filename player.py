from __future__ import annotations

from copy import deepcopy
from typing import List, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from thegame import Stack


def calculate_points(stacks: List[Stack]):
    points = 0
    for stack in stacks:
        if stack.direction.name == "up":
            points += stack[-1] - 1
        else:
            points += 100 - stack[-1]
    return points


def top(stacks: List[Stack]):
    return [stack[-1] for stack in stacks]


class Player(object):

    def __init__(self, name: str):
        self.name = name
        self.cards = []

    def check_rewind(self, stacks: List[Stack]):
        for ind, stack in enumerate(stacks):
            if stack[-1] - 10 in self.cards:
                return ind
        return None

    def try_to_play_card(self, stack, card):
        try:
            if card:
                stack.append(card)
        except ValueError:
            return False
        return True

    def get_best_draw(self, stacks: List[Stack], single_cards_allowed: bool, reserved_stacks=None):
        if reserved_stacks is None:
            reserved_stacks = set()

        # initialize brute force
        new_stacks, new_score, played_cards = ([], 400, [])

        for card1 in self.cards:

            for i in range(len(stacks)):
                tmp_stacks = deepcopy(stacks)

                # skip stack if reserved or card not playable
                if i in reserved_stacks or not self.try_to_play_card(tmp_stacks[i], card1):
                    continue
                
                # try to place another card on new stack composition
                for card2 in self.cards:
                    if len(self.cards) == 1 or single_cards_allowed:
                        card2 = None
                    elif card2 == card1:
                        continue

                    for ii in range(len(tmp_stacks)):
                        tmp_tmp_stacks = deepcopy(tmp_stacks)

                        # skip stack if reserved or card not playable
                        if ii in reserved_stacks or not self.try_to_play_card(tmp_tmp_stacks[ii], card2):
                            continue

                        if calculate_points(tmp_tmp_stacks) < new_score:
                            new_score = calculate_points(tmp_tmp_stacks)
                            new_stacks = deepcopy(tmp_tmp_stacks)
                            played_cards = [card1, card2]
                            # print(f"Cards {card1} & {card2} → Current Points {new_score}: {top(tmp_tmp_stacks)}
                            # (Old: {top(stacks)})")

        return new_stacks, new_score, played_cards

    def play(self, stacks: List[Stack], single_cards_allowed=False, reserved_stacks: Dict = None) -> List[Stack]:
        new_stacks, played_cards, new_score = (None, [], None)
        stack_score = calculate_points(stacks)
        print(f"Stacks are {top(stacks)} (Score {stack_score}).")
        print(f"Player {self.name} plays with hand {sorted(self.cards)} ...")

        if reserved_stacks:  # collect stack that OTHER players blocked
            reserved_stacks = {e for l in reserved_stacks.values() for e in l} - set(reserved_stacks[self.name])
            print(f"RESULTING RESERVED: {reserved_stacks}")
            new_stacks, new_score, played_cards = self.get_best_draw(stacks, single_cards_allowed, reserved_stacks)
        if not new_stacks:
            new_stacks, new_score, played_cards = self.get_best_draw(stacks, single_cards_allowed)

        if new_stacks:  # player found a solution
            for played_card in played_cards:
                if played_card:
                    self.cards.remove(played_card)
            print(f"Player {self.name} plays cards {played_cards} → {top(new_stacks)} (score: {new_score})")
        else:
            print(f"\033[1;31m Player {self.name} could not find a solution! Stacks remain → {top(stacks)}\033[0;0m")
        return new_stacks

    def announce_stack_reservation(self, stacks: List[Stack]):
        stacks_to_reserve = []
        for ind, stack in enumerate(stacks):
            if stack.get_reverse_number() in self.cards:
                stacks_to_reserve.append(ind)
        return stacks_to_reserve
