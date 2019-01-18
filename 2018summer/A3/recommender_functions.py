"""CSC108 A3 recommender starter code."""

from typing import TextIO, List, Dict

from recommender_constants import (MovieDict, Rating, UserRatingDict,
                                   MovieUserDict)
from recommender_constants import (MOVIE_FILE_STR, RATING_FILE_STR,
                                   MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL,
                                   MOVIE_USER_DICT_SMALL)

############## HELPER FUNCTIONS

def get_similarity(user1: Rating, user2: Rating) -> float:
    """Return the a similarity score between user1 and user2 based on their
    movie ratings. The returned similarity score is a number between 0 and 1
    inclusive. The higher the number, the more similar user1 and user2 are.

    For those who are curious, this type of similarity measure is called the
    "cosine similarity".

    >>> r1 = {1: 4.5, 2: 3.0, 3: 1.0}
    >>> r2 = {2: 4.5, 3: 3.5, 4: 1.5, 5: 5.0}
    >>> s1 = get_similarity(r1, r1)
    >>> abs(s1 - 1.0) < 0.0001 # s1 is close to 1.0
    True
    >>> s2 = get_similarity(r1, {6: 4.5})
    >>> abs(s2 - 0.0) < 0.0001 # s2 is close to 0.0
    True
    >>> round(get_similarity(r1, r2), 2)
    0.16
    """
    shared = 0.0
    for m_id in user1:
        if m_id in user2:
            shared += user1[m_id] * user2[m_id]
    norm1 = 0.0
    for m_id in user1:
        norm1 = norm1 + user1[m_id] ** 2
    norm2 = 0.0
    for m_id in user2:
        norm2 = norm2 + user2[m_id] ** 2
    return (shared * shared) / (norm1 * norm2)


############## STUDENT CONSTANTS

# write constants here
SPLIT = ","
RATING_THRESHOLD = 3.5

############## STUDENT HELPER FUNCTIONS


def get_candidate_movies(target: Rating, similars: Dict[int, float],
                         rating: UserRatingDict) -> List[int]:
    """Helper: Return a list of movies that these similar users have rated 3.5 or above,
    that our target user has not rated.

    """
    lst = []
    target_watched = list(target.keys())
    for u in similars:
        for m in rating[u]:
            if m not in target_watched and rating[u][m] >= RATING_THRESHOLD \
                    and m not in lst:
                lst.append(m)
    return lst


def num_rated_above(candidate: List[int], similar: Rating) -> int:
    """Helper: Return the number of candidate movies the similar user rated 3.5 or above.
    """
    result = 0
    for m in similar:
        if m in candidate and similar[m] >= RATING_THRESHOLD:
            result += 1
    return result


def total_rated(users: List[int], movie: int, ratings: UserRatingDict) -> int:
    """Return the number of total users who rated the movie.
    """
    result = 0
    for i in users:
        if movie in list(ratings[i].keys()):
            result += 1
    return result

############## STUDENT FUNCTIONS


def read_movies(movie_file: TextIO) -> MovieDict:
    """Return a dictionary containing movie id to (movie name, movie genres)
    in the movie_file.

    >>> movfile = open('movies_tiny.csv')
    >>> movies = read_movies(movfile)
    >>> movfile.close()
    >>> 68735 in movies
    True
    >>> movies[124057]
    ('Kids of the Round Table', [])
    >>> len(movies)
    4
    >>> movies == MOVIE_DICT_SMALL
    True
    """
    result = {}
    movie_file.readline()
    line = movie_file.readline()
    while line:
        lst = line.strip().split(SPLIT)
        result[int(lst[0])] = (lst[1], lst[4:])
        line = movie_file.readline()
    return result


def read_ratings(rating_file: TextIO) -> UserRatingDict:
    """Return a dictionary containing user id to {movie id: ratings} for the
    collection of user movie ratings in rating_file.

    >>> rating_file = open('ratings_tiny.csv')
    >>> ratings = read_ratings(rating_file)
    >>> rating_file.close()
    >>> len(ratings)
    2
    >>> ratings[1]
    {2968: 1.0, 3671: 3.0}
    >>> ratings[2]
    {10: 4.0, 17: 5.0}
    """
    result = {}
    rating_file.readline()
    line = rating_file.readline()
    while line:
        lst = line.strip().split(SPLIT)
        value = int(lst[0])
        if value not in result:
            result[value] = {}
        result[value][int(lst[1])] = float(lst[2])
        line = rating_file.readline()
    return result


def remove_unknown_movies(user_ratings: UserRatingDict,
                          movies: MovieDict) -> None:
    """Modify the user_ratings dictionary so that only movie ids that are in the
    movies dictionary is remaining. Remove any users in user_ratings that have
    no movies rated.

    >>> small_ratings = {1001: {68735: 5.0, 302156: 3.5, 10: 4.5}, 1002: {11: 3.0}}
    >>> remove_unknown_movies(small_ratings, MOVIE_DICT_SMALL)
    >>> len(small_ratings)
    1
    >>> small_ratings[1001]
    {68735: 5.0, 302156: 3.5}
    >>> 1002 in small_ratings
    False
    """
    key = []
    for u_id in user_ratings:
        movie = {}
        for m_id in user_ratings[u_id]:
            if m_id in movies:
                movie[m_id] = user_ratings[u_id][m_id]
        if movie:
            user_ratings[u_id] = movie
        else:
            key.append(u_id)
    for k in key:
        user_ratings.pop(k)


def movies_to_users(user_ratings: UserRatingDict) -> MovieUserDict:
    """Return a dictionary of movie ids to list of users who rated the movie,
    using information from the user_ratings dictionary of users to movie
    ratings dictionaries.

    >>> result = movies_to_users(USER_RATING_DICT_SMALL)
    >>> result == MOVIE_USER_DICT_SMALL
    True
    """
    movie_user_dict = {}
    for u in user_ratings:
        for m in user_ratings[u]:
            if m in movie_user_dict:
                movie_user_dict[m].append(u)
            else:
                movie_user_dict[m] = [u]
    return movie_user_dict


def get_users_who_watched(movie_ids: List[int],
                          movie_users: MovieUserDict) -> List[int]:
    """Return the list of user ids in moive_users who watched at least one
    movie in moive_ids.

    >>> get_users_who_watched([293660], MOVIE_USER_DICT_SMALL)
    [2]
    >>> lst = get_users_who_watched([68735, 302156], MOVIE_USER_DICT_SMALL)
    >>> len(lst)
    2
    """
    lst = []
    for m in movie_users:
        if m in movie_ids:
            for u in movie_users[m]:
                if u not in lst:
                    lst.append(u)
    return lst


def get_similar_users(target_rating: Rating,
                      user_ratings: UserRatingDict,
                      movie_users: MovieUserDict) -> Dict[int, float]:
    """Return a dictionary of similar user ids to similarity scores between the
    similar user's movie rating in user_ratings dictionary and the
    target_rating. Only return similarites for similar users who has at least
    one rating in movie_users dictionary that appears in target_Ratings.

    >>> sim = get_similar_users({293660: 4.5}, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL)
    >>> len(sim)
    1
    >>> round(sim[2], 2)
    0.86
    """
    dic = {}
    watched = get_users_who_watched(list(target_rating.keys()), movie_users)
    for u in watched:
        dic[u] = get_similarity(target_rating, user_ratings[u])
    return dic


def recommend_movies(target_rating: Rating,
                     movies: MovieDict,
                     user_ratings: UserRatingDict,
                     movie_users: MovieUserDict,
                     num_movies: int) -> List[int]:
    """Return a list of num_movies movie id recommendations for a target user
    with target_rating of previous movies. The recommendations come from movies
    dictionary, and are based on movies that "similar users" data in
    user_ratings / movie_users dictionaries.

    >>> recommend_movies({302156: 4.5}, MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL, 2)
    [68735]
    >>> recommend_movies({68735: 4.5}, MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL, 2)
    [302156, 293660]
    """
    similars = get_similar_users(target_rating, user_ratings, movie_users)
    movie_lst = get_candidate_movies(target_rating, similars, user_ratings)
    movies = {}
    for m in movie_lst:
        for u in movie_users[m]:
            if u in similars:
                score = similars[u]
                num_user_movie = num_rated_above(movie_lst, user_ratings[u])
                movie_popularity = total_rated(movie_users[m], m, user_ratings)
                movies[m] = movies.get(m, 0) + score / (num_user_movie * movie_popularity)
    lst = sorted(list(movies.items()))
    result = [i[0] for i in
              sorted(lst, key=lambda k: k[1], reverse=True)]
    return result[:num_movies]





if __name__ == '__main__':
    """Uncomment to run doctest"""
    #import doctest
    #doctest.testmod()
