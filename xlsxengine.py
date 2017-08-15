import const
import os
from PyQt5.QtCore import QObject
import openpyxl
import xlsxwriter


class XlsxEngine(QObject):
    def __init__(self, parent=None):
        super(XlsxEngine, self).__init__(parent)

    def export(self, title: str, header: list, data: list, color: list, footer_data: list, footer_color: list,
               widths: list):
        print("exporting data:")

        if not os.path.exists(r"report/"):
            os.mkdir(r"report/")

        wb = xlsxwriter.Workbook(r"report/" + title + ".xlsx")
        ws = wb.add_worksheet("Sheet1")

        fmtHeader = wb.add_format({
            'font_size': 10,
            'bold': True,
            'border': 2,
            'valign': 'vcenter',
            'align': 'center',
            'bg_color': '#E2E2E2'
        })

        fmtCellGood = wb.add_format({
            'font_size': 9,
            'border': 1,
            'border_color': '#848484',
            'valign': 'vcenter',
            'align': 'center',
            'bg_color': '#92D050',
            'text_wrap': True
        })

        fmtCellBad = wb.add_format({
            'font_size': 9,
            'border': 1,
            'border_color': '#848484',
            'valign': 'vcenter',
            'align': 'center',
            'bg_color': '#FF6767',
            'text_wrap': True
        })

        fmtCellNormal = wb.add_format({
            'font_size': 9,
            'border': 1,
            'border_color': '#848484',
            'valign': 'vcenter',
            'align': 'center',
            'bg_color': '#FFFFFF',
            'text_wrap': True
        })

        fmtCellPriorityLow = wb.add_format({
            'font_size': 9,
            'border': 1,
            'border_color': '#848484',
            'valign': 'vcenter',
            'align': 'center',
            'bg_color': '#AABF00',
            'text_wrap': True
        })

        fmtCellPriorityMid = wb.add_format({
            'font_size': 9,
            'border': 1,
            'border_color': '#848484',
            'valign': 'vcenter',
            'align': 'center',
            'bg_color': '#FFFF00',
            'text_wrap': True
        })

        ws.write('A1', title)

        for col in range(len(header)):
            ws.write(2, col, header[col], fmtHeader)

        for row in range(len(data)):
            for col in range(len(data[row])):
                fmt = fmtCellNormal
                if color[row][col] is not None:
                    clr = color[row][col].color().rgb()
                    if clr == const.COLOR_PAYMENT_PENDING:
                        fmt = fmtCellBad
                    elif clr == const.COLOR_PAYMENT_FINISHED:
                        fmt = fmtCellGood
                    elif clr == const.COLOR_PRIORITY_LOW:
                        fmt = fmtCellPriorityLow
                    elif clr == const.COLOR_PRIORITY_MEDIUM:
                        fmt = fmtCellPriorityMid

                ws.write(row + 3, col, data[row][col], fmt)

        for row in range(len(footer_data)):
            for col in range(len(footer_data[row])):
                fmt = fmtCellNormal
                if footer_color[row][col] is not None:
                    clr = footer_color[row][col].color().rgb()
                    if clr == const.COLOR_PAYMENT_PENDING:
                        fmt = fmtCellBad
                    elif clr == const.COLOR_PAYMENT_FINISHED:
                        fmt = fmtCellGood
                    elif clr == const.COLOR_PRIORITY_LOW:
                        fmt = fmtCellPriorityLow
                    elif clr == const.COLOR_PRIORITY_MEDIUM:
                        fmt = fmtCellPriorityMid

                ws.write(row + 3 + len(data), col, footer_data[row][col], fmt)

        # FIXME hack, allows to resize both rables
        k = 200
        if len(widths) == 11:
            k = k/1.4
        for col, w in enumerate(widths):
            ws.set_column(col, col, k*w)

        # print(len(widths), 200/len(widths))

        wb.close()

        os.startfile(r"report")
