from csvengine import CsvEngine
from sqliteengine import SqliteEngine
from domainmodel import DomainModel
from billtablemodel import BillTableModel
from persistencefacade import PersistenceFacade
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView
from PyQt5.QtCore import Qt, QSortFilterProxyModel


# TODO record commentaries from other users
class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("mw.ui", self)

        # persistence engine
        # self._persistenceEngine = CsvEngine(parent=self)
        self._persistenceEngine = SqliteEngine(parent=self)

        # facades
        self._facadePersistence = PersistenceFacade(parent=self, persistenceEngine=self._persistenceEngine)

        # models
        self._modelDomain = DomainModel(parent=self, persistenceFacade=self._facadePersistence)
        self._modelBillTable = BillTableModel(parent=self, domainModel=self._modelDomain)
        self._modelSearchProxy = QSortFilterProxyModel(parent=self)
        self._modelSearchProxy.setSourceModel(self._modelBillTable)
        # self._dbman = dbman.DbManager(self)
        #
        # self._model_authors = MapModel(self)
        #
        # # self._model_search_proxy = QSortFilterProxyModel(self)
        # self._model_suggestions = SuggestionModel(parent=self, dbmanager=self._dbman)
        # self._model_search_proxy = SuggestionSearchProxyModel(self)
        # self._model_search_proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        # self._model_search_proxy.setSourceModel(self._model_suggestions)
        #
        # self._data_mapper = QDataWidgetMapper(self)
        #
        # self._logged_user = {}

    def initApp(self):
        # init instances
        # self._persistenceEngine.initEngine(fileName="ref/1.csv")
        self._persistenceEngine.initEngine(fileName="sqlite3.db")
        self._facadePersistence.initFacade()
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
        # self.ui.tableBill.resizeRowsToContents()

    def resizeEvent(self, event):
        # print("resize event")
        self.refreshView()
