import const
# from billitem import BillItem
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QDate, pyqtSlot
from PyQt5.QtGui import QBrush, QColor


class BillPlanModel(QAbstractTableModel):
    ColumnId = 0
    ColumnProject = 1
    ColumnBillId = 2
    ColumnBillName = 3
    ColumnBillCost = 4
    ColumnCount = 5

    _headers = ["Номер", "Работа", "id счёта", "Счёт"]

    def __init__(self, parent=None, domainModel=None):
        super(BillPlanModel, self).__init__(parent)
        self._modelDomain = domainModel
        self._dicts = dict()

        self._modelDomain.billItemsInserted.connect(self.itemsInserted)
        self._modelDomain.billItemsRemoved.connect(self.itemsRemoved)

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
        return self._modelDomain.billListRowCount()

    def columnCount(self, parent=None, *args, **kwargs):
        return self.ColumnCount

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()
        item = self._modelDomain.getPlanItemAtRow(row)

        if role == Qt.DisplayRole:
            if col == self.ColumnId:
                # return QVariant(item.item_id)
                return QVariant(0)
            elif col == self.ColumnProject:
                return QVariant(self._dicts["project"].getData(item.item_project))
            elif col == self.ColumnBillId:
                return QVariant(item.item_id)
            elif col == self.ColumnBillName:
                return QVariant(item.item_name)
            elif col == self.ColumnBillCost:
                return QVariant(item.item_cost)
        # elif role == Qt.BackgroundRole:
        #     # FIXME hardcoded ids for coloring - add color codes to SQL table?
        #     retcolor = Qt.white
        #
        #     if item.item_status == 1:
        #         retcolor = const.COLOR_PAYMENT_FINISHED
        #
        #     if col == self.ColumnStatus:
        #         if item.item_status == 2:
        #             retcolor = const.COLOR_PAYMENT_PENDING
        #     if col == self.ColumnPriority:
        #         if item.item_status != 1:
        #             if item.item_priority == 2:  # 3 4
        #                 retcolor = const.COLOR_PRIORITY_LOW
        #             elif item.item_priority == 3:
        #                 retcolor = const.COLOR_PRIORITY_MEDIUM
        #             elif item.item_priority == 4:
        #                 retcolor = const.COLOR_PRIORITY_HIGH
        #     if col == self.ColumnShipmentStatus:
        #         if item.item_shipment_status == 2:
        #             retcolor = const.COLOR_ARRIVAL_PENDING
        #         if item.item_shipment_status == 3:
        #             retcolor = const.COLOR_ARRIVAL_PARTIAL
        #         if item.item_shipment_status == 4:
        #             retcolor = const.COLOR_ARRIVAL_RECLAIM
        #     return QVariant(QBrush(QColor(retcolor)))
        elif role == const.RoleNodeId:
            return QVariant(item.item_id)
        return QVariant()

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
