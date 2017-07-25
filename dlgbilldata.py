from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QDate


class DlgBillData(QDialog):

    def __init__(self, parent=None, domainModel=None, item=None):
        super(DlgBillData, self).__init__(parent)

        if item is None:
            raise ValueError("None passed to dialog constructor.")
        if domainModel is None:
            raise ValueError("None passed to dialog constructor.")

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("dlgbilldata.ui", self)

        # init instances
        self._item = item
        self._domainModel = domainModel

        self.initDialog()
        self.updateWidgets()

    def initDialog(self):
        pass
        # self.ui.dateBill.setDate()

    def updateWidgets(self):
        self.ui.dateBill.setDate(QDate().fromString(self._item.item_date, "dd.MM.yyyy"))
        self.ui.editBillName.setText(self._item.item_name)
        self.ui.editNote.setText(self._item.item_note)
