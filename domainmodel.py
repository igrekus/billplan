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

        self._dicts = self._facade.fetchDicts(self.dict_list)

        self._data = self._facade.fetchAllData()

    def rowCount(self):
        return len(self._data)

    def getItemAtRow(self, row: int):
        return self._data[row]

    def getDicts(self):
        return self._dicts

    def refreshData(self):
        print("domain model refresh call")

    def addBillRecord(self):
        print("domain model add bill record call")

    def editBillRecord(self, recordId: int):
        print("domain model edit bill record call:", recordId)

    def deleteBillRecord(self):
        print("domain model delete bill record call")

    def getBillItemById(self):
        raise NotImplementedError("implement if needed")
