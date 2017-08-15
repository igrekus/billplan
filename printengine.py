from datetime import datetime
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QColor
from copy import copy
from reportlab import rl_config
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.testutils import makeSuiteForClasses, outputfile, printLocation
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
import operator, string
from reportlab.platypus import *
# from reportlab import rl_config
from reportlab.lib.styles import PropertySet, getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus.paragraph import Paragraph
# from reportlab.lib.utils import fp_str
# from reportlab.pdfbase import pdfmetrics
from reportlab.platypus.flowables import PageBreak
import os
import unittest


class PrintEngine(QObject):

    def __init__(self, parent=None):
        super(PrintEngine, self).__init__(parent)

    def export(self, title: str, data: list, color: list):
        print("exporting data:")

        rl_config.warnOnMissingFontGlyphs = 0
        pdfmetrics.registerFont(TTFont('timesrus', 'c:\\windows\\fonts\\times.ttf'))
        pdfmetrics.registerFont(TTFont('timesrusb', 'c:\\windows\\fonts\\timesbd.ttf'))
        pdfmetrics.registerFontFamily('TimesRus', normal='timesrus', bold='timesrusb')

        GRID_STYLE_LIST = [('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]

        # GRID_STYLE = TableStyle([
        #     ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        #     ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        #     ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        #     ('VALIGN', (1, 0), (-1, -1), 'MIDDLE')
        # ])

        GRID_STYLE = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('FONT', (0, 0), (0, -1), 'timesrusb', 10)
        ])

        styleSheet = getSampleStyleSheet()

        styleTitle = styleSheet['Title']
        styleTitle.fontSize = 20
        styleTitle.fontName = 'TimesRus'

        styleCell = styleSheet['Normal']
        # styleCell.leading = 10
        styleCell.spaceBefore = 0
        styleCell.spaceAfter = 0
        styleCell.alignment = TA_JUSTIFY
        styleCell.fontName = 'TimesRus'

        lst = list()

        lst.append(Paragraph(title, styleTitle))

        dt = list()

        for i in range(len(data)):
            tmplist = list()
            for j in range(len(data[i])):
                if i == 0:
                    styleCell.fontSize = 10
                    tmplist.append(Paragraph("<b>" + str(data[i][j]) + "</b>", styleCell))
                else:
                    styleCell.fontSize = 8
                    if data[i][j] is not None:
                        tmplist.append(Paragraph(str(data[i][j]), styleCell))
                    else:
                        tmplist.append("")
                    if color[i][j] is not None:
                        GRID_STYLE.add('BACKGROUND', (i, j), (i, j), color[i][j].color().name())

            dt.append(tmplist)

        tbl = Table(dt, None, None)
        # tbl.setStyle(TableStyle(GRID_STYLE_LIST))
        tbl.setStyle(GRID_STYLE)

        lst.append(tbl)
        lst.append(Spacer(10, 10))

        template = SimpleDocTemplate(outputfile('report.pdf'), pagesize=landscape(A4), showBoundary=0,
                                     leftMargin=cm, rightMargin=cm, topMargin=cm, bottomMargin=cm)

        template.build(lst)
