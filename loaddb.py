#!/usr/bin/env python
"""
This file is responsible for loading data. Describe data below.

FILES should be a list of dictionaries with at least the following keys:

{
    'filename': 'path/to/file.xls',
    'sheet': 'sheet_name',
    'bounds': ((0, 0), (10, 10))
}

"""
# prune these imports if unnecessary
from collections import OrderedDict

import dataset
from sqlalchemy import types

from config import DATABASE_URL, TABLE_NAME, NULLS
from utils import extract_matrix, grouper

# the actual files to load
FILES = []

# force types using sqlalchemy.types
TYPES = {}

def main(reset=True):
    """
    Get a database and table
    Generate rows
    Insert chunks
    """
    db = dataset.connect(DATABASE_URL)
    if reset:
        db[TABLE_NAME].drop()

    table = db[TABLE_NAME]
    rows = generate_rows(*FILES)

    for group in grouper(rows, 1000, None):
        group = ifilter(bool, group)
        table.insert_many(group, types=TYPES)


def generate_rows(*files):
    """
    Loop through files
    Extract matrix
    Match cells to bride and groom ages
    Add state and year
    yield row
    """
    for f in files:

        print('Loading {filename}: {sheet}'.format(**f))

        matrix = extract_matrix(f['filename'], f['sheet'], f['bounds'], nulls=NULLS)

        # process and yield out data
        for row in matrix:
            yield row


if __name__ == '__main__':
    main()