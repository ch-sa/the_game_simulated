import enum
import random
from typing import List

import numpy as np

from player import Player, calculate_points

Direction = enum.Enum("Direction", "up down")


class Stack(list):

    def __init__(self, *args, direction: Direction = Direction.up):
        super().__init__(*args)
        self.direction = direction
        if self.direction == Direction.up:
            self.append(1)
        else:
            self.append(100)

    def append(self, number: int) -> None:
        if self:
            if self.direction == Direction.up and number < self[-1] and number != self[-1] - 10:
                raise ValueError(f"Number must be higher than {self[-1]} or 10 lower")
            elif self.direction == Direction.down and number > self[-1] and number != self[-1] + 10:
                raise ValueError(f"Number must be lower than {self[-1]} or 10 higher")
        super().append(number)

    def get_reverse_number(self):
        return self[-1] - 10 if self.direction == Direction.up else self[-1] + 10


class TheGame(object):
    CARDS_PER_PLAYER = {1: 8, 2: 7, 3: 6, 4: 6, 5: 6}

    def __init__(self):
        self.players: List[Player] = [Player("player_01"), Player("player_02")]

        self.stacks: List[Stack] = [Stack(direction=Direction.up), Stack(direction=Direction.up),
                                    Stack(direction=Direction.down), Stack(direction=Direction.down)]
        self.deck: List[int] = [i for i in range(2, 100, 1)]
        self.reserved_stacks = {}  # player: stacks

    def mix_cards(self):
        random.shuffle(self.deck)

    def serve_cards(self):
        cards_per_player = TheGame.CARDS_PER_PLAYER[len(self.players)]
        if len(self.players) == 2:
            cards_per_player = 7

        for i in range(cards_per_player):
            for player in self.players:
                player.cards.append(self.deck.pop(-1))
        print(f"Served {cards_per_player} to each of the {len(self.players)} players.")

    def remaining_cards(self):
        return len(self.deck) + sum([len(player.cards) for player in self.players])

    def play_rounds(self):
        game_round = 1
        while self.remaining_cards():
            print("=" * 20, str(game_round), "=" * 20)
            for player in self.players:
                self.reserved_stacks = {p.name: p.announce_stack_reservation(self.stacks) for p in self.players}
                print(f"RESERVED: {self.reserved_stacks}")
                new_stacks = player.play(self.stacks, single_cards_allowed=not self.deck, reserved_stacks=self.reserved_stacks)
                if new_stacks:
                    self.stacks = new_stacks
                else:
                    return False

                for i in range(2):
                    if len(self.deck) > 0:
                        player.cards.append(self.deck.pop(-1))
            # input(f"... {self.remaining_cards()} cards remaining ...\n")
            game_round += 1
        return True

    def play(self):
        # self.players[0].cards = [12, 21, 22, 28, 36, 59, 65]
        game_result = self.play_rounds()

        if game_result:
            print(f"\033[92mPlayers won the game with a final score of {400 - calculate_points(self.stacks)}!\033[0;0m")
            return True, 400 - calculate_points(self.stacks)
        else:
            print(f"\033[1;31mGame is over with {self.remaining_cards()} cards remaining!\033[0;0m")
            return False, self.remaining_cards()


if __name__ == '__main__':
    wins = 0
    losses = 0
    win_scores = []
    loss_cards = []

    n = 10001
    for g in range(n):
        game = TheGame()
        game.mix_cards()
        game.serve_cards()
        result, score = game.play()
        if result:
            wins += 1
            win_scores.append(score)
        else:
            losses += 1
            loss_cards.append(score)

        if g % 1000 == 0:
            print(f"Wins: {wins} ({wins / n * 100} %)")
            print(f"Losses: {losses} ({losses / n * 100} %)")

            print(f"Win scores (no. of open positions): {win_scores}")
            print(f"Losses scores (remaining cards): {loss_cards}")

            np.array(win_scores).tofile("wins.txt", sep=",")
            np.array(loss_cards).tofile("losses.txt", sep=",")


        print(f"{wins} wins vs. {losses} losses ...")

    np.array(win_scores).tofile("wins.txt", sep=",")
    np.array(loss_cards).tofile("losses.txt", sep=",")


