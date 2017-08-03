from billitem import BillItem
from PyQt5.QtCore import QObject, QModelIndex, pyqtSignal


class DomainModel(QObject):

    dict_list = ["category", "period", "priority", "project", "shipment", "status", "vendor"]

    billItemsInserted = pyqtSignal(int, int)
    billItemsRemoved = pyqtSignal(int, int)

    planItemsInserted = pyqtSignal(int, int)
    planItemsRemoved = pyqtSignal(int, int)

    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._persistenceFacade = persistenceFacade
        self._billData = list()
        self.dicts = dict()

        self._rawPlanData = dict()
        self._planData = list()

    def buildPlanData(self):
        print("building plan data")
        # self._rawPlanData = self._persistenceFacade.fetchRawPlanData()
        oldsize = len(self._planData)
        self.planItemsRemoved.emit(0, oldsize*2 - 1)
        self._planData.clear()

        for i, d in enumerate(sorted(self._billData, key=lambda item: self.dicts["project"].getData(item.item_project))):
            # TODO fix hardcoded magic numbers
            if d.item_active == 1:
                self._planData.append([i, d.item_project, d.item_id, d.item_name, d.item_cost, self._rawPlanData[d.item_id]])

        self.planItemsInserted.emit(0, len(self._planData))

    def initModel(self):
        print("init domain model")

        self.dicts = self._persistenceFacade.fetchDicts(self.dict_list)

        self._billData = self._persistenceFacade.fetchAllBillItems()

        self._rawPlanData = self._persistenceFacade.fetchRawPlanData()

        self.buildPlanData()

    def billListRowCount(self):
        return len(self._billData)

    def getBillItemAtRow(self, row: int):
        return self._billData[row]

    def getBillItemAtIndex(self, index: QModelIndex):
        return self._billData[index.row()]

    def planListRowCount(self):
        return len(self._planData)

    def getPlanItemAtRow(self, row: int):
        return self._planData[row]

    def getDicts(self):
        return self.dicts

    def getTotalForWeek(self, week):
        return sum(p[4] for p in self._planData if p[5] == week)

    def refreshData(self):
        print("domain model refresh call")

    def addBillItem(self, newItem):
        print("domain model add bill item call:", newItem)
        newId = self._persistenceFacade.insertBillItem(newItem)
        newItem.item_id = newId

        self._billData.append(newItem)
        row = len(self._billData) - 1

        self.billItemsInserted.emit(row, row)
        return row

    def updateBillItem(self, index: QModelIndex, updatedItem: BillItem):
        row = index.row()
        print("domain model update bill item call, row:", row, updatedItem)
        self._persistenceFacade.updateBillItem(updatedItem)
        self._billData[row] = updatedItem

    def deleteBillItem(self, index: QModelIndex):
        row = index.row()
        print("domain model delete bill item call, row", row)
        self._persistenceFacade.deleteBillItem(self._billData[row])
        del self._billData[row]
        self.billItemsRemoved.emit(row, row)

    def getBillItemById(self):
        raise NotImplementedError("implement if needed")

    def savePlanData(self):
        print("domain model persist plan data call")
        return self._persistenceFacade.persistPlanData(self._planData)
