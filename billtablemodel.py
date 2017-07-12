import const
# from billitem import BillItem
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QDate
from PyQt5.QtGui import QBrush, QColor


class BillTableModel(QAbstractTableModel):
    ColumnId = 0
    ColumnDate = 1
    ColumnName = 2
    ColumnCategory = 3
    ColumnVendor = 4
    ColumnCost = 5
    ColumnProject = 6
    ColumnDescription = 7
    ColumnShipmentTime = 8
    ColumnStatus = 9
    ColumnPriority = 10
    ColumnShipmentDate = 11
    ColumnShipmentStatus = 12
    ColumnPaymentWeek = 13
    ColumnNote = 14
    ColumnCount = 15

    _headers = ["Номер", "Дата", "Счёт", "Категория", "Поставщик", "Сумма", "Работа", "Назначение", "Срок",
                "Статус", "Приоритет", "Дата поставки", "Отгрузка", "Неделя оплаты", "Примечание"]

    def __init__(self, parent=None, domainModel=None):
        super(BillTableModel, self).__init__(parent)
        self._modelDomain = domainModel

    def clear(self):
        pass
        # self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        # self._data.clear()
        # self.endRemoveRows()

    def initModel(self):
        print("init suggestion model")
        # self._users = self._dbman.getUserDict()
        #
        # tmplst = self._dbman.getSuggestionList()
        # self.beginInsertRows(QModelIndex(), 0, len(tmplst)-1)
        # self._data = tmplst
        # self.endInsertRows()

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self._headers):
            return QVariant(self._headers[section])
        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        return self._modelDomain.rowCount()

    def columnCount(self, parent=None, *args, **kwargs):
        return self.ColumnCount

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            item = self._modelDomain.getItemAtRow(row)
            if col == self.ColumnId:
                return QVariant(item.item_id)
            elif col == self.ColumnDate:
                return QVariant(item.item_date)
            elif col == self.ColumnName:
                return QVariant(item.item_name)
            elif col == self.ColumnCategory:
                return QVariant(item.item_category)
            elif col == self.ColumnVendor:
                return QVariant(item.item_vendor)
            elif col == self.ColumnCost:
                return QVariant(item.item_cost)
            elif col == self.ColumnProject:
                return QVariant(item.item_project)
            elif col == self.ColumnDescription:
                return QVariant(item.item_descript)
            elif col == self.ColumnShipmentTime:
                return QVariant(item.item_shipment_time)
            elif col == self.ColumnStatus:
                return QVariant(item.item_status)
            elif col == self.ColumnPriority:
                return QVariant(item.item_priority)
            elif col == self.ColumnShipmentDate:
                return QVariant(item.item_shipment_date)
            elif col == self.ColumnShipmentStatus:
                return QVariant(item.item_shipment_status)
            elif col == self.ColumnPaymentWeek:
                return QVariant(item.item_payment_week)
            elif col == self.ColumnNote:
                return QVariant(item.item_note)

        return QVariant()
