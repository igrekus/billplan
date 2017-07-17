<<<<<<< Updated upstream
from billitem import BillItem
from PyQt5.QtCore import QObject


class DomainModel(QObject):

    dict_list = ["category", "period", "priority", "project", "shipment", "status", "vendor"]

    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._facade = persistenceFacade
        self._data = list()
        self._dicts = dict()

    def initModel(self):
        print("init domain model")

        # choose item builder depending on data source
        # if self._facade.engineType == "csv":
        #     builder = BillItem.fromRawList
        #
        # if self._facade.engineType == "sqlite":
        #     builder = BillItem.fromSqliteTuples

        self._dicts = self._facade.fetchDicts(self.dict_list)

        self._data = self._facade.fetchAllData()

    def rowCount(self):
        return len(self._data)

    def getItemAtRow(self, row: int):
        return self._data[row]

    def getDicts(self):
        return self._dicts

    def testMethod(self):
        print("domain model test method call")
=======
from billitem import BillItem
from PyQt5.QtCore import QObject


class DomainModel(QObject):

    dict_list = ["category", "period", "priority", "project", "shipment", "status", "vendor"]

    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._facade = persistenceFacade
        self._data = list()
        self._dicts = dict()

    def initModel(self):
        print("init domain model")

        # choose item builder depending on data source
        if self._facade.engineType == "csv":
            builder = BillItem.fromRawList

        if self._facade.engineType == "sqlite":
            builder = BillItem.fromSqliteTuple

        self._dicts = self._facade.fetchDicts(self.dict_list)

        self._data = [builder(d) for d in self._facade.fetchAllData()]

    def rowCount(self):
        return len(self._data)

    def getItemAtRow(self, row: int):
        return self._data[row]

    def getDicts(self):
        return self._dicts
>>>>>>> Stashed changes
