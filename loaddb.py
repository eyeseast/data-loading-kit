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
import os
import glob
from collections import OrderedDict

import dataset
import xlrd
from sqlalchemy import types

from utils import extract_matrix, grouper

# add DATABASE_NAME and TABLE_NAME below
DATA_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), 'data'))
DATABASE_NAME = ""
DATABASE_URL = "postgres://localhost/" + DATABASE_NAME

TABLE_NAME = "ages"

# add values that will become None
NULLS = set()

# the actual files to load
FILES = []

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
        table.insert_many(group)


def generate_rows(*files):
    """
    Loop through files
    Extract matrix
    Match cells to bride and groom ages
    Add state and year
    yield row
    """
    for f in FILES:

        print('Loading {filename}: {sheet}'.format(**f))

        matrix = extract_matrix(f['filename'], f['sheet'], f['bounds'], nulls=NULLS)

        # process and yield out data
        for row in matrix:
            yield row


if __name__ == '__main__':
    main()