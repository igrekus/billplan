from billitem import BillItem
from PyQt5.QtCore import QObject, QModelIndex, pyqtSignal


class DomainModel(QObject):

    dict_list = ["category", "period", "priority", "project", "shipment", "status", "vendor"]

    billItemsInserted = pyqtSignal(int, int)
    billItemsRemoved = pyqtSignal(int, int)

    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._persistenceFacade = persistenceFacade
        self._data = list()
        self.dicts = dict()

    def initModel(self):
        print("init domain model")

        self.dicts = self._persistenceFacade.fetchDicts(self.dict_list)

        self._data = self._persistenceFacade.fetchAllBillItems()

    def billListRowCount(self):
        return len(self._data)

    def getItemAtRow(self, row: int):
        return self._data[row]

    def getItemAtIndex(self, index: QModelIndex):
        return self._data[index.row()]

    def getDicts(self):
        return self.dicts

    def refreshData(self):
        print("domain model refresh call")

    def addBillItem(self, newItem):
        print("domain model add bill item call:", newItem)
        newId = self._persistenceFacade.insertBillItem(newItem)
        newItem.item_id = newId

        self._data.append(newItem)
        row = len(self._data) - 1

        self.billItemsInserted.emit(row, row)
        return row

    def updateBillItem(self, index: QModelIndex, updatedItem: BillItem):
        row = index.row()
        print("domain model update bill item call, row:", row, updatedItem)
        self._persistenceFacade.updateBillItem(updatedItem)
        self._data[row] = updatedItem

    def deleteBillItem(self, index: QModelIndex):
        row = index.row()
        print("domain model delete bill item call, row", row)
        self._persistenceFacade.deleteBillItem(self._data[row])
        del self._data[row]
        self.billItemsRemoved.emit(row, row)

    def getBillItemById(self):
        raise NotImplementedError("implement if needed")
