import const
from dlgbilldata import DlgBillData
from billitem import BillItem
from PyQt5.QtCore import QObject, QModelIndex
from PyQt5.QtWidgets import QDialog, QMessageBox


class UiFacade(QObject):

    def __init__(self, parent=None):
        super(UiFacade, self).__init__(parent)
        self._domainModel = None

    def setDomainModel(self, domainModel=None):
        self._domainModel = domainModel

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

    def requestExit(self):
        print("ui facade exit request...")
        if self._domainModel.savePlanData():
            print("...exit request ok")
        else:
            raise RuntimeError("DB connection error")
