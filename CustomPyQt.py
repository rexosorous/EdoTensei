from PyQt5.QtWidgets import QTreeWidgetItem, QListWidgetItem, QTableWidgetItem, QAction
from PyQt5 import QtCore



'''
A bunch of classes used to add extra/custom functionality to PyQt stuff
'''


def populate_drop_table(table, db, item_ids: set[int]):
    '''
    Populates a QTableWidget with drop information about a list of items

    Note:
        This is only here because this code appears in both app.py and RecipeWindow.py,
        so I wanted to abstract it away and this just seemed like the most appropriate place to put it

    Args:
        table (QTableWidget)
        db (DBHandler)
        item_ids (set[int])
    '''
    # clear the table first
    while table.rowCount():
        table.removeRow(0)

    for item_id in item_ids:
        for data in db.get_item_drops_by_id(item_id):
            last_row = table.rowCount()
            table.insertRow(last_row)
            fixed_location = data[3][data[3].find('area/')+5:] if 'area' in data[3] else data[3]
            table.setItem(last_row, 0, QTableWidgetItem(data[0]))
            table.setItem(last_row, 1, QTableWidgetItem(f'{data[1]}%'))
            table.setItem(last_row, 2, QTableWidgetItem(data[2]))
            table.setItem(last_row, 3, QTableWidgetItem(fixed_location))





class Tree:
    '''
    Basically a custom QTreeWidget without being one.

    Note:
        We can't inherit from QTreeWidget and replace the existing QTreeWidget created by QtDesigner
        as that would lose a lot of the settings and attributes and stuff set up by QtDesigner.
        So instead, we pass an instance of that QTreeWidget created by QtDesigner and hold onto it as
        a class attribute and we can interact with it directly.

    Args:
        Qt (QTreeWidget)

    Attributes:
        Qt (QTreeWidget)
        map (dict): A map to all of the TreeItems by item ID
            {
                item_id (int): list[TreeItem]
            }
    '''
    def __init__(self, Qt):
        self.Qt = Qt
        self.map = dict()



    def create_context_menu(self):
        '''
        Creates the right-click context menu for the MainFrame
        '''
        self.Qt.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.open_action = QAction("Add Recipes", self.Qt)
        self.remove_action = QAction("Remove This Recipe", self.Qt)
        self.Qt.addAction(self.open_action)
        self.Qt.addAction(self.remove_action)



    def add_product(self, item_id: int, db):
        '''
        Adds a product item as a top level item in the tree and then adds the ingredients in the recipe that makes the product if there is one

        Args:
            item_id (int)
            db (DBHandler)
        '''
        item_name = db.get_item_name(item_id)
        product_owned_qty = db.get_owned_qty(item_id)
        product_need_qty = 0 if product_owned_qty else 1
        product_widget = TreeItem(None, item_id, item_name, 1, product_owned_qty, product_need_qty)

        if item_id not in self.map:
            self.map[item_id] = list()
        self.map[item_id].append(product_widget)

        self.build_recipe(db, product_widget)
        self.Qt.addTopLevelItem(product_widget)
        self.Qt.expandAll()
        for index in range(self.Qt.columnCount()):
            self.Qt.resizeColumnToContents(index)



    def build_recipe(self, db, parent_widget: QTreeWidgetItem):
        '''
        Recursively builds the full recipe for a product item
        This works by finding the immediate children/ingredients for an item,
        then for each of those, find the immediate children and so on and so forth
        until all recipe ingredients have been found.

        Note:
            The need quantity set here is only the amount needed for THIS recipe.
            Take this example:
                legendary weapon    1   0   1
                    alkahest        5   0   5
                bloodline           1   0   1
                    alkahest        10  0   10
            The need quantity for each alkahest is correct for that recipe, but taking all the cipes into account,
            the need qty should be 15.
            After all recipes are added, self.fix_need_qty() should be called to fix this issue.

        Args:
            db (DBHandler)
            parent_widget (TreeItem)
        '''
        recipe = db.get_item_recipe(parent_widget.id_)
        if not recipe:
            # this means that there's no children for this recipe (it's a base item)
            return

        for ingredient_data in recipe:
            child = TreeItem(parent_widget, *ingredient_data, ingredient_data[2] * parent_widget.need_qty - ingredient_data[3])
            child.set_need_qty((child.recipe_qty * parent_widget.need_qty) - child.owned_qty)
            if child.id_ not in self.map:
                self.map[child.id_] = list()
            self.map[child.id_].append(child)
            self.build_recipe(db, child)



    def update_quantities(self, db):
        '''
        Recursively updates the quantities of items owned and items needed in the item helper tree. This makes sure the numbers
        stay accurate as items are gained (or lost) during runtime.

        Args:
            db (DBHandler)
            widgets (list[TreeItem])
        '''
        def recursive(db, parent):
            children = [parent.child(index) for index in range(parent.childCount())]
            for child in children:
                owned_qty = db.get_owned_qty(child.id_)
                need_qty = (child.recipe_qty * parent.need_qty) - owned_qty
                child.set_owned_qty(owned_qty)
                child.set_need_qty(need_qty)
                recursive(db, child)

        roots = [self.Qt.topLevelItem(index) for index in range(self.Qt.topLevelItemCount())]
        for product in roots:
            owned_qty = db.get_owned_qty(product.id_)
            if owned_qty:
                product.set_owned_qty(owned_qty)
                product.set_need_qty(0)
            recursive(db, product)



    def remove_recipe(self, selected_widget: QTreeWidgetItem = None):
        '''
        Removes a product and its recipe.
        Able to do so even if the selected widget is an ingredient and not a product

        Args:
            selected_widget (TreeItem, optional): if not provided, defaults to the currently selected item
        '''
        if not selected_widget:
            selected_widget = self.Qt.currentItem()

        # gets the top level item (the product item widget)
        while selected_widget.parent():
            selected_widget = selected_widget.parent()
        selected_index = self.Qt.indexOfTopLevelItem(selected_widget)
        self.Qt.takeTopLevelItem(selected_index)



    def get_product_ids(self) -> list[int]:
        '''
        Only returns the product ids and not any ingredient ids

        Returns:
            list[int]
        '''
        return [self.Qt.topLevelItem(index).id_ for index in range(self.Qt.topLevelItemCount())]



    def clear(self):
        self.Qt.clear()





class TreeItem(QTreeWidgetItem):
    '''
    Basically just a QTreeWidgetItem that can hold custom data

    Columns:
        0: name
        1: recipe qty
        2: owned qty
        3: need qty

    Args:
        item_id (int)
        name (str)
        recipe_qty (int)
        owned_qty (int)
        need_qty (int, optional)

    Attributes:
        item_id (int): see above
    '''
    def __init__(self, parent: QTreeWidgetItem, item_id: int, name: str, recipe_qty: int, owned_qty: int, need_qty: int = 0):
        super().__init__(parent, [name, str(recipe_qty), str(owned_qty), str(need_qty)])
        self.id_ = item_id
        self.name = name
        self.recipe_qty = recipe_qty
        self.owned_qty = owned_qty
        self.need_qty = need_qty
        if self.need_qty < 0:
            self.need_qty = 0

    def set_owned_qty(self, qty: int):
        self.owned_qty = qty
        self.setText(2, str(qty))

    def set_need_qty(self, qty: int):
        self.need_qty = qty
        if self.need_qty < 0:
            self.need_qty = 0
        self.setText(3, str(self.need_qty))





class ListItem(QListWidgetItem):
    '''
    Basically just a QListWidgetItem that can hold custom data

    Args:
        item_id (int): the item id that this represents

    Attributes:
        item_id (int): see above
    '''
    def __init__(self, item_name: str, item_id: int):
        super().__init__(item_name)
        self.id_ = item_id