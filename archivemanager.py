import datetime
import os
import pathlib2

import shutil
from PyQt5.QtCore import QObject

local_months = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
                'Ноябрь', 'Декабрь']

class ArchiveManager(QObject):
    def __init__(self, parent=None, arcPath=None):
        super(ArchiveManager, self).__init__(parent)

        self._archivePath: str = arcPath

        print('init archive manager')

    def makeDirForDate(self, date: str):
        month, year = date.split(".")[1:]
        directory = self._archivePath + '\\' + year + '\\' + month + "_" + local_months[int(month)]
        pathlib2.Path(directory).mkdir(parents=True, exist_ok=True)
        return directory

    def storeDocument(self, oldPath: str, date: str):
        if os.path.isfile(oldPath):
            newPath = os.path.normcase(self.makeDirForDate(date) + "\\" + os.path.basename(oldPath))
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
