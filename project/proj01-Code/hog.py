""" Project 1: The Game of Hog. """

from dice import six_sided, make_test_dice
from math import floor, sqrt

GOAL_SCORE = 50  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

# ANSWER QUESTION 00

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # BEGIN PROBLEM 1
    i = 1
    total = 0
    one_flag = False

    while i <= num_rolls:
        i += 1
        temp = dice()
        if temp == 1:
            one_flag = True
        total += temp

    if one_flag:
        return 1
    else:
        return total
    # END PROBLEM 1


def picky_piggy(opponent_score):
    """Return the points scored from rolling 0 dice accodring to Picky Piggy.

    opponent_score:  The total score of the other player.
    """
    # BEGIN PROBLEM 2
    return abs((opponent_score % 10) - ((opponent_score % 100) // 10)) * 2 + 1
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Return the points scored for the turn rolling NUM_ROLLS dices when the
    opponent has OPPONENT_SCORE points.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the other player.
    dice:            A function that simulates a single dice roll outcome.
    """
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return picky_piggy(opponent_score)
    else:
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def swine_swap(score):
    """Return whether the players' scores will be swapped due to Swine Swap.

    score:           The total score of the current player.

    Hint: for this problem, you will find the math function sqrt useful.
    >>> sqrt(9)
    3.0
    >>> floor(sqrt(9))
    3
    >>> floor(sqrt(8))
    2
    """
    # BEGIN PROBLEM 4
    if sqrt(score) != floor(sqrt(score)):
        return False
    else:
        return True
    # END PROBLEM 4


def play(strategy0, strategy1,
         score0=0, score1=0, dice=six_sided, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    E.g., play(always_roll_5, always_roll_5) simulates a game in which both 
    players always choose to roll 5.

    A strategy function, such as always_roll_5, takes the current player's
    score and the opponent's score, and returns the number of dice that the
    corresponding player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    while (score0 < goal) and (score1 < goal):
        if who:
            score1 += take_turn(strategy1(score1, score0), score0, dice)
            if swine_swap(score1):
                score1, score0 = score0, score1
        else:
            score0 += take_turn(strategy0(score0, score1), score1, dice)
            if swine_swap(score0):
                score1, score0 = score0, score1
        who = 1 - who
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the oppononent's score.
    """
    return 5


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10
    # BEGIN PROBLEM 6
    return lambda player, opponent: n
    # END PROBLEM 6


def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # Roll one more to catch up
    else:
        return 5


def is_always_roll(strategy, goal=GOAL_SCORE):
    """Return whether strategy always chooses the same number of dice to roll.

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    const = strategy(0, 0)
    for player in range(0, goal):
        for opponent in range(0, goal):
            if strategy(player, opponent) != const:
                return False
            const = strategy(player, opponent)
    return True
    # END PROBLEM 7


def make_averaged(original_function, trials_count=10000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TOTAL_SAMPLES times.

    To implement this function, you will have to use *args syntax.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    3.0
    """
    # BEGIN PROBLEM 8
    def inner(*args):
        i = 1
        total = 0
        while i <= trials_count:
            i += 1
            total += original_function(*args)
        return total / trials_count
    return inner
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, total_samples=100):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of TOTAL_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    choice = 1
    now = 1
    score_max = 0

    while now <= 10:
        score_now = (make_averaged(roll_dice, total_samples))(now, dice)
        if score_now > score_max:
            choice = now
            score_max = score_now
        now += 1
    
    return choice
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:',
          average_win_rate(always_roll(6)))  # near 0.5
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('picky_strategy win rate:', average_win_rate(picky_strategy))
    print('swine_strategy win rate:', average_win_rate(swine_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


def picky_strategy(score, opponent_score, threshold=8, num_rolls=6):
    """This strategy returns 0 dice if that gives at least THRESHOLD points,
    and returns NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if picky_piggy(opponent_score) >= threshold:
        return 0
    return num_rolls
    # END PROBLEM 10


def swine_strategy(score, opponent_score, threshold=8, num_rolls=6):
    """This strategy returns 0 dice when this would gives the player at least
    THRESHOLD points in this turn. Otherwise, it returns NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    picky_score = picky_piggy(opponent_score)
    apply_score = score + picky_score
    if swine_swap(apply_score):
        if opponent_score - score >= threshold:
            return 0
        else:
            return num_rolls
    else:
        return 0 if picky_score >= threshold else num_rolls
    # END PROBLEM 11

def final_strategy(score, opponent_score):
    expectation = 406031 / 46656
    change_num = [1, 4, 9, 16, 25, 36, 49, 64]
    now = score + picky_piggy(opponent_score)
    if (opponent_score - score > expectation) and (score + 1) in change_num:
        return 10
    if (now) > expectation:
        if(now) in change_num:
            if (picky_piggy(now) + opponent_score) in change_num and (now - opponent_score - picky_piggy(now)) > 0:
                return 0
            return 6
        if (picky_piggy(now) + opponent_score) in change_num and (now - opponent_score - picky_piggy(now)) > 0:
            return 6
        return 0
    if (score in [0, 3]) and (opponent_score) > 24:
        return 1
    return 6


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


if __name__ == '__main__':
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
