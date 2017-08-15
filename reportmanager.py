from PyQt5.QtCore import QObject


class ReportManager(QObject):
    def __init__(self, parent=None, reportEngine=None):
        super(ReportManager, self).__init__(parent)

        self._engine = reportEngine

    def setEngine(self, engine):
        self._engine = engine

    def makeReport(self, title: str, header: list, data: list, color: list, footer_data: list, footer_color: list,
                   widths: list):
        print("making report using engine:", self._engine)
        self._engine.export(title, header, data, color, footer_data, footer_color, widths)
