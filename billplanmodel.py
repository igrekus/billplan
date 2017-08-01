import const
import datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QDate, pyqtSlot
from PyQt5.QtGui import QBrush, QColor


class BillPlanModel(QAbstractTableModel):
    # FIXME fix all magical constants
    ColumnId = 0
    ColumnProject = 1
    ColumnBillId = 2
    ColumnBillName = 3
    ColumnBillCost = 4
    ColumnCount = 5 + 5

    _headers = ["Номер", "Работа", "id счёта", "Счёт", "Сумма"]

    def __init__(self, parent=None, domainModel=None):

        def week_range(date):
            # TODO process year end week number wrap
            """
            Find the first/last day of the week for the given day.
            Starts Mon ends Sun.

            Returns a tuple of ``(start_date, end_date)``.
            """
            # dow is Mon = 1 ... Sun = 7
            year, week, dow = date.isocalendar()

            # find the first day of the week
            if dow == 1:
                start_date = date
            else:
                start_date = date - datetime.timedelta(dow - 1)

            end_date = start_date + datetime.timedelta(4)

            return start_date, end_date

        super(BillPlanModel, self).__init__(parent)
        self._modelDomain = domainModel
        self._dicts = dict()
        self._modelDomain.billItemsInserted.connect(self.itemsInserted)
        self._modelDomain.billItemsRemoved.connect(self.itemsRemoved)

        self._currentWeek = datetime.datetime.now().date().isocalendar()[1]
        self._weeksInHeader = [n for n in range(self._currentWeek, self._currentWeek + 5)]

        for i in range(5):
            d1, d2 = week_range(datetime.datetime.now().date() + datetime.timedelta(7 * i))
            self._headers.append(d1.strftime("%d.%m") + "-" + d2.strftime("%d.%m"))

    def clear(self):
        pass
        # self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        # self._data.clear()
        # self.endRemoveRows()

    def initModel(self):
        print("init bill plan model")
        self._dicts = self._modelDomain.getDicts()

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self._headers):
            return QVariant(self._headers[section])
        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        return self._modelDomain.planListRowCount() + 1

    def columnCount(self, parent=None, *args, **kwargs):
        return self.ColumnCount

    def setData(self, index, value, role=None):
        # FIXME bypasses ui facade to modify the domain model directly
        # FIXME should notify ui facade to modify domain model through the facade
        row = index.row()
        col = index.column()
        if value == 2:
            self._modelDomain._planData[row][5] = self._currentWeek + col - 5
        elif value == 0:
            self._modelDomain._planData[row][5] = None

        self.dataChanged.emit(self.index(row, 0, QModelIndex()), self.index(row, self.ColumnCount - 1, QModelIndex()), [])
        return True

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        # process virtual "total" row
        if index.row() == self._modelDomain.planListRowCount():
            if role != Qt.DisplayRole:
                return QVariant()

            if index.column() > self.ColumnBillCost:
                total = self._modelDomain.getTotalForWeek(self._currentWeek + index.column() - 5)
                return QVariant("Итого: " + "{:.2f}".format(float(total / 100)) + " руб")

            return QVariant()

        col = index.column()
        row = index.row()
        item = self._modelDomain.getPlanItemAtRow(row)

        if role == Qt.DisplayRole:
            if col == self.ColumnId:
                return QVariant(item[0])
            elif col == self.ColumnProject:
                return QVariant(self._dicts["project"].getData(item[1]))
            elif col == self.ColumnBillId:
                return QVariant(item[2])
            elif col == self.ColumnBillName:
                return QVariant(item[3])
            elif col == self.ColumnBillCost:
                return QVariant(item[4])
            elif col > self.ColumnBillCost:
                if item[5] is not None and item[5] == self._currentWeek + col - 5:
                    return QVariant(str(item[2]) + ": " + "{:.2f}".format(float(item[4] / 100)) + " руб")

        elif role == Qt.BackgroundRole:
            if col > self.ColumnBillCost:
                if item[5] is not None and item[5] == self._currentWeek + col - 5:
                    return QVariant(QBrush(QColor(const.COLOR_PAYMENT_FINISHED)))

        elif role == Qt.CheckStateRole:
            if col > self.ColumnBillCost:
                if item[5] is not None and item[5] == self._currentWeek + col - 5:
                    return QVariant(2)
                else:
                    return QVariant(0)

        elif role == const.RoleNodeId:
            return QVariant(item.item_id)

        return QVariant()

    def flags(self, index):
        f = super(BillPlanModel, self).flags(index)
        if index.row() == self._modelDomain.planListRowCount():
            return Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsSelectable

        if index.column() > self.ColumnBillCost:
            f = f | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        return f

    @pyqtSlot(int, int)
    def itemsInserted(self, first: int, last: int):
        self.beginInsertRows(QModelIndex(), first, last)
        # print("table model slot:", first, last)
        self.endInsertRows()

    @pyqtSlot(int, int)
    def itemsRemoved(self, first: int, last: int):
        self.beginRemoveRows(QModelIndex(), first, last)
        # print("table model slot:", first, last)
        self.endRemoveRows()
