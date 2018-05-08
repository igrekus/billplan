import bisect

import const
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex, QVariant


class MapModel(QAbstractListModel):
    def __init__(self, parent=None, data=None):
        super(MapModel, self).__init__(parent)
        self.mapData = dict()
        self.strList = list()
        if data is not None:
            self.initModel(data)

    def initModel(self, data: dict):
        count = len(data.values()) - 1
        if count < 0:
            count = 0
        self.beginInsertRows(QModelIndex(), 0, count)
        self.mapData = data
        self.strList = list(sorted(self.mapData.values()))
        self.endInsertRows()

        self.addItemAtPosition(0, 0, "Все")

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self.mapData) - 1)
        self.mapData.clear()
        self.strList.clear()
        self.endRemoveRows()

    def addItemAtPosition(self, pos, id_, string):
        self.beginInsertRows(QModelIndex(), pos, pos);
        self.mapData[id_] = string
        self.strList.insert(pos, string)
        self.endInsertRows()

    def addItem(self, id_, string):
        self.mapData[id_] = string

        tmplist = self.strList.copy()[1:]

        pos = bisect.bisect_left(tmplist, string) + 1

        self.beginInsertRows(QModelIndex(), pos, pos)
        self.strList.insert(pos, string)
        self.endInsertRows()

    def updateItem(self, id_, string):
        pos = self.strList.index(self.mapData[id_])

        self.mapData[id_] = string
        self.strList[pos] = string

        # self.dataChanged(self.index(pos, 0, QModelIndex()), self.index(pos, 0, QModelIndex()))

    def removeItem(self, id_):
        # self.beginRemoveRows()
        self.strList.remove(self.mapData[id_])
        del self.mapData[id_]
        # self.endRemoveRows()

    def isEmpty(self):
        return not bool(self.strList)

    def headerData(self, section, orientation, role=None):
        headers = ["Имя"]
        if orientation == Qt.Horizontal and section < len(headers):
            return QVariant(headers[section])

        return QVariant()

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        return len(self.strList)

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant

        row = index.row()
        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            return QVariant(self.strList[row])
        elif role == const.RoleNodeId:
            return QVariant(self.getId(self.strList[row]))

    def getId(self, search_str=""):
        for i, string in self.mapData.items():
            if string == search_str:
                return i

    def getData(self, id_=None):
        if self.mapData[id_]:
            return self.mapData[id_]
        else:
            return None

#     void
#     MapModel::removeItem(const
#     qint32
#     id)
#     {
#         qint32
#     row = m_strList.indexOf(m_mapData.id.value(id));
#
#     m_mapData.di.remove(m_mapData.id.value(id));
#     m_mapData.id.remove(id);
#
#     beginRemoveRows(QModelIndex(), row, row);
#     m_strList.removeAt(row);
#     endRemoveRows();
#     }
