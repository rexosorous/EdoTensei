import sqlite3

class DBHandler:
    def __init__(self):
        self.conn = sqlite3.connect('forge.db')
        self.db = self.conn.cursor()
        # self.create_tables()
        # self.populate_tables()

    def create_tables(self):
        self.db.execute('CREATE TABLE IF NOT EXISTS item_types (id INTEGER, name TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS difficulties (id INTEGER, name TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER, name TEXT, item_type_id INTEGER, quantity INTEGER)')
        self.db.execute('CREATE TABLE IF NOT EXISTS drops (item_id INTEGER, location_url TEXT, droprate REAL, difficulty_id INTEGER)')
        self.db.execute('CREATE TABLE IF NOT EXISTS recipes (product_id INTEGER, ingredient_id INTEGER, quantity INTEGER)')
        self.conn.commit()

    def populate_tables(self):
        self.db.execute('INSERT INTO item_types VALUES (0, "material")')
        self.db.execute('INSERT INTO item_types VALUES (1, "equipment")')
        self.db.execute('INSERT INTO item_types VALUES (2, "bloodline")')
        self.db.execute('INSERT INTO item_types VALUES (3, "ninja")')
        self.db.execute('INSERT INTO item_types VALUES (4, "legendary weapon")')

        self.db.execute('INSERT INTO difficulties VALUES (0, "beginner")')
        self.db.execute('INSERT INTO difficulties VALUES (1, "easy")')
        self.db.execute('INSERT INTO difficulties VALUES (2, "medium")')
        self.db.execute('INSERT INTO difficulties VALUES (3, "hard")')
        self.db.execute('INSERT INTO difficulties VALUES (4, "extreme")')
        self.db.execute('INSERT INTO difficulties VALUES (5, "impossible")')
        self.db.execute('INSERT INTO difficulties VALUES (6, "forbidden")')

        self.conn.commit()
