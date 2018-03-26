from billitem import BillItem
from mapmodel import MapModel
from PyQt5.QtCore import QObject


class PersistenceFacade(QObject):

    def __init__(self, parent=None, persistenceEngine=None):
        super(PersistenceFacade, self).__init__(parent)

        self._engine = persistenceEngine
        self.engineType = self._engine._engineType

    def initFacade(self):
        print("init persistence facade:", self._engine._engineType)

    def getDicts(self, dict_list: list):
        # make domain model dicts from raw SQL records
        dicts = dict()
        for n in dict_list:
            dicts[n] = MapModel(data=dict(self._engine.fetchDict(n)))
        return dicts

    def getBillList(self):
        return [BillItem.fromSqlTuple(r) for r in self._engine.fetchMainData()]

    def getRawPlanData(self):
        return {r[1]: [r[2], r[3], r[4]] for r in self._engine.fetchAllPlanRecrods()}

    def updateBillItem(self, item: BillItem):
        print("persistence facade update call:", item)
        self._engine.updateMainDataRecord(item.toTuple())

    def insertBillItem(self, item: BillItem) -> int:
        print("persistence facade insert call:", item)
        return self._engine.insertMainDataRecord(item.toTuple())

    def deleteBillItem(self, item: BillItem):
        print("persistence facade delete call:", item)
        self._engine.deleteMainDataRecord((item.item_id, ))

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
