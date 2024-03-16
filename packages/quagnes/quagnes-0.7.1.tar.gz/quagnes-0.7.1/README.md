# Summary
This package solves the Agnes solitaire card game. It can be used
to solve the version with the rules implemented in the GNOME AisleRiot
package on Debian and the rules attributed to Dalton in 1909 [1,2].

# Background
Agnes is a difficult solitaire card game. This package solves the game
automatically. Users can simulate random games and estimate the percentage
of starting positions that are solvable.

# Rules (AisleRiot variant)
Deal seven piles in the tableau such that the first pile has one card and
the last pile has seven. The top card in each pile is exposed. Deal one
card to the foundation (base card). Foundations are built up by suit, and
the tableau is built down by color. Wrap from king to ace when necessary.
Piles of cards in sequence in the same color can be moved in the tableau.
Empty tableau piles cannot be filled except by dealing from the stock.
Dealing from the stock adds one card to the bottom of each tableau pile, so
a game will have three deals of seven cards and a final deal of two cards.
Cards cannot be played back from the foundation to the tableau.

# Rules (Dalton 1909)
The version described by Dalton modifies the above rules as follows [1,2]:
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

    if rc==1:
        f = open(f'winners/win{rep}.txt', 'w', encoding='utf-8')
        f.write(new_game.print_history())
        f.close()
```

# Optimizations
Some optimizations were used to improve the run-time:
1. For the AisleRiot variant, if the highest rank card (e.g., a king if
the base card is an ace) is placed in a tableau pile below a lower card
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
`move_to_empty_file=False` or when `maximize_score=True`.

2. A card is immediately placed on a foundation if its rank is no more than
the rank of the top foundation card of the same color suit plus two. For
example, if the base card is an ace, and we have already played up to the
six of spades in the foundation, we immediately play the ace of clubs up to
the eight of clubs (if possible) to the foundation. We would not
immediately play the nine of clubs to the foundation as it might be needed
in the tableau to move the eight of spades.

3. We track states that we have already determined to be not winnable in
a set. For example, suppose the initial state has two possible moves: M1)
move a card from pile 1 to 2; M2) move a card from pile 4 to 5. Once we
determine the sequence M1 → M2 is not winnable, there is no need to check
the sequence M2 → M1, as they both result in the same state. 

4. To prevent infinite loops, we check whether the same state has been
repeated since the last deal or move to foundation. If the state is a
repeat, we consider no valid moves to be available from that state. This is
to prevent, for example, moving the eight of spaces between the nine of
clubs and nine of spades in an infinite loop. A useful heuristic is likely
to never move to the same-color suit when the same suit is available.
However, pathological examples can be constructed where this is a losing
strategy.

# Statistical Analysis
One thousand simulated games were played using Python version 3.11.2 on a
laptop running 32-bit Debian GNU/Linux 9. We calculated the proportion of
games winnable and the 95% confidence interval using the Clopper-Pearson
method for the default parameters, which correpond to the rules used in
AisleRiot.

# Results
Twelve of the 1000 (1.2%: 95% CI [0.6%, 2.0%]) simulated games were winnable.
The simulations took 80 minutes to run on a laptop running Debian. The number
of states examined for each simulation was heavily skewed, with mean (SD)
of 93,600 (1,790,000) and median (IQR) of 1 (1, 48.5) states. The two longest
simulations accounted for 73.4% of the total states examined. The maximum
number of states examined was over 54 million.

# Discussion
We found 1.2% games were winnable. This is over two hundred times higher than
the 45 wins in one million reported by Wolter [3]. Wolter also reports a
'very fast' run time (although he does not give exact details), while we found
very large search trees that must be explored.

Much of the work for this project was originally done in 2019 assuming all
cards were dealt face-up using Python 3.5. This 2024 update used Python 3.11.2.
In 2019 we ported the Python code to C++ for performance testing and found a
five-fold improvement. When porting the code to Python 3.11, we found a two-fold
decrease in run-time when switching the data structures used from tuples to
dataclasses for the structures representing cards and moves.

The program ran out of memory when attempting to play under Dalton's rules.
Large amounts of memory may be requrired because sets are used to store
states that are known to be unsuccessful. A parameter `track_threshold` has
been added that allows a user to approximately control the size of this set.
Some memory is still needed to detect loops.

# References
[1] Agnes (card game). Wikipedia. 
   https://en.wikipedia.org/wiki/Agnes_(card_game). Retrieved March 15, 2024.

[2] Dalton W (1909). "My favourite Patiences" in The Strand Magazine, Vol 38.

[3] Wolter J (2013). Experimental analysis of Agnes Sorel solitaire.
    https://politaire.com/article/agnessorel.html. Retrieved March 15, 2024.

