from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem


class TableRowDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(TableRowDelegate, self).__init__(parent)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        super().paint(painter, option, index)

        painter.save()
        painter.drawLine(option.rect.topLeft(), option.rect.topRight())
        painter.restore()
