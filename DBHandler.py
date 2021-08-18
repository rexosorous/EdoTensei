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
        result = self.db.execute(f'SELECT id FROM items WHERE name="{name}"').fetchone()
        if not result:
            raise NotFoundError(name)
        return result[0]

    def get_item_name(self, id_: int) -> str:
        result = self.db.execute(f'SELECT name FROM items WHERE id={id_}').fetchone()
        if not result:
            raise NotFoundError(str(id_))
        return result[0]



    def update_quantity(self, id_or_name: int or str, qty: int):
        if isinstance(id_or_name, int):
            self.db.execute(f'UPDATE items SET quantity_{self.account}={qty} WHERE id={id_or_name}')
        elif isinstance(id_or_name, str):
            self.db.execute(f'UPDATE items SET quantity_{self.account}={qty} WHERE name="{id_or_name}"')
        self.conn.commit()


    def get_owned_qty(self, item_id) -> int:
        return self.db.execute(f'SELECT quantity_{self.account} FROM items WHERE id={item_id}').fetchone()[0]

    def get_all_items(self) -> list[set[int, str]]:
        return self.db.execute(f'SELECT id, name FROM items ORDER BY item_type_id DESC').fetchall()

    def get_craftable_items(self) -> list[set[int, str]]:
        return self.db.execute(f'SELECT DISTINCT id, name FROM recipes INNER JOIN items ON product_id=id ORDER BY item_type_id DESC').fetchall()

    def get_item_recipe(self, item_id) -> list[set[int, str, int, int]]:
        return self.db.execute(f'SELECT id, name, quantity, quantity_{self.account} FROM recipes INNER JOIN items ON ingredient_id=id WHERE product_id={item_id}').fetchall()

    def get_item_drops_by_id(self, item_id) -> list[set[str, str, float, str]]:
        return self.db.execute(f'SELECT items.name, droprate, difficulties.name, location_url FROM drops INNER JOIN items ON item_id=items.id INNER JOIN difficulties ON difficulty_id=difficulties.id WHERE item_id={item_id}').fetchall()

    def get_item_drops_by_name(self, item_id) -> list[set[str, str, float, str]]:
        return self.db.execute(f'SELECT items.name, droprate, difficulties.name, location_url FROM drops INNER JOIN items ON item_id=items.id INNER JOIN difficulties ON difficulty_id=difficulties.id WHERE items.name="{item_id}"').fetchall()

    def query(self, query_str) -> list[set]:
        return self.db.execute(query_str).fetchall()