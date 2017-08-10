from PyQt5.QtCore import QObject


class PrintEngine(QObject):

    def __init__(self, parent=None):
        super(PrintEngine, self).__init__(parent)

    def export(self, data: list):
        print("exporting data:")
        for d, c in data:
            print(d)
            print(c)
