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
This package solves Agnes (Agnes Sorel) solitaire card games. It can be
used to solve games having the rules implemented in the GNOME AisleRiot
package and the rules attributed to Dalton in 1909 and Parlett in 1979
among others [1–3] and to calculate win rates.

EXAMPLE
-------
import random
import quagnes

random.seed(12345)
n_reps = 1000

attributes = ['n_states_checked', 'n_deal', 'n_move_to_foundation',
    'n_move_card_in_tableau','n_no_move_possible','max_score','max_depth',
    'current_depth']

# header for the output file
print('rc,' + ','.join(attributes))

for rep in range(0, n_reps):
    new_game=quagnes.Agnes()
    rc = new_game.play()

    # Write the return code and selected attributes from the game
    out_str = (str(rc) + ',' +
        ','.join([ str(getattr(new_game, attr)) for attr in attributes ]))
    print(out_str, flush=True)

    # rc==1 are games that were won
    if rc==1:
        f = open(f'winners/win{rep}.txt', 'w', encoding='utf-8')
        f.write(new_game.print_history())
        f.close()

BACKGROUND
----------
Agnes is a difficult solitaire card game. This package solves the game
automatically. Users can simulate random games and calculate win rates
under various permutations of rules.

In 1979 Parlett named the two main variants of Agnes as Agnes Sorel (the
variant / set of variants described here) and Agnes Bernauer (a variant/set
of variants that uses a reserve) [3]. This package only considers Agnes
Sorel.

RULES
-----
Because our interest in this problem arose from playing the game in
the GNOME AisleRiot package, we describe the rules of the game first
for this software and describe other rules as lists of modifications.
There is considerable heterogeneity in the rules used (see Keller [4] for
some discussion of the history).

RULES (FaceDown-NoFill [AisleRiot version 3.22.23])
----------------------------------------------------
Deal seven piles in the tableau such that the first pile has one card and
the last pile has seven. The top card in each pile is exposed. Deal one
card to the foundation (base card). Foundations are built up by suit, and
the tableau is built down by color. Wrap from king to ace when necessary.
Piles of cards in sequence in the same suit can be moved in the tableau.
Empty tableau piles cannot be filled except by dealing from the stock.
Dealing from the stock adds one card to the bottom of each tableau pile,
so a game will have three more deals of seven cards and a final deal of
two cards. Cards cannot be played back from the foundation to the tableau.

We refer to these rules as FaceDown-NoFill.

The FaceDown-NoFill rules can be played by constructing an `Agnes` object
with the default parameters.

RULES (Dalton 1909)
------------------
The version described by Dalton is as described for the FaceDown-NoFill
version with the following modifications [1,2]:
1. A single exposed card can be moved into an empty tableau column,
   although this isn't required.
2. Cards in sequence can only be moved when they are the same suit
   (instead of the same color).
3. All cards are dealt face-up in the tableau.

The Dalton rules can be played by constructing an `Agnes` object with
`face_up=True`, `move_to_empty_pile='any 1'` and `move_same_suit=True`.
The second modification

RULES (Parlett 1979)
--------------------
The version described by Parlett is as described for the FaceDown-NoFill
version with the following modifications [1,3]:
1. Cards in sequence can only be moved when they are the same suit
   (instead of the same color).
2. Suit sequences must be moved as a whole sequence, eg, if the 6 and 7 of
   Clubs are under the 8 of Spades, the 6 of Clubs cannot be moved off to
   the 7 of Spades, but the 6 and 7 of Clubs could together be moved to
   under the 8 of Clubs.
3. All cards are dealt face-up in the tableau.

The Parlett rules can be played by constructing an `Agnes` object with
`face_up=True`, `move_same_suit=True`, `split_same_suit_runs=False`.

REFERENCES
----------
[1] Agnes (card game). Wikipedia.
   https://en.wikipedia.org/wiki/Agnes_(card_game). Retrieved
   March 15, 2024.

[2] Dalton W (1909). "My favourite Patiences" in The Strand Magazine,
    Vol 38.

[3] Parlett D (1979). The Penguin Book of Patience. London: Penguin.

[4] Keller M (2021). Whitehead and Agnes -- packing in color.
    https://www.solitairelaboratory.com/whitehead.html. Retrieved
    March 17, 2024.
"""

#------------------------------------------------------------------------------
# File:    __init__.py
# Date:    2024-03-14
# Author:  Ray Griner
# Changes:
#------------------------------------------------------------------------------
__author__ = 'Ray Griner'
__version__ = '0.8.0'
__all__ = ['Agnes']

from .agnes import Agnes
