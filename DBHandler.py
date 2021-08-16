import sqlite3



class NotFoundError(Exception):
    def __init__(self, item_name):
        super().__init__()
        self.item_name = item_name




class DBHandler:
    def __init__(self, account: str = 'account_1'):
        # account should either be 'account_1' or 'account_2
        self.conn = sqlite3.connect('forge.db')
        self.db = self.conn.cursor()
        self.account = account
        # self.create_tables()
        # self.populate_tables()

    def create_tables(self):
        self.db.execute('CREATE TABLE IF NOT EXISTS item_types (id INTEGER, name TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS difficulties (id INTEGER, name TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER, name TEXT, item_type_id INTEGER, quantity_1 INTEGER, quantity_2 INTEGER)')
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



    def get_item_id(self, name: str) -> int:
        # case sensitive!
        result = self.db.execute(f'SELECT id FROM items WHERE name={name}').fetchone()
        if not result:
            raise NotFoundError(name)
        return result[0]



    def update_quantity(self, id_or_name: int or str, qty: int):
        if isinstance(id_or_name, int):
            self.db.execute(f'UPDATE items SET quantity_{self.account}={qty} WHERE id={id_or_name}')
        elif isinstance(id_or_name, str):
            self.db.execute(f'UPDATE items SET quantity_{self.account}={qty} WHERE name="{id_or_name}"')
        self.conn.commit()