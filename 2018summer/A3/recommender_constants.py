"""CSC108 Recommender constants and types."""
from typing import List, Dict

# Data Types

MovieDict = Dict[int, tuple]
Rating = Dict[int, float]
UserRatingDict = Dict[int, Rating]
MovieUserDict = Dict[int, List[int]]

# Constants -- do not modify!

MOVIE_FILE_STR = \
    """movie_id,title,release_date,runtime,genres
68735,Warcraft,2016-05-25,123.0,Action,Adventure,Fantasy
293660,Deadpool,2016-02-09,108.0,Action,Adventure,Comedy
302156,Criminal,2016-04-14,113.0,Action
124057,Kids of the Round Table,1997-07-08,89.0
"""

RATING_FILE_STR = \
    """user_id,movie_id,rating,timestamp
1,2968,1.0,1260759200
1,3671,3.0,1260759117
2,10,4.0,835355493
2,17,5.0,835355681
"""

MOVIE_DICT_SMALL = {
    68735: ('Warcraft', ['Action', 'Adventure', 'Fantasy']),
    293660: ('Deadpool', ['Action', 'Adventure', 'Comedy']),
    302156: ('Criminal', ['Action']),
    124057: ('Kids of the Round Table', [])
}
USER_RATING_DICT_SMALL = {
    1: {68735: 3.5, 302156: 4.0},
    2: {68735: 1.0, 124057: 1.5, 293660: 4.5}
}
MOVIE_USER_DICT_SMALL = {
    293660: [2],
    68735: [1, 2],
    302156: [1],
    124057: [2]
}

