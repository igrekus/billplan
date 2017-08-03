import csv
import sqlite3
from billitem import BillItem
from PyQt5.QtCore import QObject


class SqliteEngine(QObject):
    def __init__(self, parent=None):
        super(SqliteEngine, self).__init__(parent)

        # TODO make properties
        self.engineType = "sqlite"
        self._inFileName = None
        self._connection = None

    def initEngine(self, fileName=None):
        print("init sqlite engine")
        self._inFileName = fileName
        self._connection = sqlite3.connect(self._inFileName)

        # with open("ref/1.csv") as f:
        #     reader = csv.reader(f, delimiter=";")
        #     with self._connection:
        #         for n, l in enumerate(reader):
        #             cursor = self._connection.execute("UPDATE bill SET bill_desc = '" + str(l[7]) + "'"
        #                                               " WHERE bill_id = " + str(n + 1))
        #             print(n, l[7])


    def fetchAllBillRecords(self):
        print("sqlite fetch all records")
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
                                              ", main.bill_plan.plan_week"
                                              "  FROM bill "
                                              " INNER JOIN bill_plan ON bill_plan.plan_billRef = bill.bill_id"
                                              " WHERE bill.bill_id > 0"
                                              "   AND archive = 0")
            return cursor.fetchall()

    def fetchDicts(self, dict_list: list):
        print("sqlite engine fetch dicts")
        def fetchDict(connection, dict_name: str):
            cursor = connection.execute("SELECT " + dict_name + "_id, " + dict_name + "_name"
                                        "  FROM " + dict_name + " "
                                        " WHERE " + dict_name + "_id > 0")
            return cursor.fetchall()

        return [fetchDict(self._connection, d) for d in dict_list]

    def fetchAllPlanRecrods(self):
        print("sqlite engine fetch raw plan data")
        with self._connection:
            cursor = self._connection.execute("SELECT main.bill_plan.plan_id"
                                              ", main.bill_plan.plan_billRef"
                                              ", main.bill_plan.plan_year"
                                              ", main.bill_plan.plan_week"
                                              "  FROM main.bill_plan"
                                              " WHERE main.bill_plan.plan_id > 0")
            return cursor.fetchall()

    def shutdownEngine(self):
        self._connection.close()

    def updateBillRecord(self, data: list):
        print("sqlite engine update bill record:", data)
        with self._connection:
            cursor = self._connection.cursor()
            cursor.execute("UPDATE bill "
                           "   SET bill_date = ?"
                           "     , bill_name = ?"
                           "     , bill_category = ?"
                           "     , bill_vendor = ?"
                           "     , bill_cost = ?"
                           "     , bill_project = ?"
                           "     , bill_desc = ?"
                           "     , bill_shipment_time = ?"
                           "     , bill_status = ?"
                           "     , bill_priority = ?"
                           "     , bill_shipment_date = ?"
                           "     , bill_shipment_status = ?"
                           "     , bill_week = ?"
                           "     , bill_note = ?"
                           "     , archive = 0"
                           " WHERE bill_id = ?", data)

    def insertBillRecord(self, data: list):
        print("sqlite engine insert bill record:", data)
        with self._connection:
            cursor = self._connection.execute(" INSERT INTO bill "
                                              "      ( bill_date"
                                              "      , bill_name"
                                              "      , bill_category"
                                              "      , bill_vendor"
                                              "      , bill_cost"
                                              "      , bill_project"
                                              "      , bill_desc"
                                              "      , bill_shipment_time"
                                              "      , bill_status"
                                              "      , bill_priority"
                                              "      , bill_shipment_date"
                                              "      , bill_shipment_status"
                                              "      , bill_week"
                                              "      , bill_note"
                                              "      , archive"
                                              "      , bill_id)"
                                              " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL)", data[:-1])
            rec_id = cursor.lastrowid
            cursor = self._connection.execute(" INSERT INTO bill_plan"
                                              "           ( plan_id"
                                              "           , plan_billRef"
                                              "           , plan_year"
                                              "           , plan_week)"
                                              "      VALUES (NULL, ?, 0, 0)", (rec_id, ))
        return rec_id

    def deleteBillRecord(self, record: BillItem):
        print("sqlite engine delete bill record:", record)
        with self._connection:
            cursor = self._connection.cursor()
            cursor.execute("UPDATE bill"
                           "   SET archive = 1 "
                           " WHERE bill_id = ?", (record.item_id, ))

    def updatePlanData(self, data):
        # TODO error handling
        print("sqlite engine update plan data...")
        with self._connection:
            cursor = self._connection.cursor()
            cursor.executemany("UPDATE bill_plan"
                               "   SET plan_year = ? "
                               "     , plan_week = ? "
                               " WHERE plan_billRef = ?", data)
        print("...update end")
        return True
