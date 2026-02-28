import sys
import os
import hashlib
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "uis"))
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidget
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator, QStandardItemModel, QFont
from PyQt5.uic import loadUi
from uis.main_screen_v2_0_1 import Ui_MainWindow
from uis.giris import Ui_Login as giris_Ui_Form
from classes.settings import SettingsWindow
from classes.reagents import ReagentWindow
from classes.liquid import LiquidWindow
from classes.reagent_define import ReagentDefineWindow
from classes.card import CardWindow
from classes.card_define import CardDefineWindow
from classes.history import HistoryWindow
from classes.log import LogWindow
from classes.sample import SampleWindow
from database import Database , User
from map import load_or_compute
from classes.monitor import IslabGraphicsScene
from classes.logger import Logger, ACTIONS
from classes.layout.layout_page import LayoutPage

from can_sim import CanSimHandler

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp
import time


# from reagentLoad import reagentDefine_MainWindow  # settings_Dialog sınıfını settings.py'den alıyoruz
# import resources_rc  # resources.qrc dosyanızın compile edilmiş hali

# Bu kod en son geliştirilen koddur.

class LoginWindow(QtWidgets.QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.ui = giris_Ui_Form()  # giris.ui dosyasındaki tasarımı kullan
        self.ui.setupUi(self)
        self.db = Database()
        self.ui.lineEdit_username.setText("islab")
        self.ui.lineEdit_password.setText("123")

        self.ui.button_enter.clicked.connect(self.check_pass)
        self.ui.lineEdit_username.setFocus()
        self.main_app : MyApp = main_app

    def check_pass(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()
        
        self.user = self.db.check_user(username, password)
        if self.user:
            self.accept_login()

        else:
            QMessageBox.warning(self, 'Hata', 'Kullanıcı adı veya şifre yanlış.', QMessageBox.Ok)

    def accept_login(self):
        # Ana uygulamayı başlat
        if self.main_app.user is None:
            self.main_app.logger.log(ACTIONS["login"], self.user)
            self.main_app.user = self.user
            self.main_app.showFullScreen()
            self.main_app.show()
            self.close()  # Login penceresini kapat
        # kullanıcı değişikliği yapılacaksa
        else:
            self.main_app.logger.log(ACTIONS["logout"], self.main_app.user)
            self.main_app.logger.log(ACTIONS["login"], self.user)
            self.main_app.user = self.user
            self.close()  # Login penceresini kapat

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.check_pass()
        return super().keyPressEvent(event)
    
    # def show(self): # giriş ekranını atlaması için
    #     super().show()
    #     self.ui.button_enter.click()
    

class MyApp(QMainWindow):
    def __init__(self, user : User):
        super(MyApp, self).__init__()
        # Load the main UI file
        # loadUi('main_screen_v1.0.1.ui', self) # Versiyon isim algoritması: İlk rakam eğer UI layout'u değişirse artacak, ikinci rakam yeni butonlar 
        #fonksiyonellikler katılırsa artacacak, üçüncü rakam olan sistemde sadece küçük değişiklikler yapılması durumunda artacak
        self._user = user

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        with open(os.path.join("yeni_gui", "button_icons.json"), "r") as f:
            self.button_icons = json.load(f)
        for key, value in self.button_icons.items():
            if isinstance(value, list):
                self.button_icons[key] = [os.path.normpath(p) for p in value]
        self.button_icon_size = self.button_icons["icon_size"]

        self.set_lineedit_validators()
        self.define_variables()
        self.connect_buttons()
        self.set_scene_and_graphicsviews()
        self.adjust_table_columns()

        self.logger.log(ACTIONS["start"], self.user)

        self.login_window = LoginWindow(self)
        self.login_window.show()


        self.selected_page_button = self.ui.monitor_toolButton
        self.ui.monitor_toolButton.click()

        self.pipette_arbitration_id = 0x01
        self.reagent_0_arbitration_id = 0x02
        self.reagent_1_arbitration_id = 0x03
        self.sample_0_arbitration_id = 0x04
        self.sample_1_arbitration_id = 0x05
        self.sample_2_arbitration_id = 0x06

    @property
    def user(self):
        return self._user
    
    @user.setter
    #user type 3 ise sadece izleme ekranına erişebilir
    def user(self, user):
        if user is None:
            return
        if user.type == 3:
            self.ui.settings_toolButton.setEnabled(False)
            self.ui.reagentDefine_toolButton.setEnabled(False)
            self.ui.cardDefine_toolButton.setEnabled(False)
            self.ui.layout_toolButton.setEnabled(False)     
            self.ui.liquid_toolButton.setEnabled(False)  
            self.ui.log_toolButton.setEnabled(False)     

        else:
            self.ui.settings_toolButton.setEnabled(True)
            self.ui.reagentDefine_toolButton.setEnabled(True)
            self.ui.cardDefine_toolButton.setEnabled(True)
            self.ui.layout_toolButton.setEnabled(True)
            self.ui.liquid_toolButton.setEnabled(True)  
            self.ui.log_toolButton.setEnabled(True)
        self._user = user
        self.ui.monitor_toolButton.click()
            


    def define_variables(self):
        self.db = Database()
        self.logger = Logger(self)

        self.settings_window = SettingsWindow(self)
        self.reagent_window = ReagentWindow(self)
        self.card_window = CardWindow(self)
        self.card_define_window = CardDefineWindow(self)
        self.liquid_window = LiquidWindow(self)
        self.reagent_define_window = ReagentDefineWindow(self)
        self.history_window = HistoryWindow(self)
        self.log_window = LogWindow(self)
        self.sample_window = SampleWindow(self)

        self.can_sim = CanSimHandler()
        self.can_sim.message_received.connect(self.can_message_received)
    #     self.can_sim.message_received.connect(self.can_position_received)

    # def can_position_received(self, position):
    #     self.scene.change_reagent_position(0, position[0])
    #     self.scene.change_crosshair_position(position[1], position[2])

    def connect_buttons(self):
        self.ui.menu_toolButton.clicked.connect(self.menu_ac_kapa)
        self.ui.pushButton_exit.clicked.connect(self.exit)
        self.ui.simulation.clicked.connect(self.start_simulation)

        self.ui.monitor_toolButton.clicked.connect(lambda: (self.ui.stackedWidget.setCurrentWidget(self.ui.monitor_page),
                                                            self.active_page_changed(self.ui.monitor_toolButton),
                                                            self.logger.log(ACTIONS["monitor_page"], self.user)))
        self.ui.settings_toolButton.clicked.connect(lambda:(self.settings_window.update(),
                                                            self.ui.stackedWidget.setCurrentWidget(self.ui.settings_page),
                                                            self.active_page_changed(self.ui.settings_toolButton),
                                                            self.logger.log(ACTIONS["settings_page"], self.user)))
        self.ui.history_toolButton.clicked.connect(lambda: (self.ui.stackedWidget.setCurrentWidget(self.ui.history_page),
                                                            self.active_page_changed(self.ui.history_toolButton),
                                                            self.logger.log(ACTIONS["history_page"], self.user)))
        self.ui.card_toolButton.clicked.connect(lambda: (   self.card_window.update(),
                                                            self.ui.stackedWidget.setCurrentWidget(self.ui.card_page),
                                                            self.active_page_changed(self.ui.card_toolButton),
                                                            self.logger.log(ACTIONS["card_page"], self.user)))
        self.ui.reagentDefine_toolButton.clicked.connect(lambda: (  self.reagent_define_window.update(),
                                                                    self.ui.stackedWidget.setCurrentWidget(self.ui.reagent_define_page),
                                                                    self.active_page_changed(self.ui.reagentDefine_toolButton),
                                                                    self.logger.log(ACTIONS["reagent_define_page"], self.user)))
        self.ui.reagent_toolButton.clicked.connect(lambda: (self.reagent_window.update(),
                                                            self.ui.stackedWidget.setCurrentWidget(self.ui.reagent_page),
                                                            self.active_page_changed(self.ui.reagent_toolButton),
                                                            self.logger.log(ACTIONS["reagent_page"], self.user)))
        self.ui.liquid_toolButton.clicked.connect(lambda: ( self.liquid_window.update(),
                                                            self.ui.stackedWidget.setCurrentWidget(self.ui.liquid_page),
                                                            self.active_page_changed(self.ui.liquid_toolButton),
                                                            self.logger.log(ACTIONS["liquid_page"], self.user)))
        self.ui.cardDefine_toolButton.clicked.connect(lambda: ( self.card_define_window.update(),
                                                                self.ui.stackedWidget.setCurrentWidget(self.ui.card_define_page),
                                                                self.active_page_changed(self.ui.cardDefine_toolButton),
                                                                self.logger.log(ACTIONS["card_define_page"], self.user)))
        self.ui.pushButton_user_change.clicked.connect(lambda: (self.login_window.setWindowModality(QtCore.Qt.ApplicationModal),
                                                                self.login_window.show(),
                                                                self.logger.log(ACTIONS["user_change_page"], self.user)))
        self.ui.layout_toolButton.clicked.connect(lambda: ( self.ui.stackedWidget.setCurrentWidget(self.ui.layout_page),
                                                            self.active_page_changed(self.ui.layout_toolButton),
                                                            self.logger.log(ACTIONS["layout_page"], self.user)))
        self.ui.about_toolButton.clicked.connect(lambda: (  self.ui.stackedWidget.setCurrentWidget(self.ui.about_page),
                                                            self.active_page_changed(self.ui.about_toolButton),
                                                            self.logger.log(ACTIONS["about_page"], self.user)))
        self.ui.sample_toolButton.clicked.connect(lambda: ( self.ui.stackedWidget.setCurrentWidget(self.ui.sample_page),
                                                            self.active_page_changed(self.ui.sample_toolButton),
                                                            self.logger.log(ACTIONS["sample_page"], self.user)))
        self.ui.test_toolButton.clicked.connect(lambda: ( self.ui.stackedWidget.setCurrentWidget(self.ui.test_page),
                                                            self.active_page_changed(self.ui.test_toolButton),
                                                            self.logger.log(ACTIONS["test_page"], self.user)))
        self.ui.log_toolButton.clicked.connect(lambda: ( self.log_window.update(),
                                                            self.ui.stackedWidget.setCurrentWidget(self.ui.log_page),
                                                            self.active_page_changed(self.ui.log_toolButton),
                                                            self.logger.log(ACTIONS["log_page"], self.user)))

    def start_simulation(self):
        # ==================== HIZ ÇARPANI AYARI ====================
        # 1.0 = normal hız
        # 2.0 = 2 kat hızlı
        # 5.0 = 5 kat hızlı
        # 0.5 = yarı hızda (yavaş)
        # İstediğiniz değeri buradan değiştirebilirsiniz:
        self.scene.pipette.speed_multiplier = 1.0
        # ===========================================================

        #self.scene.pipette.move_to(100, 50)
        #self.scene.pipette.move_to(200, 400)
        #self.scene.pipette.move_to(300, 200)

        #self.scene.pipette.move_to(*self.scene.reagent_0.get_reagent_index_position(0))
        #self.scene.pipette.move_to(*self.scene.reagent_1.get_reagent_index_position(4))


        #self.scene.pipette.move_to(25, 210) # reagent0 top
        #self.scene.pipette.aspirate(1000)
        #self.scene.pipette.move_to(25, 594) # reagent0 bottom
        #self.scene.pipette.dispense(100)
#
        #self.scene.pipette.move_to(80, 208) # reagent1 top
        #self.scene.pipette.dispense(100)
        #self.scene.pipette.move_to(80, 592) # reagent1 bottom
        #self.scene.pipette.dispense(800)
#
        #self.scene.pipette.move_to(140, 32) # sample0 top
        #self.scene.pipette.move_to(141, 592) # sample0 bottom
#
        #self.scene.pipette.move_to(180, 34) # sample1 top
        #self.scene.pipette.move_to(181, 592) # sample1 bottom
#
        #self.scene.pipette.move_to(226, 38) # sample2 top
        #self.scene.pipette.move_to(226, 589) # sample2 bottom
#
        #self.scene.pipette.move_to(309, 69) # liss
        #self.scene.pipette.move_to(409, 69) # bromelin
#
        #self.scene.pipette.move_to(282, 153) # dilute0 top left
        #self.scene.pipette.move_to(405, 153) # dilute0 top right
        #self.scene.pipette.move_to(282, 345) # dilute0 bottom left
#
        #self.scene.pipette.move_to(283, 414) # dilute1 top left
        #self.scene.pipette.move_to(405, 414) # dilute1 top right
        #self.scene.pipette.move_to(282, 610) # dilute1 bottom left
#
        #self.scene.pipette.move_to(520, -18) # card0 top left
        #self.scene.pipette.move_to(820, -19) # card0 top rigth
        #self.scene.pipette.move_to(520, 121) # card0 bottom left
#
        #self.scene.pipette.move_to(520, 181) # card1 top left
        #self.scene.pipette.move_to(820, 181) # card1 top rigth
        #self.scene.pipette.move_to(520, 320) # card1 bottom left
#
        #self.scene.pipette.move_to(520, 381) # card2 top left
        #self.scene.pipette.move_to(820, 381) # card2 top rigth
        #self.scene.pipette.move_to(520, 520) # card2 bottom left
#
        #self.scene.pipette.move_to(520, 581) # card3 top left
        #self.scene.pipette.move_to(820, 581) # card3 top rigth
        #self.scene.pipette.move_to(520, 720) # card3 bottom left

        maps = load_or_compute()
        self.scene.pipette.move_to(*maps["liss"])
        self.scene.pipette.aspirate(1200)
        # ================== Put liss into dilute plate =======================
        for i in range(12):

            self.scene.pipette.move_to(*maps["d1"][i // 8, i % 8])
            self.scene.pipette.dispense(100)


        # =============== Prepare solution and place onto jel cards ====================
        for i in range(12):
            # Aspirate sample from sample plate
            self.scene.pipette.move_to(*maps["s1"][i])
            self.scene.pipette.aspirate(100)

            # Dispense sample into dilute plate
            self.scene.pipette.move_to(*maps["d1"][i // 8, i % 8])
            self.scene.pipette.dispense(100)

            # Mix the solution
            self.scene.pipette.aspirate(100)
            self.scene.pipette.dispense(100)
            self.scene.pipette.aspirate(100)
            self.scene.pipette.dispense(100)
            self.scene.pipette.aspirate(1000)

            # Dispense sample onto jel cards
            for j in range(8):
                self.scene.pipette.move_to(*maps["c1"][i, j])
                self.scene.pipette.dispense(1000/8)


            # Wash the pipette
            self.scene.pipette.move_to(*maps["wash"])
            self.scene.pipette.aspirate(500)
            self.scene.pipette.dispense(500)
            self.scene.pipette.aspirate(500)
            self.scene.pipette.dispense(500)

        
    def menu_ac_kapa(self):
        page_buttons = self.ui.page_buttons_menu.findChildren(QtWidgets.QToolButton)
        for button in page_buttons:
            if button.toolButtonStyle() == QtCore.Qt.ToolButtonIconOnly:
                button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
                button.setStyleSheet("padding-right: 0px")
            elif button.toolButtonStyle() == QtCore.Qt.ToolButtonTextBesideIcon:
                button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
                button.setStyleSheet("padding-right: 15px")

    def active_page_button(self, button):
        self.selected_page_button.setProperty("active", False)
        try:
            icon_path = self.button_icons[self.selected_page_button.objectName()][0]
            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
            self.selected_page_button.setIcon(icon)
            self.selected_page_button.setIconSize(QtCore.QSize(self.button_icon_size, self.button_icon_size))
        except KeyError:
            pass
        self.selected_page_button.style().unpolish(self.selected_page_button)
        self.selected_page_button.style().polish(self.selected_page_button)
        self.selected_page_button = button
        self.selected_page_button.setProperty("active", True)
        try:
            icon_path = self.button_icons[self.selected_page_button.objectName()][1]
            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
            self.selected_page_button.setIcon(icon)
            self.selected_page_button.setIconSize(QtCore.QSize(self.button_icon_size, self.button_icon_size))
        except KeyError:
            pass
        self.selected_page_button.style().unpolish(self.selected_page_button)
        self.selected_page_button.style().polish(self.selected_page_button)

    def active_page_changed(self, button):
        self.active_page_button(button)
        self.update_menu_scene(self.ui.stackedWidget.currentWidget())

    def update_menu_scene(self, page):
        if page == self.ui.monitor_page:
            self.ui.menu_graphics_view_frame.hide()
            self.ui.menu_graphicsView_2.hide()
            self.scene.all_visible()
        elif page == self.ui.reagent_page:
            self.ui.menu_graphics_view_frame.show()
            self.ui.menu_graphicsView.setMinimumWidth(120)
            self.ui.menu_graphicsView.setMaximumWidth(120)
            self.ui.menu_graphicsView.centerOn(60, 350)
            self.ui.menu_graphicsView_2.show()
            self.ui.menu_graphicsView_2.setMinimumWidth(210)
            self.ui.menu_graphicsView_2.setMaximumWidth(210)
            self.ui.menu_graphicsView_2.centerOn(355, 350)
            self.scene.only_visible(("reagent", "dilute"))
        elif page == self.ui.card_page:
            self.ui.menu_graphics_view_frame.show()
            self.ui.menu_graphicsView.setMinimumWidth(405)
            self.ui.menu_graphicsView.setMaximumWidth(405)
            self.ui.menu_graphicsView.centerOn(675, 310)
            self.ui.menu_graphicsView_2.hide()
            self.scene.only_visible("card")
        elif page == self.ui.sample_page:
            self.ui.menu_graphics_view_frame.show()
            self.ui.menu_graphicsView.setMinimumWidth(150)
            self.ui.menu_graphicsView.setMaximumWidth(150)
            self.ui.menu_graphicsView.centerOn(190, 350)
            self.ui.menu_graphicsView_2.hide()
            self.scene.only_visible("sample")
        elif page == self.ui.settings_page:
            self.ui.menu_graphics_view_frame.hide()
        elif page == self.ui.reagent_define_page:
            self.ui.menu_graphics_view_frame.hide()
        elif page == self.ui.settings_page:
            self.ui.menu_graphics_view_frame.hide()
        elif page == self.ui.history_page:
            self.ui.menu_graphics_view_frame.hide()
        elif page == self.ui.liquid_page:
            self.ui.menu_graphics_view_frame.hide()
        elif page == self.ui.card_define_page:
            self.ui.menu_graphics_view_frame.hide()
        elif page == self.ui.layout_page:
            self.ui.menu_graphics_view_frame.hide()
            self.layout_page.on_page_shown()
        elif page == self.ui.about_page:
            self.ui.menu_graphics_view_frame.hide()
        elif page == self.ui.test_page:
            self.ui.menu_graphics_view_frame.hide()
            self.scene.all_visible()


        if page == self.ui.test_page:
            print(self.ui.groupBox_8.size())
            print(self.ui.reagent_1_test_set_pushButton.size())


    def set_scene_and_graphicsviews(self):
        self.scene = IslabGraphicsScene(main_app=self)
        self.scene.reagent_id_single_click_signal.connect(self.reagent_id_signal)
        self.scene.reagent_id_double_click_signal.connect(self.reagent_double_click)
        self.scene.card_id_double_click_signal.connect(self.card_double_click)
        self.scene.sample_id_double_click_signal.connect(self.sample_double_click)
        self.scene.liss_double_click_signal.connect(self.liss_double_click)

        self.ui.monitor_graphicsView.setScene(self.scene)
        self.ui.monitor_graphicsView.setMouseTracking(True)
        self.ui.monitor_graphicsView.centerOn(300, 350)
        self.ui.monitor_graphicsView.wheelEvent = lambda event: event.ignore()

        self.ui.menu_graphicsView.setScene(self.scene)
        self.ui.menu_graphicsView.setMouseTracking(True)
        self.ui.menu_graphicsView.wheelEvent = lambda event: event.ignore()

        self.ui.menu_graphicsView_2.setScene(self.scene)
        self.ui.menu_graphicsView_2.setMouseTracking(True)
        self.ui.menu_graphicsView_2.wheelEvent = lambda event: event.ignore()

        self.ui.layout_graphicsView.setScene(self.scene)
        self.ui.layout_graphicsView.setMouseTracking(True)
        self.ui.layout_graphicsView.scale(0.8, 0.8)
        self.ui.layout_graphicsView.centerOn(650, 370)
        self.ui.layout_graphicsView.wheelEvent = lambda event: event.ignore()

        self.ui.test_graphicsView.setScene(self.scene)
        self.ui.test_graphicsView.setMouseTracking(True)
        self.ui.test_graphicsView.wheelEvent = lambda event: event.ignore()
        self.ui.test_graphicsView.scale(0.9, 0.9)
        self.ui.test_graphicsView.centerOn(400, 400)


        self.reagent_window.reagent_monitor_update_signal.connect(self.scene.update_reagent)

        self.layout_page = LayoutPage(self)

    def set_lineedit_validators(self):
        int_validator = QIntValidator(0, 10000, self)
        self.ui.layout_x_lineedit.setValidator(int_validator)
        self.ui.layout_y_lineedit.setValidator(int_validator)
        self.ui.layout_z_lineedit.setValidator(int_validator)

    def adjust_table_columns(self):
        history_table_column_stretch = [2,2,2,3,1,1,1]
        history_table_column_width = 80
        for i, stretch in enumerate(history_table_column_stretch):
            # self.ui.history_page_tableWidget.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            # self.ui.history_page_tableWidget.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            self.ui.history_page_tableWidget.setColumnWidth(i, stretch * history_table_column_width)

        ###### SAMPLE SAYFASINA TAŞINDI, HISTORY DE KENDİ SAYFASINA TAŞINACAK
        # sample_table_column_stretch = [1,1]
        # sample_table_column_width = 500
        # for table in self.ui.sample_tabWidget.findChildren(QtWidgets.QTableWidget):
        #     for i, stretch in enumerate(sample_table_column_stretch):
        #         table.setColumnWidth(i, stretch * sample_table_column_width)

    def can_message_received(self, message):
        arbitration_id = message[0]
        if arbitration_id == self.reagent_0_arbitration_id:
            self.scene.change_reagent_position(0, message[1])
            self.ui.reagent_1_current_value_label.setText(str(message[1]))
        elif arbitration_id == self.reagent_1_arbitration_id:
            self.scene.change_reagent_position(1, message[1])
            self.ui.reagent_2_current_value_label.setText(str(message[1]))
        elif arbitration_id == self.sample_0_arbitration_id:
            self.scene.change_sample_position(0, message[1])
            self.ui.sample_1_current_value_label.setText(str(message[1]))
        elif arbitration_id == self.sample_1_arbitration_id:
            self.scene.change_sample_position(1, message[1])
            self.ui.sample_2_current_value_label.setText(str(message[1]))
        elif arbitration_id == self.sample_2_arbitration_id:
            self.scene.change_sample_position(2, message[1])
            self.ui.sample_3_current_value_label.setText(str(message[1]))
        elif arbitration_id == self.pipette_arbitration_id:
            self.scene.change_pipette_position(message[1])
            self.ui.pipette_current_value_label.setText(str(message[1]))


    def reagent_id_signal(self, id):
        # print(id)
        pass

    def reagent_double_click(self, list):
        reagent_section = list[0]
        reagent_id = list[1]
        ##############
        if reagent_section == 1 and reagent_id == 3:
            self.can_sim.start_can_sim()
        elif reagent_section == 1 and reagent_id == 4:
            self.can_sim.stop()
        ##############
        if self.ui.stackedWidget.currentWidget() == self.ui.layout_page:
            
            layout = self.db.get_layout("Reagent" ,reagent_section)
            if layout:
                self.layout_page.fill_layout_popup(layout, reagent_id)

        elif self.ui.stackedWidget.currentWidget() == self.ui.reagent_page:
            self.ui.rs_tabWidget.setCurrentIndex(reagent_section)
            table_widget = self.ui.rs_tabWidget.currentWidget().findChild(QtWidgets.QTableWidget)
            table_widget.selectRow(reagent_id)
            table_widget.setCurrentCell(reagent_id, 1)
            table_item = table_widget.item(reagent_id, 1)
            if table_item is None:
                table_item = QtWidgets.QTableWidgetItem()
                table_widget.setItem(reagent_id, 1, table_item)
            table_widget.editItem(table_item)

    def card_double_click(self, list):
        card_section = list[0]
        card_id = list[1]

        print(card_section, card_id)

        if self.ui.stackedWidget.currentWidget() == self.ui.card_page:
            self.ui.card_page_tabWidget.setCurrentIndex(card_section)
            table_widget = self.ui.card_page_tabWidget.currentWidget().findChild(QtWidgets.QTableWidget)
            table_widget.selectRow(card_id)
            table_widget.setCurrentCell(card_id, 0)
            table_item = table_widget.item(card_id, 0)
            if table_item is None:
                table_item = QtWidgets.QTableWidgetItem()
                table_widget.setItem(card_id, 0, table_item)
            table_widget.editItem(table_item)

        elif self.ui.stackedWidget.currentWidget() == self.ui.layout_page:
            layout = self.db.get_layout("Card", card_section)
            if layout:
                pass

    def sample_double_click(self, list):
        sample_section = list[0]
        sample_id = list[1]

        if self.ui.stackedWidget.currentWidget() == self.ui.sample_page:
            self.ui.sample_tabWidget.setCurrentIndex(sample_section)
            table_widget = self.ui.sample_tabWidget.currentWidget().findChild(QtWidgets.QTableWidget)
            table_widget.selectRow(sample_id)
            # table_widget.setCurrentCell(sample_id, 0)
            # table_item = table_widget.item(sample_id, 0)
            # if table_item is None:
            #     table_item = QtWidgets.QTableWidgetItem()
            #     table_widget.setItem(sample_id, 0, table_item)
            # table_widget.editItem(table_item)

        elif self.ui.stackedWidget.currentWidget() == self.ui.layout_page:
            layout = self.db.get_layout("Sample", sample_section)
            if layout:
                self.layout_page.fill_layout_popup(layout, sample_id)

    def liss_double_click(self, id):
        if self.ui.stackedWidget.currentWidget() == self.ui.reagent_page:
            table_widget = self.ui.liss_tabWidget.currentWidget().findChild(QtWidgets.QTableWidget)
            table_widget.selectRow(id)
            table_widget.setCurrentCell(id, 1)
            table_item = table_widget.item(id, 1)
            if table_item is None:
                table_item = QtWidgets.QTableWidgetItem()
                table_widget.setItem(id, 1, table_item)
            table_widget.editItem(table_item)
        
        elif self.ui.stackedWidget.currentWidget() == self.ui.layout_page:
            layout = self.db.get_layout("Liss", 0)
            if layout:
                self.layout_page.fill_layout_popup(layout, id)

    def exit(self):
        self.logger.log(ACTIONS["close"], self.user)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if sys.platform.startswith("linux"):
        QFont.insertSubstitution("Calibri", "DejaVu Sans")
        QFont.insertSubstitution("Arial", "DejaVu Sans")

    MainApp = MyApp(None)
    sys.exit(app.exec_())
