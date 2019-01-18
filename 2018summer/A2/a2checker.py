"""Checker for CSC108 Assignment 2"""

import sys

sys.path.insert(0, './pyta')


print("================= Start: checking coding style =================")

import python_ta
python_ta.check_all('stress_and_rhyme_functions.py', config='pyta/a2_pyta.txt')

print("================= End: checking coding style =================\n")


print("================= Start: checking parameter and return types =================")

import builtins
import copy

# Check for use of functions print and input.
our_print = print
our_input = input

def disable_print(*_args, **_kwargs):
    """ Notices if print is called """
    raise Exception("You must not call built-in function print!")


def disable_input(*_args, **_kwargs):
    """ Notices if input is called """
    raise Exception("You must not call built-in function input!")

builtins.print = disable_print
builtins.input = disable_input

import stress_and_rhyme_functions

# Type checks and simple checks for stress_and_rhyme_functions module

# A small pronouncing table that can be used in docstring examples.
SMALL_TABLE = [['A', 'BOX', 'CONSISTENT', 'DON\'T', 'FOX', 'IN', 'SOCKS'],
               [['AH0'],
                ['B', 'AA1', 'K', 'S'],
                ['K', 'AH0', 'N', 'S', 'IH1', 'S', 'T', 'AH0', 'N', 'T'],
                ['D', 'OW1', 'N', 'T'],
                ['F', 'AA1', 'K', 'S'],
                ['IH0', 'N'],
                ['S', 'AA1', 'K', 'S']]]

# Type check and simple check stress_and_rhyme_functions.get_word
result = stress_and_rhyme_functions.get_word('BOX  B AA1 K S')
assert isinstance(result, str), \
    '''stress_and_rhyme_functions.get_word should return a str,''' \
    ''' but returned {0}.'''.format(type(result))
assert result, \
    '''stress_and_rhyme_functions.get_word('BOX  B AA1 K S')''' \
    ''' should return 'BOX', but ''' \
    '''returned {0}.'''.format(result)

# Type check and simple check stress_and_rhyme_functions.get_pronunciation
result = stress_and_rhyme_functions.get_pronunciation('BOX  B AA1 K S')
assert isinstance(result, list), \
    """stress_and_rhyme_functions.get_pronunciation should return a list,""" \
    """ but returned {0}.""".format(type(result))
assert result == ['B', 'AA1', 'K', 'S'], \
    """stress_and_rhyme_functions.get_pronunciation('BOX  B AA1 K S')""" \
    """ should return ['B', 'AA1', 'K', 'S'] but """ \
    """returned {0}.""".format(result)

# Type check and simple check stress_and_rhyme_functions.make_pronouncing_table
result = stress_and_rhyme_functions.make_pronouncing_table(['BOX  B AA1 K S'])
assert isinstance(result, list), \
    """stress_and_rhyme_functions.make_pronouncing_table should return a list,""" \
    """ but returned {0}.""".format(type(result))
assert result == [['BOX'], [['B', 'AA1', 'K', 'S']]], \
    """stress_and_rhyme_functions.make_pronouncing_table(['BOX  B AA1 K S'])""" \
    """ should return [['BOX'], [['B', 'AA1', 'K', 'S']]] but """ \
    """returned {0}.""".format(result)

# Type check and simple check stress_and_rhyme_functions.look_up_pronunciation
result = stress_and_rhyme_functions.look_up_pronunciation("Don't!", SMALL_TABLE)
assert isinstance(result, list), \
    """stress_and_rhyme_functions.look_up_pronunciation should return a list,""" \
    """ but returned {0}.""".format(type(result))
assert result == ['D', 'OW1', 'N', 'T'], \
    """stress_and_rhyme_functions.look_up_pronunciation("Don't!", SMALL_TABLE)""" \
    """ should return ['D', 'OW1', 'N', 'T'] but """ \
    """returned {0}.""".format(result)

# Type check and simple check stress_and_rhyme_functions.is_vowel_phoneme
result = stress_and_rhyme_functions.is_vowel_phoneme("AE0")
assert isinstance(result, bool), \
    """stress_and_rhyme_functions.is_vowel_phoneme should return a bool,""" \
    """ but returned {0}.""".format(type(result))
assert result == True, \
    """stress_and_rhyme_functions.is_vowel_phoneme("AE0")""" \
    """ should return True but """ \
    """returned {0}.""".format(result)

# Type check and simple check stress_and_rhyme_functions.last_syllable
result = stress_and_rhyme_functions.last_syllable(['D', 'OW1', 'N', 'T'])
assert isinstance(result, list), \
    """stress_and_rhyme_functions.last_syllable should return a list,""" \
    """ but returned {0}.""".format(type(result))
assert result == ['OW1', 'N', 'T'], \
    """stress_and_rhyme_functions.last_syllable(['D', 'OW1', 'N', 'T'])""" \
    """ should return ['OW1', 'N', 'T'] but """ \
    """returned {0}.""".format(result)

# Type check and simple check stress_and_rhyme_functions.convert_to_lines
short_file = open("short.txt", "r")
result = stress_and_rhyme_functions.convert_to_lines(short_file)
short_file.close()
assert isinstance(result, list), \
    """stress_and_rhyme_functions.convert_to_lines should return a list,""" \
    """ but returned {0}.""".format(type(result))
assert result == ["I'll sit here instead,", '', 'A cloud on my head'], \
    """stress_and_rhyme_functions.convert_to_lines(open('short.txt'))""" \
    """ should return ["I'll sit here instead,", '', 'A cloud on my head'] but """ \
    """returned {0}.""".format(result)

# Type check and simple check stress_and_rhyme_functions.detect_rhyme_scheme
result = stress_and_rhyme_functions.detect_rhyme_scheme(['BOX','FOX'], SMALL_TABLE)
assert isinstance(result, list), \
    """stress_and_rhyme_functions.detect_rhyme_scheme should return a list,""" \
    """ but returned {0}.""".format(type(result))
assert result == ['A', 'A'], \
    """stress_and_rhyme_functions.detect_rhyme_scheme(['BOX','FOX'], SMALL_TABLE)""" \
    """ should return ['A', 'A'] but """ \
    """returned {0}.""".format(result)

# Type check and simple check stress_and_rhyme_functions.get_stress_pattern
result = stress_and_rhyme_functions.get_stress_pattern('consistent', SMALL_TABLE)
assert isinstance(result, str), \
    """stress_and_rhyme_functions.get_stress_pattern should return a str,""" \
    """ but returned {0}.""".format(type(result))
assert result == 'x / x     ', \
    """stress_and_rhyme_functions.get_stress_pattern('consistent', SMALL_TABLE)""" \
    """ should return 'x / x     ' but """ \
    """returned {0}.""".format(result)

builtins.print = our_print
builtins.input = our_input


print("================= End: checking parameter and return types =================\n")

print("The parameter and return type checker passed.")
print("This means we will be able to test your code.")
print("It does NOT mean your code is necessarily correct.")
print("You should run your own thorough tests to convince yourself your code is correct.")
print()
print("Scroll up to review the output of checking coding style.")
