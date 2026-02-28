from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp

class CardWindow():
    def __init__(self, main_app):
        self.main_app : MyApp = main_app
        self.ui = self.main_app.ui
        self.db = self.main_app.db

        self.ui.card1_tableWidget.setRowCount(12)
        self.ui.card1_tableWidget.setColumnCount(3)
        self.ui.card2_tableWidget.setRowCount(12)
        self.ui.card2_tableWidget.setColumnCount(3)
        self.ui.card3_tableWidget.setRowCount(12)
        self.ui.card3_tableWidget.setColumnCount(3)
        self.ui.card4_tableWidget.setRowCount(12)
        self.ui.card4_tableWidget.setColumnCount(3)

        self.card1_reagents_barcode = { 0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None, 10: None, 11: None}
        self.card2_reagents_barcode = { 0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None, 10: None, 11: None}
        self.card3_reagents_barcode = { 0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None, 10: None, 11: None}
        self.card4_reagents_barcode = { 0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None, 10: None, 11: None}

        self.ui.card1_tableWidget.cellChanged.connect(lambda : self.update_row_card(1))
        self.ui.card2_tableWidget.cellChanged.connect(lambda : self.update_row_card(2))
        self.ui.card3_tableWidget.cellChanged.connect(lambda : self.update_row_card(3))
        self.ui.card4_tableWidget.cellChanged.connect(lambda : self.update_row_card(4))

    def update_row_card(self, card_no):
        row = self.ui.__getattribute__(f"card{card_no}_tableWidget").currentRow()
        column = self.ui.__getattribute__(f"card{card_no}_tableWidget").currentColumn()

        if column != 0:
            pass
        else:
            try:
                barcode = self.ui.__getattribute__(f"card{card_no}_tableWidget").item(row, 0).text()
                card_name = self.db.get_card_name(barcode)
                if card_name:
                    self.ui.__getattribute__(f"card{card_no}_tableWidget").item(row, 1).setText(card_name)
                    self.__getattribute__(f"card{card_no}_reagents_barcode")[row] = barcode

            except Exception as e:
                print(e)
                pass

    def update(self):

        for row, barcode in self.card1_reagents_barcode.items():
            if barcode:
                self.ui.card1_tableWidget.item(row, 0).setText(barcode)

            else:
                try:
                    self.ui.card1_tableWidget.item(row, 0).setText("")
                    self.ui.card1_tableWidget.item(row, 1).setText("")
                    self.ui.card1_tableWidget.item(row, 2).setText("")
                except:
                    pass
            
        for row, barcode in self.card2_reagents_barcode.items():
            if barcode:
                self.ui.card2_tableWidget.item(row, 0).setText(barcode)

            else:
                try:
                    self.ui.card2_tableWidget.item(row, 0).setText("")
                    self.ui.card2_tableWidget.item(row, 1).setText("")
                    self.ui.card2_tableWidget.item(row, 2).setText("")
                except:
                    pass
        
        for row, barcode in self.card3_reagents_barcode.items():
            if barcode:
                self.ui.card3_tableWidget.item(row, 0).setText(barcode)

            else:
                try:
                    self.ui.card3_tableWidget.item(row, 0).setText("")
                    self.ui.card3_tableWidget.item(row, 1).setText("")
                    self.ui.card3_tableWidget.item(row, 2).setText("")
                except:
                    pass
        
        for row, barcode in self.card4_reagents_barcode.items():
            if barcode:
                self.ui.card4_tableWidget.item(row, 0).setText(barcode)

            else:
                try:
                    self.ui.card4_tableWidget.item(row, 0).setText("")
                    self.ui.card4_tableWidget.item(row, 1).setText("")
                    self.ui.card4_tableWidget.item(row, 2).setText("")
                except:
                    pass
        