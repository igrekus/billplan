import const
import re
from PyQt5.QtCore import QSortFilterProxyModel, QDate, Qt


class BillSearchProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(BillSearchProxyModel, self).__init__(parent)

        self.filterProject = 0
        self.filterStatus = 0
        self.filterPriority = 0
        self.filterShipment = 0
        self.filterFromDate = QDate.currentDate()
        self.filterUntilDate = QDate.currentDate()
        self._filterString = ""
        self._filterRegex = re.compile(self._filterString, flags=re.IGNORECASE)

    @property
    def filterString(self):
        return self._filterString

    @filterString.setter
    def filterString(self, string):
        if type(string) == str:
            self._filterString = string
            self._filterRegex = re.compile(string, flags=re.IGNORECASE)
        else:
            raise TypeError("Filter must be a str.")

    def filterAcceptsRow(self, source_row, source_parent_index):
        source_index = self.sourceModel().index(source_row, self.filterKeyColumn(), source_parent_index)
        if source_index.isValid():
            project = self.sourceModel().index(source_row, 0, source_parent_index).data(const.RoleProject)
            status = self.sourceModel().index(source_row, 0, source_parent_index).data(const.RoleStatus)
            priority = self.sourceModel().index(source_row, 0, source_parent_index).data(const.RolePriority)
            shipment = self.sourceModel().index(source_row, 0, source_parent_index).data(const.RoleShipment)
            date = self.sourceModel().index(source_row, 0, source_parent_index).data(const.RoleDate)

            # print(project, status, priority, shipment, date)

            if self.filterProject != 0 and self.filterProject != project:
                return False
            if self.filterStatus != 0 and self.filterStatus != status:
                return False
            if self.filterPriority != 0 and self.filterPriority != priority:
                return False
            if self.filterShipment != 0 and self.filterShipment != shipment:
                return False
            if not self.filterFromDate <= date <= self.filterUntilDate:
                return False

            for i in range(self.sourceModel().columnCount()):
                if self._filterRegex.findall(str(self.sourceModel().index(source_row, i, source_parent_index).data(Qt.DisplayRole))):
                    return True

            # return True

        return False
