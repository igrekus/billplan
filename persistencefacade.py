from PyQt5.QtCore import QObject


class PersistenceFacade(QObject):

    def __init__(self, parent=None, persistenceEngine=None):
        super(PersistenceFacade, self).__init__(parent)

        self._engine = persistenceEngine
        self.engineType = self._engine.engineType

    def initFacade(self):
        print("init persistence facade")

    def fetchAllData(self):
        return self._engine.fetchAllData()
