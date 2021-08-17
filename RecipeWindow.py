from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QTreeWidgetItem
import qasync

import gui.recipe_window


class ListItem(QListWidgetItem):
    def __init__(self, item_name: str, item_id: int):
        super().__init__(item_name)
        self.id_ = item_id


class RecipeWindow(QMainWindow, gui.recipe_window.Ui_MainWindow):
    def __init__(self, db, sigs):
        # big note. changes here don't have to be 'updated' for it to reflect in the gui
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.sigs = sigs
        self.connect_events()

    def connect_events(self):
        self.items_list.itemClicked.connect(self.show_recipe)

    @qasync.asyncSlot()
    async def open(self):
        await self.populate_items()
        self.show()

    @qasync.asyncSlot()
    async def populate_items(self):
        craftables = self.db.get_craftable_items()
        for item in craftables:
            self.items_list.addItem(ListItem(item[1], item[0]))

    def show_recipe(self, selected_list_item):
        # for some reason this breaks when you try to make this async
        self.recipe_tree.clear()
        selected_item_id = selected_list_item.id_
        selected_item_name = selected_list_item.text()
        # QTreeWidgetItems need to be passed an array of strings which print out the text for each column
        # should be like [item name, quantity needed, quantity owned]
        # you can omit fields if you'd like

        # top = QTreeWidgetItem(['test'])
        # child = QTreeWidgetItem(top, ['test child', '420', '69'])
        # self.recipe_tree.addTopLevelItem(top)
        # self.recipe_tree.expandAll()

        product = QTreeWidgetItem([selected_item_name])
        self.build_recipe(product, selected_item_id)
        self.recipe_tree.addTopLevelItem(product)
        self.recipe_tree.expandAll()


    def build_recipe(self, parent_widget, parent_item_id):
        data = self.db.get_item_recipe(parent_item_id) # should return id, name, qty needed, qty owned
        if not data:
            return
        for ingredient in data:
            child = QTreeWidgetItem(parent_widget, [str(x) for x in ingredient[1:]])
            self.build_recipe(child, ingredient[0])