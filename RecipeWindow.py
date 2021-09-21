# dependencies
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QTreeWidgetItem, QTableWidgetItem
import qasync

# local modules
import gui.recipe_window
import CustomPyQt



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
        self.recipe_tree = CustomPyQt.Tree(self.recipe_tree)
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
            self.items_list.addItem(CustomPyQt.ListItem(item[1], item[0]))



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
            self.items_list.addItem(CustomPyQt.ListItem(item[1], item[0]))



    @qasync.asyncSlot()
    async def select_top(self):
        '''
        When the user hits Enter on their keyboard in the searchbox, select the top-most item
        '''
        self.items_list.setCurrentRow(0)
        await self.populate_item_data(self.items_list.item(0))



    @qasync.asyncSlot(QListWidgetItem)
    async def populate_item_data(self, selected_list_item: CustomPyQt.ListItem):
        '''
        Populates both self.recipe_tree and self.location_table when an item is selected from self.items_list

        Args:
            selected_list_item (ListItem)
        '''
        selected_item_id = selected_list_item.id_
        self.recipe_tree.clear()
        self.recipe_tree.add_product(selected_item_id, self.db)
        self.show_drops(self.recipe_tree.get_item_ids())



    @qasync.asyncSlot(list)
    async def show_drops(self, item_ids: set[int]):
        '''
        Populates self.location_table with the location data of each item in the selected recipe

        Args:
            item_ids (set[int]): all the items to provide location data for. because this is a set,
                                 there will not be any duplicate entries
        '''
        CustomPyQt.populate_drop_table(self.location_table, self.db, item_ids)



    @qasync.asyncSlot()
    async def add_to_item_helper(self):
        '''
        Takes the currently selected item and its recipe and places it in the MainWindow's item helper
        Called when the user clicks the "Add" button
        '''
        self.sigs.add_to_item_helper.emit(self.recipe_tree.get_product_ids()[0])