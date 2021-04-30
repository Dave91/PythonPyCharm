import win32com.client as win32
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from xlrd import open_workbook


owb = Workbook()
ows = owb.active
for i in range(10):
    ows.append([i])

adatf = Reference(ows, min_col=1, min_row=1, max_col=1, max_row=10)
diag = BarChart()
diag.add_data(adatf)
ows.add_chart(diag, "E10")
owb.save("diagproba.xlsx")

excel = win32.gencache.EnsureDispatch('Excel.Application')
excel.Visible = True
wb = excel.Workbooks.Add()
ws = wb.Worksheets('Munka1')
ws.Name = 'Python excel teszt'
ws.Cells(1, 1).Value = 'proba folyamatban...'
print(ws.Cells(1, 1).Value)
for i in range(1, 5):
    ws.Cells(2, i).Value = i
ws.Range(ws.Cells(3, 1), ws.Cells(3, 4)).Value = [5, 6, 7, 8]
ws.Range("A4:D4").Value = [i for i in range(9, 13)]
ws.Cells(5, 4).Formula = '=SUM(A2:D4)'
ws.Cells(5, 4).Font.Size = 16
ws.Cells(5, 4).Font.Bold = True

wbo = open_workbook('excelproba.xls')
print(f'\nMunkalapok: {wbo.nsheets} db')
for sheet in wbo.sheets():
    print(f'\n{sheet.name}')
    print(f'Oszl.: {sheet.ncols}')
    print(f'Sor: {sheet.nrows}')

print('\nproba befejeződött')
