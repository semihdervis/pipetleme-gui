from PyQt5.QtWidgets import QListWidgetItem, QWidget, QHBoxLayout, QLabel

from database import Database, Reagent
from classes.message_box import *


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp

class ReagentDefineWindow():
    def __init__(self, main_app):

        self.main_app : MyApp = main_app
        self.ui = self.main_app.ui
        self.db = self.main_app.db 

        self.selected_reagent = None

        self.disable_all()

        self.operation = 0  # 0 select,  1 new,  2 edit 

        self.ui.reagent_define_listWidget.itemSelectionChanged.connect(self.update_selected_reagent)
        self.update()


        self.ui.save_reagent_define_pushButton.setEnabled(False)
        self.ui.cancel_reagent_define_pushButton.setEnabled(False)

        self.ui.delete_reagent_define_pushButton.clicked.connect(self.delete_reagent)
        self.ui.new_reagent_define_pushButton.clicked.connect(self.new_reagent)
        self.ui.edit_reagent_define_pushButton.clicked.connect(self.edit_reagent)
        self.ui.save_reagent_define_pushButton.clicked.connect(self.save_reagent)
        self.ui.cancel_reagent_define_pushButton.clicked.connect(self.cancel_reagent)


    def update(self):
        self.operation = 0

        reagents = self.db.get_reagents()

        if len(reagents) > 0:
            self.ui.reagent_define_listWidget.clear()
            for reagent in reagents:

                widget = QWidget()
                layout = QHBoxLayout()
                label1 = QLabel(str(reagent.barcode))
                label2 = QLabel(reagent.name)
                layout.addWidget(label1)
                layout.addWidget(label2)
                widget.setLayout(layout)
                item = QListWidgetItem()
                self.ui.reagent_define_listWidget.addItem(item)
                self.ui.reagent_define_listWidget.setItemWidget(item, widget)
                
            self.ui.reagent_define_listWidget.setCurrentRow(0)
        else:
            self.selected_reagent = None


    def update_selected_reagent(self):

        self.disable_all()
        
        if self.operation == 1:
            self.ui.reagent_define_listWidget.takeItem(self.ui.reagent_define_listWidget.count()-1)


        self.ui.save_reagent_define_pushButton.setEnabled(False)
        self.ui.cancel_reagent_define_pushButton.setEnabled(False)
        self.ui.new_reagent_define_pushButton.setEnabled(True)
        self.ui.edit_reagent_define_pushButton.setEnabled(True)
        self.ui.delete_reagent_define_pushButton.setEnabled(True)
        self.operation = 0


        if len(self.ui.reagent_define_listWidget.selectedItems()) == 0:
            self.selected_reagent = None
            return
        
        barcode = self.ui.reagent_define_listWidget.itemWidget(self.ui.reagent_define_listWidget.selectedItems()[0]).layout().itemAt(0).widget().text()

        self.selected_reagent = self.db.get_reagent(barcode)  

        if self.selected_reagent:
            try:
                self.ui.reagent_define_barcode_lineEdit.setText(str(self.selected_reagent.barcode))
                self.ui.reagent_define_name_lineEdit.setText(self.selected_reagent.name)
                self.ui.reagent_define_referance_no_lineEdit.setText(str(self.selected_reagent.ref_no))
                self.ui.reagent_define_volume_doubleSpinBox.setValue(self.selected_reagent.volume)
                self.ui.reagent_define_type_lineEdit.setText(self.selected_reagent.type)
                self.ui.reagent_define_check_date_checkBox.setChecked(self.selected_reagent.check_date)
            except Exception as e:
                message_box("Error: " + str(e))

    def save_reagent(self):

        if self.operation == 1 :
            # boş veri var mı kontrol et
            if self.ui.reagent_define_barcode_lineEdit.text() == "" or self.ui.reagent_define_name_lineEdit.text() == "" or self.ui.reagent_define_referance_no_lineEdit.text() == "" or self.ui.reagent_define_type_lineEdit.text() == "":
                message_box("Please fill all the fields.")
                return
            
            if self.db.get_reagent(self.ui.reagent_define_barcode_lineEdit.text()):
                message_box("Barcode already exists.")
                return
            try:
                self.db.add_reagent(Reagent(self.ui.reagent_define_name_lineEdit.text(), self.ui.reagent_define_referance_no_lineEdit.text(), self.ui.reagent_define_barcode_lineEdit.text(), self.ui.reagent_define_volume_doubleSpinBox.value(), self.ui.reagent_define_type_lineEdit.text(), self.ui.reagent_define_check_date_checkBox.isChecked()))
            except Exception as e:
                message_box("Error: " + str(e))
                return


        elif self.operation == 2:
            # boş veri var mı kontrol et
            if self.ui.reagent_define_barcode_lineEdit.text() == "" or self.ui.reagent_define_name_lineEdit.text() == "" or self.ui.reagent_define_referance_no_lineEdit.text() == "" or self.ui.reagent_define_type_lineEdit.text() == "":
                message_box("Please fill all the fields.")
                return

            if str(self.selected_reagent.barcode) != self.ui.reagent_define_barcode_lineEdit.text() and self.db.get_reagent(self.ui.reagent_define_barcode_lineEdit.text()):
                message_box("Barcode already exists.")
                return
            
            try:
                self.db.update_reagent(self.selected_reagent, Reagent(self.ui.reagent_define_name_lineEdit.text(), self.ui.reagent_define_referance_no_lineEdit.text(), self.ui.reagent_define_barcode_lineEdit.text(), self.ui.reagent_define_volume_doubleSpinBox.value(), self.ui.reagent_define_type_lineEdit.text(), self.ui.reagent_define_check_date_checkBox.isChecked()))
            except Exception as e:
                message_box("Error: " + str(e))
                return
            
        self.operation = 0
        self.update()
                

    def edit_reagent(self):
        self.operation = 2

        self.enable_all()
        self.ui.save_reagent_define_pushButton.setEnabled(True)
        self.ui.cancel_reagent_define_pushButton.setEnabled(True)
        self.ui.new_reagent_define_pushButton.setEnabled(False)
        self.ui.edit_reagent_define_pushButton.setEnabled(False)
        self.ui.delete_reagent_define_pushButton.setEnabled(False)
        

    def new_reagent(self):

        #yeni satır ekle
        widget = QWidget()
        layout = QHBoxLayout()
        label1 = QLabel("---")
        label2 = QLabel("New Reagent")
        layout.addWidget(label1)
        layout.addWidget(label2)
        widget.setLayout(layout)
        item = QListWidgetItem()
        self.ui.reagent_define_listWidget.addItem(item)
        self.ui.reagent_define_listWidget.setItemWidget(item, widget)
        self.ui.reagent_define_listWidget.setCurrentRow(self.ui.reagent_define_listWidget.count()-1)

        self.operation = 1
        self.ui.reagent_define_barcode_lineEdit.clear()
        self.ui.reagent_define_name_lineEdit.clear()
        self.ui.reagent_define_referance_no_lineEdit.clear()
        self.ui.reagent_define_volume_doubleSpinBox.setValue(0) 
        self.ui.reagent_define_type_lineEdit.clear()
        self.ui.reagent_define_check_date_checkBox.setChecked(False)

        self.ui.save_reagent_define_pushButton.setEnabled(True)
        self.ui.cancel_reagent_define_pushButton.setEnabled(True)
        self.ui.new_reagent_define_pushButton.setEnabled(False)
        self.ui.edit_reagent_define_pushButton.setEnabled(False)
        self.ui.delete_reagent_define_pushButton.setEnabled(False)


        self.enable_all()


    def delete_reagent(self):
        if self.selected_reagent:
            if yes_no_message_box("Are you sure you want to delete " + self.selected_reagent.name + "?") == QMessageBox.Yes:
                self.db.delete_reagent(self.selected_reagent)
                self.update()


    def cancel_reagent(self):

        if self.operation == 1:
            self.operation = 0
            self.disable_all()
            self.ui.reagent_define_listWidget.setCurrentRow(0)
            self.ui.reagent_define_listWidget.takeItem(self.ui.reagent_define_listWidget.count()-1)
        
        elif self.operation == 2:
            self.operation = 0
            self.disable_all()
            self.ui.reagent_define_listWidget.setCurrentRow(0)
            self.update_selected_reagent()


    def enable_all(self):
        self.ui.reagent_define_barcode_lineEdit.setDisabled(False)
        self.ui.reagent_define_name_lineEdit.setDisabled(False)
        self.ui.reagent_define_referance_no_lineEdit.setDisabled(False)
        self.ui.reagent_define_check_date_checkBox.setDisabled(False)
        self.ui.reagent_define_volume_doubleSpinBox.setDisabled(False)
        self.ui.reagent_define_type_lineEdit.setDisabled(False)
    
    def disable_all(self):
        self.ui.reagent_define_barcode_lineEdit.setDisabled(True)
        self.ui.reagent_define_name_lineEdit.setDisabled(True)
        self.ui.reagent_define_referance_no_lineEdit.setDisabled(True)
        self.ui.reagent_define_check_date_checkBox.setDisabled(True)
        self.ui.reagent_define_volume_doubleSpinBox.setDisabled(True)
        self.ui.reagent_define_type_lineEdit.setDisabled(True)
