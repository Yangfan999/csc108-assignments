"""Starter code for Assignment 1 CSC108 Summer 2018"""

SPECIAL_CASE_SCHOOL_1 = 'Fort McMurray Composite High'
SPECIAL_CASE_SCHOOL_2 = 'Father Mercredi High School'
SPECIAL_CASE_YEAR = '2017'
ACCEPT = 'accept'
REJECT = 'reject'
ACCEPT_WITH_SCHOLARSHIP = 'accept with scholarship'
NE = 'NE'
# Add other constants here


def is_special_case(record: str) -> bool:
    """Return True iff the student represented by record is a special case.

    >>> is_special_case('Jacqueline Smith,Fort McMurray Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    True
    >>> is_special_case('Jacqueline Smith,Father Something High School,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    False
    >>> is_special_case('Jacqueline Smith,Fort McMurray Composite High,2015,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    False
    """

    first_index = record.find(',') + 1
    sec_index = record.find(',', first_index)
    third_index = record.find(',', sec_index + 1)
    return (record[first_index:sec_index] == SPECIAL_CASE_SCHOOL_1
            or record[first_index:sec_index] == SPECIAL_CASE_SCHOOL_2) \
        and record[sec_index + 1:third_index] == SPECIAL_CASE_YEAR


def get_final_mark(record: str, mark: str, exam: str) -> float:
    """ Return the average for coursework mark and exam mark as the final mark
    exam mark count for zero if an student miss the exam unless he is in a
    special case.

    >>> get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts','90', 'NE' )
    90.0
    >>> get_final_mark('Jacqueline Smith,Father Something High School,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts','90', 'NE')
    45.0
    >>> get_final_mark('Jacqueline Smith,Father Something High School,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts','90', '91')
    90.5
    """
    if exam == NE:
        if is_special_case(record):
            return float(mark)
        else:
            return float(mark) / 2
    else:
        s = (float(mark) + float(exam))
        return s / 2


def get_both_marks(record: str, code: str) -> str:
    """ Return the string coursework mark and exam mark if the course code
    matches course record that given, otherwise return empty string.

    >>> get_both_marks('MAT,97,NE', 'MAT')
    '97 NE'
    >>> get_both_marks('MAT,97,NE', 'ENG')
    ''
    >>> get_both_marks('MAT,97,98', 'MAT')
    '97 98'
    """
    first_index = record.find(',')
    sec_index = record.find(',', first_index + 1)
    if record[:first_index] == code:
        return record[first_index + 1:sec_index] + ' ' + record[sec_index + 1:]
    else:
        return ''


def extract_course(transcript: str, th: int) -> str:
    """ Return the course record from the student transcript by the indicating
    number from second parameter.

    >>> extract_course('MAT,90,94,ENG,92,NE,CHM,80,85', 2)
    'ENG,92,NE'
    >>> extract_course('MAT,90,94,ENG,92,NE,CHM,80,85', 3)
    'CHM,80,85'
    >>> extract_course('MAT,90,94,ENG,92,NE,CHM,80,85', 1)
    'MAT,90,94'
    """
    s = 10
    k = (th - 1) * s
    if k + 9 > len(transcript):
        return transcript[k:]
    else:
        return transcript[k:k + 9]


def applied_to_degree(record: str, deg: str) -> bool:
    """ Return Ture if and only if the student applied the given degree.

    >>> applied_to_degree('Jacqueline Smith,Fort McMurray Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts', 'BArts')
    True
    >>> applied_to_degree('Jacqueline Smith,Fort McMurray Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts', 'BSci')
    False
    """
    s = len(deg)
    return record[-s:] == deg and record[-s - 1] == ','


def decide_admission(score, cutoff) -> str:
    """ Return 'accept' if a student's mark above the cut off mark but below the
    scholarship cutoff, return 'reject' if a student's mark below the cutoff
    mark and return 'accept with scholarship' if a a student's mark above cutoff
    mark more than or equal to 5.

    >>> decide_admission(90, 80)
    'accept with scholarship'
    >>> decide_admission(90, 87)
    'accept'
    >>> decide_admission(90, 91)
    'reject'
    """
    cos = float(cutoff) + 5
    if float(score) < float(cutoff):
        return REJECT
    elif float(cutoff) <= float(score) < cos:
        return ACCEPT
    else:
        return ACCEPT_WITH_SCHOLARSHIP
