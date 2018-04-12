import const
import sys
from billitem import BillItem
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QDate


class DlgBillData(QDialog):

    def __init__(self, parent=None, domainModel=None, billItem=None, orderItem=None):
        super(DlgBillData, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("dlgbilldata.ui", self)

        # init instances
        self._currentItem: BillItem = billItem
        self._newItem = None
        self._orderItem = orderItem
        self._domainModel = domainModel

        self.initDialog()

        if self._currentItem is None:
            if self._orderItem is None:
                self.resetWidgets()
            else:
                self.updateWidgetsFromOrder()
        else:
            self.updateWidgets()

    def initDialog(self):
        self.ui.comboCategory.setModel(self._domainModel.dicts["category"])
        self.ui.comboVendor.setModel(self._domainModel.dicts["vendor"])
        self.ui.spinCost.setMaximum(sys.maxsize)
        self.ui.comboProject.setModel(self._domainModel.dicts["project"])
        self.ui.comboPeriod.setModel(self._domainModel.dicts["period"])
        self.ui.comboStatus.setModel(self._domainModel.dicts["status"])
        self.ui.comboPriority.setModel(self._domainModel.dicts["priority"])
        self.ui.comboShipment.setModel(self._domainModel.dicts["shipment"])

        # widget tweaks
        self.ui.lblWeek.setVisible(False)
        self.ui.spinWeek.setVisible(False)
        self.ui.lblNote.setVisible(False)
        self.ui.editNote.setVisible(False)
        # self.ui.lblDateShipment.setVisible(False)
        # self.ui.dateShipment.setVisible(False)
        # self.ui.lblStatus.setVisible(False)
        # self.ui.comboStatus.setVisible(False)

        # setup signals
        self.ui.comboCategory.currentIndexChanged.connect(self.onComboCategoryCurrentIndexChanged)
        self.ui.btnOk.clicked.connect(self.onBtnOkClicked)
        self.ui.btnAddDoc.clicked.connect(self.onBtnAddDocClicked)

    def updateWidgets(self):
        self.ui.dateBill.setDate(QDate().fromString(self._currentItem.item_date, "dd.MM.yyyy"))
        self.ui.editBillName.setText(self._currentItem.item_name)
        self.ui.comboCategory.setCurrentText(self._domainModel.dicts["category"].getData(self._currentItem.item_category))
        self.ui.comboVendor.setCurrentText(self._domainModel.dicts["vendor"].getData(self._currentItem.item_vendor))
        self.ui.spinCost.setValue(float(self._currentItem.item_cost)/100)
        self.ui.comboProject.setCurrentText(self._domainModel.dicts["project"].getData(self._currentItem.item_project))
        self.ui.textDescript.setPlainText(self._currentItem.item_descript)
        self.ui.comboPeriod.setCurrentText(self._domainModel.dicts["period"].getData(self._currentItem.item_shipment_time))
        self.ui.comboStatus.setCurrentText(self._domainModel.dicts["status"].getData(self._currentItem.item_status))
        self.ui.comboPriority.setCurrentText(self._domainModel.dicts["priority"].getData(self._currentItem.item_priority))
        self.ui.dateShipment.setDate(QDate().fromString(self._currentItem.item_shipment_date, "dd.MM.yyyyy"))
        self.ui.comboShipment.setCurrentText(self._domainModel.dicts["shipment"].getData(self._currentItem.item_shipment_status))
        self.ui.spinWeek.setValue(self._currentItem.item_payment_week)
        self.ui.editNote.setText(self._currentItem.item_note)
        self.ui.editDoc.setText(self._currentItem.item_doc)
        self.ui.editOrder.setText(str(self._currentItem.item_order if self._currentItem.item_order is not None else 0))

    def resetWidgets(self):
        self.ui.dateBill.setDate(QDate().currentDate())
        self.ui.editBillName.setText("")
        self.ui.comboCategory.setCurrentIndex(0)
        self.ui.comboVendor.setCurrentIndex(0)
        self.ui.spinCost.setValue(0)
        self.ui.comboProject.setCurrentIndex(0)
        self.ui.textDescript.setPlainText("")
        self.ui.comboPeriod.setCurrentIndex(1)
        self.ui.comboStatus.setCurrentIndex(1)
        self.ui.comboPriority.setCurrentIndex(4)
        self.ui.dateShipment.setDate(QDate().currentDate())
        self.ui.comboShipment.setCurrentIndex(3)
        self.ui.spinWeek.setValue(0)
        self.ui.editNote.setText("")
        self.ui.editDoc.setText("")
        self.ui.editOrder.setText("0")

    def updateWidgetsFromOrder(self):
        self.ui.dateBill.setDate(QDate().currentDate())
        self.ui.editBillName.setText("")
        self.ui.comboCategory.setCurrentIndex(0)
        self.ui.comboVendor.setCurrentIndex(0)
        self.ui.spinCost.setValue(0)
        self.ui.comboProject.setCurrentIndex(0)
        self.ui.textDescript.setPlainText(self._orderItem.item_name + "\n" + self._orderItem.item_descript)
        self.ui.comboPeriod.setCurrentIndex(1)
        self.ui.comboStatus.setCurrentIndex(1)
        self.ui.comboPriority.setCurrentIndex(4)
        self.ui.dateShipment.setDate(QDate().fromString(self._orderItem.item_date_receive.isoformat(), "yyyy-MM-dd"))
        self.ui.comboShipment.setCurrentIndex(3)
        self.ui.spinWeek.setValue(0)
        self.ui.editNote.setText("")
        self.ui.editDoc.setText("")
        self.ui.editOrder.setText(str(self._orderItem.item_id))

    def verifyInputData(self):
        if not self.ui.editBillName.text():
            QMessageBox.information(self, "Ошибка", "Введите название счёта.")
            return False

        if self.ui.comboCategory.currentData(const.RoleNodeId) == 0:
            QMessageBox.information(self, "Ошибка", "Выберите категорию.")
            return False

        if self.ui.comboVendor.currentData(const.RoleNodeId) == 0:
            QMessageBox.information(self, "Ошибка", "Выберите поставщика.")
            return False

        if self.ui.spinCost.value() == 0:
            QMessageBox.information(self, "Ошибка", "Введите сумму.")
            return False

        if self.ui.comboProject.currentData(const.RoleNodeId) == 0:
            QMessageBox.information(self, "Ошибка", "Выберите работу.")
            return False

        if not self.ui.textDescript.toPlainText():
            QMessageBox.information(self, "Ошибка", "Введите назначение счёта.")
            return False

        if self.ui.comboPeriod.currentData(const.RoleNodeId) == 0:
            QMessageBox.information(self, "Ошибка", "Выберите срок поставки.")
            return False

        if self.ui.comboStatus.currentData(const.RoleNodeId) == 0:
            QMessageBox.information(self, "Ошибка", "Выберите статус.")
            return False

        if self.ui.comboPriority.currentData(const.RoleNodeId) == 0:
            QMessageBox.information(self, "Ошибка", "Выберите приоритет.")
            return False

        if self.ui.comboShipment.currentData(const.RoleNodeId) == 0:
            QMessageBox.information(self, "Ошибка", "Выберите статус поставки.")
            return False

        return True

    def collectData(self):
        id_ = None
        if self._currentItem is not None:
            id_ = self._currentItem.item_id

        priority = self.ui.comboPriority.currentData(const.RoleNodeId)
        if self.ui.comboStatus.currentData(const.RoleNodeId) == 1:
            priority = 1

        self._newItem = BillItem(id_=id_
                                 , date=self.ui.dateBill.date().toString("dd.MM.yyyy")
                                 , name=self.ui.editBillName.text()
                                 , category=self.ui.comboCategory.currentData(const.RoleNodeId)
                                 , vendor=self.ui.comboVendor.currentData(const.RoleNodeId)
                                 , cost=int(self.ui.spinCost.value() * 100)
                                 , project=self.ui.comboProject.currentData(const.RoleNodeId)
                                 , descript=self.ui.textDescript.toPlainText()
                                 , shipment_time=self.ui.comboPeriod.currentData(const.RoleNodeId)
                                 , status=self.ui.comboStatus.currentData(const.RoleNodeId)
                                 , priority=priority
                                 , shipment_date=self.ui.dateShipment.date().toString("dd.MM.yyyy")
                                 , shipment_status=self.ui.comboShipment.currentData(const.RoleNodeId)
                                 , payment_week=self.ui.spinWeek.value()
                                 , note=self.ui.editNote.text()
                                 , doc=self.ui.editDoc.text()
                                 , order=int(self.ui.editOrder.text()))

        # TODO verify data change, reject dialog if not changed

    def getData(self):
        return self._newItem

    def onBtnOkClicked(self):
        if not self.verifyInputData():
            return

        self.collectData()
        self.accept()

    def onBtnAddDocClicked(self):
        fileName = QFileDialog.getOpenFileName(self, "Выбрать документ", "./", "Все файлы (*)")
        self.ui.editDoc.setText(fileName[0])

    def onComboCategoryCurrentIndexChanged(self, index):
        if index == 1:
            self.ui.comboShipment.setCurrentIndex(2)
        elif index == 2:
            self.ui.comboShipment.setCurrentIndex(3)
