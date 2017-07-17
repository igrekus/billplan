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

    @pyqtSlot(name="procActAddRecord")
    def procActAddRecord(self):
        print("proc act add call")

    @pyqtSlot(QModelIndex, name="procActEditRecord")
    def procActEditRecord(self):
        print("proc act add call")

    @pyqtSlot(QModelIndex, name="procActDeleteRecord")
    def procActDeleteRecord(self):
        print("proc act add call")
