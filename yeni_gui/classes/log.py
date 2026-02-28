from database import Log, USER_TYPES
from classes.logger import ACTIONS

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QCheckBox, QScrollArea
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp

class LogWindow():
    def __init__(self,main_app):
        self.main_app : MyApp = main_app
        self.ui  = self.main_app.ui
        self.db  = self.main_app.db

        #self.ui.user_type_filter_scrrolArea 5 comboboxa sahip
        self.user_name_checkboxes = []
        self.user_type_checkboxes = []
        self.action_checkboxes = []

        self.user_name_list = self.db.get_user_names()
        self.user_type_list = USER_TYPES.values()
        self.action_list = ACTIONS.values()

        self.make_checkboxes(self.user_name_list, self.user_name_checkboxes, self.ui.username_filter_widget)
        self.make_checkboxes(self.user_type_list, self.user_type_checkboxes, self.ui.user_type_filter_widget)
        self.make_checkboxes(self.action_list, self.action_checkboxes, self.ui.action_filter_widget)

        self.ui.filter_time_pushButton.clicked.connect(self.toggle_filter_time)
        self.ui.filter_action_pushButton.clicked.connect(self.toggle_filter_action)
        self.ui.filter_username_pushButton.clicked.connect(self.toggle_filter_username)
        self.ui.filter_user_type_pushButton.clicked.connect(self.toggle_filter_user_type)

        self.ui.filter_log_pushButton.clicked.connect(self.filter_logs)

        self.update()


    def update(self):
        self.ui.end_time_filter_dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.logs: list[Log] = self.db.get_logs()
        self.ui.log_tableWidget.setRowCount(len(self.logs))
        self.fill_log_table()


    def fill_log_table(self):
        for i, log in enumerate(self.logs):
            self.ui.log_tableWidget.setItem(i, 0, QTableWidgetItem(str(log.time)))
            self.ui.log_tableWidget.setItem(i, 1, QTableWidgetItem(str(log.user_name)))
            self.ui.log_tableWidget.setItem(i, 2, QTableWidgetItem(str(log.user_type)))
            self.ui.log_tableWidget.setItem(i, 3, QTableWidgetItem(str(log.action)))
            self.ui.log_tableWidget.setItem(i, 4, QTableWidgetItem(str(log.details)))

    def filter_logs(self):
        start_time = self.ui.start_time_filter_dateTimeEdit.dateTime().toPyDateTime()
        end_time = self.ui.end_time_filter_dateTimeEdit.dateTime().toPyDateTime()

        if self.user_name_checkboxes[0].isChecked():
            selected_user_names = None
        else:
            selected_user_names = [cb.text() for cb in self.user_name_checkboxes if cb.isChecked()]

        if self.user_type_checkboxes[0].isChecked():
            selected_user_types = None
        else:
            selected_user_types = [
                key for key, value in USER_TYPES.items()
                if value in [cb.text() for cb in self.user_type_checkboxes if cb.isChecked()]
            ]

        if self.action_checkboxes[0].isChecked():
            selected_actions = None
        else:
            selected_actions = [cb.text() for cb in self.action_checkboxes if cb.isChecked()]

        filtered_logs = self.db.filter_logs(start_time, end_time, selected_user_names, selected_user_types, selected_actions)

        self.ui.log_tableWidget.setRowCount(len(filtered_logs))
        for i, log in enumerate(filtered_logs):
            self.ui.log_tableWidget.setItem(i, 0, QTableWidgetItem(str(log.time)))
            self.ui.log_tableWidget.setItem(i, 1, QTableWidgetItem(str(log.user_name)))
            self.ui.log_tableWidget.setItem(i, 2, QTableWidgetItem(str(log.user_type)))
            self.ui.log_tableWidget.setItem(i, 3, QTableWidgetItem(str(log.action)))
            self.ui.log_tableWidget.setItem(i, 4, QTableWidgetItem(str(log.details)))

    def make_checkboxes(self, items, checkbox_list : list, widget : QWidget):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        widget.setLayout(layout)

        select_all_cb = QCheckBox("Hepsini Seç")
        select_all_cb.setChecked(True)
        layout.addWidget(select_all_cb)
        checkbox_list.append(select_all_cb)

        for item in items:
            cb = QCheckBox(item)
            cb.setChecked(True)
            layout.addWidget(cb)
            checkbox_list.append(cb)
            cb.stateChanged.connect(lambda state, cb=cb: self.control_checkboxes(checkbox_list, state))
        select_all_cb.stateChanged.connect(lambda state: self.select_all_changed(state, checkbox_list))
       
    def select_all_changed(self, state, checkbox_list, close_only=False):
        for cb in checkbox_list:
            if not close_only or cb.isChecked():
                cb.setChecked(state == Qt.Checked)

    def control_checkboxes(self, checkbox_list, state):
        # eğer hepsi seçili iken biri kapatılırsa hepsini seç kutucuğu kapatılır
        if state == Qt.Unchecked:
            if checkbox_list[0].isChecked():
                checkbox_list[0].blockSignals(True)
                checkbox_list[0].setChecked(False)
                checkbox_list[0].blockSignals(False)
        else:
            #hepsini seç harici hepsi seçili mi kontrol et
            all_checked = all(cb.isChecked() for cb in checkbox_list[1:])
            if all_checked:
                checkbox_list[0].setChecked(True)#

    def toggle_filter_time(self):
        visible = self.ui.filter_time_pushButton.isChecked()
        self.ui.time_filter_scrollArea.setVisible(visible)

    def toggle_filter_username(self):
        visible = self.ui.filter_username_pushButton.isChecked()
        self.ui.username_filter_scrollArea.setVisible(visible)
    
    def toggle_filter_user_type(self):
        visible = self.ui.filter_user_type_pushButton.isChecked()
        self.ui.user_type_filter_scrollArea.setVisible(visible)
    
    def toggle_filter_action(self):
        visible = self.ui.filter_action_pushButton.isChecked()
        self.ui.action_filter_scrollArea.setVisible(visible)
            



        
