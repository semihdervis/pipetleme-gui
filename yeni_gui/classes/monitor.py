from PyQt5.QtCore import QObject, Qt, pyqtSignal, QPoint, QTimer, QVariantAnimation, QPointF, QAbstractAnimation
from PyQt5.QtGui import QPixmap, QPen, QLinearGradient, QColor, QRadialGradient, QColor, QFont, QCursor
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QToolTip, QLabel, QGraphicsColorizeEffect
from database import Database
import time
import random
import math

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp

class IslabGraphicsScene(QGraphicsScene):
    reagent_id_single_click_signal = pyqtSignal(list)
    reagent_id_double_click_signal = pyqtSignal(list)
    card_id_single_click_signal = pyqtSignal(list)
    card_id_double_click_signal = pyqtSignal(list)
    sample_id_single_click_signal = pyqtSignal(list)
    sample_id_double_click_signal = pyqtSignal(list)
    liss_single_click_signal = pyqtSignal(int)
    liss_double_click_signal = pyqtSignal(int)
    def __init__(self, main_app):
        super(IslabGraphicsScene, self).__init__(main_app)
        self.main_app : MyApp = main_app
        self.db: Database = self.main_app.db
        self.setSceneRect(-500, -500, 2500, 2500)
        # Mouse konumu için küçük bir label; mouseMoveEvent içinde güncelleniyor
        self.cursor_pos_text = QGraphicsTextItem("x: -, y: -")
        self.cursor_pos_text.setFont(QFont("Arial", 8))
        self.cursor_pos_text.setDefaultTextColor(QColor("#ffffff"))
        self.cursor_pos_text.setZValue(1000)
        self.addItem(self.cursor_pos_text)
        self.cursor_pos_text.setPos(self.sceneRect().left() + 5, self.sceneRect().top() + 5)

        self.items = {
            "reagent": [],
            "sample": [],
            "dilute": [],
            "card": [],
        }

        self.reagent_0 = Reagent(0, self.main_app)
        self.addItem(self.reagent_0.get_item())
        self.items["reagent"].append(self.reagent_0)
        self.reagent_0.single_click_signal.connect(self.reagent_id_single_click_signal.emit)
        self.reagent_0.double_click_signal.connect(self.reagent_id_double_click_signal.emit)
        self.reagent_1 = Reagent(1, self.main_app)
        self.addItem(self.reagent_1.get_item())
        self.items["reagent"].append(self.reagent_1)
        self.reagent_1.single_click_signal.connect(self.reagent_id_single_click_signal.emit)
        self.reagent_1.double_click_signal.connect(self.reagent_id_double_click_signal.emit)

        self.sample_0 = Sample(0)
        self.sample_0.single_click_signal.connect(self.sample_id_single_click_signal.emit)
        self.sample_0.double_click_signal.connect(self.sample_id_double_click_signal.emit)
        self.addItem(self.sample_0.get_item())
        self.items["sample"].append(self.sample_0)
        self.sample_1 = Sample(1)
        self.sample_1.single_click_signal.connect(self.sample_id_single_click_signal.emit)
        self.sample_1.double_click_signal.connect(self.sample_id_double_click_signal.emit)
        self.addItem(self.sample_1.get_item())
        self.items["sample"].append(self.sample_1)
        self.sample_2 = Sample(2)
        self.sample_2.single_click_signal.connect(self.sample_id_single_click_signal.emit)
        self.sample_2.double_click_signal.connect(self.sample_id_double_click_signal.emit)
        self.addItem(self.sample_2.get_item())
        self.items["sample"].append(self.sample_2)

        self.wash_station = WashStation()
        self.addItem(self.wash_station.get_item())

        self.dilute_0 = Dilute(0)
        self.dilute_0.liss_double_click_signal.connect(self.liss_double_click_signal.emit)
        self.addItem(self.dilute_0.get_item())
        self.items["dilute"].append(self.dilute_0)

        self.card_0 = Card(0)
        self.card_0.single_click_signal.connect(self.card_id_single_click_signal.emit)
        self.card_0.double_click_signal.connect(self.card_id_double_click_signal.emit)
        self.addItem(self.card_0.get_item())
        self.items["card"].append(self.card_0)
        self.card_1 = Card(1)
        self.card_1.single_click_signal.connect(self.card_id_single_click_signal.emit)
        self.card_1.double_click_signal.connect(self.card_id_double_click_signal.emit)
        self.addItem(self.card_1.get_item())
        self.items["card"].append(self.card_1)
        self.card_2 = Card(2)
        self.card_2.single_click_signal.connect(self.card_id_single_click_signal.emit)
        self.card_2.double_click_signal.connect(self.card_id_double_click_signal.emit)
        self.addItem(self.card_2.get_item())
        self.items["card"].append(self.card_2)
        self.card_3 = Card(3)
        self.card_3.single_click_signal.connect(self.card_id_single_click_signal.emit)
        self.card_3.double_click_signal.connect(self.card_id_double_click_signal.emit)
        self.addItem(self.card_3.get_item())
        self.items["card"].append(self.card_3)

        self.pipette = Pipette()
        self.addItem(self.pipette.get_item())
        # self.pipette.get_item().hide()
        self.items["pipette"] = [self.pipette]

        # self.reagent_0.draw_circle(0)
        # self.reagent_0.draw_circle(1, Qt.red)
        # self.reagent_0.draw_circle(2, Qt.green)

        # self.reagent_1.draw_circle(1, QColor(235, 120, 20))

    def only_visible(self, parca_name):
        for parca in self.items:
            for item in self.items[parca]:
                if parca in parca_name if isinstance(parca_name, list) or isinstance(parca_name, tuple) else parca == parca_name:
                    item.get_item().show()
                else:
                    item.get_item().hide()

    def all_visible(self):
        for parca in self.items:
            for item in self.items[parca]:
                item.get_item().show()

    def mouseMoveEvent(self, event):
        """Mouse sahnedeyken konumu gösterir."""
        pos = event.scenePos()
        self.cursor_pos_text.setPlainText(f"x: {pos.x():.1f}, y: {pos.y():.1f}")
        self.cursor_pos_text.setPos(pos.x() + 10, pos.y() + 10)
        super().mouseMoveEvent(event)

    def change_pipette_position(self, position):
        x, y = position
        self.pipette.change_position(x, y)

    def change_reagent_position(self, parca_id, y):
        reagent = self.items["reagent"][parca_id]
        reagent.change_position(y)
    
    def change_sample_position(self, parca_id, y):
        sample = self.items["sample"][parca_id]
        sample.change_position(y)

    def update_reagent(self, parca_id):
        reagent = self.items["reagent"][parca_id]
        reagent.update_reagents()

class Reagent(QObject):
    single_click_signal = pyqtSignal(list)
    double_click_signal = pyqtSignal(list)
    def __init__(self, parca_id, main_app):
        super(Reagent, self).__init__()
        self.main_app : MyApp = main_app
        self.ui = self.main_app.ui
        self.db: Database = self.main_app.db
        self.parca_id = parca_id
        image_path = "yeni_gui/images/reagent.png"
        self.image = QPixmap(image_path)
        self.image_item = QGraphicsPixmapItem(self.image)
        self.image_item.setPos(0+parca_id*55, 0)
        self.image_item.mousePressEvent = self.press_event
        self.last_press_time = 0

        #self.image_item.setAcceptHoverEvents(True)
        self.image_item.hoverLeaveEvent = self.tooltip_hide
        self.image_item.hoverMoveEvent = self.hover_move_event

        self.tooltip_label = QLabel()
        self.tooltip_label.setStyleSheet("background-color: silver; border: 1px solid black; padding: 5px;")
        self.tooltip_label.setFont(QFont("Arial", 8))
        self.tooltip_label.setAlignment(Qt.AlignCenter)
        self.tooltip_label.setWindowFlags(Qt.ToolTip)
        self.tooltip_label.hide()
        self.tooltip_label.leaveEvent = self.tooltip_hide

        self.tooltip_show_hide_time = 500

        self.last_tooltip_time = 0
        self.last_tooltip_id = None

        self.last_mouse_x = None
        self.last_mouse_y = None

        self.tooltip_hide_timer = QTimer()
        self.tooltip_hide_timer.setSingleShot(True)
        self.tooltip_hide_timer.timeout.connect(self.hide_tooltip_if_needed)

        self.tooltip_show_timer = QTimer()
        self.tooltip_show_timer.setSingleShot(True)
        self.tooltip_show_timer.timeout.connect(self.show_tooltip)

        self.circle_radius = 10
        self.drawed_circles = {0:None, 1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None}

    def get_item(self):
        return self.image_item
    
    def get_id_from_position(self, x, y):
        if 8 < x < 50 and 190 < y < 610:
            y = y - 190
            id = int(y // 48)
        else:
            id = None
        return id

    def press_event(self, event):
        id = self.get_id_from_position(event.pos().x(), event.pos().y())

        if time.time() - self.last_press_time < 0.3:
            self.last_press_time = 0
            if id is not None:
                self.double_click_signal.emit([self.parca_id, id])
        else:
            self.last_press_time = time.time()
            if id is not None:
                self.single_click_signal.emit([self.parca_id, id])

    def hover_move_event(self, event):
        id = self.get_id_from_position(event.pos().x(), event.pos().y())

        if id is not None and self.get_reagent_name(id)[1] is not None:
            self.tooltip_hide_timer.stop()
            self.last_tooltip_id = id
            self.last_mouse_x = event.screenPos().x()
            self.last_mouse_y = event.screenPos().y()
            if not self.tooltip_show_timer.isActive():
                self.tooltip_show_timer.start(self.tooltip_show_hide_time)
            else:
                self.tooltip_show_timer.stop()
                self.tooltip_show_timer.start(self.tooltip_show_hide_time)
        else:
            self.last_tooltip_id = None
            self.last_mouse_x = None
            self.last_mouse_y = None
            self.tooltip_hide()

    def show_tooltip(self):
        x = QCursor.pos().x()
        y = QCursor.pos().y()
        if self.last_mouse_x == x and self.last_mouse_y == y:
            reagent_name, barcode = self.get_reagent_name(self.last_tooltip_id)
            text = f"Reagent {self.parca_id}, ID: {self.last_tooltip_id}\nReagent Name: {reagent_name}\nBarcode: {barcode}"
            self.tooltip_label.setText(text)
            self.tooltip_label.move(QPoint(x + 15, y + 5))
            self.tooltip_label.show()

    def hide_tooltip_if_needed(self, event=None):
        if not self.tooltip_label.underMouse():
            self.tooltip_label.hide()

    def tooltip_hide(self, event=None):
        if not self.tooltip_hide_timer.isActive():
            self.tooltip_hide_timer.start(self.tooltip_show_hide_time)

    def get_reagent_name(self, id):
        reagent_table_widget = self.ui.r1_tableWidget if self.parca_id == 0 else self.ui.r2_tableWidget
        table_item = reagent_table_widget.item(id, 1)
        if table_item:
            barcode = table_item.text()
            reagent = self.db.get_reagent(barcode)
            if reagent:
                reagnet_name = reagent.name
                return reagnet_name, barcode
        return None, None
    
    def change_position(self, y):
        self.image_item.setPos(0+self.parca_id*55, y)

    def get_reagent_index_position(self, id):
        x = self.parca_id * 55 + 17 + self.circle_radius
        y = 199 + id * 48 + self.circle_radius
        return x, y

    def draw_circle(self, id, color="#FF3b3b"):
        x_offset = 17
        y_offset = 199 + id * 48

        circle = QGraphicsEllipseItem(0, 0, self.circle_radius * 2, self.circle_radius * 2)
        circle.setPen(QPen(Qt.NoPen))
        circle.setParentItem(self.image_item)
        circle.setPos(x_offset, y_offset)

        gradient = QRadialGradient(self.circle_radius-3, self.circle_radius+1, self.circle_radius)
        gradient.setColorAt(0, QColor(color).lighter(150))
        gradient.setColorAt(0.7, QColor(color))
        gradient.setColorAt(1, QColor(color).darker(150))
        circle.setBrush(gradient)

        self.drawed_circles[id] = circle

    def erase_circle(self, id):
        if self.drawed_circles[id] is not None:
            self.image_item.scene().removeItem(self.drawed_circles[id])
            del self.drawed_circles[id]
            self.drawed_circles[id] = None

    def update_reagents(self):
        for id in range(9):
            reagent_name, barcode = self.get_reagent_name(id)
            if reagent_name:
                if self.drawed_circles[id] is None:
                    self.draw_circle(id)
            else:
                self.erase_circle(id)


class Sample(QObject):
    single_click_signal = pyqtSignal(list)
    double_click_signal = pyqtSignal(list)
    def __init__(self, parca_id, parent=None):
        super(Sample, self).__init__(parent)
        self.parca_id = parca_id
        image_path = "yeni_gui/images/sample.png"
        self.image = QPixmap(image_path)
        self.image = self.image.scaled(100, 775, aspectRatioMode=Qt.KeepAspectRatio)

        self.image_item = QGraphicsPixmapItem(self.image)
        self.image_item.setPos(120+parca_id*43, 0)
        self.image_item.mousePressEvent = self.press_event

        self.last_press_time = 0

        #self.image_item.setAcceptHoverEvents(True)
        self.image_item.hoverLeaveEvent = self.tooltip_hide
        self.image_item.hoverMoveEvent = self.hover_move_event

        self.tooltip_label = QLabel(parent)
        self.tooltip_label.setStyleSheet("background-color: silver; border: 1px solid black; padding: 5px;")
        self.tooltip_label.setFont(QFont("Arial", 8))
        self.tooltip_label.setAlignment(Qt.AlignCenter)
        self.tooltip_label.setWindowFlags(Qt.ToolTip)
        self.tooltip_label.hide()
        self.tooltip_label.leaveEvent = self.tooltip_hide

        self.tooltip_show_hide_time = 500

        self.last_tooltip_time = 0
        self.last_tooltip_id = None

        self.last_mouse_x = None
        self.last_mouse_y = None

        self.tooltip_hide_timer = QTimer()
        self.tooltip_hide_timer.setSingleShot(True)
        self.tooltip_hide_timer.timeout.connect(self.hide_tooltip_if_needed)

        self.tooltip_show_timer = QTimer()
        self.tooltip_show_timer.setSingleShot(True)
        self.tooltip_show_timer.timeout.connect(self.show_tooltip)

        self.gap_size = 0.0167
        self.x_min = 0.177
        self.x_max = 0.77
        self.y_min = 0.031
        self.y_max = 0.775
        self.y_max += self.gap_size
        self.circle_size = (self.y_max-self.y_min)/16-self.gap_size

        # if self.parca_id == 0:
        #     y_position = self.y_min * self.image.height()
        #     for i in range(16):
        #         color = random.choice([Qt.red, Qt.green, Qt.blue, Qt.yellow, Qt.magenta, Qt.cyan, Qt.darkRed, Qt.darkGreen, Qt.darkBlue, Qt.darkYellow, Qt.darkMagenta, Qt.darkCyan])

        #         line = QGraphicsLineItem(self.x_min * self.image.width(), y_position, 
        #                                 self.x_max * self.image.width(), y_position)
        #         line.setPen(QPen(color, 2))  # Set line color and thickness
        #         line.setParentItem(self.image_item)
        #         y_position += self.circle_size * self.image.height()
        #         line = QGraphicsLineItem(self.x_min * self.image.width(), y_position,
        #                                     self.x_max * self.image.width(), y_position)
        #         line.setPen(QPen(color, 2))
        #         line.setParentItem(self.image_item)
        #         y_position += self.gap_size * self.image.height()

    def get_item(self):
        return self.image_item

    def get_id_from_position(self, x, y):
        if self.x_min < x/self.image.width() < self.x_max and self.y_min < y/self.image.height() < self.y_max:
            id = (y/self.image.height()-self.y_min) // (self.circle_size+self.gap_size)
            gap_check = (y/self.image.height()-self.y_min) % (self.circle_size+self.gap_size) <= self.circle_size
            if gap_check:
                id = int(id)
            else:
                id = None
        else:
            id = None
        return id

    def press_event(self, event):
        if time.time() - self.last_press_time < 0.3:
            self.last_press_time = 0
            id = self.get_id_from_position(event.pos().x(), event.pos().y())
            if id is not None:
                self.double_click_signal.emit([self.parca_id, int(id)])
        else:
            self.last_press_time = time.time()

    def hover_move_event(self, event):
        id = self.get_id_from_position(event.pos().x(), event.pos().y())

        if id is not None:
            self.tooltip_hide_timer.stop()
            self.last_tooltip_id = id
            self.last_mouse_x = event.screenPos().x()
            self.last_mouse_y = event.screenPos().y()
            if not self.tooltip_show_timer.isActive():
                self.tooltip_show_timer.start(self.tooltip_show_hide_time)
            else:
                self.tooltip_show_timer.stop()
                self.tooltip_show_timer.start(self.tooltip_show_hide_time)
        else:
            self.last_tooltip_id = None
            self.last_mouse_x = None
            self.last_mouse_y = None
            self.tooltip_hide()

    def show_tooltip(self):
        x = QCursor.pos().x()
        y = QCursor.pos().y()
        if self.last_mouse_x == x and self.last_mouse_y == y:
            text = f"Position: {x}, {y}\nSample {self.parca_id}, ID: {self.last_tooltip_id}"
            self.tooltip_label.setText(text)
            self.tooltip_label.move(QPoint(x + 15, y + 5))
            self.tooltip_label.show()

    def hide_tooltip_if_needed(self, event=None):
        if not self.tooltip_label.underMouse():
            self.tooltip_label.hide()

    def tooltip_hide(self, event=None):
        if not self.tooltip_hide_timer.isActive():
            self.tooltip_hide_timer.start(self.tooltip_show_hide_time)

    def change_position(self, y):
        self.image_item.setPos(120+self.parca_id*43, y)


class WashStation(QObject):
    def __init__(self, parent=None):
        super(WashStation, self).__init__(parent)
        image_path = "yeni_gui/images/wash_station.png"
        self.image = QPixmap(image_path)
        self.image = self.image.scaled(100, 100, aspectRatioMode=Qt.KeepAspectRatio)
        self.image_item = QGraphicsPixmapItem(self.image)
        # Position above the dilute plate (dilute is at 250, 0)
        self.image_item.setPos(250, -110)

    def get_item(self):
        return self.image_item


class Dilute(QObject):
    liss_single_click_signal = pyqtSignal(int)
    liss_double_click_signal = pyqtSignal(int)
    def __init__(self, parca_id, parent=None):
        super(Dilute, self).__init__(parent)
        self.parca_id = parca_id
        image_path = "yeni_gui/images/dilute.png"
        self.image = QPixmap(image_path)
        self.image = self.image.scaled(650, 650, aspectRatioMode=Qt.KeepAspectRatio)
        self.image_item = QGraphicsPixmapItem(self.image)
        self.image_item.setPos(250, 0)
        self.image_item.mousePressEvent = self.press_event
        self.last_press_time = 0

        #self.image_item.setAcceptHoverEvents(True)
        self.image_item.hoverLeaveEvent = self.tooltip_hide
        self.image_item.hoverMoveEvent = self.hover_move_event

        self.tooltip_label = QLabel(parent)
        self.tooltip_label.setStyleSheet("background-color: silver; border: 1px solid black; padding: 5px;")
        self.tooltip_label.setFont(QFont("Arial", 8))
        self.tooltip_label.setAlignment(Qt.AlignCenter)
        self.tooltip_label.setWindowFlags(Qt.ToolTip)
        self.tooltip_label.hide()
        self.tooltip_label.leaveEvent = self.tooltip_hide

        self.tooltip_show_hide_time = 500

        self.last_tooltip_time = 0
        self.last_tooltip_id = None

        self.last_mouse_x = None
        self.last_mouse_y = None

        self.tooltip_hide_timer = QTimer()
        self.tooltip_hide_timer.setSingleShot(True)
        self.tooltip_hide_timer.timeout.connect(self.hide_tooltip_if_needed)

        self.tooltip_show_timer = QTimer()
        self.tooltip_show_timer.setSingleShot(True)
        self.tooltip_show_timer.timeout.connect(self.show_tooltip)


    def get_item(self):
        return self.image_item
    
    def get_id_from_position(self, x, y):
        if ((x-60)**2 + (y-68)**2)**0.5 < 35:
            id = 0
        elif ((x-160)**2 + (y-68)**2)**0.5 < 35:
            id = 1
        else:
            id = None
        return id

    def press_event(self, event):
        if time.time() - self.last_press_time < 0.3:
            self.last_press_time = 0
            id = self.get_id_from_position(event.pos().x(), event.pos().y())
            if id is not None:
                self.liss_double_click_signal.emit(id)
        else:
            self.last_press_time = time.time()

    def hover_move_event(self, event):
        id = self.get_id_from_position(event.pos().x(), event.pos().y())

        if id is not None:
            self.tooltip_hide_timer.stop()
            self.last_tooltip_id = id
            self.last_mouse_x = event.screenPos().x()
            self.last_mouse_y = event.screenPos().y()
            if not self.tooltip_show_timer.isActive():
                self.tooltip_show_timer.start(self.tooltip_show_hide_time)
            else:
                self.tooltip_show_timer.stop()
                self.tooltip_show_timer.start(self.tooltip_show_hide_time)
        else:
            self.last_tooltip_id = None
            self.last_mouse_x = None
            self.last_mouse_y = None
            self.tooltip_hide()

    def show_tooltip(self):
        x = QCursor.pos().x()
        y = QCursor.pos().y()
        if self.last_mouse_x == x and self.last_mouse_y == y:
            text = f"Position: {x}, {y}\nLISS {self.last_tooltip_id}"
            self.tooltip_label.setText(text)
            self.tooltip_label.move(QPoint(x + 15, y + 5))
            self.tooltip_label.show()

    def hide_tooltip_if_needed(self, event=None):
        if not self.tooltip_label.underMouse():
            self.tooltip_label.hide()

    def tooltip_hide(self, event=None):
        if not self.tooltip_hide_timer.isActive():
            self.tooltip_hide_timer.start(self.tooltip_show_hide_time)


class Card(QObject):
    single_click_signal = pyqtSignal(list)
    double_click_signal = pyqtSignal(list)
    def __init__(self, parca_id, parent=None):
        super(Card, self).__init__(parent)
        self.parca_id = parca_id
        image_path = "yeni_gui/images/card.png"
        self.image = QPixmap(image_path)
        self.image = self.image.scaled(400, 400, aspectRatioMode=Qt.KeepAspectRatio)
        self.image_item = QGraphicsPixmapItem(self.image)
        self.image_item.setPos(475, -50+parca_id*200)
        self.image_item.mousePressEvent = self.press_event
        self.last_press_time = 0

        #self.image_item.setAcceptHoverEvents(True)
        self.image_item.hoverLeaveEvent = self.tooltip_hide
        self.image_item.hoverMoveEvent = self.hover_move_event

        self.tooltip_label = QLabel(parent)
        self.tooltip_label.setStyleSheet("background-color: silver; border: 1px solid black; padding: 5px;")
        self.tooltip_label.setFont(QFont("Arial", 8))
        self.tooltip_label.setAlignment(Qt.AlignCenter)
        self.tooltip_label.setWindowFlags(Qt.ToolTip)
        self.tooltip_label.hide()
        self.tooltip_label.leaveEvent = self.tooltip_hide

        self.tooltip_show_hide_time = 500

        self.last_tooltip_time = 0
        self.last_tooltip_id = None

        self.last_mouse_x = None
        self.last_mouse_y = None

        self.tooltip_hide_timer = QTimer()
        self.tooltip_hide_timer.setSingleShot(True)
        self.tooltip_hide_timer.timeout.connect(self.hide_tooltip_if_needed)

        self.tooltip_show_timer = QTimer()
        self.tooltip_show_timer.setSingleShot(True)
        self.tooltip_show_timer.timeout.connect(self.show_tooltip)


        self.light_radius = 7
        self.drawed_status_lights = {0:None, 1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None, 10:None, 11:None}
        self.create_gradients()

        # self.draw_status_light(0, 0)
        # self.draw_status_light(1, 1)
        # self.draw_status_light(2, 2)
        # self.draw_status_light(6, 0)
        # self.draw_status_light(7, 1)
        # self.draw_status_light(8, 2)
        # for i in range(12):
        #     self.draw_status_light(i, random.choice([0, 1, 2]))

    def get_item(self):
        return self.image_item
    
    def get_id_from_position(self, x, y):
        if 35 < x < 182 and 24 < y < 191:
            id = (y-24)/28
            id = int(id) if id % 1 < 0.7 else None
        elif 210 < x < 360 and 24 < y < 191:
            id = (y-24)/28+6
            id = int(id) if id % 1 < 0.7 else None
        else:
            id = None
        return id

    def press_event(self, event):
        if time.time() - self.last_press_time < 0.3:
            self.last_press_time = 0
            id = self.get_id_from_position(event.pos().x(), event.pos().y())
            if id is not None:
                self.double_click_signal.emit([self.parca_id, id])
        else:
            self.last_press_time = time.time()

    def hover_move_event(self, event):
        id = self.get_id_from_position(event.pos().x(), event.pos().y())

        if id is not None:
            self.tooltip_hide_timer.stop()
            self.last_tooltip_id = id
            self.last_mouse_x = event.screenPos().x()
            self.last_mouse_y = event.screenPos().y()
            if not self.tooltip_show_timer.isActive():
                self.tooltip_show_timer.start(self.tooltip_show_hide_time)
            else:
                self.tooltip_show_timer.stop()
                self.tooltip_show_timer.start(self.tooltip_show_hide_time)
        else:
            self.last_tooltip_id = None
            self.last_mouse_x = None
            self.last_mouse_y = None
            self.tooltip_hide()

    def show_tooltip(self):
        x = QCursor.pos().x()
        y = QCursor.pos().y()
        if self.last_mouse_x == x and self.last_mouse_y == y:
            text = f"Position: {x}, {y}\nCard {self.parca_id}, ID: {self.last_tooltip_id}"
            self.tooltip_label.setText(text)
            self.tooltip_label.move(QPoint(x + 15, y + 5))
            self.tooltip_label.show()

    def hide_tooltip_if_needed(self, event=None):
        if not self.tooltip_label.underMouse():
            self.tooltip_label.hide()

    def tooltip_hide(self, event=None):
        if not self.tooltip_hide_timer.isActive():
            self.tooltip_hide_timer.start(self.tooltip_show_hide_time)

    def create_gradients(self):
        self.red_gradient = QRadialGradient(self.light_radius-1.5, self.light_radius-1.5, self.light_radius)
        self.red_gradient.setColorAt(0, QColor(Qt.red).lighter(300))
        self.red_gradient.setColorAt(0.7, QColor(Qt.red))
        self.red_gradient.setColorAt(1, QColor(Qt.red).darker(140))

        green = "#00D500"
        self.green_gradient = QRadialGradient(self.light_radius-1.5, self.light_radius-1.5, self.light_radius)
        self.green_gradient.setColorAt(0, QColor(green).lighter(400))
        self.green_gradient.setColorAt(0.8, QColor(green))
        self.green_gradient.setColorAt(1, QColor(green).darker(140))        

        self.blue_gradient = QRadialGradient(self.light_radius-1.5, self.light_radius-1.5, self.light_radius)
        self.blue_gradient.setColorAt(0, QColor(Qt.blue).lighter(300))
        self.blue_gradient.setColorAt(0.7, QColor(Qt.blue))
        self.blue_gradient.setColorAt(1, QColor(Qt.blue).darker(140))

    def draw_status_light(self, id, status):

        if status == 0:
            gradient = self.red_gradient
        elif status == 1:
            gradient = self.green_gradient
        else:
            gradient = self.blue_gradient

        x = 194 if id < 6 else 367
        y = 34 + (id % 6) * 27.5

        x-=self.light_radius
        y-=self.light_radius

        circle = QGraphicsEllipseItem(0, 0, self.light_radius * 2, self.light_radius * 2)
        circle.setPen(QPen(Qt.NoPen))
        circle.setParentItem(self.image_item)
        circle.setPos(x, y)
        circle.setBrush(gradient)

        self.drawed_status_lights[id] = circle

    def erase_status_light(self, id):
        if self.drawed_status_lights[id] is not None:
            self.image_item.scene().removeItem(self.drawed_status_lights[id])
            del self.drawed_status_lights[id]
            self.drawed_status_lights[id] = None



class Pipette(QObject):
    def __init__(self):
        super().__init__()

        self._base_pix = QPixmap("yeni_gui/images/pipette_crosshair.png").scaled(50, 50)
        self.image_item = QGraphicsPixmapItem(self._base_pix)
        self.image_item.setOffset(-self._base_pix.width()/2, -self._base_pix.height()/2)

        self._color_effect = QGraphicsColorizeEffect()
        self._color_effect.setStrength(0)
        self.image_item.setGraphicsEffect(self._color_effect)
        
        self._base_scale = 1.0
        self._max_scale = 1.6
        self._capacity_ul = 1200
        self._volume_ul = 0
        self._color_full = QColor("#d50000")
        self._color_empty = QColor("#00c853")
        self._speed_multiplier = 1.0

        self.anim = QVariantAnimation(self)
        self.anim.valueChanged.connect(self.image_item.setPos)
        self.anim.finished.connect(self._on_finished)

        self.crosshair_anim = QVariantAnimation(self)
        self.crosshair_anim.valueChanged.connect(self._set_crosshair_state)
        self.crosshair_anim.finished.connect(self._on_crosshair_finished)

        self.queue = []
        self._cb = None
        self._busy = False
        self._wait_timer = QTimer(self)
        self._wait_timer.setSingleShot(True)
        self._wait_timer.timeout.connect(self._on_finished)

    @property
    def speed_multiplier(self):
        return self._speed_multiplier
    
    @speed_multiplier.setter
    def speed_multiplier(self, value):
        if value <= 0:
            raise ValueError("Hız çarpanı 0'dan büyük olmalı")
        self._speed_multiplier = value

    def get_item(self):
        return self.image_item

    def change_position(self, x, y):
        self.image_item.setPos(x, y)

    # ─────────────── HELPER METODLAR ───────────────
    def _enqueue(self, kind, payload, auto_wait=False):
        """Ortak kuyruk ekleme mantığı."""
        self.queue.append((kind, payload))
        if not self._busy:
            self._start_next()
        if auto_wait:
            self.wait(500)

    def _get_ratio(self, volume=None):
        """Hacim oranını hesapla (0-1 arası)."""
        vol = self._volume_ul if volume is None else volume
        return max(0.0, min(1.0, vol / self._capacity_ul)) if self._capacity_ul > 0 else 0.0

    def _adj(self, ms):
        """Hız çarpanına göre süreyi ayarla."""
        return int(ms / self._speed_multiplier)

    # ─────────────── PUBLIC API ───────────────
    def move_to(self, x, y, speed=0.4, callback=None):
        self._enqueue("move", (x, y, speed, callback), auto_wait=True)

    def aspirate(self, amount_ul, duration_ms=400):
        self._enqueue("aspirate", (amount_ul, duration_ms), auto_wait=True)

    def dispense(self, amount_ul, duration_ms=300):
        self._enqueue("dispense", (amount_ul, duration_ms), auto_wait=True)

    def wait(self, ms, callback=None):
        self._enqueue("wait", (ms, callback))

    # ─────────────── QUEUE PROCESSING ───────────────
    def _start_next(self):
        if not self.queue:
            return
        self._busy = True
        kind, payload = self.queue.pop(0)

        if kind == "wait":
            ms, self._cb = payload
            self._wait_timer.start(self._adj(ms))
        elif kind in ("aspirate", "dispense"):
            self._handle_volume(kind, payload)
        else:
            self._handle_move(payload)

    def _handle_volume(self, kind, payload):
        amount_ul, duration_ms = payload
        delta = amount_ul if kind == "aspirate" else -amount_ul
        target = max(0, min(self._capacity_ul, self._volume_ul + delta))
        
        self.crosshair_anim.stop()
        self.crosshair_anim.setDuration(self._adj(duration_ms))
        self.crosshair_anim.setStartValue(self._get_ratio())
        self.crosshair_anim.setEndValue(self._get_ratio(target))
        self._volume_ul = target
        self._cb = None
        self.crosshair_anim.start()

    def _handle_move(self, payload):
        x, y, speed, self._cb = payload
        start, end = self.image_item.pos(), QPointF(x, y)
        distance = math.hypot(end.x() - start.x(), end.y() - start.y())
        
        self.anim.stop()
        self.anim.setDuration(self._adj(distance / speed))
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.start()

    def _on_finished(self):
        if self._cb:
            self._cb()
            self._cb = None
        self._busy = False
        self._start_next()

    def _on_crosshair_finished(self):
        self._busy = False
        self._start_next()

    # ─────────────── CROSSHAIR VISUALS ───────────────
    def _update_crosshair(self):
        self._set_crosshair_state(self._get_ratio())

    def _set_crosshair_state(self, ratio):
        ratio = max(0.0, min(1.0, float(ratio) if isinstance(ratio, (int, float)) else 0.0))
        
        self.image_item.setScale(self._base_scale + (self._max_scale - self._base_scale) * ratio)
        self._color_effect.setColor(self._mix_color(self._color_empty, self._color_full, ratio))
        self._color_effect.setStrength(0.9 if ratio > 0 else 0)

    def _mix_color(self, c1: QColor, c2: QColor, t: float) -> QColor:
        return QColor(
            int(c1.red()   + (c2.red()   - c1.red())   * t),
            int(c1.green() + (c2.green() - c1.green()) * t),
            int(c1.blue()  + (c2.blue()  - c1.blue())  * t)
        )