#   quagnes: a package for solving Agnes solitaire
#   Copyright (C) 2019, 2024 Ray Griner (rgriner_fwd@outlook.com)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#------------------------------------------------------------------------------

"""A package for solving Agnes solitaire.

SUMMARY
-------
This package solves the Agnes solitaire card game. It can be used
to solve the version with the rules implemented in the GNOME AisleRiot
package on Debian and the rules attributed to Dalton in 1909 [1,2].

BACKGROUND
----------
Agnes is a difficult solitaire card game. This package solves the game
automatically. Users can simulate random games and estimate the percentage
of starting positions that are solvable.


RULES (AisleRiot variant)
-------------------------
Deal seven piles in the tableau such that the first pile has one card and
the last pile has seven. The top card in each pile is exposed. Deal one
card to the foundation (base card). Foundations are built up by suit, and
the tableau is built down by color. Wrap from king to ace when necessary.
Piles of cards in sequence in the same color can be moved in the tableau.
Empty tableau piles cannot be filled except by dealing from the stock.
Dealing from the stock adds one card to the bottom of each tableau pile, so
a game will have three deals of seven cards and a final deal of two cards.
Cards cannot be played back from the foundation to the tableau.


RULES (Dalton 1909)
------------------
According to Wikipedia, the version described by Dalton modifies the above
rules as follows [1,2]:
1. Cards in sequence can only be moved when they are the same suit
  (instead of the same color).
2. A single exposed card can be moved into an empty tableau column,
   although this isn't required.

The Dalton rules can be played by constructing an Agnes object with
`move_to_empty_pile=True` and `move_same_suit=True`. However, note that
the first option enlarges the space of eligible moves substantially and the
program ran out of memory during testing on one of the first simulations.
The parameter `track_threshold` was therefore added to indirectly manage the
memory used.

EXAMPLE
-------
import random
import quagnes

random.seed(12345)
n_reps = 1000

attributes = ['n_states_checked', 'n_deal', 'n_move_to_foundation',
      'n_move_card_in_tableau','n_no_move_possible','max_score',
      'max_depth','current_depth']

# header for the output file
print('rc,' + ','.join(attributes))

for rep in range(0, n_reps):
    new_game=quagnes.Agnes()
    rc = new_game.play()

    # Write the return code and selected attributes from the game
    out_str = (str(rc) + ',' +
        ','.join([ str(getattr(new_game, attr)) for attr in attributes ]))
    print(out_str, flush=True)

    if rc==1:
        f = open(f'winners/win{rep}.txt', 'w',
                 encoding='utf-8')
        f.write(new_game.print_history())
        f.close()


REFERENCES
----------
[1] Agnes (card game). Wikipedia.
    https://en.wikipedia.org/wiki/Agnes_(card_game). Retrieved
    March 15, 2024.

[2] Dalton W (1909). "My favourite Patiences" in The Strand Magazine, 
    Vol 38.

[3] Wolter J (2013). Experimental analysis of Agnes Sorel solitaire.
    https://politaire.com/article/agnessorel.html. Retrieved
    March 15, 2024.
"""

#------------------------------------------------------------------------------
# File:    __init__.py
# Date:    2024-03-14
# Author:  Ray Griner
# Changes:
#------------------------------------------------------------------------------
__author__ = 'Ray Griner'
__version__ = '0.7.0'
__all__ = ['Agnes']

from .agnes import Agnes
