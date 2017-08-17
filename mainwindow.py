from csvengine import CsvEngine
from sectionheaderview import SectionHeaderView
from sqliteengine import SqliteEngine
from printengine import PrintEngine
from tablerowdelegate import TableRowDelegate
from xlsxengine import XlsxEngine
import datetime
import isoweek
import const
from reportmanager import ReportManager
from domainmodel import DomainModel
from billtablemodel import BillTableModel
from billplanmodel import BillPlanModel
from persistencefacade import PersistenceFacade
from billsearchproxymodel import BillSearchProxyModel
from uifacade import UiFacade
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QAction, QMessageBox, QApplication, QTableView
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QItemSelectionModel, QDate


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        # TODO !!! use dict.get(key, default) !!!
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("mainwindow.ui", self)

        # report manager
        self._reportManager = ReportManager(parent=self)

        # report engines
        self._xlsxEngine = XlsxEngine(parent=self)
        self._reportManager.setEngine(self._xlsxEngine)
        # self._printEngine = PrintEngine(parent=self)
        # self._reportManager.setEngine(self._printEngine)

        # persistence engine
        # self._persistenceEngine = CsvEngine(parent=self)
        self._persistenceEngine = SqliteEngine(parent=self)

        # facades
        self._persistenceFacade = PersistenceFacade(parent=self, persistenceEngine=self._persistenceEngine)
        self._uiFacade = UiFacade(parent=self, reportManager=self._reportManager)

        # models
        # domain
        self._modelDomain = DomainModel(parent=self, persistenceFacade=self._persistenceFacade)

        # bill list + search proxy
        self._modelBillList = BillTableModel(parent=self, domainModel=self._modelDomain)
        self._modelBillSearchProxy = BillSearchProxyModel(parent=self)
        self._modelBillSearchProxy.setSourceModel(self._modelBillList)

        # bill plan + search proxy
        self._modelBillPlan = BillPlanModel(parent=self, domainModel=self._modelDomain)
        self._modelPlanSearchProxy = QSortFilterProxyModel(parent=self)
        self._modelPlanSearchProxy.setSourceModel(self._modelBillPlan)

        # connect ui facade to models
        self._uiFacade.setDomainModel(self._modelDomain)
        self._uiFacade.setBillModel(self._modelBillSearchProxy)
        self._uiFacade.setPlanModel(self._modelPlanSearchProxy)

        # actions
        self.actRefresh = QAction("Обновить", self)
        self.actAddBillRecord = QAction("Добавить счёт...", self)
        self.actEditBillRecord = QAction("Изменить счёт...", self)
        self.actDeleteBillRecord = QAction("Удалить счёт...", self)
        self.actPrint = QAction("Распечатать...", self)
        self.actOpenDictEditor = QAction("Словари", self)

    def buildWeekSelectionCombo(self):
        year, week, day = datetime.datetime.now().isocalendar()
        week_list = list()
        for i in range(1, isoweek.Week.last_week_of_year(year).week + 1):
            w = isoweek.Week(year, i)
            week_list.append(str(i) + ": " + str(w.monday().strftime("%d.%m")) + "-" + str(w.friday().strftime("%d.%m")))

        self.ui.comboWeek.addItems(week_list)
        self.ui.comboWeek.setCurrentIndex(week - 1)

    def initApp(self):
        # init instances
        # self._persistenceEngine.initEngine(fileName="ref/1.csv")
        self._persistenceEngine.initEngine(fileName="sqlite3.db")
        self._persistenceFacade.initFacade()
        # self._uiFacade.initFacade()
        self._modelDomain.initModel()
        self._modelDomain.buildPlanData()
        self._modelBillList.initModel()
        self._modelBillPlan.initModel()

        # init UI
        # bill list table
        self.ui.tableBill: QTableView
        self.ui.tableBill.setModel(self._modelBillSearchProxy)
        self.ui.tableBill.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableBill.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableBill.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # draw delegates
        # self.ui.tableBill.setItemDelegateForRow(0, TableRowDelegate(self.ui.tableBill))
        # self.ui.tableBill.setHorizontalHeader(SectionHeaderView(Qt.Horizontal, parent=self.ui.tableBill))
        # formatting
        self.ui.tableBill.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.ui.tableBill.horizontalHeader().setHighlightSections(False)
        self.ui.tableBill.horizontalHeader().setFixedHeight(24)
        self.ui.tableBill.horizontalHeader().setStretchLastSection(True)
        self.ui.tableBill.horizontalHeader().setStyleSheet("QHeaderView::section {"
                                                           "    padding: 4px;"
                                                           "    border-style: none;"
                                                           "    border-color: #000000;"
                                                           "    border-bottom: 1px solid #000000;"
                                                           "    border-right: 1px solid #000000;"
                                                           "}"
                                                           "QHeaderView::section:horizontal {"
                                                           "    border-right: 1px solid #000000"
                                                           "}")
        # self.ui.tableBill.horizontalHeader().setAutoFillBackground(False)
        self.ui.tableBill.verticalHeader().setVisible(False)
        # self.ui.tableBill.verticalHeader().setDefaultSectionSize(40)
        self.ui.tableBill.setWordWrap(True)
        self.ui.tableBill.resizeRowsToContents()
        self.ui.tableBill.setStyleSheet("QTableView { gridline-color : black}")
        self.ui.tableBill.hideColumn(14)
        # self.ui.tableBill.setSpan(0, 0, 1, 3)

        # bill plan table
        self.ui.tablePlan.setModel(self._modelPlanSearchProxy)
        self.ui.tablePlan.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.tablePlan.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tablePlan.setEditTriggers(QAbstractItemView.SelectedClicked)
        self.ui.tablePlan.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.ui.tablePlan.horizontalHeader().setHighlightSections(False)
        self.ui.tablePlan.horizontalHeader().setFixedHeight(24)
        self.ui.tablePlan.horizontalHeader().setStretchLastSection(True)
        self.ui.tablePlan.horizontalHeader().setStyleSheet("QHeaderView::section {"
                                                           "    padding: 4px;"
                                                           "    border-style: none;"
                                                           "    border-color: #000000;"
                                                           "    border-bottom: 1px solid #000000;"
                                                           "    border-right: 1px solid #000000;"
                                                           "}"
                                                           "QHeaderView::section:horizontal {"
                                                           "    border-right: 1px solid #000000"
                                                           "}")
        self.ui.tablePlan.verticalHeader().setVisible(False)
        self.ui.tablePlan.hideColumn(0)
        # self.ui.tablePlan.hideColumn(3)
        self.ui.tablePlan.hideColumn(4)
        # self.ui.tablePlan.verticalHeader().setDefaultSectionSize(40)
        self.ui.tablePlan.setWordWrap(True)
        self.ui.tablePlan.resizeRowsToContents()
        # self.ui.tablePlan.setSpan(0, 0, 1, 3)
        self.ui.tablePlan.setStyleSheet("QTableView { gridline-color : black }")
        # self.ui.tablePlan.setItemDelegateForRow(0, TableRowDelegate(self.ui.tablePlan))

        # setup filter widgets
        self.ui.comboProjectFilter.setModel(self._modelDomain.dicts["project"])
        self.ui.comboStatusFilter.setModel(self._modelDomain.dicts["status"])
        self.ui.comboPriorityFilter.setModel(self._modelDomain.dicts["priority"])
        self.ui.comboShipmentFilter.setModel(self._modelDomain.dicts["shipment"])
        self.ui.dateFromFilter.setDate(QDate.fromString(self._modelDomain.getEarliestBillDate(), "dd.MM.yyyy"))
        self.ui.dateUntilFilter.setDate(QDate.currentDate())

        # self.btnRefresh.setVisible(False)

        self.buildWeekSelectionCombo()

        # create actions
        self.initActions()

        # setup ui widget signals
        # buttons
        self.ui.btnRefresh.clicked.connect(self.onBtnRefreshClicked)
        self.ui.btnAddBill.clicked.connect(self.onBtnAddBillClicked)
        self.ui.btnEditBill.clicked.connect(self.onBtnEditBillClicked)
        self.ui.btnDeleteBill.clicked.connect(self.onBtnDeleteBillClicked)
        self.ui.btnPrint.clicked.connect(self.onBtnPrintClicked)
        self.ui.btnDictEditor.clicked.connect(self.onBtnDictEditorClicked)

        # table widgets
        self.ui.tableBill.doubleClicked.connect(self.onTableBillDoubleClicked)
        self.ui.tabWidget.currentChanged.connect(self.onTabBarCurrentChanged)

        # search widgets
        self.ui.comboWeek.currentIndexChanged.connect(self.onComboWeekCurrentIndexChanged)
        self.ui.editSearch.textChanged.connect(self.setSearchFilter)
        self.ui.comboProjectFilter.currentIndexChanged.connect(self.setSearchFilter)
        self.ui.comboStatusFilter.currentIndexChanged.connect(self.setSearchFilter)
        self.ui.comboPriorityFilter.currentIndexChanged.connect(self.setSearchFilter)
        self.ui.comboShipmentFilter.currentIndexChanged.connect(self.setSearchFilter)
        self.ui.dateFromFilter.dateChanged.connect(self.setSearchFilter)
        self.ui.dateUntilFilter.dateChanged.connect(self.setSearchFilter)

        self.setSearchFilter()

        self.ui.btnRefresh.setVisible(False)

    def initActions(self):
        self.actRefresh.setShortcut("Ctrl+R")
        self.actRefresh.setStatusTip("Обновить данные")
        self.actRefresh.triggered.connect(self.procActRefresh)

        self.actAddBillRecord.setShortcut("Ctrl+A")
        self.actAddBillRecord.setStatusTip("Добавить новый счёт")
        self.actAddBillRecord.triggered.connect(self.procActAddBillRecord)

        # self.actEditBillRecord.setShortcut("Ctrl+A")
        self.actEditBillRecord.setStatusTip("Добавить новый счёт")
        self.actEditBillRecord.triggered.connect(self.procActEditRecord)

        # self.actDeleteBillRecord.setShortcut("Ctrl+A")
        self.actDeleteBillRecord.setStatusTip("Добавить новый счёт")
        self.actDeleteBillRecord.triggered.connect(self.procActDeleteRecord)

        self.actPrint.setStatusTip("Напечатать текущую таблицу")
        self.actPrint.triggered.connect(self.procActPrint)

        self.actOpenDictEditor.setStatusTip("Открыть редактор словарей")
        self.actOpenDictEditor.triggered.connect(self.procActOpenDictEditor)

    def refreshView(self):
        screenRect = QApplication.desktop().screenGeometry()

        tbwidth = screenRect.width() - 50
        self.ui.tableBill.setColumnWidth(0, tbwidth * 0.04)  # +0.01
        self.ui.tableBill.setColumnWidth(1, tbwidth * 0.06)
        self.ui.tableBill.setColumnWidth(2, tbwidth * 0.07)
        self.ui.tableBill.setColumnWidth(3, tbwidth * 0.07)
        self.ui.tableBill.setColumnWidth(4, tbwidth * 0.06)
        self.ui.tableBill.setColumnWidth(5, tbwidth * 0.06)
        self.ui.tableBill.setColumnWidth(6, tbwidth * 0.06)
        self.ui.tableBill.setColumnWidth(7, tbwidth * 0.215)  # +0.02
        self.ui.tableBill.setColumnWidth(8, tbwidth * 0.06)
        self.ui.tableBill.setColumnWidth(9, tbwidth * 0.065)
        self.ui.tableBill.setColumnWidth(10, tbwidth * 0.06)
        self.ui.tableBill.setColumnWidth(11, tbwidth * 0.06)
        self.ui.tableBill.setColumnWidth(12, tbwidth * 0.06)
        self.ui.tableBill.setColumnWidth(13, tbwidth * 0.04)
        # self.ui.tableBill.setColumnWidth(14, tbwidth * 0.03)
        self.ui.tableBill.setColumnWidth(15, tbwidth * 0.01)

        tpwidth = screenRect.width() - 45
        # 1 2 3 5 .. week count - 1
        # self.ui.tablePlan.setColumnWidth(0, tpwidth * 0.035)
        self.ui.tablePlan.setColumnWidth(1, tpwidth * 0.13)
        self.ui.tablePlan.setColumnWidth(2, tpwidth * 0.05)
        self.ui.tablePlan.setColumnWidth(3, tpwidth * 0.10)
        # self.ui.tablePlan.setColumnWidth(4, tpwidth * 0.06)
        self.ui.tablePlan.setColumnWidth(5, tpwidth * 0.09)
        self.ui.tablePlan.setColumnWidth(6, tpwidth * 0.09)
        self.ui.tablePlan.setColumnWidth(7, tpwidth * 0.09)
        self.ui.tablePlan.setColumnWidth(8, tpwidth * 0.09)
        self.ui.tablePlan.setColumnWidth(9, tpwidth * 0.09)
        self.ui.tablePlan.setColumnWidth(10, tpwidth * 0.09)
        self.ui.tablePlan.setColumnWidth(11, tpwidth * 0.09)
        self.ui.tablePlan.setColumnWidth(12, tpwidth * 0.09)

    # ui events
    def onBtnRefreshClicked(self):
        self.actRefresh.trigger()

    def onBtnAddBillClicked(self):
        self.actAddBillRecord.trigger()

    def onBtnEditBillClicked(self):
        self.actEditBillRecord.trigger()

    def onBtnDeleteBillClicked(self):
        self.actDeleteBillRecord.trigger()

    def onBtnDictEditorClicked(self):
        self.actOpenDictEditor.trigger()

    def onBtnPrintClicked(self):
        self.actPrint.trigger()

    def onTableBillDoubleClicked(self):
        self.actEditBillRecord.trigger()

    def onTabBarCurrentChanged(self, index):
        if index == 1:
            self._modelDomain.buildPlanData()

    def onComboWeekCurrentIndexChanged(self, index):
        self._modelBillPlan.updateHeader(index + 1)

    # misc events
    def resizeEvent(self, event):
        # print("resize event")
        self.refreshView()
        # self.ui.tableBill.resizeRowsToContents()
        # self.ui.tablePlan.resizeRowsToContents()

    def closeEvent(self, *args, **kwargs):
        # TODO error handling on saving before exiting
        self._uiFacade.requestExit()
        super(MainWindow, self).closeEvent(*args, **kwargs)

    # action processing
    # send user commands to the ui facade: (command, parameters (like indexes, etc.))
    def procActRefresh(self):
        print("act refresh trigger")
        self._uiFacade.requestRefresh()
        self.refreshView()
        self.ui.tableBill.resizeRowsToContents()
        self.ui.tablePlan.resizeRowsToContents()

    def procActAddBillRecord(self):
        # print("act add record trigger")
        row = self._uiFacade.requestAddBillRecord()

        if row is not None:
            index = self._modelBillSearchProxy.mapFromSource(self._modelBillList.index(row, 0))
            self.ui.tableBill.scrollTo(index)
            self.ui.tableBill.selectionModel().setCurrentIndex(index, QItemSelectionModel.Select
                                                               | QItemSelectionModel.Rows)

    def procActEditRecord(self):
        # print("act edit record trigger")
        if not self.ui.tableBill.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка", "Изменить: пожалуйста, выберите запись.")
            return

        selectedIndex = self.ui.tableBill.selectionModel().selectedIndexes()[0]
        self._uiFacade.requestEditBillRecord(self._modelBillSearchProxy.mapToSource(selectedIndex))

    def procActDeleteRecord(self):
        # print("act delete record trigger")
        if not self.ui.tableBill.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка", "Удалить: пожалуйста, выберите запись.")
            return

        selectedIndex = self.ui.tableBill.selectionModel().selectedIndexes()[0]
        self._uiFacade.requestDeleteRecord(self._modelBillSearchProxy.mapToSource(selectedIndex))

    def procActPrint(self):
        self._uiFacade.requestPrint(self.ui.tabWidget.currentIndex())

    def setSearchFilter(self, dummy=0):
        self._modelBillSearchProxy.filterString = self.ui.editSearch.text()
        self._modelBillSearchProxy.filterProject = self.ui.comboProjectFilter.currentData(const.RoleNodeId)
        self._modelBillSearchProxy.filterStatus = self.ui.comboStatusFilter.currentData(const.RoleNodeId)
        self._modelBillSearchProxy.filterPriority = self.ui.comboPriorityFilter.currentData(const.RoleNodeId)
        self._modelBillSearchProxy.filterShipment = self.ui.comboShipmentFilter.currentData(const.RoleNodeId)
        self._modelBillSearchProxy.filterFromDate = self.ui.dateFromFilter.date()
        self._modelBillSearchProxy.filterUntilDate = self.ui.dateUntilFilter.date()
        self._modelBillSearchProxy.invalidate()
        self.ui.tableBill.hideColumn(14)

    def procActOpenDictEditor(self):
        self._uiFacade.requestOpenDictEditor()
