import pymysql
from PyQt5.QtCore import QObject


class MysqlEngine(QObject):
    def __init__(self, parent=None, dbItemClass=None):
        super(MysqlEngine, self).__init__(parent)

        # TODO make properties
        self._engineType = "mysql"
        self._connection = None
        self._dbItemClass = dbItemClass

    def connectToDatabase(self):
        try:
            f = open("connection.ini")
        except IOError:
            return False, str("connection.ini not found.")

        lines = f.readlines()
        f.close()

        settings = dict()
        for s in lines:
            # print(s)
            if s.strip() and s[0] != "#":
                sett = s.strip().split("=")
                settings[sett[0]] = sett[1]
            else:
                continue

        try:
            self._connection = pymysql.connect(host=settings['host'],
                                               port=int(settings['port']),
                                               user=settings['username'],
                                               passwd=settings['password'],
                                               db=settings['database'],
                                               charset='utf8mb4')
        except pymysql.MySQLError as e:
            return False, str("DB error: " + str(e.args[0]) + " " + e.args[1])

        return True, "connection established"

    def initEngine(self):
        print("init mysql engine")
        ok, err = self.connectToDatabase()

    def execSimpleQuery(self, string):
        with self._connection:
            cur = self._connection.cursor()
            cur.execute(string)

        print("query:", cur._last_executed, "| rows:", cur.rowcount)
        return cur

    def execParametrizedQuery(self, string, param):
        with self._connection:
        # try:
            cur = self._connection.cursor()
            cur.execute(string, param)

        # except Exception as e:
        #     print(e)

        print("query:", cur._last_executed, "| rows:", cur.rowcount)
        return cur

    def execBulkQuery(self, string, paramlist):
        with self._connection:
            cur = self._connection.cursor()
            cur.executemany(string, paramlist)

        print("query:", cur._last_executed, "| rows:", cur.rowcount)
        return cur

    def fetchMainData(self):
        return self.execSimpleQuery(self._dbItemClass.itemListRequestString()).fetchall()

    def fetchDict(self, name):
        # TODO make dict ORM
        return self.execSimpleQuery("CALL get" + name + "List()").fetchall()

    def insertMainDataRecord(self, data):
        # TODO: construct parameter list by number of data items
        q = "CALL insertMainData(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # print(q, data[:-1])
        cursor = self.execParametrizedQuery(q, data[:-1])
        rec_id = cursor.fetchone()[0]
        return rec_id

    def updateMainDataRecord(self, data):
        q = "CALL updateMainData(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # print(q, data)
        self.execParametrizedQuery(q, data)

    def deleteMainDataRecord(self, data):
        q = "CALL deleteMainData(%s)"
        # print(q, data)
        self.execParametrizedQuery(q, data)

    def insertDictRecord(self, dictName, data):
        print("mysql engine insert dict record:", dictName, data)
        q = "CALL insert" + dictName + "Record(%s)"
        cur = self.execParametrizedQuery(q, data)
        rec_id = cur.fetchall()[0][0]
        return rec_id

    def updateDictRecord(self, dictName, data):
        print("mysql engine update dict record:", dictName, data)
        q = "CALL update" + dictName + "Record(%s, %s)"
        self.execParametrizedQuery(q, data)

    def deleteDictRecord(self, dictName, data):
        # TODO: no delete methods in DB procs
        print("mysql engine delete dict record:", dictName, data)
        q = "CALL delete" + dictName + "Record(%s)"
        # self.execParametrizedQuery(q, data)

    # domain-specific methods
    def checkUserData(self, data):
        print("mysql engine check user data:", data)
        q = "CALL _checkUserData(%s, %s)"
        return self.execParametrizedQuery(q, data).fetchall()

    def fetchAllPlanRecrods(self):
        return self.execSimpleQuery("CALL getAllPlanRecrods()").fetchall()

    def insertOrderRecord(self, data):
        q = "CALL insertOrderRecord(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        print(q, data[:-1])
        cursor = self.execParametrizedQuery(q, data[:-1])
        rec_id = cursor.fetchone()[0]
        return rec_id


    def updatePlanData(self, data):
        # TODO error handling
        print("mysql engine update plan data...", data)
        q = "CALL updatePlanRecord(%s, %s, %s, %s)"
        self.execBulkQuery(q, data)
        print("...update end")
        return True

    def fetchOrderData(self):
        return self.execSimpleQuery("CALL getOrderList()")

    def updateOrderData(self, data):
        print("mysql engine update order data:", data)
        q = "CALL updateOrderData(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # print(q, data)
        try:
            self.execParametrizedQuery(q, data)
        except Exception as ex:
            print(ex)

