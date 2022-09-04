from openpyxl.styles import Font, Alignment
import openpyxl


def treatment():
    wb = openpyxl.load_workbook('Countries list.xlsx')
    ws = wb.active
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 12
    wb.save('Countries list.xlsx')
    return


if __name__ == '__main__':
    treatment()
