from billitem import BillItem
from mapmodel import MapModel
from PyQt5.QtCore import QObject


class PersistenceFacade(QObject):

    def __init__(self, parent=None, persistenceEngine=None):
        super(PersistenceFacade, self).__init__(parent)

        self._engine = persistenceEngine
        self.engineType = self._engine.engineType

    def initFacade(self):
        print("init persistence facade:", self._engine.engineType)

    def fetchDicts(self, dict_list: list):
        # make domain model dicts from raw SQL records
        return {n: MapModel(data=dict(d)) for n, d in zip(dict_list, self._engine.fetchDicts(dict_list))}

    def fetchAllBillItems(self):
        return [BillItem.fromSqliteTuple(r) for r in self._engine.fetchAllBillRecords()]

    def updateBillItem(self, item):
        self._engine.updateBillRecrod(item)

    def insertBillItem(self, item) -> int:
        print("persistence facade insert call:", item)
        return self._engine.insertBillRecord(item)

    def deleteBillItem(self, item):
        print("persistence facade delete call:", item)
        self._engine.deleteBillRecord(item)
