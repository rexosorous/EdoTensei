# dependencies
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QTreeWidgetItem, QTableWidgetItem
import qasync

# local modules
import gui.recipe_window



class ListItem(QListWidgetItem):
    '''
    Basically just a QListWidgetItem that can hold custom data

    Args:
        item_id (int): the item id that this QListWidgetItem represents

    Attributes:
        item_id (int): see above
    '''
    def __init__(self, item_name: str, item_id: int):
        super().__init__(item_name)
        self.id_ = item_id



class RecipeWindow(QMainWindow, gui.recipe_window.Ui_MainWindow):
    '''
    Handles the GUI and logic for the recipe window
    Only pops up/opens when the user right clicks in the item helper and clicks "Add Recipes"

    Args:
        db (DBHandler)
        sigs (Signals)

    Attributes:
        db (DBHandler)
        sigs (Signals)
    '''
    def __init__(self, db, sigs):
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.sigs = sigs
        self.connect_events()



    def connect_events(self):
        self.lw_checkbox.stateChanged.connect(self.search)
        self.bl_checkbox.stateChanged.connect(self.search)
        self.equipment_checkbox.stateChanged.connect(self.search)
        self.materials_checkbox.stateChanged.connect(self.search)
        self.crafted_checkbox.stateChanged.connect(self.search)
        self.dropped_checkbox.stateChanged.connect(self.search)
        self.searchbar.textChanged.connect(self.search)
        self.searchbar.returnPressed.connect(self.select_top)
        self.items_list.itemClicked.connect(self.populate_item_data)
        self.add_button.clicked.connect(self.add_to_item_helper)



    @qasync.asyncSlot()
    async def open(self):
        await self.populate_items() # make sure to fill the window with stuff before showing it to the user
        self.show()



    @qasync.asyncSlot()
    async def populate_items(self):
        '''
        Populates self.items_list with every item in the game (not including ninjas used for crafting)
        '''
        all_items = self.db.get_all_items()
        for item in all_items:
            self.items_list.addItem(ListItem(item[1], item[0]))



    @qasync.asyncSlot()
    async def search(self):
        '''
        Populates self.items_list depending on the search parameters
        Called whenever any of the checkboxes are clicked or when the user types in the searchbox
        Works by building a sqlite3 query based on the search parameters
        '''
        self.items_list.clear()

        # build a db query
        search_term = self.searchbar.text()

        item_types = []
        if self.materials_checkbox.checkState() == Qt.Checked:
            item_types.append('0')
        if self.equipment_checkbox.checkState() == Qt.Checked:
            item_types.append('1')
        if self.bl_checkbox.checkState() == Qt.Checked:
            item_types.append('2')
        if self.lw_checkbox.checkState() == Qt.Checked:
            item_types.append('4')

        obtained = []
        if self.crafted_checkbox.checkState() == Qt.Checked:
            obtained.append('EXISTS (SELECT 1 FROM drops WHERE id=item_id)')
        if self.dropped_checkbox.checkState() == Qt.Checked:
            obtained.append('EXISTS (SELECT 1 FROM recipes WHERE id=product_id)')

        base_query = 'SELECT DISTINCT id, name FROM items WHERE'
        search_query = f'name LIKE "%{search_term}%"'
        item_query = f'item_type_id IN ({", ".join(item_types)})'
        obtained_query = f'{" OR ".join(obtained)}'
        if not obtained_query:
            obtained_query = '0'
        else:
            obtained_query = f'({obtained_query})'

        built_query = f'{base_query} {" AND ".join([search_query, item_query, obtained_query])} ORDER BY item_type_id DESC'
        items = self.db.query(built_query)

        for item in items:
            self.items_list.addItem(ListItem(item[1], item[0]))



    @qasync.asyncSlot()
    async def select_top(self):
        '''
        When the user hits Enter on their keyboard in the searchbox, select the top-most item
        '''
        self.items_list.setCurrentRow(0)
        await self.populate_item_data(self.items_list.item(0))



    @qasync.asyncSlot(QListWidgetItem)
    async def populate_item_data(self, selected_list_item: ListItem):
        '''
        Populates both self.recipe_tree and self.location_table when an item is selected from self.items_list

        Args:
            selected_list_item (ListItem)
        '''
        selected_item_id = selected_list_item.id_
        selected_item_name = selected_list_item.text()
        recipe_item_ids = await self.show_recipe(selected_item_id, selected_item_name)
        await self.show_drops(recipe_item_ids)



    @qasync.asyncSlot(int, str)
    async def show_recipe(self, item_id: int, item_name: str) -> set[int]:
        '''
        Populates self.recipe_tree

        Note:
            this is a pretty sloppy implementation
            this only has a return variable because i couldn't figure out a more elegant way
            of finding all the unique item ids in this recipoe

        Note:
            tree columns:
                0. item name
                1. qty required by recipe
                2. qty owned
                3. qty needed to obtain

        Args:
            item_id (int)
            item_name (str)

        Returns:
            set[int]: all the unique item ids in this recipe
        '''
        self.recipe_tree.clear()
        product_owned_qty = self.db.get_owned_qty(item_id)
        product_needed_qty = '0' if product_owned_qty else '1' 
        product_widget = QTreeWidgetItem([item_name, '1', str(product_owned_qty), product_needed_qty])
        all_item_ids = await self.build_recipe(product_widget, item_id)
        all_item_ids.add(item_id)
        self.recipe_tree.addTopLevelItem(product_widget)
        self.recipe_tree.expandAll()
        return all_item_ids



    @qasync.asyncSlot(object, int)
    async def build_recipe(self, parent_widget: QTreeWidgetItem, parent_item_id: int) -> set[int]:
        '''
        A recursive function that builds a product item's full recipe
        and also keeps a set of all the unique item ids in the recipe

        Args:
            parent_widget (QTreeWidgetItem)
            parent_item_id (int)

        Returns:
            set[int]: all the unique item ids generated by this recipe
        '''
        data = self.db.get_item_recipe(parent_item_id) # should return id, name, qty needed to craft, qty owned
        if not data:
            return set()
        children_ids = set()
        for ingredient in data:
            parent_needed_qty = int(parent_widget.text(3))
            craft_qty = ingredient[2]
            owned_qty = ingredient[3]
            needed_qty = (parent_needed_qty * craft_qty) - owned_qty
            if needed_qty < 0:
                needed_qty = 0

            child = QTreeWidgetItem(parent_widget, [str(x) for x in ingredient[1:]])
            child.setText(3, str(needed_qty))
            children_ids.add(ingredient[0])
            children_ids.update(await self.build_recipe(child, ingredient[0]))
        return children_ids



    @qasync.asyncSlot(list)
    async def show_drops(self, item_ids: set[int]):
        '''
        Populates self.location_table with the location data of each item in the selected recipe
        
        Args:
            item_ids (set[int]): all the items to provide location data for. because this is a set,
                                 there will not be any duplicate entries
        '''
        # clears the table because self.location_table.clear() is not a thing
        while self.location_table.rowCount():
            self.location_table.removeRow(0)

        for item_id in item_ids:
            for data in self.db.get_item_drops_by_id(item_id):
                last_row = self.location_table.rowCount()
                self.location_table.insertRow(last_row)
                fixed_location = data[3][data[3].find('area/')+5:] if 'area' in data[3] else data[3]
                self.location_table.setItem(last_row, 0, QTableWidgetItem(data[0]))
                self.location_table.setItem(last_row, 1, QTableWidgetItem(f'{data[1]}%'))
                self.location_table.setItem(last_row, 2, QTableWidgetItem(data[2]))
                self.location_table.setItem(last_row, 3, QTableWidgetItem(fixed_location))



    @qasync.asyncSlot()
    async def add_to_item_helper(self):
        '''
        Takes the currently selected item and its recipe and places it in the MainWindow's item helper
        Called when the user clicks the "Add" button
        '''
        self.sigs.add_to_item_helper.emit(self.recipe_tree.topLevelItem(0).text(0))