from billitem import BillItem
from PyQt5.QtCore import QObject


class DomainModel(QObject):
    
    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._facade = persistenceFacade
        self._data = list()

    def initModel(self):
        print("init domain model")

        # choose item builder depending on data source
        if self._facade.engineType == "csv":
            builder = BillItem.fromRawList

        self._data = [builder(d) for d in self._facade.fetchAllData()]

    def rowCount(self):
        return len(self._data)

    def getItemAtRow(self, row: int):
        return self._data[row]
