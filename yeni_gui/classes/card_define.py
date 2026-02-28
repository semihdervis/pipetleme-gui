
from PyQt5.QtWidgets import QListWidgetItem, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from database import Database, Card
from classes.message_box import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp

class CardDefineWindow():
    def __init__(self,main_app):
        self.main_app : MyApp = main_app
        self.ui = self.main_app.ui
        self.db = self.main_app.db

        self.selected_card = None
    
        self.operation = 0  # 0 select,  1 new,  2 edit 

        self.fill_comboboxes()

        self.ui.card_define_listWidget.itemSelectionChanged.connect(self.update_selected_card)
        self.update()

        self.ui.save_card_define_pushButton.setEnabled(False)
        self.ui.cancel_card_define_pushButton.setEnabled(False)
        self.ui.import_card_define_pushButton.setEnabled(False)
        self.ui.export_card_define_pushButton.setEnabled(False)

        #barcode değiştikçe test name değişsin
        self.ui.cd_barcode_lineEdit.textChanged.connect(self.update_test_name)

        self.ui.edit_card_define_pushButton.clicked.connect(self.edit_card)
        self.ui.new_card_define_pushButton.clicked.connect(self.new_card)
        self.ui.delete_card_define_pushButton.clicked.connect(self.delete_card)
        self.ui.save_card_define_pushButton.clicked.connect(self.save_card)
        self.ui.cancel_card_define_pushButton.clicked.connect(self.cancel_card)

        self.disable_all()


    def update(self):

        list_contents = self.db.get_table_cards()

        if len(list_contents) > 0:
            self.ui.card_define_listWidget.clear()

            for card in list_contents:

                widget = QWidget()
                layout = QHBoxLayout()
                label1 = QLabel(str(card[0]))   #barcode
                label2 = QLabel(card[1])        #card_name
                label3 = QLabel(card[2])        #test_name
                #labeller içindeki yazının boyutu kadar genişlesin
                
                label1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                label3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                # Yazıyı kesmeden kaydırma çubuğu sağlamak için
                label1.setWordWrap(True)
                label2.setWordWrap(True)
                label3.setWordWrap(True)


                label1.setMinimumWidth(50)  # Varsayılan bir genişlik
                label2.setMinimumWidth(250)  # En uzun metne göre belirlenebilir
                label3.setMinimumWidth(250)

                layout.addWidget(label1)
                layout.addWidget(label2)
                layout.addWidget(label3)
                widget.setLayout(layout)
                item = QListWidgetItem()
                self.ui.card_define_listWidget.addItem(item)
                self.ui.card_define_listWidget.setItemWidget(item, widget)

            self.ui.card_define_listWidget.setCurrentRow(0)
        else:
            self.selected_card = None
            self.ui.card_define_listWidget.clear()


    def update_selected_card(self):

        self.disable_all()
        
        self.ui.save_card_define_pushButton.setEnabled(False)
        self.ui.cancel_card_define_pushButton.setEnabled(False)
        self.ui.new_card_define_pushButton.setEnabled(True)
        self.ui.edit_card_define_pushButton.setEnabled(True)
        self.ui.delete_card_define_pushButton.setEnabled(True)
        self.operation = 0

        if len(self.ui.card_define_listWidget.selectedItems()) == 0:
            self.selected_card = None
            return

        barcode = self.ui.card_define_listWidget.itemWidget(self.ui.card_define_listWidget.selectedItems()[0]).layout().itemAt(0).widget().text()
        test_name = self.ui.card_define_listWidget.itemWidget(self.ui.card_define_listWidget.selectedItems()[0]).layout().itemAt(2).widget().text()

        self.selected_card = self.db.get_card(barcode, test_name)

        if self.selected_card:
            self.ui.cd_card_name_lineEdit.setText(self.selected_card.card_name if self.selected_card.card_name else "")
            self.ui.cd_test_name_lineEdit.setText(self.selected_card.test_name if self.selected_card.test_name else "")
            self.ui.cd_barcode_lineEdit.setText(str(self.selected_card.barcode) if self.selected_card.barcode else "")
            self.ui.cd_ref_no_lineEdit.setText(str(self.selected_card.ref_no) if self.selected_card.ref_no else "")
            self.ui.cd_card_type_comboBox.setCurrentText(self.selected_card.card_type if self.selected_card.card_type else "")
            self.ui.cd_cell_define_lineEdit.setText(self.selected_card.cell_define if self.selected_card.cell_define else "")
            self.ui.cd_test_count_spinBox.setValue(self.selected_card.test_count if self.selected_card.test_count else 0)
            self.ui.cd_is_used_checkBox.setChecked(self.selected_card.is_used if self.selected_card.is_used else False)
            self.ui.cd_card_picture_lineEdit.setText(self.selected_card.card_picture if self.selected_card.card_picture else "")
            self.ui.cd_erythroracyte_checkBox.setChecked(self.selected_card.need_erythroracyte if self.selected_card.need_erythroracyte else False)
            self.ui.cd_need_incubator_checkBox.setChecked(self.selected_card.need_incubator if self.selected_card.need_incubator else False)
            self.ui.cd_incubate_time_spinBox.setValue(self.selected_card.incubation_time if self.selected_card.incubation_time else 0)
            self.ui.cd_sample_vol_spinBox.setValue(self.selected_card.sample_volume if self.selected_card.sample_volume else 0)
            self.ui.cd_sample_liquid_comboBox.setCurrentText(self.selected_card.sample_liquid if self.selected_card.sample_liquid else "")
            self.ui.cd_liss_vol_spinBox.setValue(self.selected_card.liss_volume if self.selected_card.liss_volume else 0)
            self.ui.cd_liss_liquid_comboBox.setCurrentText(self.selected_card.liss_liquid if self.selected_card.liss_liquid else "")
            self.ui.cd_liss_reagent_comboBox.setCurrentText(self.selected_card.liss_reagent if self.selected_card.liss_reagent else "")
            self.ui.cd_mix_vol_spinBox.setValue(self.selected_card.mix_volume if self.selected_card.mix_volume else 0)
            self.ui.cd_mix_cycle_spinBox.setValue(self.selected_card.mix_cycle if self.selected_card.mix_cycle else 0)
            self.ui.cd_mix_liquid_comboBox.setCurrentText(self.selected_card.mix_liquid if self.selected_card.mix_liquid else "")
            self.ui.cd_asp_vol_spinBox.setValue(self.selected_card.asp_volume if self.selected_card.asp_volume else 0)
            self.ui.cd_sample_cell_sequence_lineEdit.setText(self.selected_card.cell_sequence if self.selected_card.cell_sequence else "")
            self.ui.cd_need_serum_checkBox.setChecked(self.selected_card.need_serum if self.selected_card.need_serum else False)
            self.ui.cd_serum_vol_spinBox.setValue(self.selected_card.serum_volume if self.selected_card.serum_volume else 0)
            self.ui.cd_serum_liquid_comboBox.setCurrentText(self.selected_card.serum_liquid if self.selected_card.serum_liquid else "")
            self.ui.cd_serum_cell_sequence_lineEdit.setText(self.selected_card.serum_cell_sequence if self.selected_card.serum_cell_sequence else "")
   

    def save_card(self):

        if self.operation == 1:
            if self.ui.cd_barcode_lineEdit.text() == "" or self.ui.cd_test_name_lineEdit.text() == "":
                message_box("Barcode and Test Name cannot be empty!")
                return
            if self.db.get_card(self.ui.cd_barcode_lineEdit.text(), self.ui.cd_test_name_lineEdit.text()):
                message_box("Barcode and Test Name already exists!")
                return
            
            #eğer aynı card adı ve farklı barcode varsa
            card_names = self.db.get_card_names()
            if self.ui.cd_card_name_lineEdit.text() in card_names and self.db.get_card_name(self.ui.cd_barcode_lineEdit.text()) != self.ui.cd_card_name_lineEdit.text():
                message_box("Card name already exists!")
                return

            #eğer bu kart daha önce yoksa
            if self.ui.cd_card_name_lineEdit.text() not in card_names:
                try:
                    self.db.add_card_name(self.ui.cd_barcode_lineEdit.text() ,self.ui.cd_card_name_lineEdit.text())
                except Exception as e:
                    message_box("Error1: " + str(e))
                    return

            try:
                self.db.add_card(Card(self.ui.cd_barcode_lineEdit.text(), self.ui.cd_card_name_lineEdit.text(),self.ui.cd_ref_no_lineEdit.text(), self.ui.cd_test_name_lineEdit.text(), self.ui.cd_card_type_comboBox.currentText(), self.ui.cd_cell_define_lineEdit.text(), self.ui.cd_test_count_spinBox.value(), self.ui.cd_is_used_checkBox.isChecked(), self.ui.cd_card_picture_lineEdit.text(), self.ui.cd_need_incubator_checkBox.isChecked(), self.ui.cd_incubate_time_spinBox.value(),self.ui.cd_erythroracyte_checkBox.isChecked(), self.ui.cd_sample_vol_spinBox.value(), self.ui.cd_sample_liquid_comboBox.currentText(), self.ui.cd_liss_vol_spinBox.value(), self.ui.cd_liss_liquid_comboBox.currentText(), self.ui.cd_liss_reagent_comboBox.currentText(), self.ui.cd_mix_vol_spinBox.value(), self.ui.cd_mix_cycle_spinBox.value(), self.ui.cd_mix_liquid_comboBox.currentText(), self.ui.cd_asp_vol_spinBox.value(), self.ui.cd_sample_cell_sequence_lineEdit.text(), self.ui.cd_need_serum_checkBox.isChecked(), self.ui.cd_serum_vol_spinBox.value(), self.ui.cd_serum_liquid_comboBox.currentText(), self.ui.cd_serum_cell_sequence_lineEdit.text(), ""))
            except Exception as e:
                message_box("Error2: " + str(e))

        elif self.operation == 2:
            try:
                self.db.update_card(Card(self.ui.cd_barcode_lineEdit.text(), self.ui.cd_card_name_lineEdit.text(), self.ui.cd_test_name_lineEdit.text(), self.ui.cd_ref_no_lineEdit.text(), self.ui.cd_card_type_comboBox.currentText(), self.ui.cd_cell_define_lineEdit.text(), self.ui.cd_test_count_spinBox.value(), self.ui.cd_is_used_checkBox.isChecked(), self.ui.cd_card_picture_lineEdit.text(), self.ui.cd_need_incubator_checkBox.isChecked(), self.ui.cd_incubate_time_spinBox.value(),self.ui.cd_erythroracyte_checkBox.isChecked(), self.ui.cd_sample_vol_spinBox.value(), self.ui.cd_sample_liquid_comboBox.currentText(), self.ui.cd_liss_vol_spinBox.value(), self.ui.cd_liss_liquid_comboBox.currentText(), self.ui.cd_liss_reagent_comboBox.currentText(), self.ui.cd_mix_vol_spinBox.value(), self.ui.cd_mix_cycle_spinBox.value(), self.ui.cd_mix_liquid_comboBox.currentText(), self.ui.cd_asp_vol_spinBox.value(), self.ui.cd_sample_cell_sequence_lineEdit.text(), self.ui.cd_need_serum_checkBox.isChecked(), self.ui.cd_serum_vol_spinBox.value(), self.ui.cd_serum_liquid_comboBox.currentText(), self.ui.cd_serum_cell_sequence_lineEdit.text(),self.selected_card.script))
            except Exception as e:
                message_box("Error3: " + str(e))
                return
        
        self.operation = 0
        self.update()

    def edit_card(self):
        self.operation = 2
        self.enable_all()

        #barcode ve test name değiştirilemez
        self.ui.cd_barcode_lineEdit.setEnabled(False)
        self.ui.cd_test_name_lineEdit.setEnabled(False)
        self.ui.cd_card_name_lineEdit.setEnabled(False)

        self.ui.save_card_define_pushButton.setEnabled(True)
        self.ui.cancel_card_define_pushButton.setEnabled(True)
        self.ui.new_card_define_pushButton.setEnabled(False)
        self.ui.edit_card_define_pushButton.setEnabled(False)
        self.ui.delete_card_define_pushButton.setEnabled(False)

    
    def new_card(self):
        #yeni satır ekleme
        widget = QWidget()
        layout = QHBoxLayout()
        label1 = QLabel("")
        label2 = QLabel("")
        label3 = QLabel("")
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        widget.setLayout(layout)
        item = QListWidgetItem()
        self.ui.card_define_listWidget.addItem(item)
        self.ui.card_define_listWidget.setItemWidget(item, widget)
        self.ui.card_define_listWidget.setCurrentRow(self.ui.card_define_listWidget.count()-1)

        self.operation = 1

        self.ui.cd_card_name_lineEdit.clear()
        self.ui.cd_test_name_lineEdit.clear()
        self.ui.cd_barcode_lineEdit.clear()
        self.ui.cd_ref_no_lineEdit.clear()
        self.ui.cd_card_type_comboBox.setCurrentText("")
        self.ui.cd_cell_define_lineEdit.clear()
        self.ui.cd_test_count_spinBox.setValue(0)
        self.ui.cd_is_used_checkBox.setChecked(False)
        self.ui.cd_card_picture_lineEdit.clear()
        self.ui.cd_erythroracyte_checkBox.setChecked(False)
        self.ui.cd_need_incubator_checkBox.setChecked(False)
        self.ui.cd_incubate_time_spinBox.setValue(0)
        self.ui.cd_sample_vol_spinBox.setValue(0)
        self.ui.cd_sample_liquid_comboBox.setCurrentText("")
        self.ui.cd_liss_vol_spinBox.setValue(0)
        self.ui.cd_liss_liquid_comboBox.setCurrentText("")
        self.ui.cd_liss_reagent_comboBox.setCurrentText("")
        self.ui.cd_mix_vol_spinBox.setValue(0)
        self.ui.cd_mix_cycle_spinBox.setValue(0)
        self.ui.cd_mix_liquid_comboBox.setCurrentText("")
        self.ui.cd_asp_vol_spinBox.setValue(0)
        self.ui.cd_sample_cell_sequence_lineEdit.clear()
        self.ui.cd_need_serum_checkBox.setChecked(False)
        self.ui.cd_serum_vol_spinBox.setValue(0)
        self.ui.cd_serum_liquid_comboBox.setCurrentText("")
        self.ui.cd_serum_cell_sequence_lineEdit.clear()

        self.ui.save_card_define_pushButton.setEnabled(True)
        self.ui.cancel_card_define_pushButton.setEnabled(True)
        self.ui.new_card_define_pushButton.setEnabled(False)
        self.ui.edit_card_define_pushButton.setEnabled(False)
        self.ui.delete_card_define_pushButton.setEnabled(False)
        
        self.enable_all()

    def delete_card(self):
        if self.selected_card:
            if yes_no_message_box("Are you sure you want to delete " + self.selected_card.test_name + "?") == QMessageBox.Yes:
                self.db.delete_card(self.selected_card)
                self.update()

    def cancel_card(self):

        if self.operation == 1:
            self.operation = 0
            self.disable_all()
            self.ui.card_define_listWidget.setCurrentRow(0)
            self.ui.card_define_listWidget.takeItem(self.ui.card_define_listWidget.count()-1)
            
        elif self.operation == 2:
            self.operation = 0
            self.disable_all()
            self.ui.card_define_listWidget.setCurrentRow(0)
            self.update_selected_card()

    def update_test_name(self):
        if self.db.get_card_name(self.ui.cd_barcode_lineEdit.text()):
            self.ui.cd_card_name_lineEdit.setText(self.db.get_card_name(self.ui.cd_barcode_lineEdit.text()))
            self.ui.cd_card_name_lineEdit.setEnabled(False)
        else:
            self.ui.cd_card_name_lineEdit.setEnabled(True)


    def disable_all(self):
        self.ui.cd_asp_vol_spinBox.setEnabled(False)
        self.ui.cd_barcode_lineEdit.setEnabled(False)
        self.ui.cd_cell_define_lineEdit.setEnabled(False)
        self.ui.cd_card_name_lineEdit.setEnabled(False)
        self.ui.cd_card_picture_lineEdit.setEnabled(False)
        self.ui.cd_card_type_comboBox.setEnabled(False)
        self.ui.cd_serum_liquid_comboBox.setEnabled(False)
        self.ui.cd_serum_vol_spinBox.setEnabled(False)
        self.ui.cd_serum_cell_sequence_lineEdit.setEnabled(False)
        self.ui.cd_need_serum_checkBox.setEnabled(False)
        self.ui.cd_sample_cell_sequence_lineEdit.setEnabled(False)
        self.ui.cd_incubate_time_spinBox.setEnabled(False)
        self.ui.cd_need_incubator_checkBox.setEnabled(False)
        self.ui.cd_erythroracyte_checkBox.setEnabled(False)
        self.ui.cd_liss_liquid_comboBox.setEnabled(False)
        self.ui.cd_liss_vol_spinBox.setEnabled(False)
        self.ui.cd_liss_reagent_comboBox.setEnabled(False)
        self.ui.cd_mix_vol_spinBox.setEnabled(False)
        self.ui.cd_mix_cycle_spinBox.setEnabled(False)
        self.ui.cd_mix_liquid_comboBox.setEnabled(False)
        self.ui.cd_ref_no_lineEdit.setEnabled(False)
        self.ui.cd_test_count_spinBox.setEnabled(False)
        self.ui.cd_test_name_lineEdit.setEnabled(False)
        self.ui.cd_is_used_checkBox.setEnabled(False)
        self.ui.cd_sample_liquid_comboBox.setEnabled(False)
        self.ui.cd_sample_vol_spinBox.setEnabled(False)
        self.ui.cd_reagent_cell_sequence_lineEdit.setEnabled(False)
        self.ui.cd_reagent_liquid_comboBox.setEnabled(False)
        self.ui.cd_reagent_vol_spinBox.setEnabled(False)
        self.ui.cd_reagent_name_comboBox.setEnabled(False)

    def enable_all(self):
        self.ui.cd_asp_vol_spinBox.setEnabled(True)
        self.ui.cd_barcode_lineEdit.setEnabled(True)
        self.ui.cd_cell_define_lineEdit.setEnabled(True)
        self.ui.cd_card_name_lineEdit.setEnabled(True)
        self.ui.cd_card_picture_lineEdit.setEnabled(True)
        self.ui.cd_card_type_comboBox.setEnabled(True)
        self.ui.cd_serum_liquid_comboBox.setEnabled(True)
        self.ui.cd_serum_vol_spinBox.setEnabled(True)
        self.ui.cd_serum_cell_sequence_lineEdit.setEnabled(True)  
        self.ui.cd_need_serum_checkBox.setEnabled(True)
        self.ui.cd_sample_cell_sequence_lineEdit.setEnabled(True)
        self.ui.cd_incubate_time_spinBox.setEnabled(True)
        self.ui.cd_need_incubator_checkBox.setEnabled(True)
        self.ui.cd_erythroracyte_checkBox.setEnabled(True)
        self.ui.cd_liss_liquid_comboBox.setEnabled(True)
        self.ui.cd_liss_vol_spinBox.setEnabled(True)
        self.ui.cd_liss_reagent_comboBox.setEnabled(True)
        self.ui.cd_mix_vol_spinBox.setEnabled(True)
        self.ui.cd_mix_cycle_spinBox.setEnabled(True)
        self.ui.cd_mix_liquid_comboBox.setEnabled(True)
        self.ui.cd_ref_no_lineEdit.setEnabled(True)
        self.ui.cd_test_count_spinBox.setEnabled(True)
        self.ui.cd_test_name_lineEdit.setEnabled(True)
        self.ui.cd_is_used_checkBox.setEnabled(True)
        self.ui.cd_sample_liquid_comboBox.setEnabled(True)
        self.ui.cd_sample_vol_spinBox.setEnabled(True)
        self.ui.cd_reagent_cell_sequence_lineEdit.setEnabled(True)
        self.ui.cd_reagent_liquid_comboBox.setEnabled(True)
        self.ui.cd_reagent_vol_spinBox.setEnabled(True)
        self.ui.cd_reagent_name_comboBox.setEnabled(True)

    def fill_comboboxes(self):
        liquids = self.db.get_liquid_names()
        liquids.insert(0, "")

        self.ui.cd_sample_liquid_comboBox.clear()
        self.ui.cd_liss_liquid_comboBox.clear()
        self.ui.cd_mix_liquid_comboBox.clear()
        self.ui.cd_serum_liquid_comboBox.clear()
        self.ui.cd_reagent_liquid_comboBox.clear()
        self.ui.cd_reagent_name_comboBox.clear()
        self.ui.cd_liss_reagent_comboBox.clear()

        self.ui.cd_sample_liquid_comboBox.addItems(liquids)
        self.ui.cd_liss_liquid_comboBox.addItems(liquids)
        self.ui.cd_mix_liquid_comboBox.addItems(liquids)
        self.ui.cd_serum_liquid_comboBox.addItems(liquids)
        self.ui.cd_reagent_liquid_comboBox.addItems(liquids)
        