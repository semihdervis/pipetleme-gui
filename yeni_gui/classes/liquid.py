from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from database import Liquid
from classes.message_box import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp


class LiquidWindow():
    def __init__(self, main_app):
        self.main_app : MyApp  = main_app
        self.ui = self.main_app.ui
        self.db = self.main_app.db
        
        self.selected_liquid : Liquid = None

        #isimi değişmeyecek şekilde
        self.ui.liquid_name_lineEdit.setReadOnly(True)

        self.disable_all()

        self.operation = 0  #0 select,  1 new,  2 edit , 3 copy

        #listwidgeti doldur
        self.ui.liquid_listWidget.itemSelectionChanged.connect(self.update_selected_liquid)
        self.update()

        self.ui.save_liquid_pushButton.setEnabled(False)
        self.ui.cancel_liquid_pushButton.setEnabled(False)

        


        self.ui.delete_liquid_pushButton.clicked.connect(self.delete_liquid)
        self.ui.new_liquid_pushButton.clicked.connect(self.new_liquid)
        self.ui.cancel_liquid_pushButton.clicked.connect(self.cancel_liquid)
        self.ui.copy_liquid_pushButton.clicked.connect(self.copy_liquid)
        self.ui.save_liquid_pushButton.clicked.connect(self.save_liquid)
        self.ui.edit_liquid_pushButton.clicked.connect(self.edit_liquid)
    

    def edit_liquid(self):

        self.operation = 2

        self.enable_all()
        self.ui.liquid_name_lineEdit.setReadOnly(True)

        self.ui.save_liquid_pushButton.setEnabled(True)
        self.ui.cancel_liquid_pushButton.setEnabled(True)
        self.ui.copy_liquid_pushButton.setEnabled(False)
        self.ui.delete_liquid_pushButton.setEnabled(False)
        self.ui.new_liquid_pushButton.setEnabled(False)
        self.ui.edit_liquid_pushButton.setEnabled(False)

    def save_liquid(self):

        if self.operation == 1 or self.operation == 3:
            liquid_name = self.ui.liquid_name_lineEdit.text()
            if not liquid_name:
                message_box("Please enter a name for the liquid", QMessageBox.Warning)
                return
            if self.db.get_liquid(liquid_name):
                message_box("Liquid with the same name already exists", QMessageBox.Warning)
                return

            if self.ui.liquid_detect_radioButton.isChecked():
                detect_mode = 0
            elif self.ui.liquid_detect_radioButton_1.isChecked():
                detect_mode = 1
            elif self.ui.liquid_detect_radioButton_2.isChecked():
                detect_mode = 2 
            
            id = self.db.liquid_max_id() + 1
            try:
                self.db.insert_liquid(Liquid(id ,liquid_name, self.ui.trans_air_gap_spinBox.value(), self.ui.tip_air_gap_spinBox.value(), self.ui.aspirate_speed_spinBox.value(), self.ui.aspirate_ramp_spinBox.value(), self.ui.aspirate_delay_spinBox.value(), self.ui.detect_speed_spinBox.value(), self.ui.detect_ramp_spinBox.value(), self.ui.submerge_spinBox.value(), self.ui.additional_volume_spinBox.value(), self.ui.mix_speed_spinBox.value(), self.ui.mix_ramp_spinBox.value(), self.ui.track_speed_spinBox.value(), self.ui.track_ramp_spinBox.value(), self.ui.dispense_speed_spinBox.value(), self.ui.dispense_ramp_spinBox.value(), self.ui.dispense_delay_spinBox.value(), self.ui.enable_clot_checkBox.isChecked(), self.ui.liquid_track_checkBox.isChecked(), detect_mode, self.ui.flush_tip_time_spinBox.value()))
            except Exception as e:
                message_box("Error: " + str(e))
                return

        elif self.operation == 2:
            
            if self.ui.liquid_detect_radioButton.isChecked():
                detect_mode = 0
            elif self.ui.liquid_detect_radioButton_1.isChecked():
                detect_mode = 1
            elif self.ui.liquid_detect_radioButton_2.isChecked():
                detect_mode = 2 
            
            try:
                self.db.update_liquid(Liquid(self.selected_liquid.id, self.selected_liquid.name, self.ui.trans_air_gap_spinBox.value(), self.ui.tip_air_gap_spinBox.value(), self.ui.aspirate_speed_spinBox.value(), self.ui.aspirate_ramp_spinBox.value(), self.ui.aspirate_delay_spinBox.value(), self.ui.detect_speed_spinBox.value(), self.ui.detect_ramp_spinBox.value(), self.ui.submerge_spinBox.value(), self.ui.additional_volume_spinBox.value(), self.ui.mix_speed_spinBox.value(), self.ui.mix_ramp_spinBox.value(), self.ui.track_speed_spinBox.value(), self.ui.track_ramp_spinBox.value(), self.ui.dispense_speed_spinBox.value(), self.ui.dispense_ramp_spinBox.value(), self.ui.dispense_delay_spinBox.value(), self.ui.enable_clot_checkBox.isChecked(), self.ui.liquid_track_checkBox.isChecked(), detect_mode, self.ui.flush_tip_time_spinBox.value()))
            except Exception as e:
                message_box("Error: " + str(e))
                return

        self.operation = 0
        self.update()


    def copy_liquid(self):

        copy_liquid_name = self.ui.liquid_name_lineEdit.text() + " (Copy)"
        counter = 1
        while self.db.get_liquid(copy_liquid_name):
            copy_liquid_name = self.ui.liquid_name_lineEdit.text() + " (Copy)_" + str(counter)
            counter += 1

        self.ui.liquid_listWidget.addItem(copy_liquid_name)
        self.ui.liquid_listWidget.setCurrentRow(self.ui.liquid_listWidget.count()-1)

        self.operation = 3
        
        self.ui.liquid_name_lineEdit.setText(copy_liquid_name)
        
        self.enable_all()

        self.ui.save_liquid_pushButton.setEnabled(True)
        self.ui.cancel_liquid_pushButton.setEnabled(True)
        self.ui.edit_liquid_pushButton.setEnabled(False)
        self.ui.copy_liquid_pushButton.setEnabled(False)
        self.ui.delete_liquid_pushButton.setEnabled(False)
        self.ui.new_liquid_pushButton.setEnabled(False)


    def cancel_liquid(self):

        if self.operation == 1 or self.operation == 3:
            self.operation = 0
            self.disable_all()
            self.ui.liquid_listWidget.setCurrentRow(0)
            self.ui.liquid_listWidget.takeItem(self.ui.liquid_listWidget.count()-1)

        if self.operation == 2:
            self.operation = 0
            self.disable_all()
            self.ui.liquid_listWidget.setCurrentRow(0)
            


    def new_liquid(self):

        #yeni satır ekle
        self.ui.liquid_listWidget.addItem("New Liquid")
        self.ui.liquid_listWidget.setCurrentRow(self.ui.liquid_listWidget.count()-1)

        self.operation = 1
        #bütün lineeditleri temizle
        self.ui.liquid_name_lineEdit.clear()
        self.ui.liquid_name_lineEdit.setReadOnly(False)

        self.ui.trans_air_gap_spinBox.setValue(0)
        self.ui.tip_air_gap_spinBox.setValue(0)
        self.ui.aspirate_speed_spinBox.setValue(0)
        self.ui.aspirate_ramp_spinBox.setValue(0)
        self.ui.aspirate_delay_spinBox.setValue(0)
        self.ui.detect_speed_spinBox.setValue(0)
        self.ui.detect_ramp_spinBox.setValue(0)
        self.ui.submerge_spinBox.setValue(0)
        self.ui.additional_volume_spinBox.setValue(0)
        self.ui.mix_speed_spinBox.setValue(0)
        self.ui.mix_ramp_spinBox.setValue(0)
        self.ui.track_speed_spinBox.setValue(0)
        self.ui.track_ramp_spinBox.setValue(0)
        self.ui.dispense_speed_spinBox.setValue(0)
        self.ui.dispense_ramp_spinBox.setValue(0)
        self.ui.dispense_delay_spinBox.setValue(0)
        self.ui.flush_tip_time_spinBox.setValue(0)

        self.ui.enable_clot_checkBox.setChecked(False)
        self.ui.liquid_track_checkBox.setChecked(False)
        self.ui.liquid_detect_radioButton.setChecked(True)

        self.ui.save_liquid_pushButton.setEnabled(True)
        self.ui.cancel_liquid_pushButton.setEnabled(True)

        self.ui.copy_liquid_pushButton.setEnabled(False)
        self.ui.delete_liquid_pushButton.setEnabled(False)
        self.ui.new_liquid_pushButton.setEnabled(False)
        self.ui.edit_liquid_pushButton.setEnabled(False)


    def update(self):
        
        liquids = self.db.get_liquid_names()

        #eğer listede eleman varsa ilkini seçecek şekilde yapıyorum değişebililr bu kısım
        if len(liquids) > 0:
            self.ui.liquid_listWidget.clear()
            self.ui.liquid_listWidget.addItems(liquids)
            self.ui.liquid_listWidget.setCurrentRow(0)
        else:
            self.selected_liquid = None


    def update_selected_liquid(self):

        self.disable_all()

        if self.operation == 1 or self.operation == 3:
            # yeni gelen son satır silinecek
            self.ui.liquid_listWidget.takeItem(self.ui.liquid_listWidget.count()-1)


        self.ui.save_liquid_pushButton.setEnabled(False)
        self.ui.cancel_liquid_pushButton.setEnabled(False)
        self.ui.copy_liquid_pushButton.setEnabled(True) 
        self.ui.delete_liquid_pushButton.setEnabled(True)
        self.ui.new_liquid_pushButton.setEnabled(True)
        self.ui.edit_liquid_pushButton.setEnabled(True)

        self.operation = 0

        
        if len(self.ui.liquid_listWidget.selectedItems()) == 0:
            selected_liquid = None
            return
        liquid_name = self.ui.liquid_listWidget.selectedItems()[0].text()
        self.selected_liquid = self.db.get_liquid(liquid_name)
        if self.selected_liquid:
            try:
                self.ui.liquid_name_lineEdit.setText(self.selected_liquid.name)
                self.ui.trans_air_gap_spinBox.setValue(self.selected_liquid.trans_air_gap)
                self.ui.tip_air_gap_spinBox.setValue(self.selected_liquid.tip_air_gap)
                self.ui.aspirate_speed_spinBox.setValue(self.selected_liquid.aspirate_speed)
                self.ui.aspirate_ramp_spinBox.setValue(self.selected_liquid.aspirate_ramp)
                self.ui.aspirate_delay_spinBox.setValue(self.selected_liquid.aspirate_delay)
                self.ui.detect_speed_spinBox.setValue(self.selected_liquid.detect_speed)
                self.ui.detect_ramp_spinBox.setValue(self.selected_liquid.detect_ramp)
                self.ui.submerge_spinBox.setValue(self.selected_liquid.submerge)
                self.ui.additional_volume_spinBox.setValue(self.selected_liquid.additional_volume)
                self.ui.mix_speed_spinBox.setValue(self.selected_liquid.mix_speed)
                self.ui.mix_ramp_spinBox.setValue(self.selected_liquid.mix_ramp)
                self.ui.track_speed_spinBox.setValue(self.selected_liquid.track_speed)
                self.ui.track_ramp_spinBox.setValue(self.selected_liquid.track_ramp)
                self.ui.dispense_speed_spinBox.setValue(self.selected_liquid.dispense_speed)
                self.ui.dispense_ramp_spinBox.setValue(self.selected_liquid.dispense_ramp)
                self.ui.dispense_delay_spinBox.setValue(self.selected_liquid.dispense_delay)
                self.ui.flush_tip_time_spinBox.setValue(int(self.selected_liquid.flush_tip_time))
                if self.selected_liquid.enable_clot:
                    self.ui.enable_clot_checkBox.setChecked(True)
                else:
                    self.ui.enable_clot_checkBox.setChecked(False)
                if self.selected_liquid.need_track:
                    self.ui.liquid_track_checkBox.setChecked(True)
                else:
                    self.ui.liquid_track_checkBox.setChecked(False)
                if self.selected_liquid.detect_mode == 0:
                    self.ui.liquid_detect_radioButton.setChecked(True)
                elif self.selected_liquid.detect_mode == 1:
                    self.ui.liquid_detect_radioButton_1.setChecked(True)
                elif self.selected_liquid.detect_mode == 2:
                    self.ui.liquid_detect_radioButton_2.setChecked(True)
            
            except Exception as e:
                message_box("Error: " + str(e))

    def delete_liquid(self):
        if self.selected_liquid:
            if yes_no_message_box("Are you sure you want to delete " + self.selected_liquid.name + "?") == QMessageBox.Yes:
                self.db.delete_liquid(self.selected_liquid.name)
                self.update()

        else:
            message_box("Please select a liquid to delete", QMessageBox.Warning)
    
    
    
    def enable_all(self):

        self.ui.liquid_name_lineEdit.setReadOnly(False)
        self.ui.trans_air_gap_spinBox.setEnabled(True)
        self.ui.tip_air_gap_spinBox.setEnabled(True)
        self.ui.aspirate_speed_spinBox.setEnabled(True)
        self.ui.aspirate_ramp_spinBox.setEnabled(True)
        self.ui.aspirate_delay_spinBox.setEnabled(True)
        self.ui.detect_speed_spinBox.setEnabled(True)
        self.ui.detect_ramp_spinBox.setEnabled(True)
        self.ui.submerge_spinBox.setEnabled(True)
        self.ui.additional_volume_spinBox.setEnabled(True)
        self.ui.mix_speed_spinBox.setEnabled(True)
        self.ui.mix_ramp_spinBox.setEnabled(True)
        self.ui.track_speed_spinBox.setEnabled(True)
        self.ui.track_ramp_spinBox.setEnabled(True)
        self.ui.dispense_speed_spinBox.setEnabled(True)
        self.ui.dispense_ramp_spinBox.setEnabled(True)
        self.ui.dispense_delay_spinBox.setEnabled(True)
        self.ui.flush_tip_time_spinBox.setEnabled(True)
        self.ui.enable_clot_checkBox.setEnabled(True)
        self.ui.liquid_track_checkBox.setEnabled(True)
        self.ui.liquid_detect_radioButton.setEnabled(True)
        self.ui.liquid_detect_radioButton_1.setEnabled(True)
        self.ui.liquid_detect_radioButton_2.setEnabled(True)
    
    def disable_all(self):
        
        self.ui.liquid_name_lineEdit.setReadOnly(True)
        self.ui.trans_air_gap_spinBox.setEnabled(False)
        self.ui.tip_air_gap_spinBox.setEnabled(False)
        self.ui.aspirate_speed_spinBox.setEnabled(False)
        self.ui.aspirate_ramp_spinBox.setEnabled(False)
        self.ui.aspirate_delay_spinBox.setEnabled(False)
        self.ui.detect_speed_spinBox.setEnabled(False)
        self.ui.detect_ramp_spinBox.setEnabled(False)
        self.ui.submerge_spinBox.setEnabled(False)
        self.ui.additional_volume_spinBox.setEnabled(False)
        self.ui.mix_speed_spinBox.setEnabled(False)
        self.ui.mix_ramp_spinBox.setEnabled(False)
        self.ui.track_speed_spinBox.setEnabled(False)
        self.ui.track_ramp_spinBox.setEnabled(False)
        self.ui.dispense_speed_spinBox.setEnabled(False)
        self.ui.dispense_ramp_spinBox.setEnabled(False)
        self.ui.dispense_delay_spinBox.setEnabled(False)
        self.ui.flush_tip_time_spinBox.setEnabled(False)
        self.ui.enable_clot_checkBox.setEnabled(False)
        self.ui.liquid_track_checkBox.setEnabled(False)
        self.ui.liquid_detect_radioButton.setEnabled(False)
        self.ui.liquid_detect_radioButton_1.setEnabled(False)
        self.ui.liquid_detect_radioButton_2.setEnabled(False)

