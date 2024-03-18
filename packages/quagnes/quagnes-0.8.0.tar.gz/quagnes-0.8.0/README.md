# Summary
This package solves Agnes (Agnes Sorel) solitaire card games. It can
be used to solve games having the rules implemented in the GNOME AisleRiot
package and the rules attributed to Dalton in 1909 and Parlett in 1979
among others [1–3] and to calculate win rates.

# Example
```
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
```

# Background
Agnes is a difficult solitaire card game. This package solves the game
automatically.

Users can simulate random games and calculate win rates
under various permutations of rules, including moving sequences/runs by
same-suit or same-color, allowing or not same-suit runs to be split
in the middle of the run for a move, and to what extent empty columns
can be filled in between deals (never, a single card of any rank, 
a single card of the highest rank, a run starting with a single card of any
rank, or a run starting with a card of the highest rank), and whether 
all tableau cards are dealt face-up, or only the last card in each pile.
The package provides additional options for debugging and tuning of
the search algorithm to be faster versus more memory-efficient.

In 1979 Parlett named the two main variants of Agnes as
Agnes Sorel (the variant / set of variants described here) and Agnes Bernauer
(a variant/set of variants that uses a reserve) [3]. This package only
considers Agnes Sorel.

Some analyses of win rates for Agnes Sorel has previously been conducted.
Wolter published an experimental analysis of the win rates of this and
other solitaires, reporting 14 winnable games in a million deals under the
FaceUp-NoFill rules (defined below) [4]. Masten modified Wolter's solver
and reported 900/100,000 (0.9%) games were winnable when empty columns could not
be filled by any card, although some of the other rules used are unclear [5].
In this analysis, we conduct our own simulations to estimate win rates to
assess whether Wolter or Master are correct and add win rates for other rule
variants.

# Rules
Because our interest in this problem arose from playing the game in
the GNOME AisleRiot package, we describe the rules of the game first
for this software and describe other rules as lists of modifications.
There is considerable heterogeneity in the rules used (see Keller [6] for
some discussion of the history).

## FaceDown-NoFill (AisleRiot [version 3.22.23])
Deal seven piles in the tableau such that the first pile has one card and
the last pile has seven. The top card in each pile is exposed. Deal one
card to the foundation (base card). Foundations are built up by suit, and
the tableau is built down by color. Wrap from king to ace when necessary.
Piles of cards in sequence in the same suit can be moved in the tableau.
Empty tableau piles cannot be filled except by dealing from the stock.
Dealing from the stock adds one card to the bottom of each tableau pile,
so a game will have three more deals of seven cards and a final deal of
two cards. Cards cannot be played back from the foundation to the tableau.

We refer to these rules as FaceDown-NoFill in the discussion below.

The FaceDown-NoFill rules can be played by constructing an `Agnes` object
with the default parameters.

## Dalton (1909)
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

## Parlett (1979)
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

## Politaire (FaceUp-Fill, FaceUp-NoFill, FaceUp-NoFill-MSS)
A website called politaire.com offers solitaire play [7]. It is relevant
here as it hosts an article by Wolter [4] that analyzes the winnability of
the game as played on the site. The current rules on the website (which we
denote as FaceUp-Fill) are as described for the FaceDown-NoFill version,
with the following modifications:

1. All cards are dealt face-up in the tableau.
2. A single exposed card can be moved into an empty tableau column,
   although this isn't required.

Wolter also analyzed the game omitting the second modification (which we
denote as FaceUp-NoFill).

These rules can be played by constructing an `Agnes` object with the
following parameters:
- FaceUp-Fill: `face_up=True`, `move_to_empty_pile='any 1'`
- FaceUp-NoFill: `face_up=True`

A final variant we consider adds to the FaceUp-NoFill rules the requirement
that moves can only be done for runs of the same suit. We call this
variant FaceUp-NoFill-MSS and is implemented by adding the parameter
`move_same_suite=True` to the parameters already listed for FaceUp-Fill.

# Methodology
The following optimizations were used to improve the run-time over a naive
depth-first search:

1. When `move_to_empty_pile='none'`, if the highest rank card (e.g., a king
if the base card is an ace) is placed in a tableau pile below a lower card
of the same suit, the lower card can never be moved from the pile. This is
detected as soon as the king is placed. So some games can be determined
to be not winnable by examining only the starting state. Note while this
optimization improves run time, it is not possible to determine the
maximum possible score if a branch is terminated for this reason. This
concept can be extended by noting that if the king of clubs blocks the
queen of hearts and the king of hearts blocks the queen of clubs, the game
is also unwinnable. In general, we define after each deal a four vertex
graph (one vertex for each suit), where an edge denotes which suits are
blocked by the suit corresponding to the vertex. The state is not winnable
if a cycle exists in the graph. This optimization is disabled when
`move_to_empty_pile != 'none'` or when `maximize_score=True`.

2. A card is immediately placed on a foundation if its rank is no more than
the rank of the top foundation card of the same color suit plus two. For
example, if the base card is an ace, and we have already played up to the
six of spades in the foundation, we immediately play the ace of clubs up
to the eight of clubs (if possible) to the foundation. We would not
immediately play the nine of clubs to the foundation as it might be
needed in the tableau to move the eight of spades.

3. We track states that we have already determined to be not winnable in
a set. For example, suppose the initial state has two possible moves: M1)
move a card from pile 1 to 2; M2) move a card from pile 4 to 5. Once we
determine the sequence M1 → M2 is not winnable, there is no need to check
the sequence M2 → M1, as they both result in the same state. This
optimization can be tuned using the `track_threshold` parameter.

4. To prevent infinite loops, we check whether the same state
(arrangement of cards in the tableau) has been repeated since the last
deal or move to foundation. If the state is a repeat, we consider no valid
moves to be available at the repeated state. This is to prevent, for
example, moving the eight of spaces between the nine of clubs and nine
of spades in an infinite loop. A useful heuristic is likely to never move
to the same-color suit when the same suit is available. However,
pathological examples can be constructed where this is a losing strategy.
This optimization is disabled if `split_same_suit_runs=False`, as such
loops cannot occur under this parameter setting.

5. The simulation is implemented using two or three equal-length stacks
where the nth item describes an aspect of the state of the game at the
nth move.  These three stacks store: (1) the moves performed, (2) the valid
moves not yet attempted, and (3) a set containing the arrangement of all
tableau layouts that have occured since the last deal or move to foundation
(to prevent infinite loops of moving cards in the tableau). This third
stack is not used when `split_same_suit_runs=False`.

A single state object (`_AgnesState`) in the `Agnes` object initially
stores information about the starting state, such as the cards in the
foundation, the arrangement of cards in the tableau, and the number of
cards left in the stock. When a move is simulated or undone, the
`AgnesState` object is updated based on the move information. This
implementation is significantly faster (about 5–7 times faster) than using
a stack of `_AgnesState` objects.

# Statistical Analysis
One to ten thousand games per rule set were simulated using Python version
3.11.2 on a laptop running 32-bit Debian GNU/Linux 12. We calculated the win
rates and the 95% confidence interval (95% CI) using the Clopper-Pearson
method for the following rules: FaceDown-NoFill (n=1000),
FaceUp-NoFill (n=1000), Partlett (n=10,000), and FaceUp-NoFill-MSS (n=10,000).

For each set of rules, descriptive statistics (mean, standard deviation [SD],
median, first quartile [Q1], third quartile [Q3], and maximum) were
calculated for the number of states examined per simulation (ie, the
`Agnes.n_states_checked` attribute). The proportion of total states
checked for the two simulations with the most states checked was also
calculated.

For the FaceUp-NoFill rules, we calculated separate p-values testing the
equality of our estimate with those published by Wolter [4] and Masten [5].

# Results
## FaceDown-NoFill Rules
Twelve of the 1000 (1.2%: 95% CI [0.6%, 2.0%]) simulated games were
winnable.  The simulations took 54-80 minutes to run. (The longer time was
found testing v0.7.0 and the shorter time was found testing v0.8.0). The
number of states examined for each simulation was heavily skewed, with
approximate mean (SD) of 93,600 (1,790,000) and median (Q1, Q3) of
1 (1, 48.5) states. The two simulations with the most states examined
accounted for 73.4% of the total states examined. The maximum number of
states examined was over 54 million for a single simulation.

## FaceUp-NoFill rules
Twelve of the 1000 (1.2%: 95% CI [0.6%, 2.0%]) simulated games were
winnable. The simulations took 51 minutes to run. The number of states
examined for each simulation was heavily skewed, with approximate mean (SD)
of 90,800 (1,770,000) and median (Q1, Q3) of 1 (1, 52) states. The two
simulations with the most states examined accounted for 73.4% of the total
states examined. The maximum number of states examined was over 54 million
for a single simulation.

Our winnability rate was significantly different from those reported by
Wolter (p<.0001) and not by Masten (p=0.41).

## FaceUp-NoFill-MSS
42/10,000 (0.4%: 95% CI [0.3%, 0.5%]) simulated games were winnable. The
simulations took 75 minutes to run. The number of states examined for each
simulation was skewed, with approximate mean (SD) of 13,100 (234,000) and
median (Q1, Q3) of 1 (1, 36) states. The two longest
simulations accounted for 19.5% of the total states examined. The maximum
number of states examined was over 14.5 million for a single simulation.

## Parlett rules
40/10,000 (0.4%: 95% CI [0.3%, 0.5%]) simulated games were winnable. The
simulations took 24 minutes to run. The number of states
examined for each simulation was skewed, with approximate mean (SD) of
5872 (94,100) and median (Q1, Q3) of 1 (1, 34) states. The two longest
simulations accounted for 15.9% of the total states examined. The maximum
number of states examined was over 6.1 million for a single simulation.

# Discussion
We found 1.2% (95% CI [0.6%, 2.0%]) of games were winnable under the
FaceDown-NoFill and FaceUp-NoFill rules. Our estimate was significantly
different from the estimate of Wolter, but not of Masten.

A limitation of using Masten's results is he states win rates, but isn't
explicit about which rules are used. He refers readers to Keller's
discussion for more information, and this discussion suggests that Masten
calculated rates for FaceUp-NoFill-MSS [6,7]. Keller then also notes that all
computer implementations he had seen allow moves by colored runs and not
same-suit runs, which would corresponds to the FaceUp-NoFill rules and not
FaceUp-NoFill-MSS in our terminology [6,7].

Our FaceUp-NoFill-MSS estimate of 0.4% was significantly lower than the
0.9% reported by Masten. We therefore conjecture that Masten's win rates
are calculated based on the FaceUp-NoFill rules, as he notes that he
modified Wolter's solver, and Wolter's original solver was designed for
use with Politaire games, which use FaceUp-NoFill rules (although Wolter's
originally estimated win rates seem erroneous).

Adding 95% CIs to Masten's reported win rates gives win rates (95% CI) of
0.9% (0.8%, 1.0%) for a variant not allowing empty columns to be filled,
63.6% (63.3%, 63.9%) where the empty column can be filled by any card
(or perhaps sequence, again it is unclear), and 14.5% (14.3%, 14.7%)
for the rules where empty columns can be filled only by the highest rank
card (or perhaps sequence).

Much of the work for this project was originally completed in 2019
assuming all cards were dealt face-up using Python 3.5. This 2024 update
used Python 3.11.2. In 2019 we ported the Python code to C++ for
performance testing and found a five-fold improvement in speed. When
porting the code to Python 3.11, we found a two-fold decrease in run-time
when switching the data structures used from tuples to dataclasses for the
structures representing cards and moves.

The program ran out of memory when first attempting to play under Dalton's
rules (ie, with behavior like `track_threshold=0`). Large amounts of
memory may be required because sets are used to store states that are
known to be unsuccessful (Optimization #3).  A parameter `track_threshold`
was therefore added that allows a user to approximately control the size
of this set. Future analyses may be conducted using this parameter to
try to estimate win rates under Dalton's rules and other rule sets that
allow empty columns to be filled.

# References
[1] Agnes (card game). Wikipedia.
   https://en.wikipedia.org/wiki/Agnes_(card_game). Retrieved
   March 15, 2024.

[2] Dalton W (1909). "My favourite Patiences" in The Strand Magazine,
    Vol 38.

[3] Parlett D (1979). The Penguin Book of Patience. London: Penguin.

[4] Wolter J (2014). Rules for Agnes Sorel solitaire.
    https://politaire.com/help/agnessorel. Retrieved March 17, 2024.

[5] Masten M (2021). Agnes Sorel.
    https://solitairewinrates.com/AgnesSorel.html. Retrieved
    March 17, 2024.

[6] Keller M (2021). Whitehead and Agnes -- packing in color.
    https://www.solitairelaboratory.com/whitehead.html. Retrieved
    March 17, 2024.

[7] Wolter J (2013). Experimental analysis of Agnes Sorel solitaire.
    https://politaire.com/article/agnessorel.html. Retrieved
    March 15, 2024.

# Disclosures
We are not affiliated with any of the books, websites, or applications
discussed in this documentation, except of course for this Python package
which we wrote.
