from datetime import datetime

from PyQt5.QtGui import QBrush, QColor

import const
from dlgbilldata import DlgBillData
from dlgdicteditor import DlgDictEditor
from PyQt5.QtCore import QObject, QModelIndex, Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox


class UiFacade(QObject):

    totalsChanged = pyqtSignal()

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

        row = self._domainModel.addBillItem(dialog.getData())
        self.totalsChanged.emit()
        return row

    def requestEditBillRecord(self, targetIndex: QModelIndex):
        oldItem = self._domainModel.getBillItemAtIndex(targetIndex)
        print("ui facade edit record request:", oldItem)

        dialog = DlgBillData(item=oldItem, domainModel=self._domainModel)
        if dialog.exec() != QDialog.Accepted:
            return

        self._domainModel.updateBillItem(targetIndex, dialog.getData())
        self.totalsChanged.emit()

    def requestDeleteRecord(self, targetIndex: QModelIndex):
        print("ui facade delete record request")
        result = QMessageBox.question(self.parent(), "Вопрос",
                                      "Вы действительно хотите удалить выбранную запись?")
        if result != QMessageBox.Yes:
            return

        self._domainModel.deleteBillItem(targetIndex)
        self.totalsChanged.emit()

    def requestPrint(self, tableIndex, totals):

        print("ui facade print request")
        title = None
        data = list()
        color = list()
        header = list()
        footer_data = list()
        footer_color = list()
        widths = list()

        if tableIndex == 0:
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

        elif tableIndex == 1:
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

        self._reportManager.makeReport(title, header, data, color, footer_data, footer_color, widths)

    def requestOpenDictEditor(self):
        print("ui facade open dict editor request...")
        dialog = DlgDictEditor(domainModel=self._domainModel)

        dialog.exec()

    def requestExit(self):
        print("ui facade exit request...")
        if self._domainModel.savePlanData():
            print("...exit request ok")
        else:
            raise RuntimeError("DB connection error")
