ACTIONS ={
            "login": "Kullanıcı Girişi",
            "logout": "Kullanıcı Çıkışı",
            "start": "Program Başlatıldı",
            "close": "Program Kapatıldı",
            "open_menu": "Menü Açıldı",
            "close_menu": "Menü Kapatıldı",
            "monitor_page": "Monitör Sayfası açıldı",
            "reagent_page": "Reagent Sayfası açıldı",
            "reagent_define_page": "Reagent Define Sayfası açıldı",
            "card_page": "Card Sayfası açıldı",
            "card_define_page": "Card Define Sayfası açıldı",
            "liquid_page": "Liquid Sayfası açıldı",
            "sample_page": "Sample Sayfası açıldı",
            "layout_page": "Layout Sayfası açıldı",
            "history_page": "History Sayfası açıldı",
            "log_page": "Log Sayfası açıldı",
            "settings_page": "Settings Sayfası açıldı",
            "test_page": "Test Sayfası açıldı",
            "about_page": "About Sayfası açıldı",
            "user_change_page": "Kullanıcı Değiştirme Sayfası açıldı"
        }

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp

class Logger:
    def __init__(self, main_window):
        self.main_window : MyApp = main_window
        self.db = self.main_window.db

    
    def log(self, action, user, details = None):
        if user is None and action == ACTIONS["start"]:
            self.db.insert_log(action, None, None , details)
        elif user is None and action == ACTIONS["monitor_page"]:
            pass
        else:
            self.db.insert_log(action, user.name, user.type , details)