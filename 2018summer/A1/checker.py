import sys
sys.path.insert(0, 'pyta')

print("================= Start: checking coding style =================")

import python_ta
python_ta.check_all('admission_functions.py', config='pyta/a1_pyta.txt')

print("================= End: checking coding style =================\n")

print("================= Start: checking parameter and return types =================")

import builtins

# Check for use of functions print and input.

# IMPORTANT!
# If you are getting a syntax error here for the line:
#     our_print = print
# Then you are using the wrong version of Python! 
our_print = print
our_input = input


def disable_print(*args):
    raise Exception("You must not call print anywhere in your code!")

def disable_input(*args):
    raise Exception("You must not call input anywhere in your code!")


builtins.print = disable_print
builtins.input = disable_input

import admission_functions as af

# Get the initial values of the constants
constants_before = [af.SPECIAL_CASE_SCHOOL_1,
                    af.SPECIAL_CASE_SCHOOL_2,
                    af.SPECIAL_CASE_YEAR]


result = af.is_special_case('Jacqueline Smith,Best High School,2002,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
assert isinstance(result, bool), \
    '''af.is_special_case should return a bool, but returned {0}
       '''.format(type(result))


# Type check af.get_final_mark
record = 'Paul Gries,Ithaca High School,1986,BIO,60,70,CHM,80,90,CAT,10,20,BEng'
result = af.get_final_mark(record, '10', '20')
assert isinstance(result, float), \
    '''af.get_final_mark should return a float, but returned {0}
       '''.format(type(result))


# Type check af.get_both_marks
result = af.get_both_marks('ABC,10,20', 'ABC')
assert isinstance(result, str), \
    '''af.get_both_marks should return a str, but returned {0}
       '''.format(type(result))


# Type check af.extract_course
result = af.extract_course('ABC,10,20', 1)
assert isinstance(result, str), \
    '''af.extract_course should return a str, but returned {0}
       '''.format(type(result))


# Type check af.applied_to_degree
record = 'Paul Gries,Ithaca High School,1986,BIO,60,70,CHM,80,90,CAT,95,96,BEng'
result = af.applied_to_degree(record, 'BEng')
assert isinstance(result, bool), \
    '''af.applied_to_degree should return a bool, but returned {0}
       '''.format(type(result))


# Type check af.decide_admission
valid_strings = ['accept', 'reject', 'accept with scholarship']
for x in [18, 22, 30]:
    result = af.decide_admission(x, 20)
    assert isinstance(result, str), \
        '''af.decide_admission should return a str, but returned {0}
           '''.format(type(result))
    assert result.strip().lower() in valid_strings, \
        '''af.decide_admission should return one of {0}, but returned {1}
           '''.format("'" + "', '".join(valid_strings) + "'", "'" + result + "'")

builtins.print = our_print
builtins.input = our_input

print("================= End: checking parameter and return types =================\n")

print("================= Start: checking whether constants are unchanged =================")

# Get the final values of the constants
constants_after = [af.SPECIAL_CASE_SCHOOL_1,
                    af.SPECIAL_CASE_SCHOOL_2,
                    af.SPECIAL_CASE_YEAR]


# Check whether the constants are unchanged.
assert constants_before == constants_after, \
       """Your function(s) modified the value of a constant(s). Edit your code
        so that the values of constants are unchanged by your functions."""
print("================= End: checking whether constants are unchanged =================\n")



print("The parameter and return type checker passed.")
print("This means we will be able to test your code.")
print("It does NOT mean your code is necessarily correct.")
print("You should run your own thorough tests to convince yourself your code is correct.")
print()
print("Scroll up to review the output of checking coding style.")


