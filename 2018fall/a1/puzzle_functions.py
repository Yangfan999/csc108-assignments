""" Where's That Word? functions. """

# The constant describing the valid directions. These should be used
# in functions get_factor and check_guess.
UP = 'up'
DOWN = 'down'
FORWARD = 'forward'
BACKWARD = 'backward'

# The constants describing the multiplicative factor for finding a
# word in a particular direction.  This should be used in get_factor.
FORWARD_FACTOR = 1
DOWN_FACTOR = 2
BACKWARD_FACTOR = 3
UP_FACTOR = 4

# The constant describing the threshold for scoring. This should be
# used in get_points.
THRESHOLD = 5
BONUS = 12

# The constants describing two players and the result of the
# game. These should be used as return values in get_current_player
# and get_winner.
P1 = 'player one'
P2 = 'player two'
P1_WINS = 'player one wins'
P2_WINS = 'player two wins'
TIE = 'tie game'

# The constant describing which puzzle to play. Replace the 'puzzle1.txt' with
# any other puzzle file (e.g., 'puzzle2.txt') to play a different game.
PUZZLE_FILE = 'puzzle1.txt'


# Helper functions.  Do not modify these, although you are welcome to
# call them.

def get_column(puzzle: str, col_num: int) -> str:
    """Return column col_num of puzzle.

    Precondition: 0 <= col_num < number of columns in puzzle

    >>> get_column('abcd\\nefgh\\nijkl\\n', 1)
    'bfj'
    """

    puzzle_list = puzzle.strip().split('\n')
    column = ''
    for row in puzzle_list:
        column += row[col_num]

    return column


def get_row_length(puzzle: str) -> int:
    """Return the length of a row in puzzle.

    >>> get_row_length('abcd\\nefgh\\nijkl\\n')
    4
    """

    return len(puzzle.split('\n')[0])


def contains(text1: str, text2: str) -> bool:
    """Return whether text2 appears anywhere in text1.

    >>> contains('abc', 'bc')
    True
    >>> contains('abc', 'cb')
    False
    """

    return text2 in text1


# Implement the required functions below.

def get_current_player(player_one_turn: bool) -> str:
    """Return 'player one' iff player_one_turn is True; otherwise, return
    'player two'.

    >>> get_current_player(True)
    'player one'
    >>> get_current_player(False)
    'player two'
    """

    if player_one_turn:
        return P1
    return P2


def get_winner(s_one: int, s_two: int) -> str:
    """Return P1_WINS or P2_WINS or TIE based on the score.

    >>> get_winner(10, 5) == P1_WINS
    True
    >>> get_winner(5, 10) == P2_WINS
    True
    >>> get_winner(5, 5) == TIE
    True
    """

    if s_one > s_two:
        return P1_WINS
    if s_two > s_one:
        return P2_WINS
    return TIE


def reverse(string: str) -> str:
    """Return the reverse of the string.

    >>> reverse("abcd")
    'dcba'
    >>> reverse("")
    ''
    >>> reverse("121")
    '121'
    """

    return string[::-1]


def get_row(puzzle: str, r_num: int) -> str:
    """Return the letters in the row corresponding to the row number.

    >>> get_row("abcd\\nefgh\\nijkl\\n", 0)
    'abcd'
    >>> get_row("abcd\\nefgh\\nijkl\\n", 2)
    'ijkl'
    >>> get_row("abcd\\nefgh\\nijkl\\n", 1)
    'efgh'
    """

    lens = get_row_length(puzzle)
    index = (lens + 1) * r_num
    return puzzle[index: index + lens]


def get_factor(direction: str) -> int:
    """Return the multiplicative factor associated with this direction.

    >>> get_factor(UP)
    4
    >>> get_factor(FORWARD)
    1
    >>> get_factor(DOWN)
    2
    """

    if direction == FORWARD:
        return FORWARD_FACTOR
    if direction == DOWN:
        return DOWN_FACTOR
    if direction == BACKWARD:
        return BACKWARD_FACTOR
    return UP_FACTOR


def get_points(direction: str, n_words: int) -> int:
    """Return the points that would be earned.

    >>> get_points(BACKWARD, 2)
    24
    >>> get_points(BACKWARD, 5)
    15
    >>> get_points(BACKWARD, 1)
    39
    """

    factor = get_factor(direction)
    if n_words >= THRESHOLD:
        return THRESHOLD * factor
    res = (2 * THRESHOLD - n_words) * factor
    if n_words == 1:
        res += BONUS
    return res


def check_guess(puzzle: str, direction: str,
                word: str, line: int, left: int) -> int:
    """Return the number of points earned for this guess.

    >>> check_guess('abcd\\nefgh\\nijkl\\n', BACKWARD, 'dcba', 0, 2)
    24
    """

    if direction in (FORWARD, BACKWARD):
        guess = get_row(puzzle, line)
    else:
        guess = get_column(puzzle, line)
    if direction in (BACKWARD, UP):
        guess = reverse(guess)
    if contains(guess, word):
        return get_points(direction, left)
    return 0
