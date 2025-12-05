import sqlite3
from backend.api.db_interactions.queries import Queries

class DeleteData:
    def __init__(self):
        self.conn = sqlite3.connect("data.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")