import billitem
import const
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt


class DlgDictEditor(QDialog):

    def __init__(self, parent=None, domainModel=None):
        super(DlgDictEditor, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("dlgdicteditor.ui", self)

        # instance variavles
        self._modelDomain = domainModel
        self.dictList = {0: "category",
                         1: "vendor",
                         2: "project"}

        self.initDialog()

        self.ui.btnAdd.clicked.connect(self.onBtnAddClicked)
        self.ui.btnEdit.clicked.connect(self.onBtnEditClicked)
        self.ui.btnDelete.clicked.connect(self.onBtnDeleteClicked)
        self.ui.comboDict.currentIndexChanged.connect(self.onComboDictIndexChanged)
        self.ui.listView.doubleClicked.connect(self.onListViewDoubleClicked)

    def initDialog(self):
        self.ui.comboDict.addItems(["Категория", "Поставщик", "Работа"])
        self.ui.comboDict.setCurrentIndex(0)
        self.ui.listView.setModel(self._modelDomain.dicts["category"])
        self.ui.listView.setRowHidden(0, True)

    def onBtnAddClicked(self):
        self.addRecord()

    def onBtnEditClicked(self):
        if not self.ui.listView.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка", "Изменить: пожалуйста, выберите запись.")
            return

        self.editRecord(self.ui.listView.selectionModel().selectedIndexes()[0])

    def onBtnDeleteClicked(self):
        if not self.ui.listView.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка", "Удалить: пожалуйста, выберите запись.")
            return

        self.delRecrod(self.ui.listView.selectionModel().selectedIndexes()[0])

    def onComboDictIndexChanged(self, index):
        self.ui.listView.setModel(self._modelDomain.dicts[self.dictList[index]])
        self.ui.listView.setRowHidden(0, True)

    def addRecord(self):
        data, ok = QInputDialog.getText(self, "Добавить запись", "Введите название:", QLineEdit.Normal, "")

        if ok:
            data = data[0].upper() + data[1:]
            self._modelDomain.addDictRecord(self.dictList[self.ui.comboDict.currentIndex()], data)

    def editRecord(self, index):
        data, ok = QInputDialog.getText(self, "Изменить запись", "Введите название:", QLineEdit.Normal,
                                        index.data(Qt.DisplayRole))

        if ok:
            data = data[0].upper() + data[1:]
            self._modelDomain.editDictRecord(self.dictList[self.ui.comboDict.currentIndex()],
                                             (index.data(const.RoleNodeId), data))

    def delRecrod(self, index):
        result = QMessageBox.question(self.parent(), "Вопрос",
                                      "Вы действительно хотите удалить выбранную запись?")
        if result != QMessageBox.Yes:
            return

        self._modelDomain.deleteDictRecord(self.dictList[self.ui.comboDict.currentIndex()],
                                           index.data(const.RoleNodeId))

    def onListViewDoubleClicked(self, index):
        self.editRecord(index)
