import sqlite3
from PyQt5.QtCore import QObject


class SqliteEngine(QObject):
    def __init__(self, parent=None):
        super(SqliteEngine, self).__init__(parent)

        # TODO make properties
        self.engineType = "sqlite"
        self._inFileName = None
        self._connection = None

    def initEngine(self, fileName=None):
        print("init SQLite engine")
        self._inFileName = fileName
        self._connection = sqlite3.connect(self._inFileName)

    def fetchAllData(self):
        print("fetch all records")
        with self._connection:
            cursor = self._connection.execute("SELECT main.bill.bill_id AS id"
                                              ", main.bill.bill_date"
                                              ", main.bill.bill_name"
                                              ", main.bill.bill_category"
                                              ", main.bill.bill_vendor"
                                              ", main.bill.bill_cost"
                                              ", main.bill.bill_project"
                                              ", main.bill.bill_desc"
                                              ", main.bill.bill_shipment_time"
                                              ", main.bill.bill_status"
                                              ", main.bill.bill_priority"
                                              ", main.bill.bill_shipment_date"
                                              ", main.bill.bill_shipment_status"
                                              ", main.bill.bill_week"
                                              ", main.bill.bill_note"
                                              "  FROM bill "
                                              " WHERE bill.bill_id > 0")
            return cursor.fetchall()

    def fetchDicts(self, dict_list: list):
        print("fetch dicts")

        def fetchDict(connection, dict_name: str):
            cursor = connection.execute("SELECT " + dict_name + "_id, " + dict_name + "_name"
                                        "  FROM " + dict_name + " ")
            return cursor.fetchall()

        return [fetchDict(self._connection, d) for d in dict_list]

    def shutdownEngine(self):
        self._connection.close()
