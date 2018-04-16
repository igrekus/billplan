import datetime
from copy import deepcopy

from billitem import BillItem
from orderitem import OrderItem
from PyQt5.QtCore import QObject, QModelIndex, pyqtSignal, QDate


class DomainModel(QObject):

    dict_list = ["category", "period", "priority", "project", "shipment", "status", "vendor", "user"]

    billItemsBeginInsert = pyqtSignal(int, int)
    billItemsEndInsert = pyqtSignal()
    billItemsBeginRemove = pyqtSignal(int, int)
    billItemsEndRemove = pyqtSignal()

    planItemsBeginInsert = pyqtSignal(int, int)
    planItemsEndInsert = pyqtSignal()
    planItemsBeginRemove = pyqtSignal(int, int)
    planItemsEndRemove = pyqtSignal()

    billItemsInserted = pyqtSignal(int, int)
    billItemsRemoved = pyqtSignal(int, int)

    orderItemsInserted = pyqtSignal(int, int)

    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._persistenceFacade = persistenceFacade

        self._loggedUser = dict()

        self._billData = list()
        self.dicts = dict()

        self._rawPlanData = dict()
        self._planData = list()

        self._orderData = list()

    def buildPlanData(self):
        print("building plan data")
        oldsize = len(self._planData)

        self.planItemsBeginRemove.emit(0, oldsize + 2)
        self._planData.clear()
        self.planItemsEndRemove.emit()

        self.planItemsBeginInsert.emit(0, sum([v[2] for v in self._rawPlanData.values()]) + 1)
        for i, d in enumerate(sorted(self._billData, key=lambda item: self.dicts["project"].getData(item.item_project))):
            # TODO fix hardcoded magic numbers
            if self._rawPlanData[d.item_id][2] == 1:
                self._planData.append([i, d.item_project, d.item_id, d.item_name, d.item_cost, self._rawPlanData[d.item_id]])
                # print(self._planData[-1])
        self.planItemsEndInsert.emit()

    def initModel(self):
        print("init domain model")

        self.dicts = self._persistenceFacade.getDicts(self.dict_list)

        self._billData = self._persistenceFacade.getBillList()

        self._rawPlanData = self._persistenceFacade.getRawPlanData()

        self._orderData = self._persistenceFacade.getOrderList()

        self.buildPlanData()

    def checkLogin(self, userId: int, password: str):
        print('checking', userId, password)
        return self._persistenceFacade.checkUser(userId, password)

    def setLoggedUser(self, user: dict):
        self._loggedUser = user

    def getLoggedUser(self):
        return self._loggedUser

    def getLoggedUserLevel(self):
        return self._loggedUser["level"]

    def getLoggedUserName(self):
        return self.dicts["user"].getData(self._loggedUser["id"])

    def refreshPlanData(self):
        if self._rawPlanData:
            self._rawPlanData.clear()
        self._rawPlanData = self._persistenceFacade.fetchRawPlanData()

    def billListRowCount(self):
        return len(self._billData)

    def getBillItemAtRow(self, row: int):
        return self._billData[row]

    def getBillItemAtIndex(self, index: QModelIndex):
        return self._billData[index.row()]

    def getBillIdForOrderId(self, order: int):
        for b in self._billData:
            if b.item_order == order:
                return b.item_id
        return 0

    def getBillRowById(self, id_):
        for b in self._billData:
            if b.item_id == id_:
                return self._billData.index(b)
        return 0

    def planListRowCount(self):
        return len(self._planData)

    def getPlanItemAtRow(self, row: int):
        return self._planData[row]

    def getOrderListRowCount(self):
        return len(self._orderData)

    def getOrderItemAtRow(self, row: int):
        return self._orderData[row]

    def getOrderItemAtIndex(self, index: QModelIndex):
        return self._orderData[index.row()]

    def getOrderRowById(self, order: int):
        for o in self._orderData:
            if o.item_id == order:
                return self._orderData.index(o)
        else:
            return 0

    def getOrderStatus(self, order: int):
        for b in self._billData:
            if b.item_order == order:
                return b.item_status
        else:
            return 0

    def orderHasBill(self, order: int):
        for b in self._billData:
            if b.item_order == order:
                return True
        else:
            return False

    def billHasOrder(self, row: int):
        return bool(self._billData[row].item_order)

    def getDicts(self):
        return self.dicts

    def getTotalForWeek(self, week):
        return sum(p[4] for p in self._planData if p[5] == week)

    def getPayedTotalForWeek(self, week):
        return sum(p[4] for p in self._planData if p[5] == week and self.getBillItemById(p[2]).item_status == 1)

    def getRemainingTotalForWeek(self, week):
        return sum(p[4] for p in self._planData if p[5] == week and self.getBillItemById(p[2]).item_status != 1)

    def getTotal(self, weeks):
        return sum([self.getTotalForWeek(w) for w in weeks])

    def getPayedTotal(self, weeks):
        return sum([self.getPayedTotalForWeek(w) for w in weeks])

    def getRemainingTotal(self, weeks):
        return sum([self.getRemainingTotalForWeek(w) for w in weeks])

    def getBillTotals(self):
        payed = sum(d.item_cost for d in self._billData if d.item_status == 1)
        remaining = sum(d.item_cost for d in self._billData if d.item_status == 2)
        return payed, remaining, payed + remaining

    def setWeekForBill(self, bill_id, week):
        for i, d in enumerate(self._billData):
            if d.item_id == bill_id:
                break
        self._billData[i].item_payment_week = week

    def getBillItemById(self, bill_id):
        for d in self._billData:
            if d.item_id == bill_id:
                return d

    def getEarliestBillDate(self):
        return min([d.item_date for d in self._billData],
                   key=lambda d: QDate.fromString(d, "dd.MM.yyyy"),
                   default=QDate.currentDate())

    def refreshData(self):
        print("domain model refresh call")

    def addBillItem(self, newItem):
        print("domain model add bill item call:", newItem)
        newId = self._persistenceFacade.insertBillItem(newItem)
        newItem.item_id = newId
        # newItem.item_id = 1000

        self._billData.append(newItem)
        self._rawPlanData[newItem.item_id] = [0, 0, 0]
        # self.refreshPlanData()

        row = len(self._billData) - 1

        self.billItemsInserted.emit(row, row)
        return row

    def updateBillItem(self, index: QModelIndex, updatedItem: BillItem):
        row = index.row()
        print("domain model update bill item call, row:", row, updatedItem)

        if updatedItem.item_order:
            orderRow = self.getOrderRowById(updatedItem.item_order)
            newOrderItem: OrderItem = deepcopy(self._orderData[orderRow])
            print(updatedItem.item_shipment_date)
            if isinstance(updatedItem.item_shipment_date, datetime.date):
                newOrderItem.item_date_receive = updatedItem.item_shipment_date
            else:
                newOrderItem.item_date_receive = datetime.datetime.strptime(str(updatedItem.item_shipment_date), "%d.%m.%Y").date()
            self._orderData[orderRow] = newOrderItem
            self._persistenceFacade.updateOrderItem(newOrderItem)

        self._persistenceFacade.updateBillItem(updatedItem)
        self._billData[row] = updatedItem

    def deleteBillItem(self, index: QModelIndex):
        row = index.row()
        print("domain model delete bill item call, row", row)
        self._persistenceFacade.deleteBillItem(self._billData[row])
        del self._billData[row]
        self.billItemsRemoved.emit(row, row)

    def addOrderItem(self, newItem: OrderItem):
        print("domain model add order item call:", newItem)

        newId = self._persistenceFacade.insertOrderItem(newItem)
        newItem.item_id = newId
        # newItem.item_id = 1000

        self._orderData.append(newItem)

        row = len(self._orderData) - 1

        self.orderItemsInserted.emit(row, row)
        return row

    def updateOrderItem(self, row: int, itemToUpdate: OrderItem):
        print("domain model update order item call, row:", row, itemToUpdate)
        self._persistenceFacade.updateOrderItem(itemToUpdate)
        self._orderData[row] = itemToUpdate

    def savePlanData(self):
        print("domain model persist plan data call")
        # TODO: collect and save only changed plan data
        return self._persistenceFacade.persistPlanData(self._rawPlanData)

    def addDictRecord(self, dictName, data):
        print("domain model add dict record:", dictName, data)
        newId = self._persistenceFacade.addDictRecord(dictName, data)

        self.dicts[dictName].addItem(newId, data)

    def editDictRecord(self, dictName, data):
        print("domain model edit dict record:", dictName, data)
        self._persistenceFacade.editDictRecord(dictName, data)

        self.dicts[dictName].updateItem(data[0], data[1])

    def deleteDictRecord(self, dictName, data):
        # TODO: check for existing references
        print("domain model delete dict record:", dictName, data)
        self._persistenceFacade.deleteDictRecord(dictName, data)

        self.dicts[dictName].removeItem(data)
