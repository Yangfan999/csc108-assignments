"""Annotate Poetry main function."""

# The student created stress and rhyme module - so we can use student solutions
import stress_and_rhyme_functions as student

# Type shorthands
from typing import List, TextIO
PronouncingTable = List[List[str]]

# The Graphical User Interface (GUI) module - so we can display in new window
from tkinter import *
from tkinter.filedialog import askopenfilename

# The OS module - so we can determine whether or not a file is in folder
import os

# Our Pronouncing Dictionary file.
OUR_PRONOUNCING_DICTIONARY = 'our_dictionary.txt'

# Constants used when creating window for poem.
FONT = 'Courier'
FONT_SIZE = 14
# Limits on the size of a poem - so can fit poem in a fixed sized window.
MAX_LINES_IN_POEM = 17
MAX_CHAR_IN_POEM_LINE = 70

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

#
# Function(s) that use CSC108 course material only.
#

def read_pronouncing_dictionary(filename: str) -> PronouncingTable:
    """ Precondition: filename is the name of a file in the current directory
                  that contains a pronouncing dictionary represented
                  using the CMU pronouncing dictionary format.

    Return a pronouncing table for the pronouncing dictionary information 
    contained in file filename.

    Docstring example(s) not given since this function depends on file input.
    """

    pronouncing_dictionary_file = open(filename, 'r')
    
    # Skip the header lines in the pronouncing dictionary.
    line = pronouncing_dictionary_file.readline()
    while line.startswith(';;;'):
        line = pronouncing_dictionary_file.readline()
 
    # Read pronouncing information and put in table form
    pronouncing_lines = pronouncing_dictionary_file.readlines()
    pronouncing_table = student.make_pronouncing_table(pronouncing_lines)
    
    return pronouncing_table

#
# Functions below use more advanced python types but should be comprehensible
#

# Docstring examples are not given in the following functions since they
# would depend on using types and methods we have not covered yet.

def annotate_stress(poem_line: Entry, stress_pattern:StringVar,
                    pronouncing_table: PronouncingTable) -> None:
    """Determine the stress patterns for the words in poem_line by using the 
    pronouncing table pronouncing_table and modify stress_pattern accordingly.
    """

    stress_line = ''
    poem_line_str = poem_line.get()
    words = poem_line_str.split()
    index_in_poem_line = 0
    number_of_blanks = 0
    for word in words:
        if len(stress_line) > 0:
            # add number of blanks between words to match poem_line
            number_of_blanks = (poem_line_str.index(word, index_in_poem_line) 
                                - index_in_poem_line)
            stress_line = stress_line + ' ' * number_of_blanks
        stress_line = stress_line + student.get_stress_pattern(word, 
                                                             pronouncing_table)
        index_in_poem_line = index_in_poem_line + len(word) + number_of_blanks

    stress_pattern.set(stress_line)


def set_rhyme_scheme(poem_line_entries: List[Entry],
                     rhyme_scheme_vars: List[StringVar], 
                     pronouncing_table: PronouncingTable) -> None:
    """Determine the rhyme scheme for the poem in poem_line_entries using the
    pronouncing table pronouncing_table and modify rhyme_scheme_vars 
    accordingly.
    """

    # Get the poem from the line entries, skipping blank lines at the end.
    poem_lines =[]
    for line in poem_line_entries:
        poem_lines.append(line.get())
    while len(poem_lines) > 0 and len(poem_lines[-1]) == 0:
        poem_lines.pop()
            
    rhyme_scheme = student.detect_rhyme_scheme(poem_lines, pronouncing_table)

    # Add rhyme scheme 
    for i in range(len(rhyme_scheme)):
        rhyme_scheme_vars[i].set(rhyme_scheme[i])


def annotate_stress_and_rhyme_scheme(stress_patterns: List[StringVar], 
                                     poem_line_entries: List[Entry],
                                     rhyme_scheme_vars: List[StringVar], 
                                     pronouncing_table: 
                                     PronouncingTable) -> None:
    """Determine the stress markers and rhyme scheme for the poem in 
    poem_line_entries using the pronouncing table pronouncing_table and 
    modify stress_patterns and rhyme_scheme_vars accordingly.
    """
 
    # This poem displayed in window could have been read from a file or typed 
    # in by user. Extract the poem, process it and re-display it.

    # Extract poem from poem_line_entries into a single str.
    raw_poem = ''
    for line in poem_line_entries:
        raw_poem = raw_poem + line.get() + '\n'

    # Clear the contents of poem window.
    clear_poem(stress_patterns, poem_line_entries, rhyme_scheme_vars)

    # This is a little counter-intuitive, but write the poem into a file
    tmp_file = open('tmp_poem.txt', 'w')
    tmp_file.write(raw_poem)
    tmp_file.close()

    # Process poem and re-display poem.
    tmp_file = open('tmp_poem.txt', 'r')
    display_poem_in_window(tmp_file, poem_line_entries)
    tmp_file.close()

    # Annotate stress in each poem line.
    for i in range(len(poem_line_entries)):
        annotate_stress(poem_line_entries[i], stress_patterns[i], 
                        pronouncing_table)    

    # Display rhyme scheme.
    set_rhyme_scheme(poem_line_entries, rhyme_scheme_vars, pronouncing_table)


def display_poem_in_window(raw_poem: TextIO, poem_line_entries: 
                           List[Entry]) -> None:
    """Convert raw_poem to a list of lines with appropriate blank lines removed 
    and display in window.  Any poem line with line number greater than 
    MAX_LINES_IN_POEM is removed from the poem.  Any characters in a poem line
    that have index position MAX_CHAR_IN_POEM_LINE or more are removed from 
    the poem.
    """

    poem_lines = student.convert_to_lines(raw_poem)
    
    # Display lines of poem in poem window.
    for i in range(min(len(poem_lines), MAX_LINES_IN_POEM)):
        poem_line = poem_lines[i][:MAX_CHAR_IN_POEM_LINE]
        poem_line_entries[i].insert(0, poem_line)


def clear_poem(stress_patterns: List[StringVar], 
               poem_line_entries: List[Entry], 
               rhyme_scheme_vars: List[StringVar]) -> None:
    """Clear the poem window stress_patterns, poem_line_entries and 
    rhyme_scheme_vars.
    """
    
    for i in range(MAX_LINES_IN_POEM):
        stress_patterns[i].set('')
        rhyme_scheme_vars[i].set('')
        poem_line = poem_line_entries[i].get()
        poem_line_entries[i].delete(0, len(poem_line))


def get_poem_from_file(stress_patterns: List[StringVar], 
                       poem_line_entries: List[Entry],
                       rhyme_scheme_vars: List[StringVar]) -> None: 
    """ Clear stress_patterns, poem_line_entries, and rhyme_scheme_vars, and
    fill poem_line_entries with a new poem that is read from a file.
    """
    
    # Delete all information about displayed poem.
    clear_poem(stress_patterns, poem_line_entries, rhyme_scheme_vars)
   
    # Read new poem as a single str.
    poetry_filename = filedialog.askopenfilename()
    poetry_file = open(poetry_filename, 'r')
    display_poem_in_window(poetry_file, poem_line_entries)
    poetry_file.close()

def add_visuals_for_poem_line(row_num: int,
                              frame: Frame,
                              stress_patterns: List[StringVar],
                              poem_line_entries: List[Entry],
                              rhyme_scheme_vars: List[StringVar]) -> None:
    """Create and add the Label, stress pattern StringVar, poetry line Entry, and
    rhyme scheme StringVar to frame for row row_num, and add each to
    stress_patterns, poem_line_entries, and rhyme_scheme_vars.
    """

    line_label = Label(frame, text="Line {}:".format(1 + row_num // 2))
    line_label.grid(row=row_num + 1, column=0, sticky=E)
    
    stress_pattern = StringVar()
    stress_patterns_label = Label(frame, textvariable=stress_pattern,
                                  font=(FONT, FONT_SIZE, ''))
    stress_patterns.append(stress_pattern)
    stress_patterns_label.grid(row=row_num, column=1, sticky=W, padx=4)
    
    poem_line_entry = Entry(frame, width=MAX_CHAR_IN_POEM_LINE, 
                       font=(FONT, FONT_SIZE, ''))
    poem_line_entry.insert(0, '')
    poem_line_entries.append(poem_line_entry)
    poem_line_entry.grid(row=row_num+1, column=1)
    
    rhyme_scheme_var = StringVar()
    rhyme_scheme_label = Label(frame, width=3, textvariable=rhyme_scheme_var,
        font=(FONT, FONT_SIZE, ''))
    rhyme_scheme_vars.append(rhyme_scheme_var)
    rhyme_scheme_label.grid(row=row_num+1, column=2, sticky=W, padx=4)


def annotate_poem_in_window(pronouncing_table: PronouncingTable, 
                            frame: Frame) -> None:
    """Create and display the poetry window.  Handle button click operations.

    This function does not return until the poetry window is closed.
    
    Each line of poetry in the window has:
      - a Label "Line line_num": in even rows r, column 0
      - a stress annotations Label beside it in column 1
      - a text Entry in row r + 1, column 1 underneath the stress.
      - a rhyme scheme Label in row r + 1, column 2, after the text Entry.

    Buttons appear in column 2.
    """

    # Lists for data to be displayed in poem window.
    stress_patterns = []
    poem_line_entries = []
    rhyme_scheme_vars = []
    
    # Make room in window for MAX_LINES_IN_POEM lines of poetry.
    for i in range(MAX_LINES_IN_POEM):
        add_visuals_for_poem_line(i * 2, frame, stress_patterns,
                                  poem_line_entries, rhyme_scheme_vars)

    # Add the "Open Poem" Button to the right of the poem.
    annotate_btn = Button(
        frame,
        text="Open Poem",
        command=lambda: (
            get_poem_from_file(stress_patterns, poem_line_entries, 
                               rhyme_scheme_vars))
    )
    annotate_btn.grid(row=1, column=3)

    # Add the "Annotate Poem" Button to the right of poem.
    annotate_btn = Button(
        frame,
        text="Annotate Poem",
        command=lambda: (
            annotate_stress_and_rhyme_scheme(
                stress_patterns, poem_line_entries,
                rhyme_scheme_vars, pronouncing_table))
    )
    annotate_btn.grid(row=2, column=3)
    
    # Add the "Clear Poem" Button to the right of poem.
    annotate_btn = Button(
        frame,
        text="Clear Poem",
        command=lambda: (
            clear_poem(stress_patterns, poem_line_entries, rhyme_scheme_vars))
    )
    annotate_btn.grid(row=3, column=3)    
    
    
if __name__ == '__main__':
    
    if os.path.exists(OUR_PRONOUNCING_DICTIONARY):

        pronouncing_table = read_pronouncing_dictionary(
                                OUR_PRONOUNCING_DICTIONARY)

        # Create the poem window.  This has to be the first UI element created.
        window = Tk()
        window.title('CSC108 Poem Annotator ' +
                     '- close this window to return to python shell')
        frame = Frame(window)
        frame.pack()

        # Annotate poems until user closes the poem window.
        annotate_poem_in_window(pronouncing_table, frame)
        
        window.lift()
        window.call('wm', 'attributes', '.', '-topmost', True)
        window.after_idle(window.call, 'wm', 'attributes', '.', '-topmost',
                          False)
        window.mainloop()
    else:
        print('The Pronouncing Dictionary was not found.')
        print('Copy the file ' + OUR_PRONOUNCING_DICTIONARY +
              ' into the same folder as your A2 python files and try again.')
