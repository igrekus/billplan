import datetime

import const
import sys
from orderitem import OrderItem
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QDate


class DlgOrderData(QDialog):

    def __init__(self, parent=None, domainModel=None, item=None):
        super(DlgOrderData, self).__init__(parent)

        # TODO: login system stub
        self._activeUser = 1
        self._approver = 4

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("dlgorderdata.ui", self)

        # init instances
        self._currentItem: OrderItem = item
        self._newItem = None
        self._domainModel = domainModel

        self.initDialog()

        if self._currentItem is None:
            self.resetWidgets()
        else:
            self.updateWidgets()

    def initDialog(self):
        self.ui.comboPriority.setModel(self._domainModel.dicts["priority"])
        self.ui.comboPriority.view().setRowHidden(3, True)

        # setup signals
        self.ui.btnOk.clicked.connect(self.onBtnOkClicked)

    def updateWidgets(self):
        self.ui.editName.setText(self._currentItem.item_name)
        self.ui.spinQuantity.setValue(self._currentItem.item_quantity)
        self.ui.dateReceive.setDate(QDate().fromString(self._currentItem.item_date_receive.isoformat(), "yyyy-MM-dd"))
        self.ui.comboPriority.setCurrentText(self._domainModel.dicts["priority"].getData(self._currentItem.item_priority))
        self.ui.textDescript.setPlainText(self._currentItem.item_descript)

    def resetWidgets(self):
        self.ui.editName.setText("")
        self.ui.spinQuantity.setValue(0)
        self.ui.dateReceive.setDate(QDate().currentDate())
        self.ui.comboPriority.setCurrentIndex(4)
        self.ui.textDescript.setPlainText("")

    def verifyInputData(self):
        if not self.ui.editName.text():
            QMessageBox.information(self, "Ошибка", "Введите наименование заказа.")
            return False

        if self.ui.spinQuantity.value == 0:
            QMessageBox.information(self, "Ошибка", "Введите количество.")
            return False

        if self.ui.comboPriority.currentData(const.RoleNodeId) == 0:
            QMessageBox.information(self, "Ошибка", "Выберите приоритет.")
            return False

        if not self.ui.textDescript.toPlainText():
            QMessageBox.information(self, "Ошибка", "Введите описание.")
            return False

        return True

    def collectData(self):
        id_ = None
        approved = 2
        approved_by = self._approver
        if self._currentItem is not None:
            id_ = self._currentItem.item_id
            approved = self._currentItem.item_approved
            approved_by = self._currentItem.item_approved_by

        self._newItem = OrderItem(id_=id_,
                                  name=self.ui.editName.text(),
                                  descript=self.ui.textDescript.toPlainText(),
                                  qty=self.ui.spinQuantity.value(),
                                  date_receive=datetime.datetime.strptime(
                                      self.ui.dateReceive.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                  priority=self.ui.comboPriority.currentData(const.RoleNodeId),
                                  user=self._activeUser,
                                  approved=approved,
                                  approved_by=approved_by)

        # TODO verify data change, reject dialog if not changed

    def getData(self):
        return self._newItem

    def onBtnOkClicked(self):
        try:
            if not self.verifyInputData():
                return

            self.collectData()
            self.accept()
        except Exception as ex:
            print(ex)

