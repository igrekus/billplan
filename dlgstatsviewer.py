import datetime

import const
import sys
from orderitem import OrderItem
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QDate

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavToolbar


class DlgStatsViewer(QDialog):

    def __init__(self, parent=None, domainModel=None):
        super(DlgStatsViewer, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.ui = uic.loadUi("dlgstatsviewer.ui", self)

        # init instances
        self._domainModel = domainModel

        self.initDialog()

    def initDialog(self):
        print("init stat viewer")

        plt.figure(num=1)
        canvas = FigureCanvas(plt.figure(1))
        NavToolbar(canvas=canvas, parent=None)
        self.ui.vlPlot.addWidget(canvas)
        self.ui.vlPlot.addWidget(canvas.toolbar)

        sizes, labels = self._domainModel.getBillStats()

        total = sum(sizes)

        new_sizes = list()
        new_labels = list()

        for s, l in zip(sizes, labels):
            if s / total > 0.05:
                new_sizes.append(s)
                new_labels.append(l)

        _, _, _ = plt.pie(x=new_sizes, labels=new_labels, shadow=True, autopct='%1.1f%%', pctdistance=1.1, labeldistance=1.2)
        # plt.legend(patches, new_labels, loc='best')

        plt.axis('equal')
        plt.tight_layout()


