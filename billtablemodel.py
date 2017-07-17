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
                "Статус", "Приоритет", "Дата", "Отгрузка", "Неделя", "Примечание"]

    def __init__(self, parent=None, domainModel=None):
        super(BillTableModel, self).__init__(parent)
        self._modelDomain = domainModel
        self._dicts = dict()

    def clear(self):
        pass
        # self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        # self._data.clear()
        # self.endRemoveRows()

    def initModel(self):
        print("init suggestion model")
        self._dicts = self._modelDomain.getDicts()

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
        item = self._modelDomain.getItemAtRow(row)

        if role == Qt.DisplayRole:
            if col == self.ColumnId:
                return QVariant(item.item_id)
            elif col == self.ColumnDate:
                return QVariant(item.item_date)
            elif col == self.ColumnName:
                return QVariant(item.item_name)
            elif col == self.ColumnCategory:
                return QVariant(self._dicts["category"][item.item_category])
            elif col == self.ColumnVendor:
                return QVariant(self._dicts["vendor"][item.item_vendor])
            elif col == self.ColumnCost:
                return QVariant("{:.2f}".format(float(item.item_cost/100)))
            elif col == self.ColumnProject:
                return QVariant(self._dicts["project"][item.item_project])
            elif col == self.ColumnDescription:
                return QVariant(item.item_descript)
            elif col == self.ColumnShipmentTime:
                return QVariant(self._dicts["period"][item.item_shipment_time])
            elif col == self.ColumnStatus:
                return QVariant(self._dicts["status"][item.item_status])
            elif col == self.ColumnPriority:
                return QVariant(self._dicts["priority"][item.item_priority])
            elif col == self.ColumnShipmentDate:
                return QVariant(item.item_shipment_date)
            elif col == self.ColumnShipmentStatus:
                return QVariant(self._dicts["shipment"][item.item_shipment_status])
            elif col == self.ColumnPaymentWeek:
                return QVariant(item.item_payment_week)
            elif col == self.ColumnNote:
                return QVariant(item.item_note)
        elif role == Qt.BackgroundRole:
            # FIXME hardcoded ids for coloring - add color codes to SQL table?
            retcolor = Qt.white;

            if item.item_status == 1:
                retcolor = const.COLOR_PAYMENT_FINISHED

            if col == self.ColumnStatus:
                if item.item_status == 2:
                    retcolor = const.COLOR_PAYMENT_PENDING
            if col == self.ColumnPriority:
                if item.item_status != 1:
                    if item.item_priority == 2:  # 3 4
                        retcolor = const.COLOR_PRIORITY_LOW
                    elif item.item_priority == 3:
                        retcolor = const.COLOR_PRIORITY_MEDIUM
                    elif item.item_priority == 4:
                        retcolor = const.COLOR_PRIORITY_HIGH
            if col == self.ColumnShipmentStatus:
                if item.item_shipment_status == 2:
                    retcolor = const.COLOR_ARRIVAL_PENDING
                if item.item_shipment_status == 3:
                    retcolor = const.COLOR_ARRIVAL_PARTIAL
                if item.item_shipment_status == 4:
                    retcolor = const.COLOR_ARRIVAL_RECLAIM
            return QVariant(QBrush(QColor(retcolor)))
        return QVariant()
