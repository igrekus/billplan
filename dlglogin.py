import const

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt


class LoginDialog(QDialog):

    def __init__(self, parent=None, userModel=None, domainModel=None):
        super(LoginDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self.ui = uic.loadUi("dlglogin.ui", self)

        self._userModel = userModel
        self._domainModel = domainModel

        self._loggedUser = dict()

        # setup signals
        self.ui.btnOk.clicked.connect(self.onInputComplete)

        #
        self.initDialog()

    def initDialog(self):
        self.ui.comboLogin.setModel(self._userModel)
        self.ui.comboLogin.setCurrentIndex(1)
        self.ui.comboLogin.view().setRowHidden(0, True)
        self.ui.comboLogin.setFocus()

    def onInputComplete(self):
        userId = self.ui.comboLogin.currentData(const.RoleNodeId)
        password = self.ui.editPass.text()

        ok, level = self._domainModel.checkLogin(userId, password)

        if not ok:
            QMessageBox.warning(self, "Ошибка", "Введён неверный пароль.")
            self.ui.editPass.setFocus()
            self.ui.editPass.selectAll()
            return

        self._loggedUser = {"id": userId, "level": level, "login": self.ui.comboLogin.currentText()}
        self.accept()

    def getData(self):
        return self._loggedUser
