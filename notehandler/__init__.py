import sys
import os
sys.path.append(os.path.dirname(__file__))
import queries
from database import Database


class Main:
    pg = Database()
    
    def __init__(self, args):
        global arg
        arg = args
        if not self.showtables():
            self.send_query()

    def send_query(self):
        queries.main(arg[1:])
        return True

    def showtables(self):
        if arg[1] in ['tables', 'table', '.table', '.tables']:
            self.pg.list_tables()
            return True
