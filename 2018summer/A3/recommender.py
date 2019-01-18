"""CSC108 A3 interactive recommender."""

from typing import List
import recommender_functions as student
from recommender_constants import MovieDict, Rating, UserRatingDict, MovieUserDict

def print_recommend(target_rating: Rating,
                    movies: MovieDict,
                    ratings: UserRatingDict,
                    movie_users: MovieUserDict) -> None:
    """Print recommendations from movies for a user with target_rating, using
    data from ratings and movie_users.
    """
    results = student.recommend_movies(target_rating, 
                                       movies,
                                       ratings,
                                       movie_users,
                                       5)
    print("Watched:")
    for movie_id in target_rating:
        print(movie_id, movies[movie_id][0])
    print("Recommend:")
    for movie_id in results:
        print(movie_id, movies[movie_id][0])
    print()


def search_movie(query: str, movies_dict: MovieDict) -> List[tuple]:
    """Return a list of movies in movies_dict with query in its title.
    The match can be case insensitive.
    """
    results = []
    query = query.lower()
    for mid in movies_dict:
        title = movies_dict[mid][0]
        if query in title.lower():
            results.append((mid, title))
    return results


def recommend_interactive(movies: MovieDict,
                          ratings: UserRatingDict,
                          movie_users: MovieUserDict) -> None:
    """Recommend movies based on user input using data from movies, rating,
    and movie_users.
    """

    print("This script uses the code you wrote to recommend movies.")
    print("To begin, rate at least one movie using the 'rate' command.")
    print("You will need to know the movie ID in order to rate a movie.")
    print("You can use the 'search' command to search for a movie's ID.")
    
    command = None # user input command
    while command != 'no':
        user_ratings = {}
        while command != 'recommend':
            print()
            print("Type 'search', 'rate' or 'recommend' to search for a " +
                  "movie, rate a movie, or see recommendations.")
            command = input("Command: ")
            if command == 'search':
                print("What movie would you like to search for?")
                query = input("Search: ")
                query = query.strip()
                results = search_movie(query, movies)
                if len(results) > 0:
                    print("Search results:")
                    for k, v in results:
                        print("Movie Id: " + str(k) + ", Title: " + v)
                else:
                    print("There are no movies with that title.")
            if command == 'rate':
                print("What movie ID do you wish to rate?")
                mid = input("Movie ID: ")
                mid = int(mid)
                if mid not in movies:
                    print("That movie id does not exist.")
                else:
                    title = movies[mid][0]
                    print("What is your rating (0.5 - 5.0) for " + title + "?")
                    rating = input("Rating: ")
                    rating = float(rating)
                    if 0.5 <= rating <= 5:
                        user_ratings[mid] = rating
                    else:
                        print("Rating should be a decimal number between " +
                              "0.5 and 5.0")
            if command == 'recommend':
                if len(user_ratings) == 0:
                    print("You must rate at least one movie to use the " +
                          "recommender.")
                    command = None # to not exit the while loop
        
        print()
        print("You have rated the following movies:")
        for movie, rating in user_ratings.items():
            print(movies[movie][0] + "    -- " + str(rating))
        print()
        print("Here are your top 5 recommendations:")
        results = student.recommend_movies(user_ratings,
                                           movies,
                                           ratings, 
                                           movie_users,
                                           5)
        for movie_id in results:
            print(movie_id, movies[movie_id][0])

        print()
        print("Would you like to run another recommendation?")
        command = input("Type 'no' to exit: ")    

if __name__ == "__main__":
    # print("Reading in a list of movies.")
    movfile = open('movies.csv', 'r')
    movies = student.read_movies(movfile)
    movfile.close()

    # print("Reading in user ratings.")
    ratingfile = open('ratings_medium.csv', 'r')
    ratings = student.read_ratings(ratingfile)
    ratingfile.close()

    # print("Removing ratings for movies we have no data on.")
    student.remove_unknown_movies(ratings, movies)

    # print("Building movies to users dictionary.")
    movie_users = student.movies_to_users(ratings)


    ### You can uncomment these to test recommendations for the following movies

    # print_recommend({663:5, 274:4.5, 745:4.5}, movies, ratings, movie_users)
    # Should get: [25753, 65, 25769, 74, 82]
    
    # print_recommend({2109:3, 954:4}, movies, ratings, movie_users)
    # Should get: [2313, 100, 2049, 2642, 6970]
    
    # print_recommend({745:5}, movies, ratings, movie_users)
    # Should get: [25753, 25769, 82, 74, 2348]
    
    # print_recommend({1262:5}, movies, ratings, movie_users)
    # Should get: [4515, 2289, 1249, 55687, 2284]


    ### Run interactive recommendations

    recommend_interactive(movies, ratings, movie_users)

