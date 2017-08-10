from PyQt5.QtCore import QObject


class ReportManager(QObject):

    def __init__(self, parent=None, reportEngine=None):
        super(ReportManager, self).__init__(parent)

        self._engine = reportEngine

    def setEngine(self, engine):
        self._engine = engine

    def makeReport(self, data: list):
        print("making report using engine:", self._engine)
        self._engine.export(data)
