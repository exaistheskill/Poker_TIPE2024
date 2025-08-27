# Poker_TIPE2024
This is a school project, the main objective is to create a Poker bot with superhuman abilities in a simplified version of Texas Hold'em

# Simplified version Rules :
- Only 7 levels of cards (H (8), N (9), T (10), J, Q , K , A) (a total of 28 cards counting colors)
- 1 VS 1  
- 2 bet rounds : one pre-flop, and one after the flop
- A 4 token limit of bet per round
- A mandatory token bet every two round
- 20 tokens initialy to bet
# Results
The algorithm does pretty well againt naive strategies (random, always betting 4), but struggles against human who already played poker before.

For the stats (a gamestate is considered a win if the opponent has no token left) :
- 86% win againt random
- 71% againt fullbet
- Around 30% againt humans  (a sample of 30 human, with various backrounds in poker)
