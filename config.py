"""
Shared config
"""
import os

# add DATABASE_NAME and TABLE_NAME below
DATA_DIR = os.path.realpath('./data')
DATABASE_NAME = ""
DATABASE_URL = "postgres://localhost/" + DATABASE_NAME

TABLE_NAME = "ages"

# add values that will become None
NULLS = set()
