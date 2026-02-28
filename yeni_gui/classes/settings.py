from PyQt5.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QLabel, QListWidgetItem

from database import Database, Settings, User, USER_TYPES
from classes.message_box import message_box, yes_no_message_box

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp

class SettingsWindow():

    def __init__(self, main_app):
        
        self.main_app : MyApp = main_app
        self.ui = self.main_app.ui
        self.db = self.main_app.db

        self.selected_user = None

        self.ui.setting_username_lineEdit.setEnabled(False)
        self.ui.comboBox.setEnabled(False)
        self.ui.setting_password_lineEdit.setEnabled(False)

        self.operation = 0  # 0 select,  1 new,  2 edit        

        self.settings = self.db.get_settings()
        if not self.settings:
            self.settings = Settings()
     
        self.ui.setting_listWidget.itemSelectionChanged.connect(self.update_selected_user)
        self.ui.settings_tabWidget.currentChanged.connect(self.tab_changed)
        
        self.ui.pushButton_ok.clicked.connect(self.save_system_settings)
        self.ui.pushButton_cancel.clicked.connect(self.update)

        self.ui.save_setting_pushButton.clicked.connect(self.save_user_settings)
        self.ui.cancel_setting_pushButton.clicked.connect(self.update_user_settings)
        self.ui.new_setting_pushButton.clicked.connect(self.new_user)
        self.ui.edit_setting_pushButton.clicked.connect(self.edit_user)
        self.ui.delete_setting_pushButton.clicked.connect(self.delete_user)

    def update(self):
        self.ui.settings_tabWidget.setCurrentIndex(0)
        self.update_system_settings()
        self.update_user_settings()
        
    def tab_changed(self):
        if self.ui.settings_tabWidget.currentIndex() == 0:
            self.update_system_settings()
        elif self.ui.settings_tabWidget.currentIndex() == 1:
            self.update_user_settings()

    def update_system_settings(self):
        self.ui.lineEdit_system_name.setText(self.settings.system_name)
        self.ui.lineEdit_serial_number.setText(self.settings.serial_number)
        self.ui.comboBox_reader_port.setCurrentText(self.settings.reader_port)
        self.ui.comboBox_reader_data_bit.setCurrentText(str(self.settings.reader_data_bit))
        self.ui.comboBox_reader_parity_bit.setCurrentText(self.settings.reader_parity_bit)
        self.ui.comboBox_reader_baud_rate.setCurrentText(str(self.settings.reader_baud_rate))
        self.ui.comboBox_reader_stop_bit.setCurrentText(str(self.settings.reader_stop_bit))
        self.ui.comboBox_lis_port.setCurrentText(self.settings.lis_port)
        self.ui.comboBox_lis_data_bit.setCurrentText(str(self.settings.lis_data_bit))
        self.ui.comboBox_lis_parity_bit.setCurrentText(self.settings.lis_parity_bit)
        self.ui.comboBox_lis_baud_rate.setCurrentText(str(self.settings.lis_baud_rate))
        self.ui.comboBox_lis_stop_bit.setCurrentText(str(self.settings.lis_stop_bit))

    def save_system_settings(self):
        self.settings.system_name = self.ui.lineEdit_system_name.text()
        self.settings.serial_number = self.ui.lineEdit_serial_number.text()
        self.settings.reader_port = self.ui.comboBox_reader_port.currentText()
        self.settings.reader_data_bit = int(self.ui.comboBox_reader_data_bit.currentText())
        self.settings.reader_parity_bit = self.ui.comboBox_reader_parity_bit.currentText()
        self.settings.reader_baud_rate = int(self.ui.comboBox_reader_baud_rate.currentText())
        self.settings.reader_stop_bit = int(self.ui.comboBox_reader_stop_bit.currentText())
        self.settings.lis_port = self.ui.comboBox_lis_port.currentText()
        self.settings.lis_data_bit = int(self.ui.comboBox_lis_data_bit.currentText())
        self.settings.lis_parity_bit = self.ui.comboBox_lis_parity_bit.currentText()
        self.settings.lis_baud_rate = int(self.ui.comboBox_lis_baud_rate.currentText())
        self.settings.lis_stop_bit = int(self.ui.comboBox_lis_stop_bit.currentText())
        self.db.update_settings(self.settings)
        self.update()
        message_box("Settings saved successfully")


    def update_user_settings(self):
        self.operation = 0
        
        users = self.db.get_users_less_types(self.main_app.user.type)

        self.ui.setting_listWidget.clear()  

        for user in users:
            widget = QWidget()
            layout = QHBoxLayout()
            label1 = QLabel(user.name)
            #user type
            label2 = QLabel(USER_TYPES[user.type])
            layout.addWidget(label1)
            layout.addWidget(label2)
            widget.setLayout(layout)
            item = QListWidgetItem()
            self.ui.setting_listWidget.addItem(item)
            self.ui.setting_listWidget.setItemWidget(item, widget)


        self.ui.setting_username_lineEdit.setEnabled(False)
        self.ui.comboBox.setEnabled(False)
        self.ui.setting_password_lineEdit.setEnabled(False)

        self.ui.setting_listWidget.setCurrentRow(0)
        
    def update_selected_user(self):

        if self.operation == 1:
            self.ui.setting_password_lineEdit.setEnabled(False)
            self.ui.setting_listWidget.takeItem(self.ui.setting_listWidget.count()-1)

        self.ui.save_setting_pushButton.setEnabled(False)
        self.ui.cancel_setting_pushButton.setEnabled(False)
        self.ui.new_setting_pushButton.setEnabled(True)
        self.ui.edit_setting_pushButton.setEnabled(True)
        self.ui.delete_setting_pushButton.setEnabled(True)
        self.operation = 0

        self.ui.setting_password_lineEdit.setText("***")

        if len(self.ui.setting_listWidget.selectedItems()) == 0:
            self.selected_reagent = None
            return
        
        
        
        name = self.ui.setting_listWidget.itemWidget(self.ui.setting_listWidget.selectedItems()[0]).layout().itemAt(0).widget().text()
        
        self.selected_user = self.db.get_user(name)

        self.ui.setting_username_lineEdit.setText(name)
        if self.selected_user:
            self.ui.comboBox.setCurrentText(USER_TYPES[self.selected_user.type])
        else:
            self.ui.comboBox.setCurrentIndex(3)

    def edit_user(self):
        self.operation = 2

        self.ui.setting_username_lineEdit.setEnabled(True)
        self.ui.comboBox.setEnabled(True)
        self.ui.setting_password_lineEdit.setEnabled(False)

        self.ui.save_setting_pushButton.setEnabled(True)
        self.ui.cancel_setting_pushButton.setEnabled(True)
        self.ui.new_setting_pushButton.setEnabled(False)
        self.ui.edit_setting_pushButton.setEnabled(False)
        self.ui.delete_setting_pushButton.setEnabled(False)

    def new_user(self):


        widget = QWidget()
        layout = QHBoxLayout()
        label1 = QLabel("New User")
        label2 = QLabel("User_Type")
        layout.addWidget(label1)
        layout.addWidget(label2)
        widget.setLayout(layout)
        item = QListWidgetItem()
        self.ui.setting_listWidget.addItem(item)
        self.ui.setting_listWidget.setItemWidget(item, widget)
        self.ui.setting_listWidget.setCurrentRow(self.ui.setting_listWidget.count()-1)

        self.operation = 1
        self.ui.setting_username_lineEdit.setText("")
        self.ui.setting_password_lineEdit.setText("")
        self.ui.comboBox.setCurrentIndex(3)

        self.ui.setting_username_lineEdit.setEnabled(True)
        self.ui.comboBox.setEnabled(True)
        self.ui.setting_password_lineEdit.setEnabled(True)

        self.ui.save_setting_pushButton.setEnabled(True)
        self.ui.cancel_setting_pushButton.setEnabled(True)
        self.ui.new_setting_pushButton.setEnabled(False)
        self.ui.edit_setting_pushButton.setEnabled(False)
        self.ui.delete_setting_pushButton.setEnabled(False)

    def save_user_settings(self):

        if self.operation == 1:
            #boş veri var mı kontrol et
            if self.ui.setting_username_lineEdit.text() == "":
                message_box("Username can not be empty")
                return
            if self.ui.setting_password_lineEdit.text() == "":
                message_box("Password can not be empty")
                return
            
            #aynı isimde kullanıcı var mı kontrol et
            if self.db.get_user(self.ui.setting_username_lineEdit.text()):
                message_box("Username already exists")
                return

            # kendinden daha düşük bir kullanıcı ekleyemez
            if self.main_app.user.type != 0 and self.main_app.user.type >= self.ui.comboBox.currentIndex() :
                message_box("You can not add a user with the same or higher type")
                return
            
            try:
                self.db.add_user(User(self.ui.setting_username_lineEdit.text(), self.ui.setting_password_lineEdit.text(), self.ui.comboBox.currentIndex()))
            except Exception as e:
                message_box("Error: " + str(e))
                return
            
        elif self.operation == 2:
            #boş veri var mı kontrol et
            if self.ui.setting_username_lineEdit.text() == "":
                message_box("Username can not be empty")
                return
            
            #aynı isimde kullanıcı var mı kontrol et
            if self.selected_user.name != self.ui.setting_username_lineEdit.text() and self.db.get_user(self.ui.setting_username_lineEdit.text()):
                message_box("Username already exists")
                return

            # kendinden daha düşük bir kullanıcı ekleyemez
            if  self.main_app.user.type != 0 and self.main_app.user.type >= self.ui.comboBox.currentIndex():
                message_box("You can not add a user with the same or higher type")
                return
            
            try:
                self.db.update_user(self.selected_user, User(self.ui.setting_username_lineEdit.text(), self.ui.setting_password_lineEdit.text(), self.ui.comboBox.currentIndex()))
            except Exception as e:
                message_box("Error: " + str(e))
                return
            
        self.operation = 0
        self.update_user_settings()
        


    def delete_user(self):
        
        # eğer aynı seviyedeki biri ise silemez (kendisini de silemez)
        if self.selected_user.type == self.main_app.user.type:
            message_box("You can not delete a user with the same type")
            return
        
        if self.selected_user:
            if yes_no_message_box("Are you sure you want to delete the user?") == QMessageBox.Yes:
                self.db.delete_user(self.selected_user)
                self.update_user_settings()
                message_box("User deleted successfully")
        

        
        
        

