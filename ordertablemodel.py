import const
from copy import deepcopy
from orderitem import OrderItem
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSlot
from PyQt5.QtGui import QBrush, QColor


class OrderTableModel(QAbstractTableModel):
    # FIXME fix all magical constants
    ColumnId = 0
    ColumnName = 1
    ColumnDescription = 2
    ColumnQuantity = 3
    ColumnCost = 4
    ColumnDateReceive = 5
    ColumnPriority = 6
    ColumnUser = 7
    ColumnApproved = 8
    ColumnStatus = 9
    ColumnBill = 10
    ColumnDoc = 11
    ColumnCount = 12

    ColumnsToAlign = (ColumnQuantity, ColumnDateReceive, ColumnPriority, ColumnUser)

    _header = ['№', 'Описание', 'Назначение', 'Кол-во', 'Сумма', 'Дата поставки', 'Приоритет', 'Заказчик', 'Согласовано', 'Статус', 'Счёт', 'Файл']

    def __init__(self, parent=None, domainModel=None, rightIcon=None, docIcon=None):
        super(OrderTableModel, self).__init__(parent)

        self._modelDomain = domainModel
        self._dicts = None

        self._priorityColors = {2: const.COLOR_PRIORITY_LOW, 3: const.COLOR_PRIORITY_MEDIUM, 4: const.COLOR_PRIORITY_HIGH}

        if rightIcon is not None:
            self._rightDecoration = rightIcon
        else:
            self._rightDecoration = QColor(const.COLOR_PRIORITY_MEDIUM)

        if docIcon is not None:
            self._docDecoration = docIcon
        else:
            self._docDecoration = QColor(const.COLOR_PRIORITY_MEDIUM)

        self._loggedUser = None

        # setup signals
        self._modelDomain.orderItemsInserted.connect(self.itemsInserted)
        self._modelDomain.orderItemsRemoved.connect(self.itemsRemoved)

    def clear(self):
        pass
        # self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        # self._data.clear()
        # self.endRemoveRows()

    def initModel(self):
        print('init order table model')
        self._dicts = self._modelDomain.getDicts()
        self._loggedUser = self._modelDomain.getLoggedUser()

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self._header):
            return QVariant(self._header[section])
        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        return self._modelDomain.getOrderListRowCount()

    def columnCount(self, parent=None, *args, **kwargs):
        return self.ColumnCount

    def setData(self, index, value, role=None):
        # FIXME bypasses ui facade to modify the domain model directly
        # FIXME should notify ui facade to modify domain model through the facade
        if role == Qt.CheckStateRole:
            if index.column() == self.ColumnApproved:
                row = index.row()
                # TODO: deny approval change when order is complete if demanded
                # if self._modelDomain._orderData[row].item_status != 2:
                #     return False

                itemToUpdate: OrderItem = deepcopy(self._modelDomain.getOrderItemAtRow(row))

                if value == 2:
                    itemToUpdate.item_approved = 1
                    itemToUpdate.item_approved_by = self._loggedUser['id']
                elif value == 0:
                    itemToUpdate.item_approved = 2
                    itemToUpdate.item_approved_by = 0

                self._modelDomain.updateOrderItem(row, itemToUpdate)

                self.dataChanged.emit(self.index(row, 0, QModelIndex()),
                                      self.index(row, self.ColumnCount - 1, QModelIndex()), [])
                return True
        # self._modelDomain._planData[row][5] = tmplist
        # self._modelDomain._rawPlanData[item_id] = tmplist
        #
        # self._modelDomain.setWeekForBill(item_id, tmplist[1])

        return False

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()
        item: OrderItem = self._modelDomain.getOrderItemAtRow(row)

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if col == self.ColumnId:
                return QVariant(item.item_id)
            elif col == self.ColumnName:
                return QVariant(item.item_name)
            elif col == self.ColumnDescription:
                return QVariant(item.item_descript)
            elif col == self.ColumnQuantity:
                return QVariant(str(item.item_quantity) + ' шт./комп.')
            elif col == self.ColumnCost:
                return QVariant(f'{item.item_cost/100:,.2f}'.replace(',', ' '))
            elif col == self.ColumnDateReceive:
                return QVariant(item.item_date_receive.isoformat())
            elif col == self.ColumnPriority:
                return QVariant(self._dicts['priority'].getData(item.item_priority))
            elif col == self.ColumnUser:
                user = self._dicts['user'].getData(item.item_user)
                if user:
                    return QVariant(user)
            elif col == self.ColumnApproved:
                if item.item_approved == 1:
                    return QVariant(self._dicts['user'].getData(item.item_approved_by))
                if item.item_cost == 0:
                    return QVariant('Нет суммы')

            elif col == self.ColumnStatus:
                status = self._modelDomain.getOrderStatus(item.item_id)
                if status == 1:
                    return QVariant('Заказано')
                else:
                    return QVariant('Не заказано')

        elif role == Qt.EditRole:
            if col == self.ColumnDoc:
                return QVariant(item.item_document)

        elif role == Qt.CheckStateRole:
            if col == self.ColumnApproved:
                if self._loggedUser['level'] == 1 or self._loggedUser['level'] == 2:
                    if self._loggedUser['id'] == item.item_approved_by or item.item_approved_by == 0:
                        if item.item_cost > 0:
                            if item.item_approved == 1:
                                return QVariant(2)
                            elif item.item_approved == 2:
                                return QVariant(0)

            # elif col == self.ColumnStatus:
            #     status = self._modelDomain.getOrderStatus(item.item_id)
            #     if status == 1:
            #         return QVariant(2)
            #     elif status == 2:
            #         return QVariant(0)

        elif role == Qt.BackgroundRole:
            retcolor = Qt.white
            status = self._modelDomain.getOrderStatus(item.item_id)
            if status == 1:
                retcolor = const.COLOR_PAYMENT_FINISHED
            else:
                if col == self.ColumnPriority:
                    retcolor = self._priorityColors[item.item_priority]

            return QVariant(QBrush(QColor(retcolor)))

        elif role == Qt.TextAlignmentRole:
            if col in self.ColumnsToAlign:
                return QVariant(Qt.AlignCenter)

        elif role == Qt.DecorationRole:
            if col == self.ColumnBill:
                if self._modelDomain.orderHasBill(item.item_id):
                    return self._rightDecoration
            elif col == self.ColumnDoc:
                if item.item_document:
                    return self._docDecoration

        elif role == const.RoleNodeId:
            return QVariant(item.item_id)

        return QVariant()

    def flags(self, index: QModelIndex):
        f = super(OrderTableModel, self).flags(index)

        row = index.row()
        col = index.column()
        # if col == self.ColumnStatus:
        #     f = f | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        if col == self.ColumnApproved:
            item: OrderItem = self._modelDomain.getOrderItemAtRow(row)
            if item.item_cost > 0:
                f = f | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        return f

    def getRowById(self, id_):
        return self._modelDomain.getOrderRowById(id_)

    @pyqtSlot(int, int)
    def itemsInserted(self, first: int, last: int):
        self.beginInsertRows(QModelIndex(), first, last)
        # print('table model slot:', first, last)
        self.endInsertRows()

    @pyqtSlot(int, int)
    def itemsRemoved(self, first: int, last: int):
        self.beginRemoveRows(QModelIndex(), first, last)
        self.endRemoveRows()

    @pyqtSlot()
    def beginClearModel(self):
        self.beginResetModel()

    @pyqtSlot()
    def endClearModel(self):
        self.endResetModel()

