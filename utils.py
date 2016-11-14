"""
Common utils for common tasks
"""
import re
import string
from itertools import ifilter, izip, izip_longest

import xlrd

CELL_RE = re.compile(r'^([A-Z]+)(\d+)$')

def xlscoords(cell):
    "Turn B6 in (5, 1)"
    column, row = CELL_RE.match(cell).groups()
    column = letter_to_column(column)
    row = int(row) - 1 # because zero-index
    return row, column

# alias
c = xlscoords

def letter_to_column(letters):
    """
    Return number corresponding to excel-style column.

    Turn A into 0 and AA into 26
    """
    number = -1
    for position, letter in enumerate(reversed(letters)):        
        number += (ord(letter) - ord('A') + 1) * (26 ** position)
    return number


def extract_matrix(filename, sheet_name, bounds, nulls=frozenset()):
    "Pull a matrix of values from an xlsx file"
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_name(sheet_name)

    for r in xrange(bounds[0][0], bounds[1][0]):
        row = sheet.row_slice(r, bounds[0][1], bounds[1][1])
        row = map(get_value, row, nulls=nulls)
        yield row


def get_value(cell, nulls=frozenset()):
    "Get a DB safe value from a cell"
    if not hasattr(cell, 'value'):
        return cell

    value = cell.value
    if value in nulls:
        value = None
    return value


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

