from csvengine import CsvEngine
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
        self._persistenceEngine = CsvEngine(parent=self)

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
        self._persistenceEngine.initEngine(fileName="ref/1.csv")
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

