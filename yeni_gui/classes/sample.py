from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCheckBox, QAbstractItemView


###########
## CARD VE TEST TİPLERİ DATABASEDEN ÇEKİLECEK
## ROW SINGLE CLICK SEÇİMİNE GÖRE SCROLL AREA ENABLE EDİLİP CHECKBOXLAR UPDATELENECEK


class SampleWindow():
    def __init__(self, main_app):
        self.main_app : MyApp = main_app
        self.ui = self.main_app.ui
        self.db = self.main_app.db

        self.ui.sample_tabWidget.setCurrentIndex(0)

        # self.sample_table_widgets = self.ui.sample_tabWidget.findChildren(QtWidgets.QTableWidget)
        self.sample_table_widgets = [self.ui.s1_tableWidget, self.ui.s2_tableWidget, self.ui.s3_tableWidget]
        self.set_tables()

        self.card_types_list = ["Card 1", "Card 2", "Card 3", "Card 4", 
                        "Card 5", "Card 6", "Card 7", "Card 8",
                        "Card 9", "Card 10", "Card 11", "Card 12",
                        "Card 13", "Card 14", "Card 15", "Card 16",
                        "Card 17", "Card 18", "Card 19", "Card 20",
                        "Card 21", "Card 22", "Card 23", "Card 24",
                        "Card 25", "Card 26", "Card 27", "Card 28"]
        
        self.test_types_list = ["Test 1", "Test 2", "Test 3", "Test 4",
                        "Test 5", "Test 6", "Test 7", "Test 8",
                        "Test 9", "Test 10", "Test 11", "Test 12",
                        "Test 13", "Test 14", "Test 15", "Test 16",
                        "Test 17", "Test 18", "Test 19", "Test 20",
                        "Test 21", "Test 22", "Test 23", "Test 24",
                        "Test 25", "Test 26", "Test 27", "Test 28"]

        self.card_types_scroll_area = self.ui.card_types_scrollArea.widget()
        self.test_types_scroll_area = self.ui.test_types_scrollArea.widget()

        self.card_types_scroll_area.setDisabled(True)
        self.test_types_scroll_area.setDisabled(True)


        ###
        self.card_types_layout = self.card_types_scroll_area.layout()
        self.test_types_layout = self.test_types_scroll_area.layout()
        self.add_checkboxes(self.card_types_list, self.card_types_layout)
        self.add_checkboxes(self.test_types_list, self.test_types_layout)

    def add_checkboxes(self, items_list, layout):
        for index, item in enumerate(items_list):
            checkbox = QCheckBox(item)
            row = index // 2
            col = index % 2
            layout.addWidget(checkbox, row, col)
    ###


    def set_tables(self):
        sample_table_column_stretch = [1,1]
        sample_table_column_width = 370
        for n, table in enumerate(self.sample_table_widgets):
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.setSelectionMode(QAbstractItemView.SingleSelection)
            table.setSelectionBehavior(QAbstractItemView.SelectRows)
            table.itemSelectionChanged.connect(lambda t=table: self.selection_changed(t, t.currentRow()))

            for i, stretch in enumerate(sample_table_column_stretch):
                table.setColumnWidth(i, stretch * sample_table_column_width)

    def selection_changed(self, table, row):
        # print("Selection changed:", table, row)
        #### SEÇİME GÖRE UPDATELENECEK
        pass

