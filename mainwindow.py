from csvengine import CsvEngine
from sqliteengine import SqliteEngine
from domainmodel import DomainModel
from billtablemodel import BillTableModel
from persistencefacade import PersistenceFacade
from uifacade import UiFacade
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QAction
from PyQt5.QtCore import Qt, QSortFilterProxyModel


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("mainwindow.ui", self)

        # persistence engine
        # self._persistenceEngine = CsvEngine(parent=self)
        self._persistenceEngine = SqliteEngine(parent=self)

        # facades
        self._persistenceFacade = PersistenceFacade(parent=self, persistenceEngine=self._persistenceEngine)
        self._uiFacade = UiFacade(parent=self)

        # models
        self._modelDomain = DomainModel(parent=self, persistenceFacade=self._persistenceFacade)
        self._uiFacade.setDomainModel(self._modelDomain)
        self._modelBillTable = BillTableModel(parent=self, domainModel=self._modelDomain)
        self._modelSearchProxy = QSortFilterProxyModel(parent=self)
        self._modelSearchProxy.setSourceModel(self._modelBillTable)

        # create actions
        self.createActions()

    def initApp(self):
        # init instances
        # self._persistenceEngine.initEngine(fileName="ref/1.csv")
        self._persistenceEngine.initEngine(fileName="sqlite3.db")
        self._persistenceFacade.initFacade()
        # self._uiFacade.initFacade()
        self._modelDomain.initModel()
        self._modelBillTable.initModel()

        # init UI
        self.ui.tableBill.setModel(self._modelSearchProxy)
        self.ui.tableBill.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableBill.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableBill.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableBill.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.ui.tableBill.horizontalHeader().setHighlightSections(False)
        self.ui.tableBill.horizontalHeader().setFixedHeight(24)
        self.ui.tableBill.horizontalHeader().setStretchLastSection(True)
        self.ui.tableBill.verticalHeader().setVisible(False)
        # self.ui.tableBill.verticalHeader().setDefaultSectionSize(40)
        self.ui.tableBill.setWordWrap(True)
        self.ui.tableBill.resizeRowsToContents()

        # create actions
        self.createActions()

        # setup ui widget signals
        self.ui.btnRefresh.clicked.connect(self.onBtnRefreshClicked)

    def createActions(self):
        self.actRefresh = QAction("Обновить", self)
        self.actRefresh.setShortcut("Ctrl+R")
        self.actRefresh.setStatusTip("Обновить данные")
        self.actRefresh.triggered.connect(self._uiFacade.procActRefresh)

    def refreshView(self):
        twidth = self.ui.tableBill.frameGeometry().width() - 30
        if twidth < 200:
            twidth = 800
        self.ui.tableBill.setColumnWidth(0, twidth * 0.035)
        self.ui.tableBill.setColumnWidth(1, twidth * 0.06)
        self.ui.tableBill.setColumnWidth(2, twidth * 0.07)
        self.ui.tableBill.setColumnWidth(3, twidth * 0.07)
        self.ui.tableBill.setColumnWidth(4, twidth * 0.06)
        self.ui.tableBill.setColumnWidth(5, twidth * 0.06)
        self.ui.tableBill.setColumnWidth(6, twidth * 0.06)
        self.ui.tableBill.setColumnWidth(7, twidth * 0.18)
        self.ui.tableBill.setColumnWidth(8, twidth * 0.06)
        self.ui.tableBill.setColumnWidth(9, twidth * 0.06)
        self.ui.tableBill.setColumnWidth(10, twidth * 0.06)
        self.ui.tableBill.setColumnWidth(11, twidth * 0.06)
        self.ui.tableBill.setColumnWidth(12, twidth * 0.06)
        self.ui.tableBill.setColumnWidth(13, twidth * 0.04)
        self.ui.tableBill.setColumnWidth(14, twidth * 0.03)

    # ui events
    def onBtnRefreshClicked(self):
        self.actRefresh.trigger()
        self.ui.tableBill.resizeRowsToContents()

    def onBtnAddClicked(self):
        self.actAddBillRecord.trigger()

    def onBtnEditClicked(self):
        self.actEditBillRecord.trigger()

    def onBtnDeleteClicked(self):
        self.actDeleteBillRecords.trigger()

    # misc events
    def resizeEvent(self, event):
        # print("resize event")
        self.refreshView()

