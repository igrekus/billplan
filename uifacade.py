import const
from dlgbilldata import DlgBillData
from billitem import BillItem
from PyQt5.QtCore import QObject, QModelIndex, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox


class UiFacade(QObject):
    def __init__(self, parent=None, domainModel=None, reportManager=None):
        super(UiFacade, self).__init__(parent)
        self._domainModel = domainModel
        self._billModel = None
        self._planModel = None
        self._reportManager = reportManager

    def setDomainModel(self, domainModel=None):
        self._domainModel = domainModel

    def setBillModel(self, model):
        self._billModel = model

    def setPlanModel(self, model):
        self._planModel = model

    # process ui requests
    def requestRefresh(self):
        self._domainModel.refreshData()
        print("ui facade refresh request")

    def requestAddBillRecord(self):
        dummyItem = None
        print("ui facade add record request")

        dialog = DlgBillData(item=dummyItem, domainModel=self._domainModel)
        if dialog.exec() != QDialog.Accepted:
            return None

        return self._domainModel.addBillItem(dialog.getData())

    def requestEditBillRecord(self, targetIndex: QModelIndex):
        oldItem = self._domainModel.getBillItemAtIndex(targetIndex)
        print("ui facade edit record request:", oldItem)

        dialog = DlgBillData(item=oldItem, domainModel=self._domainModel)
        if dialog.exec() != QDialog.Accepted:
            return

        self._domainModel.updateBillItem(targetIndex, dialog.getData())

    def requestDeleteRecord(self, targetIndex: QModelIndex):
        print("ui facade delete record request")
        result = QMessageBox.question(self.parent(), "Вопрос",
                                      "Вы действительно хотите удалить выбранную запись?")
        if result != QMessageBox.Yes:
            return

        self._domainModel.deleteBillItem(targetIndex)

    def requestPrint(self, tableIndex):

        def modelRowToList(model, row):
            return [model.data(model.index(row, col), Qt.DisplayRole) for col in range(model.columnCount())], [
                model.data(model.index(row, col), Qt.BackgroundRole) for col in range(model.columnCount())]

        print("ui facade print request")
        mdl = None
        if tableIndex == 0:
            print("making bill list export data...")
            mdl = self._billModel

        elif tableIndex == 1:
            print("making plan export data...")
            mdl = self._planModel

        self._reportManager.makeReport([modelRowToList(mdl, i) for i in range(mdl.rowCount())])

    def requestExit(self):
        print("ui facade exit request...")
        if self._domainModel.savePlanData():
            print("...exit request ok")
        else:
            raise RuntimeError("DB connection error")
