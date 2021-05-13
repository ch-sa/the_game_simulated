# 'The Game' Simulated
→ *This repository is currently still in the creation phase!*

This is a simple simulation of the popular card game ['The Game'](https://de.wikipedia.org/wiki/The_Game_(Kartenspiel)), where players iteratively have to put all cards from 1 to 99 onto two increasing and two decreasing stacks.
The only possiblity to decrease/ increase the stack is to place a card exactly ten lower or ten higher to the current top card.

![Cover of the Game](http://middys.nsv.de/wp-content/uploads/2019/11/4034_The_Game_Schachtel_800.jpg)

### Game Logic
The game logic is implemented in `thegame.py`.

### Player Strategies
The player strategies are implemented in `player.py`.

### Analytics & Statistics
The current analysis of more than 5000 simulated game rounds can be found in a first [jupyter notebook](analytics/analyse_results.ipynb).