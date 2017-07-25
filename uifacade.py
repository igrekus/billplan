from dlgbilldata import DlgBillData
from PyQt5.QtCore import QObject, pyqtSlot, QModelIndex


class UiFacade(QObject):

    def __init__(self, parent=None):
        super(UiFacade, self).__init__(parent)
        self._domainModel = None

    def setDomainModel(self, domainModel=None):
        self._domainModel = domainModel

    # prosess ui signals
    @pyqtSlot(name="procActRefresh")
    def procActRefresh(self):
        self._domainModel.testMethod()
        print("proc act refresh call")

    @pyqtSlot()
    def procActAddBillRecord(self):
        dialog = DlgBillData()
        dialog.exec()
        print("proc act add call")

    @pyqtSlot()
    def procActEditRecord(self):
        self._domainModel
        print("proc act edit call")

    @pyqtSlot()
    def procActDeleteRecord(self):
        print("proc act delete call")
