"""Unit test for recommender_functions.movies_to_users"""
import unittest

from recommender_functions import movies_to_users

class TestMoviesToUsers(unittest.TestCase):

    def test_movies_to_users(self):
        actual = movies_to_users({1: {10: 3.0}, 2: {10: 3.5}})
        expected = {10: [1, 2]}
        self.assertEqual(actual, expected)

    # Add tests below to create a complete set of tests without redundant tests
    # Redundant tests are tests that would only catch bugs that another test
    # would also catch.

    def test_movies_to_users_empty_entire(self):
        actual = movies_to_users({})
        expected = {}
        self.assertEqual(actual, expected)

    def test_movies_to_users_empty_sub(self):
        actual = movies_to_users({1: {}, 2: {10: 3.5}})
        expected = {10: [2]}
        self.assertEqual(actual, expected)

    def test_two_different_users(self):
        actual = movies_to_users({1: {2: 2}, 2: {10: 3.5}})
        expected = {10: [2], 2: [1]}
        self.assertEqual(actual, expected)

    def test_same_id(self):
        actual = movies_to_users({1: {1: 2}, 2: {10: 3.5}})
        expected = {10: [2], 1: [1]}
        self.assertEqual(actual, expected)

    def test_rate_same_movies(self):
        actual = movies_to_users({1: {2: 2, 10: 3}, 2: {10: 3.5}, 3: {2: 4}})
        expected = {2: [1, 3], 10: [1, 2]}
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main(exit=False)
