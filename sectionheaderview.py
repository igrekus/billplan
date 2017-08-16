from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPaintEvent, QPainter
from PyQt5.QtWidgets import QHeaderView


class SectionHeaderView(QHeaderView):

    def __init__(self, orientation, parent=None):
        super(SectionHeaderView, self).__init__(orientation, parent)

    # def paintEvent(self, event: QPaintEvent):
    #     super(SectionHeaderView, self).paintEvent(event)

    def paintSection(self, painter: QPainter, rect: QRect, index):
        print(index, rect)
        super(SectionHeaderView, self).paintSection(painter, rect, index)
        painter.save()
        painter.drawLine(rect.topLeft().x() - 1, rect.topLeft().y(),
                         rect.bottomLeft().x() - 1, rect.bottomLeft().y())
        painter.drawLine(rect.topRight().x(), rect.topRight().y(),
                         rect.bottomRight().x(), rect.bottomRight().y())
        painter.restore()
