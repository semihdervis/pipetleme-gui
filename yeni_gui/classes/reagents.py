from PyQt5.QtCore import pyqtSignal, QObject

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp


class ReagentWindow(QObject):
    reagent_monitor_update_signal = pyqtSignal(int)
    def __init__(self, main_app):
        super().__init__()
        self.main_app : MyApp = main_app
        self.ui = self.main_app.ui
        self.db = self.main_app.db

        self.ui.r1_tableWidget.setRowCount(9)
        self.ui.r1_tableWidget.setColumnCount(7)
        self.ui.r2_tableWidget.setRowCount(9)
        self.ui.r2_tableWidget.setColumnCount(7)
        
        self.r1_reagents_barcode = { 0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None}
        self.r2_reagents_barcode = { 0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None}  
        self.liss_reagents_barcode = { 0: None, 1: None}                    

        # 2. sütündaki eleman değince satırı güncelle
        self.ui.r1_tableWidget.cellChanged.connect(self.update_row_r1)
        self.ui.r2_tableWidget.cellChanged.connect(self.update_row_r2)
        self.ui.liss_tableWidget.cellChanged.connect(self.update_row_liss)

    def update_row_liss(self):
        row = self.ui.liss_tableWidget.currentRow()
        column = self.ui.liss_tableWidget.currentColumn()

        if column != 1:
            pass
        else:
            
            try:
                reagent = self.db.get_reagent(self.ui.liss_tableWidget.item(row, column).text())
                if reagent:
                    # disconnect 
                    self.ui.liss_tableWidget.cellChanged.disconnect(self.update_row_liss)
                    print(reagent)
                    self.ui.liss_tableWidget.item(row, 0).setText(str(reagent.ref_no))
                    self.ui.liss_tableWidget.item(row, 2).setText(reagent.name)
                    self.ui.liss_tableWidget.item(row, 5).setText(str(reagent.volume))
                    self.liss_reagents_barcode[row] = reagent.barcode
                    self.ui.liss_tableWidget.cellChanged.connect(self.update_row_liss)

            except Exception as e:
                print(e)
                pass
        
    def update_row_r1(self):
        row = self.ui.r1_tableWidget.currentRow()
        column = self.ui.r1_tableWidget.currentColumn()

        if column != 1:
            return
        else:
            
            try:
                reagent = self.db.get_reagent(self.ui.r1_tableWidget.item(row, column).text())
                self.ui.r1_tableWidget.cellChanged.disconnect(self.update_row_r1)
                if reagent:
                    self.ui.r1_tableWidget.item(row, 0).setText(str(reagent.ref_no))
                    self.ui.r1_tableWidget.item(row, 2).setText(reagent.name)
                    self.ui.r1_tableWidget.item(row, 5).setText(str(reagent.volume))
                    self.r1_reagents_barcode[row] = reagent.barcode
                else:
                    self.ui.r1_tableWidget.item(row, 0).setText("")
                    self.ui.r1_tableWidget.item(row, 2).setText("")
                    self.ui.r1_tableWidget.item(row, 5).setText("")
                    self.r1_reagents_barcode[row] = None

                self.ui.r1_tableWidget.cellChanged.connect(self.update_row_r1)

                self.reagent_monitor_update_signal.emit(0)

            except Exception as e:
                print(e)
                pass

    def update_row_r2(self):
        row = self.ui.r2_tableWidget.currentRow()
        column = self.ui.r2_tableWidget.currentColumn()

        if column != 1:
            return
        else:
            
            try:
                reagent = self.db.get_reagent(self.ui.r2_tableWidget.item(row, column).text())
                self.ui.r2_tableWidget.cellChanged.disconnect(self.update_row_r2)
                if reagent:
                    self.ui.r2_tableWidget.item(row, 0).setText(str(reagent.ref_no))
                    self.ui.r2_tableWidget.item(row, 2).setText(reagent.name)
                    self.ui.r2_tableWidget.item(row, 5).setText(str(reagent.volume))
                    self.r2_reagents_barcode[row] = reagent.barcode
                else:
                    self.ui.r2_tableWidget.item(row, 0).setText("")
                    self.ui.r2_tableWidget.item(row, 2).setText("")
                    self.ui.r2_tableWidget.item(row, 5).setText("")
                    self.r2_reagents_barcode[row] = None

                self.ui.r2_tableWidget.cellChanged.connect(self.update_row_r2)

                self.reagent_monitor_update_signal.emit(1)

            except Exception as e:
                print(e)
                pass
    
    def update(self):

        # self.reagnts_barcode sözlüğündeki barkodları alıp güncelle
        for row, barcode in self.r1_reagents_barcode.items():
            if barcode:
                self.ui.r1_tableWidget.item(row, 1).setText(str(barcode))
    
            else:
                try:
                    self.ui.r1_tableWidget.item(row, 0).setText("")
                    self.ui.r1_tableWidget.item(row, 1).setText("")
                    self.ui.r1_tableWidget.item(row, 2).setText("")
                    self.ui.r1_tableWidget.item(row, 5).setText("")
                except:
                    pass
        
        for row, barcode in self.r2_reagents_barcode.items():
            if barcode:
                self.ui.r2_tableWidget.item(row, 1).setText(str(barcode))
                
            else:
                try:
                    self.ui.r2_tableWidget.item(row, 0).setText("")
                    self.ui.r2_tableWidget.item(row, 1).setText("")
                    self.ui.r2_tableWidget.item(row, 2).setText("")
                    self.ui.r2_tableWidget.item(row, 5).setText("")
                except:
                    pass

        for row, barcode in self.liss_reagents_barcode.items():
            if barcode:
                self.ui.liss_tableWidget.item(row, 1).setText(str(barcode))
                
            else:
                try:
                    self.ui.liss_tableWidget.item(row, 0).setText("")
                    self.ui.liss_tableWidget.item(row, 1).setText("")
                    self.ui.liss_tableWidget.item(row, 2).setText("")
                    self.ui.liss_tableWidget.item(row, 5).setText("")
                except:
                    pass