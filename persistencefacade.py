from PyQt5.QtCore import QObject


class PersistenceFacade(QObject):

    def __init__(self, parent=None, persistenceEngine=None):
        super(PersistenceFacade, self).__init__(parent)

        self._engine = persistenceEngine
        self.engineType = self._engine.engineType

    def initFacade(self):
        print("init persistence facade:", self._engine.engineType)

    def fetchDicts(self, dict_list: list):
        return {n: dict(d) for n, d in zip(dict_list, self._engine.fetchDicts(dict_list))}

    def fetchAllData(self):
        return self._engine.fetchAllData()
