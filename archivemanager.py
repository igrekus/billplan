import datetime
import os
import pathlib2

import shutil
from PyQt5.QtCore import QObject

local_months = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
                'Ноябрь', 'Декабрь']
bills = 'Счета'
orders = 'Заказы'

class ArchiveManager(QObject):
    def __init__(self, parent=None, arcPath=None):
        super(ArchiveManager, self).__init__(parent)

        self._archivePath: str = arcPath
        self._archivePathBills = ''
        self._archivePathOrders = ''

        print('init archive manager')

    # def makeDirsForDate(self, date: str):
    #     month, year = date.split(".")[1:]
    #     bill_dir = self._archivePath + '\\' + year + '\\' + month + "_" + local_months[int(month)] + '\\' + bills
    #     order_dir = self._archivePath + '\\' + year + '\\' + month + "_" + local_months[int(month)] + '\\' + orders
    #     # directory = self._archivePath + '\\' + year + '\\' + month + "_" + local_months[int(month)]
    #
    #     pathlib2.Path(bill_dir).mkdir(parents=True, exist_ok=True)
    #     pathlib2.Path(order_dir).mkdir(parents=True, exist_ok=True)
    #
    #     return bill_dir, order_dir

    def makeBillDirsForDate(self, date: str):
        month, year = date.split(".")[1:]
        bill_dir = self._archivePath + '\\' + year + '\\' + month + "_" + local_months[int(month)] + '\\' + bills

        pathlib2.Path(bill_dir).mkdir(parents=True, exist_ok=True)

        return bill_dir

    def makeOrderDirsForDate(self, date: datetime.date):
        year, month = date.isoformat().split("-")[:2]
        order_dir = self._archivePath + '\\' + year + '\\' + month + "_" + local_months[int(month)] + '\\' + orders

        pathlib2.Path(order_dir).mkdir(parents=True, exist_ok=True)

        return order_dir


    def storeBillDocument(self, oldPath: str, date: str):
        if os.path.isfile(oldPath):
            newPath = os.path.normcase(self.makeBillDirsForDate(date) + "\\" + os.path.basename(oldPath))
            oldPath = os.path.normcase(oldPath)

            if os.path.normcase(oldPath) != newPath:
                try:
                    shutil.copy2(oldPath, newPath)
                except Exception as ex:
                    print('error copying file:', ex)
                    return False, ''

            print("storing", oldPath, "to", newPath)
            return True, newPath

        return True, ''

    def storeOrderDocument(self, oldPath: str, date: str):
        if os.path.isfile(oldPath):
            newPath = os.path.normcase(self.makeOrderDirsForDate(date) + "\\" + os.path.basename(oldPath))
            oldPath = os.path.normcase(oldPath)

            if os.path.normcase(oldPath) != newPath:
                try:
                    shutil.copy2(oldPath, newPath)
                except Exception as ex:
                    print('error copying file:', ex)
                    return False, ''

            print("storing", oldPath, "to", newPath)
            return True, newPath

        return True, ''

