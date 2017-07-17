import csv
from PyQt5.QtCore import QObject


class CsvEngine(QObject):

    def __init__(self, parent=None):
        super(CsvEngine, self).__init__(parent)

        # TODO make properties
        self.engineType = "csv"
        self._inFileName = None

    def initEngine(self, fileName=None):
        print("init CSV engine")
        self._inFileName = fileName

    def fetchAllData(self):
        print("fetch all recordss")
        with open(self._inFileName) as fileHandle:
            reader = csv.reader(fileHandle, delimiter=";")
            return [l for l in reader]
