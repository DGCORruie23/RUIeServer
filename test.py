import openpyxl as opxl
from openpyxl.writer.excel import save_virtual_workbook

workbook = opxl.load_workbook(filename='tmp/dup.xlsm', keep_vba=True)
worksheet = workbook.active

worksheet.append(['uno'])

workbook.save("info.xlsm")