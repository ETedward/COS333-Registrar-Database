# -----------------------------------------------------------------------
# database.py
# Author: Bob Dondero
# -----------------------------------------------------------------------

from sqlite3 import connect
from sys import stderr
from os import path
import regserver
# -----------------------------------------------------------------------

class Database:

    def __init__(self):
        self._connection = None

    def connect(self):
        DATABASE_NAME = 'reg.sqlite'
        if not path.isfile(DATABASE_NAME):
            raise Exception('Database connection failed')
        self._connection = connect(DATABASE_NAME)

    def disconnect(self):
        self._connection.close()

    def search(a,b,c,d):
        return managedb(a,b,c,d)