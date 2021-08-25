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
    '''
    def __init__(self, Qt):
        self.Qt = Qt

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
        product_needed_qty = '0' if product_owned_qty else '1' 
        product_widget = TreeItem(None, [item_name, '1', str(product_owned_qty), product_needed_qty], item_id)
        self.build_recipe(product_widget, db)
        self.Qt.addTopLevelItem(product_widget)
        self.Qt.expandAll()



    def build_recipe(self, parent_widget: QTreeWidgetItem, db):
        '''
        Recursively builds the full recipe for a product item
        This works by finding the immediate children/ingredients for an item,
        then for each of those, find the immediate children and so on and so forth
        until all recipe ingredients have been found.
        
        Args:
            parent_widget (TreeItem)
            db (DBHandler)
        '''
        data = db.get_item_recipe(parent_widget.id_)
        if not data:
            return
        
        for ingredient in data:
            parent_needed_qty = int(parent_widget.text(3))
            craft_qty = ingredient[2]
            owned_qty = ingredient[3]
            needed_qty = (parent_needed_qty * craft_qty) - owned_qty
            if needed_qty < 0:
                needed_qty = 0

            child = TreeItem(parent_widget, [str(x) for x in ingredient[1:]], ingredient[0])
            child.setText(3, str(needed_qty))
            self.build_recipe(child, db)



    def update_quantities(self, db, current_widgets: list[QTreeWidgetItem] = None):
        '''
        Recursively updates the quantities of items owned in the item helper tree. This makes sure the number stays accurate as items are gained (or lost) during runtime
        Usually called when scraping forge.
        '''
        if not current_widgets:
            current_widgets = [self.Qt.topLevelItem(index) for index in range(self.Qt.topLevelItemCount())]

        for parent in current_widgets:
            qty = db.get_owned_qty(parent.id_)
            parent.setText(2, str(qty))
            children = [parent.child(index) for index in range(parent.childCount())]
            if not children:
                continue
            self.update_quantities(db, children)



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



    def get_item_ids(self, current_widgets: list[QTreeWidgetItem] = None) -> set[int]:
        '''
        Recursively iterates through all the items in this tree and compiles a set of every item id 

        Args:
            current_widgets (list[TreeItem], optional): if not provided

        Returns:
            set[int]
        '''
        if not current_widgets:
            current_widgets = [self.Qt.topLevelItem(index) for index in range(self.Qt.topLevelItemCount())]
        item_ids = set([x.id_ for x in current_widgets])

        for parent in current_widgets:
            children = [parent.child(index) for index in range(parent.childCount())]
            if not children:
                continue
            item_ids.update(self.get_item_ids(children))
        return item_ids



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

    Args:
        item_id (int): the item id that this represents

    Attributes:
        item_id (int): see above
    '''
    def __init__(self, parent: QTreeWidgetItem, display_values: list[str], item_id: int):
        super().__init__(parent, display_values)
        self.id_ = item_id





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