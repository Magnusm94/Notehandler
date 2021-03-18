#!/usr/bin/env python

import sys, os
import psycopg2
sys.path.append(os.path.dirname(__file__))
from database import Database
import pandas as pd


def new():
    pg(f"""
    INSERT INTO {table} (note)
    VALUES ('{string}');
    """)
    return True


def search():
    df = pd.DataFrame(pg(f"SELECT * FROM {table} ORDER BY noteID;"))
    if len(df.columns):
        df.columns = ['noteID', 'note', 'timestamp']
        print(df[df['note'].str.contains(string)].to_string(index=False))
        return True
    return None


def delete(noteID):
    pg(f"""
    DELETE FROM {table} WHERE noteID = {noteID};
    """)
    return True


def update(noteID, string):
    pg(f"""
    UPDATE {table} 
    SET note = '{string}'
    WHERE noteID = {noteID};
    """)
    return True


def new_subject():
    try:
        pg(f"""
        CREATE TABLE {table} (noteID SERIAL, note TEXT UNIQUE NOT NULL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(3));
        """)
        return True
    except psycopg2.errors.DuplicateTable:
        print('Table already exists.')
        return False
    except psycopg2.errors.InvalidSchemaName:
        pg.__init__()
        schema = table.split('.')[0]
        pg(f"""
        CREATE SCHEMA {schema};
        """)
        print(f'Created new schema {schema}')
        new_subject()


def main(args):
    try:
        global table, string, pg
        table = ".".join(args[:2])
        parameter = args[2]
    except:
        sys.exit('Missing arguments')

    string = " ".join(args[3:])
    pg = Database()

    if parameter in ['create', '--create', '-c']:
        if new_subject():
            return True

    elif parameter in ['-n', '--new', 'new']:
        if new():
            return True

    elif parameter in ['-s', '--search', 'search']:
        if search():
            return True

    elif parameter in ['delete', '-d', '--delete']:
        for i in args[3:]:
            delete(i)
        return True

    elif parameter in ['update', '-u', '--update']:
        update(args[3], " ".join(args[4:]))
        return True

    else:
        sys.exit('Invalid arguments.')
