from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTreeWidgetItem

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp

COLOR_UNSAVED = QColor(220, 50, 50)
COLOR_SAVED = QColor(50, 180, 50)


class LayoutButtonHandler:
    """
    Layout sayfasındaki butonların (yön, init, save, mix, flush)
    fonksiyonlarını yönetir. Şimdilik terminale veri basar,
    sonrasında CAN bus ile veri göndermek için genişletilecek.
    """

    STEP_RADIO_MAP = {
        "layout_1_radioButton": 1,
        "layout_2_radioButton": 2,
        "layout_5_radioButton": 5,
        "layout_10_radioButton": 10,
        "layout_20_radioButton": 20,
        "layout_50_radioButton": 50,
        "layout_100_radioButton": 100,
        "layout_200_radioButton": 200,
        "layout_500_radioButton": 500,
    }

    def __init__(self, main_app: "MyApp"):
        self.main_app = main_app
        self.ui = main_app.ui
        self._saved_items: set[int] = set()
        self._connect_buttons()
        self._init_tree_colors()

    def _connect_buttons(self):
        ui = self.ui

        # Yön butonları
        ui.layout_left_toolButton.clicked.connect(lambda: self._move("X", -1))
        ui.layout_right_toolButton.clicked.connect(lambda: self._move("X", 1))
        ui.layout_front_toolButton.clicked.connect(lambda: self._move("Y", 1))
        ui.layout_back_toolButton.clicked.connect(lambda: self._move("Y", -1))
        ui.layout_up_toolButton.clicked.connect(lambda: self._move("Z", -1))
        ui.layout_down_toolButton.clicked.connect(lambda: self._move("Z", 1))

        # Init butonları
        ui.layout_init_x_pushButton.clicked.connect(lambda: self._init_axis("X"))
        ui.layout_init_y_pushButton.clicked.connect(lambda: self._init_axis("Y"))
        ui.layout_init_z_pushButton.clicked.connect(lambda: self._init_axis("Z"))

        # Save butonları
        ui.layout_save_as_first_pushButton.clicked.connect(lambda: self._save("First"))
        ui.layout_save_as_last_pushButton.clicked.connect(lambda: self._save("Last"))
        ui.layout_save_as_travel_pushButton.clicked.connect(lambda: self._save("Travel"))
        ui.layout_save_as_zcan_pushButton.clicked.connect(lambda: self._save("Zscan"))
        ui.layout_save_as_zmax_pushButton.clicked.connect(lambda: self._save("Zmax"))
        ui.layout_save_as_zdisp_pushButton.clicked.connect(lambda: self._save("ZDisp"))
        ui.layout_save_as_zmax_pushButton_2.clicked.connect(self._save_general)

        # Mix butonları
        ui.layout_start_mix_pushButton.clicked.connect(self._start_mix)
        ui.layout_stop_mix_pushButton.clicked.connect(self._stop_mix)

        # Flush
        ui.layout_flush_tip_pushButton.clicked.connect(self._flush_tip)

    # ──────────── TreeWidget renk yönetimi ────────────

    def _init_tree_colors(self):
        """Tüm treeWidget öğelerini kırmızı olarak işaretler."""
        tree = self.ui.treeWidget
        for i in range(tree.topLevelItemCount()):
            self._set_color_recursive(tree.topLevelItem(i), COLOR_UNSAVED)

    @staticmethod
    def _set_color_recursive(item: QTreeWidgetItem, color: QColor):
        item.setForeground(0, color)
        for i in range(item.childCount()):
            LayoutButtonHandler._set_color_recursive(item.child(i), color)

    def _mark_item_saved(self, item: QTreeWidgetItem):
        """Öğeyi yeşile boyar ve üst öğelerin rengini günceller."""
        self._saved_items.add(id(item))
        item.setForeground(0, COLOR_SAVED)
        self._update_ancestors(item)

    def _update_ancestors(self, item: QTreeWidgetItem):
        """Üst öğeleri kontrol eder: tüm çocuklar yeşilse yeşil, değilse kırmızı."""
        parent = item.parent()
        while parent is not None:
            if self._all_leaves_saved(parent):
                parent.setForeground(0, COLOR_SAVED)
            else:
                parent.setForeground(0, COLOR_UNSAVED)
            parent = parent.parent()

    def _all_leaves_saved(self, item: QTreeWidgetItem) -> bool:
        """Verilen öğenin altındaki tüm yaprakların kaydedilip kaydedilmediğini kontrol eder."""
        if item.childCount() == 0:
            return id(item) in self._saved_items
        return all(
            self._all_leaves_saved(item.child(i))
            for i in range(item.childCount())
        )

    # ──────────── Yardımcı metodlar ────────────

    def get_step_size(self) -> int:
        """Seçili radio button'dan adım büyüklüğünü döndürür."""
        for name, value in self.STEP_RADIO_MAP.items():
            radio = getattr(self.ui, name)
            if radio.isChecked():
                return value
        if self.ui.layout_other_radioButton.isChecked():
            try:
                return int(self.ui.layout_other_lineedit.text())
            except ValueError:
                return 0
        return 50

    def _get_positions(self):
        """X, Y, Z lineedit'lerden mevcut pozisyonları okur."""
        try:
            x = int(self.ui.layout_x_lineedit.text())
        except ValueError:
            x = 0
        try:
            y = int(self.ui.layout_y_lineedit.text())
        except ValueError:
            y = 0
        try:
            z = int(self.ui.layout_z_lineedit.text())
        except ValueError:
            z = 0
        return x, y, z

    def _set_position(self, axis: str, value: int):
        """Belirtilen eksenin lineedit'ini günceller."""
        lineedit = getattr(self.ui, f"layout_{axis.lower()}_lineedit")
        lineedit.setText(str(value))

    # ──────────── Buton handler'ları ────────────

    def _move(self, axis: str, direction: int):
        """Yön butonlarına basıldığında çağrılır."""
        step = self.get_step_size()
        x, y, z = self._get_positions()
        positions = {"X": x, "Y": y, "Z": z}
        new_value = positions[axis] + direction * step
        self._set_position(axis, new_value)
        print(f"[Layout] Move {axis} {'+'if direction > 0 else ''}{direction * step}  ->  {axis}={new_value}")
        # TODO: CAN bus ile motora hareket komutu gönder

    def _init_axis(self, axis: str):
        """Init butonlarına basıldığında ekseni sıfırlar."""
        self._set_position(axis, 0)
        print(f"[Layout] Init {axis} -> 0")
        # TODO: CAN bus ile motora init komutu gönder

    def _save(self, save_type: str):
        """Save butonlarına basıldığında mevcut pozisyonu kaydeder."""
        x, y, z = self._get_positions()
        print(f"[Layout] Save As {save_type}  ->  X={x}, Y={y}, Z={z}")
        # TODO: Veritabanına veya layout popup'a kaydet

    def _get_selected_item_name(self) -> str | None:
        """TreeWidget'te seçili olan öğenin tam yol adını döndürür.
        Örn: 'Dilution > Dilution 1 > Top Left'
        Seçili öğe yoksa None döner."""
        items = self.ui.treeWidget.selectedItems()
        if not items:
            return None
        item = items[0]
        parts = []
        current = item
        while current is not None:
            parts.append(current.text(0))
            current = current.parent()
        parts.reverse()
        return " > ".join(parts)

    def _save_general(self):
        """TreeWidget'te seçili olan yaprak öğenin X, Y, Z pozisyonunu kaydeder."""
        items = self.ui.treeWidget.selectedItems()
        if not items:
            print("[Layout] Save General  ->  Hiçbir öğe seçili değil!")
            return
        item = items[0]
        if item.childCount() > 0:
            print(f"[Layout] Save General  ->  '{item.text(0)}' bir üst öğe, sadece yaprak öğeler kaydedilebilir!")
            return
        selected = self._get_selected_item_name()
        x, y, z = self._get_positions()
        print(f"[Layout] Save General '{selected}'  ->  X={x}, Y={y}, Z={z}")
        self._mark_item_saved(item)
        # TODO: Seçili öğenin pozisyonunu veritabanına kaydet

    def _start_mix(self):
        """Mix başlatır."""
        print("[Layout] Start Mix")
        # TODO: CAN bus ile mix komutu gönder

    def _stop_mix(self):
        """Mix durdurur."""
        print("[Layout] Stop Mix")
        # TODO: CAN bus ile mix durdur komutu gönder

    def _flush_tip(self):
        """Tip yıkama işlemi başlatır."""
        flush_time = self.ui.layout_flush_time_spinBox.value()
        print(f"[Layout] Flush Tip  ->  Süre: {flush_time}s")
        # TODO: CAN bus ile flush komutu gönder
