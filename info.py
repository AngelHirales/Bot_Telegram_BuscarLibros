import xlrd
book = xlrd.open_workbook("pagina.xls")
print("The number of worksheets is {0}".format(book.nsheets))
print("Worksheet name(s): {0}".format(book.sheet_names()))
sh = book.sheet_by_index(4)
print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
#print("Cell D30 is {0}".format(sh.cell_value(rowx=9, colx=3)))
for rx in range(sh.nrows):
    print(sh.row(rx))