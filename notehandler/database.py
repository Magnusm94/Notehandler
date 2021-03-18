#!/usr/bin/env python

import sys, os
import psycopg2
import pandas as pd
import json


login = json.load(open(os.path.dirname(__file__) + '/login.json', 'r'))


class Database:

    def __init__(self):
        self.conn = psycopg2.connect(**login)

    def column_names(self, tablename):
        return [i[0] for i in self(f"select column_name from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '{tablename}';")]

    def __call__(self, query):
        cur = self.conn.cursor()
        try:
            cur.execute(query)
        except psycopg2.errors.UniqueViolation:
            sys.exit("Duplicate not allowed.")
        response = cur.fetchall() if 'select' in query.lower() else None
        cur.close()
        self.conn.commit()
        return response

    def list_tables(self):
        schemas = [i[0] for i in self(
            "SELECT schema_name FROM information_schema.schemata;") 
            if not i[0] in ['pg_toast', 'pg_catalog', 'information_schema']]

        tables = []
        for s in schemas:
            tables.extend([f'{s}.{i[0]}' for i in self(
                f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{s}';")])
        print("\n".join(tables))
        return True


if __name__ == "__main__":
    query = " ".join([arg for arg in sys.argv[1:]])
    pg = Database()
    result = pg(query)
    if result:
        df = pd.DataFrame(result)
