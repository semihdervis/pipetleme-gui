from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF, QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsScene, QTreeWidget, QTreeWidgetItem

# treeWidget yollarını (tuple) sahne koordinatlarına eşleyen harita.
# Yol: top-level item(0)'ın child indeksleri.
# Örn: (0, 0, 0) = Components > Reagent > Reagent 1 > Top
COORDINATE_MAP = {
    # Reagent
    (0, 0, 0): (25, 210),    # Reagent 1 Top
    (0, 0, 1): (25, 594),    # Reagent 1 Bottom
    (0, 1, 0): (80, 208),    # Reagent 2 Top
    (0, 1, 1): (80, 592),    # Reagent 2 Bottom
    # Sample
    (1, 0, 0): (140, 32),    # Sample 1 Top
    (1, 0, 1): (141, 592),   # Sample 1 Bottom
    (1, 1, 0): (180, 34),    # Sample 2 Top
    (1, 1, 1): (181, 592),   # Sample 2 Bottom
    (1, 2, 0): (226, 38),    # Sample 3 Top
    (1, 2, 1): (226, 589),   # Sample 3 Bottom
    # Dilution
    (2, 0, 0): (282, 153),   # Dilution 1 Top Left
    (2, 0, 1): (405, 153),   # Dilution 1 Top Right
    (2, 0, 2): (282, 345),   # Dilution 1 Bottom Left
    (2, 1, 0): (283, 414),   # Dilution 2 Top Left
    (2, 1, 1): (405, 414),   # Dilution 2 Top Right
    (2, 1, 2): (282, 610),   # Dilution 2 Bottom Left
    # Jel Card
    (3, 0, 0): (520, -18),   # Jel Card 1 Top Left
    (3, 0, 1): (820, -19),   # Jel Card 1 Top Right
    (3, 0, 2): (520, 121),   # Jel Card 1 Bottom Left
    (3, 1, 0): (520, 181),   # Jel Card 2 Top Left
    (3, 1, 1): (820, 181),   # Jel Card 2 Top Right
    (3, 1, 2): (520, 320),   # Jel Card 2 Bottom Left
    (3, 2, 0): (520, 381),   # Jel Card 3 Top Left
    (3, 2, 1): (820, 381),   # Jel Card 3 Top Right
    (3, 2, 2): (520, 520),   # Jel Card 3 Bottom Left
    (3, 3, 0): (520, 581),   # Jel Card 4 Top Left
    (3, 3, 1): (820, 581),   # Jel Card 4 Top Right
    (3, 3, 2): (520, 720),   # Jel Card 4 Bottom Left
    # Liss / Bromelin / Wash
    (4,): (309, 69),          # Liss
    (5,): (409, 69),          # Bromelin
    (6,): (300, -65),         # Wash Station
}

ARROW_HEIGHT = 45
ARROW_HEAD_HEIGHT = 16
ARROW_SHAFT_HALF_W = 3
ARROW_HEAD_HALF_W = 11


def _build_arrow_polygon():
    """Aşağıya bakan ok şekli; ucu (0, 0) noktasındadır."""
    s = ARROW_SHAFT_HALF_W
    h = ARROW_HEAD_HALF_W
    ah = ARROW_HEAD_HEIGHT
    total = ARROW_HEIGHT
    return QPolygonF([
        QPointF(-s, -total),
        QPointF(s, -total),
        QPointF(s, -ah),
        QPointF(h, -ah),
        QPointF(0, 0),
        QPointF(-h, -ah),
        QPointF(-s, -ah),
    ])


def _get_item_path(item: QTreeWidgetItem):
    """
    Bir treeWidget öğesinin top-level item altındaki indeks yolunu döndürür.
    Örn: Reagent > Reagent 1 > Top  ->  (0, 0, 0)
    Top-level item'ın kendisi için None döner.
    """
    indices = []
    current = item
    while current.parent() is not None:
        parent = current.parent()
        indices.append(parent.indexOfChild(current))
        current = parent
    if not indices:
        return None
    indices.reverse()
    return tuple(indices)


class ArrowManager:
    """
    Layout sayfasındaki treeWidget öğeleri tıklandığında
    sahne üzerinde ilgili kuyucuğa ok işaretçisi gösterir.
    """

    def __init__(self, scene: QGraphicsScene, tree_widget: QTreeWidget):
        self.scene = scene
        self.tree_widget = tree_widget

        self._arrow_item = QGraphicsPolygonItem(_build_arrow_polygon())
        self._arrow_item.setBrush(QBrush(QColor(220, 40, 40, 200)))
        self._arrow_item.setPen(QPen(QColor(160, 20, 20), 1.2))
        self._arrow_item.setZValue(999)
        self._arrow_item.hide()
        self.scene.addItem(self._arrow_item)

        self.tree_widget.itemClicked.connect(self._on_item_clicked)

    def _on_item_clicked(self, item: QTreeWidgetItem, _column: int):
        path = _get_item_path(item)
        if path is None:
            self.hide_arrow()
            return

        coord = COORDINATE_MAP.get(path)
        if coord is None:
            self.hide_arrow()
            return

        self.show_arrow(coord[0], coord[1])

    def show_arrow(self, x: float, y: float):
        self._arrow_item.setPos(x, y)
        self._arrow_item.show()

    def hide_arrow(self):
        self._arrow_item.hide()
