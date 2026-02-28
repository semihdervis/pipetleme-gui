from PyQt5 import QtCore, QtWidgets
from uis.layout_popup import Ui_Dialog as LayoutPopupDialog
from database import Database, Layout
from classes.layout.arrow_functions import ArrowManager
from classes.layout.button_functions import LayoutButtonHandler

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp


class LayoutPage:
    """
    Layout sayfasının ana fonksiyonlarını barındırır.
    Popup penceresi, ok işaretçisi, buton bağlantıları ve
    save/fill işlemleri bu sınıf üzerinden yönetilir.
    """

    def __init__(self, main_app: "MyApp"):
        self.main_app = main_app
        self.ui = main_app.ui
        self.db: Database = main_app.db

        self._setup_popup()
        self.arrow_manager = ArrowManager(main_app.scene, self.ui.treeWidget)
        self.button_handler = LayoutButtonHandler(main_app)

    def _setup_popup(self):
        self.popup_window = QtWidgets.QDialog(
            self.main_app,
            QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowCloseButtonHint,
        )
        self.popup_dialog = LayoutPopupDialog()
        self.popup_dialog.setupUi(self.popup_window)
        self.popup_dialog.cancel_pushButton.clicked.connect(self.popup_window.close)
        self.popup_dialog.ok_pushButton.clicked.connect(self.save_layout)

    # ──────────── Sayfa gösterildiğinde ────────────

    def on_page_shown(self):
        """Layout sayfası aktif olduğunda çağrılır."""
        self.ui.layout_graphicsView.centerOn(450, 370)
        self.main_app.scene.all_visible()
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            self.ui.treeWidget.expandItem(self.ui.treeWidget.topLevelItem(i))

    # ──────────── Layout kaydetme ────────────

    def save_layout(self):
        layout = Layout()
        rack_name, rack_id = self.popup_dialog.rack_name_lineEdit.text().split(" ")
        layout.rack_name = rack_name
        layout.rack_id = int(rack_id) - 1

        layout.x_pos = self.popup_dialog.x_spinBox.value()
        layout.y_pos = self.popup_dialog.y_spinBox.value()
        layout.width = self.popup_dialog.width_spinBox.value()
        layout.height = self.popup_dialog.height_spinBox.value()
        layout.row_count = self.popup_dialog.row_spinBox.value()
        layout.column_count = self.popup_dialog.col_spinBox.value()

        layout.first_hole_x = self.popup_dialog.first_hole_x_spinBox.value()
        layout.first_hole_y = self.popup_dialog.first_hole_y_spinBox.value()
        layout.first_hole_z = self.popup_dialog.first_hole_z_spinBox.value()
        layout.last_hole_x = self.popup_dialog.last_hole_x_spinBox.value()
        layout.last_hole_y = self.popup_dialog.last_hole_y_spinBox.value()
        layout.last_hole_z = self.popup_dialog.last_hole_z_spinBox.value()

        layout.z_travel = self.popup_dialog.z_travel_spinBox.value()
        layout.z_scan = self.popup_dialog.z_scan_spinBox.value()
        layout.z_disp = self.popup_dialog.z_disp_spinBox.value()
        layout.z_max = self.popup_dialog.z_max_spinBox.value()
        layout.description = self.popup_dialog.description_lineEdit.text()

        self.db.update_layout(layout)
        print("layout güncellendi")
        self.popup_window.close()

    # ──────────── Layout popup doldurma ────────────

    def fill_layout_popup(self, layout: Layout, hole_id: int):
        dlg = self.popup_dialog

        dlg.rack_name_lineEdit.setText(f"{layout.rack_name} {layout.rack_id + 1}")
        dlg.description_lineEdit.setText(layout.description or "")

        dlg.x_spinBox.setValue(layout.x_pos or 0)
        dlg.y_spinBox.setValue(layout.y_pos or 0)
        dlg.width_spinBox.setValue(layout.width or 0)
        dlg.height_spinBox.setValue(layout.height or 0)
        dlg.row_spinBox.setValue(layout.row_count or 0)
        dlg.col_spinBox.setValue(layout.column_count or 0)

        dlg.first_hole_x_spinBox.setValue(layout.first_hole_x or 0)
        dlg.first_hole_y_spinBox.setValue(layout.first_hole_y or 0)
        dlg.first_hole_z_spinBox.setValue(layout.first_hole_z or 0)
        dlg.last_hole_x_spinBox.setValue(layout.last_hole_x or 0)
        dlg.last_hole_y_spinBox.setValue(layout.last_hole_y or 0)
        dlg.last_hole_z_spinBox.setValue(layout.last_hole_z or 0)

        dlg.z_travel_spinBox.setValue(layout.z_travel or 0)
        dlg.z_scan_spinBox.setValue(layout.z_scan or 0)
        dlg.z_disp_spinBox.setValue(layout.z_disp or 0)
        dlg.z_max_spinBox.setValue(layout.z_max or 0)

        if layout.column_count == 1:
            diff_x = 0
        else:
            diff_x = (layout.last_hole_x - layout.first_hole_x) // (layout.column_count - 1)

        if layout.row_count == 1:
            diff_y = 0
        else:
            diff_y = (layout.last_hole_y - layout.first_hole_y) // (layout.row_count - 1)

        diff_z = layout.last_hole_z - layout.first_hole_z
        current_hole_x = layout.first_hole_x + diff_x * hole_id
        current_hole_y = layout.first_hole_y + diff_y * hole_id
        current_hole_z = layout.first_hole_z + diff_z * hole_id

        dlg.current_hole_x_spinBox.setValue(current_hole_x)
        dlg.current_hole_y_spinBox.setValue(current_hole_y)
        dlg.current_hole_z_spinBox.setValue(current_hole_z)
        dlg.current_hole_id_label.setText(f"{hole_id}")

        self.popup_window.setModal(True)
        self.popup_window.show()
