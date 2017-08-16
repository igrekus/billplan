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

    def fetchRawPlanData(self):
        return {r[1]: [r[2], r[3], r[4]] for r in self._engine.fetchAllPlanRecrods()}

    def updateBillItem(self, item: BillItem):
        print("persistence facade update call:", item)
        self._engine.updateBillRecord(item.toTuple())

    def insertBillItem(self, item: BillItem) -> int:
        print("persistence facade insert call:", item)
        return self._engine.insertBillRecord(item.toTuple())

    def deleteBillItem(self, item):
        print("persistence facade delete call:", item)
        self._engine.deleteBillRecord(item)

    def persistPlanData(self, data):
        print("persistence facade persist plan data call")
        return self._engine.updatePlanData([tuple([v[0], v[1], v[2], k]) for k, v in data.items()])

    def addDictRecord(self, dictName, data):
        print("persistence facade add dict record:", dictName, data)
        return self._engine.insertDictRecord(dictName, (data, ))

    def editDictRecord(self, dictName, data):
        print("persistence facade add dict record:", dictName, data)
        return self._engine.updateDictRecord(dictName, (data[1], data[0]))

    def deleteDictRecord(self, dictName, data):
        print("persistence facade add dict record:", dictName, data)
        return self._engine.deleteDictRecord(dictName, (data, ))
