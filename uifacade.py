import const
from dlgbilldata import DlgBillData
from PyQt5.QtCore import QObject, pyqtSlot, QModelIndex


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
        print("ui facade add record request")
        self._domainModel.addBillRecord()
        # dialog = DlgBillData()
        # dialog.exec()

    def requestEditBillRecord(self, selectedIndex: QModelIndex):
        oldItem = self._domainModel.getItemAtRow(selectedIndex.row())
        print("ui facade edit record request:", oldItem)

        dialog = DlgBillData(item=oldItem, domainModel=self._domainModel)
        dialog.exec()
        # self._domainModel.editBillRecord(selectedIndex.data(const.RoleNodeId))

    def requestDeleteRecord(self):
        print("ui facade add record request")
        self._domainModel.deleteBillRecord()

