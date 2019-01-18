"""Functions for annotating poetry."""

# Type shorthands
from typing import List, TextIO
PronouncingTable = List[List[str]]

# The main module - need to import so that window code works correctly
import annotate_poetry

NO_STRESS_SYMBOL = 'x'
PRIMARY_STRESS_SYMBOL = '/'
SECONDARY_STRESS_SYMBOL = '\\'  # note: len('\\') == 1 due to special character

"""
A pronouncing table: a nested list, [list of str, list of list of str]
  o a two item list, contains two parallel lists
  o the first item is a list of words (each item in this sublist is a str
    for which str.isupper() is True)
  o the second item is a list of pronunciations, where a pronunciation is a
    list of phonemes (each item in this sublist is a list of str)
  o the pronunciation for the word at index i in the list of words is at index
    i in the list of pronunciations
"""

# A small pronouncing table that can be used in docstring examples.
SMALL_TABLE = [['A', 'BOX', 'CONSISTENT', 'DON\'T', 'FOX', 'IN', 'SOCKS'],
               [['AH0'],
                ['B', 'AA1', 'K', 'S'],
                ['K', 'AH0', 'N', 'S', 'IH1', 'S', 'T', 'AH0', 'N', 'T'],
                ['D', 'OW1', 'N', 'T'],
                ['F', 'AA1', 'K', 'S'],
                ['IH0', 'N'],
                ['S', 'AA1', 'K', 'S']]]

othersmalltabel = [['BIVIANO', 'BIVIN', 'BIVINS',
                    'BIVONA', 'BIVOUAC', 'BIWEEKLY', 'BIX', 'BIXBY',
                    'BIXEL', 'BIXLER', 'BIZ',
                    'BIZANGO', 'BIZARRE', 'BIZET'],
                   [['B', 'IY2', 'V', 'IY0', 'AA1', 'N', 'OW0'],
                    ['B', 'IH1', 'V', 'IH0', 'N'],
                    ['B', 'IH1', 'V', 'IH0', 'N', 'Z'],
                    ['B', 'IH0', 'V', 'OW1', 'N', 'AH0'],
                    ['B', 'IH1', 'V', 'W', 'AE0', 'K'],
                    ['B', 'AY0', 'W', 'IY1', 'K', 'L', 'IY0'],
                    ['B', 'IH1', 'K', 'S'],
                    ['B', 'IH1', 'K', 'S', 'B', 'IY0'],
                    ['B', 'IH1', 'K', 'S', 'AH0', 'L'],
                    ['B', 'IH1', 'K', 'S', 'L', 'ER0'],
                    ['B', 'IH1', 'Z'],
                    ['B', 'IH0', 'Z', 'AE1', 'NG', 'G', 'OW0'],
                    ['B', 'AH0', 'Z', 'AA1', 'R'], ['B', 'IH0', 'Z', 'EH1', 'T']]]

"""
A pronouncing dictionary is a list of pronouncing lines, where a pronouncing
line is a line in the CMU Pronouncing Dictionary format:
  a word followed by the phonemes describing how to pronounce the word.
  o example:
    BOX  B AA1 K S
"""

# A small pronouncing dictionary that can be used in docstring examples.
SMALL_PRONOUNCING_DICT = [
    'A AH0',
    'BOX B AA1 K S',
    'CONSISTENT K AH0 N S IH1 S T AH0 N T',
    'DON\'T D OW1 N T',
    'FOX F AA1 K S',
    'IN IH0 N',
    'SOCKS S AA1 K S']

othersmalldict = [
    'BIVIANO  B IY2 V IY0 AA1 N OW0',
    'BIVIN  B IH1 V IH0 N',
    'BIVINS  B IH1 V IH0 N Z',
    'BIVONA  B IH0 V OW1 N AH0',
    'BIVOUAC  B IH1 V W AE0 K',
    'BIWEEKLY  B AY0 W IY1 K L IY0',
    'BIX  B IH1 K S',
    'BIXBY  B IH1 K S B IY0',
    'BIXEL  B IH1 K S AH0 L',
    'BIXLER  B IH1 K S L ER0',
    'BIZ  B IH1 Z',
    'BIZANGO  B IH0 Z AE1 NG G OW0',
    'BIZARRE  B AH0 Z AA1 R',
    'BIZET  B IH0 Z EH1 T']


# ===================== Provided Helper Functions =============================

def prepare_word(s: str) -> str:
    """Return a new string based on s in which all letters have been converted
    to uppercase and punctuation characters have been stripped from both ends.

    Inner punctuation is left unchanged.

    This function prepares a word for looking up in a pronouncing table.

    >>> prepare_word('Birthday!!!')
    'BIRTHDAY'
    >>> prepare_word('"Quoted?"')
    'QUOTED'
    >>> prepare_word("Don't!")
    "DON'T"
    """

    punctuation = """!"`@$%^&_+-={}|\\/—,;:'.-?)([]<>*#\n\t\r"""
    result = s.upper().strip(punctuation)
    return result


def get_rhyme_scheme_letter(offset: int) -> str:
    """Return the letter corresponding to the offset from 'A'.  Helpful when
    labelling a poem with its rhyme scheme.

    Precondition: 0 <= offset <= 25

    >>> get_rhyme_scheme_letter(0)
    'A'
    >>> get_rhyme_scheme_letter(25)
    'Z'
    """

    return chr(ord('A') + offset)


def get_word(pronu_line: str) -> str:
    """
    Return only the word from the pronuncing line

    >>> get_word('BOX B AA1 K S')
    'BOX'
    >>> get_word('CONSISTENT K AH0 N S IH1 S T AH0 N T')
    'CONSISTENT'
    >>> get_word('SOCKS S AA1 K S')
    'SOCKS'
    """
    index_num = pronu_line.find(' ')
    return pronu_line[:index_num]


def get_pronunciation(pronu_line: str) -> List[str]:
    """
    Return the pronuncing line as a list

    >>> get_pronunciation('BOX B AA1 K S')
    ['B', 'AA1', 'K', 'S']
    >>> get_pronunciation('IN IH0 N')
    ['IH0', 'N']

    """
    return pronu_line.split()[1:]


def make_pronouncing_table(pronouncing_list: List[str]) -> PronouncingTable:
    """

    NOTE: This is not the first function that you should write, but we included
    the function header and one example for illustrative purposes. You should
    fill in the proper docstring and add another example to this function. You
    should also write other functions.

    >>> SMALL_TABLE == make_pronouncing_table(SMALL_PRONOUNCING_DICT)
    True
    >>> othersmalltabel == make_pronouncing_table(othersmalldict)
    True

    """
    result = []
    words_list = []
    pronoun = []
    for item in pronouncing_list:
        words_list.append(get_word(item))
    result.append(words_list)
    for item in pronouncing_list:
        pronoun.append(get_pronunciation(item))
    result.append(pronoun)
    return result


def look_up_pronunciation(word: str, pron_table: PronouncingTable) -> List[str]:
    """
    Return the word's pronouncation from the pronouncing table

    >>> look_up_pronunciation('BOX', SMALL_TABLE)
    ['B', 'AA1', 'K', 'S']
    >>> look_up_pronunciation('CONSISTENT', SMALL_TABLE)
    ['K', 'AH0', 'N', 'S', 'IH1', 'S', 'T', 'AH0', 'N', 'T']
    """
    index = pron_table[0].index(prepare_word(word))
    return pron_table[1][index]


def is_vowel_phoneme(word: str) -> bool:
    """
    Return True iff the word is a vowel phoneme
    whichhas three characters, with the first character being
    one of A, E, I, O, or U, the second character
    is an upper case letter, and the last character is one of 0, 1, or 2

    >>> is_vowel_phoneme('AA1')
    True
    >>> is_vowel_phoneme('K')
    False
    """
    return len(word) >= 3 and word[1].isupper()\
           and word[-1] in ['0', '1', '2'] \
           and word[0] in ['A', 'E', 'I', 'O', 'U']


def last_syllable(pron_list: List[str]) -> List[str]:
    """
    Return the last vowel phoneme and any subsequent consonant phoneme(s) from the list

    >>> last_syllable(['K', 'AH0', 'N', 'S', 'IH1', 'S', 'T', 'AH0', 'N', 'T'])
    ['AH0', 'N', 'T']
    >>> last_syllable(['K', 'N', 'S', 'S', 'T', 'N', 'T'])
    ['K', 'N', 'S', 'S', 'T', 'N', 'T']

    """

    pron_list.reverse()
    reverse = pron_list[:]
    pron_list.reverse()
    for item in range(len(reverse)):
        if is_vowel_phoneme(reverse[item]):
            result = reverse[:item + 1]
            result.reverse()
            return result
    return pron_list


def convert_to_lines(poem: TextIO) -> List[str]:
    """
    Return list of poem lines
    """
    res = []
    line = poem.readline()
    while line == '\n':
        line = poem.readline()
    while line != '':
        if line == '\n':
            res.append('')
        else:
            res.append(line.strip())
        line = poem.readline()
    res.reverse()
    for i in range(len(res)):
        if res[i] != '':
            res = res[i:]
            res.reverse()
            return res
    res.reverse()
    return res



def detect_rhyme_scheme(peom: List[str], pron_table: PronouncingTable) -> List[str]:
    """
    Return the rhyme scheme list with the order of each poem lines

    >>> b = ['BoX','FOx', 'sOCKS']
    >>> detect_rhyme_scheme(b, SMALL_TABLE)
    ['A', 'A', 'A']

    >>> b = ['CONSISTENT', "DON\'T", 'FOX']
    >>> detect_rhyme_scheme(b, SMALL_TABLE)
    ['A', 'B', 'C']
    """
    res = []
    word_pronce = []
    for line in peom:
        if line != '':
            line_list = line.strip().split()
            last_pron = look_up_pronunciation(prepare_word(line_list[-1]), pron_table)
            lastsyll = last_syllable(last_pron)
            if lastsyll not in word_pronce:
                word_pronce.append(lastsyll)
            index = word_pronce.index(lastsyll)
            res.append(get_rhyme_scheme_letter(index))
        else:
            res.append('')
    return res


def get_stress_pattern(word: str, pron_table: PronouncingTable) -> str:
    """
    Return a string of stress pattern for the words by using the sybol of three
    levels stress, make the string have the same length of the word by using blank.

    >>> get_stress_pattern('box',SMALL_TABLE)
    '/  '
    >>> get_stress_pattern('fox',SMALL_TABLE)
    '/  '
    >>> get_stress_pattern('CONsIStENT',SMALL_TABLE)
    'x / x     '
    >>> get_stress_pattern('a',SMALL_TABLE)
    'x'
    """

    res = ''
    pron_list = look_up_pronunciation(word, pron_table)
    for item in pron_list:
        if is_vowel_phoneme(item):
            if item[-1] == '0':
                res += NO_STRESS_SYMBOL + ' '
            elif item[-1] == '1':
                res += PRIMARY_STRESS_SYMBOL + ' '
            else:
                res += SECONDARY_STRESS_SYMBOL + ' '
    result = res.strip()
    i = 0
    n = len(word) - len(result)
    while i < n:
        result += ' '
        i += 1
    return result


if __name__ == '__main__':

    """Optional: uncomment the lines import doctest and doctest.testmod() to
    have your docstring examples run when you run stress_and_rhyme_functions.py
    NOTE: your docstrings MUST be properly formatted for this to work!
    """
    import doctest
    doctest.testmod()
