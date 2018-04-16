import sys
import const

from copy import deepcopy
from datetime import datetime
from billitem import BillItem
from dlgbilldata import DlgBillData
from dlgdicteditor import DlgDictEditor
from dlglogin import LoginDialog
from dlgorderdata import DlgOrderData
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QObject, QModelIndex, Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox


class UiFacade(QObject):

    totalsChanged = pyqtSignal()

    def __init__(self, parent=None, domainModel=None, reportManager=None, archiveManager=None):
        super(UiFacade, self).__init__(parent)
        self._domainModel = domainModel
        self._billModel = None
        self._planModel = None
        self._orderModel = None
        self._reportManager = reportManager
        self._archiveManager = archiveManager
        print("init facade")

    def setDomainModel(self, domainModel=None):
        self._domainModel = domainModel

    def setBillModel(self, model):
        self._billModel = model

    def setPlanModel(self, model):
        self._planModel = model

    def setOrderModel(self, model):
        self._orderModel = model

    def requestLogin(self):
        dialog = LoginDialog(self.parent(), userModel=self._domainModel.dicts['user'], domainModel=self._domainModel)

        if dialog.exec() != QDialog.Accepted:
            return False

        self._domainModel.setLoggedUser(dialog.getData())
        return True

    def saveDocument(self, item: BillItem):
        ok, archivDocPath = self._archiveManager.storeDocument(item.item_doc, item.item_date)
        if not ok:
            QMessageBox.warning(self.parent(), "Ощибка", "Ошибка при сохранении документа.")
        newItem = deepcopy(item)
        newItem.item_doc = archivDocPath
        return newItem

    # process ui requests
    def requestRefresh(self):
        self._domainModel.refreshData()
        print("ui facade refresh request")

    def requestAddBillRecord(self):
        print("ui facade add bill record request")

        dialog = DlgBillData(billItem=None, domainModel=self._domainModel)
        if dialog.exec() != QDialog.Accepted:
            return None

        row = self._domainModel.addBillItem(self.saveDocument(dialog.getData()))

        self.totalsChanged.emit()
        return row

    def requestEditBillRecord(self, targetIndex: QModelIndex):
        oldItem = self._domainModel.getBillItemAtIndex(targetIndex)
        print("ui facade edit bill record request:", oldItem)

        dialog = DlgBillData(billItem=oldItem, domainModel=self._domainModel)
        if dialog.exec() != QDialog.Accepted:
            return

        self._domainModel.updateBillItem(targetIndex, self.saveDocument(dialog.getData()))

        self.totalsChanged.emit()

    def requestDeleteRecord(self, targetIndex: QModelIndex):
        print("ui facade delete bill record request")
        result = QMessageBox.question(self.parent(), "Вопрос",
                                      "Вы действительно хотите удалить выбранную запись?")
        if result != QMessageBox.Yes:
            return

        self._domainModel.deleteBillItem(targetIndex)
        self.totalsChanged.emit()

    def requestMakeBillFromOrder(self, index: QModelIndex):
        print("ui facade make bill from order request")
        item = self._domainModel.getOrderItemAtIndex(index)

        dialog = DlgBillData(billItem=None, orderItem=item, domainModel=self._domainModel)
        if dialog.exec() != QDialog.Accepted:
            return None

        row = self._domainModel.addBillItem(self.saveDocument(dialog.getData()))

        self.totalsChanged.emit()
        return row

    def requestAddOrderRecord(self):
        print("ui facade add order record request")

        dialog = DlgOrderData(item=None, domainModel=self._domainModel, loggedUser=self._domainModel.getLoggedUser)
        if dialog.exec() != QDialog.Accepted:
            return None

        row = self._domainModel.addOrderItem(dialog.getData())

        return row

    def requestEditOrderRecord(self, targetIndex: QModelIndex):
        oldItem = self._domainModel.getOrderItemAtIndex(targetIndex)
        print("ui facade edit order request:", oldItem)

        dialog = DlgOrderData(item=oldItem, domainModel=self._domainModel, loggedUser=self._domainModel.getLoggedUser)
        if dialog.exec() != QDialog.Accepted:
            return

        self._domainModel.updateOrderItem(targetIndex.row(), dialog.getData())

    def requestPrint(self, currentTab, totals):
        # TODO: extract methods
        print("ui facade print request")
        title = None
        data = list()
        color = list()
        header = list()
        footer_data = list()
        footer_color = list()
        widths = list()

        if currentTab == 0:
            print("making bill list export data...")

            title = "Отчёт о состоянии счетов на " + datetime.now().strftime("%d.%m.%Y")

            header = [self._billModel.headerData(i, Qt.Horizontal, Qt.DisplayRole) for i in
                      range(self._billModel.columnCount() - 5)]

            for i in range(self._billModel.rowCount()):
                d = [self._billModel.data(self._billModel.index(i, j), Qt.DisplayRole) for j in
                     range(self._billModel.columnCount() - 5)]
                c = [self._billModel.data(self._billModel.index(i, j), Qt.BackgroundRole) for j in
                     range(self._billModel.columnCount() - 5)]
                data.append(d)
                color.append(c)

            for i in range(3):
                labels = ["Оплачено:", "Осталось:", "Всего:"]
                cols = [QBrush(QColor(const.COLOR_PAYMENT_FINISHED)),
                        QBrush(QColor(const.COLOR_PAYMENT_PENDING)),
                        None]

                d = [""]*11
                d[4] = labels[i]
                d[5] = "{:,.2f}".format(float(totals[i] / 100)).replace(",", " ")

                c = [None]*11
                c[5] = cols[i]

                footer_data.append(d)
                footer_color.append(c)

            widths = [0.04, 0.06, 0.07, 0.07, 0.06, 0.06, 0.06, 0.215, 0.06, 0.065, 0.06, 0.06, 0.06, 0.04, 0.001, 0.01]

        elif currentTab == 1:
            print("making plan export data...")
            title = "План оплаты счетов с " + \
                    self._planModel.headerData(5, Qt.Horizontal, Qt.DisplayRole).replace(": ", "(") + ") по " + \
                    self._planModel.headerData(self._planModel.columnCount() - 1, Qt.Horizontal,
                                               Qt.DisplayRole).replace(": ", "(") + ")"
            header = [self._planModel.headerData(i, Qt.Horizontal, Qt.DisplayRole) for i in
                      range(self._planModel.columnCount()) if i != 0 and i != 4]

            for i in range(self._planModel.rowCount() - 2):
                d = [self._planModel.data(self._planModel.index(i, j), Qt.DisplayRole) for j in
                     range(self._planModel.columnCount()) if j != 0 and j != 4]
                c = [self._planModel.data(self._planModel.index(i, j), Qt.BackgroundRole) for j in
                     range(self._planModel.columnCount()) if j != 0 and j != 4]
                data.append(d)
                color.append(c)

            for i in range(self._planModel.rowCount() - 2, self._planModel.rowCount()):
                d = [self._planModel.data(self._planModel.index(i, j), Qt.DisplayRole) for j in
                     range(self._planModel.columnCount()) if j != 0 and j != 4]
                c = [self._planModel.data(self._planModel.index(i, j), Qt.BackgroundRole) for j in
                     range(self._planModel.columnCount()) if j != 0 and j != 4]
                footer_data.append(d)
                footer_color.append(c)

            widths = [0.13, 0.05, 0.10, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09]

        elif currentTab == 2:
            print("making order list report data...")
            return

        self._reportManager.makeReport(title, header, data, color, footer_data, footer_color, widths)

    def requestOpenDictEditor(self):
        print("ui facade open dict editor request...")
        dialog = DlgDictEditor(domainModel=self._domainModel)

        dialog.exec()

    def requestExit(self, index):
        # TODO make settings class if needed, only current week is saved for now
        print("ui facade exit request...")
        print("saving preferences...", index)
        # TODO extract saving process into settings class, only send a message from UI
        with open("settings.ini", mode='tw') as f:
            f.write("week="+str(index + 1))

        if self._domainModel.savePlanData():
            print("...exit request ok")
        else:
            raise RuntimeError("DB connection error")
