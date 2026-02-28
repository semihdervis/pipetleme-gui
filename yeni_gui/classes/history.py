
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QGraphicsView

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_screen import MyApp

class HistoryWindow(QObject):

    def __init__(self, main_app):
        self.main_app : MyApp = main_app

        self.ui = self.main_app.ui
        self.db = self.main_app.db

        self.graphics_view : QGraphicsView = self.ui.history_graphicsView
        self.graphics_view.wheelEvent = lambda event: event.ignore()

        self.draw_png_background()

    def draw_png_background(self):
        scene = QtWidgets.QGraphicsScene()
        self.graphics_view.setScene(scene)
        # Create a QPixmap with the desired size
        pixmap = QtGui.QPixmap(600, 300)
        pixmap.fill(QtCore.Qt.transparent)

        # Create a QPainter to draw on the QPixmap
        painter = QtGui.QPainter(pixmap)

        # Set the size of the squares
        square_size = 10

        # Draw the checkerboard pattern
        for y in range(0, pixmap.height(), square_size):
            for x in range(0, pixmap.width(), square_size):
                if (x // square_size + y // square_size) % 2 == 0:
                    painter.fillRect(x, y, square_size, square_size, QtGui.QColor(200, 200, 200))  # Light gray
                else:
                    painter.fillRect(x, y, square_size, square_size, QtGui.QColor(255, 255, 255))  # White

        # End the QPainter
        painter.end()

        # Set the QPixmap as the background of the QGraphicsScene
        scene.addPixmap(pixmap)
