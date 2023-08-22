from pdfminer.high_level import extract_text
import xlsxwriter
import os

ex = {}
info = []
tag = ['горячие точки']
columns = [{'header': 'дата'}, {'header': "регион"}, {'header': "число"}, {'header': "точки"}]

text = extract_text('20120401.pdf')
fin = text.split()
info.append(str(fin[fin.index('на') - 1]))
info.append(str(fin[fin.index('природных') - 1]))
info.append(str(fin[fin.index('горячие') - 1]))
info.append(str(fin[fin.index('активных') - 1]))
info.append(str(fin[fin.index('точка).') - 2])[1:])
info.append(str(fin[fin.index('Максимальное') + 5]) + ' ' +
            str(fin[fin.index('Максимальное') + 6]) + ' ' + str(fin[fin.index('Максимальное') + 7])[1:-2])
info.append(str(fin[fin.index('них') + 3]))

ex[str(fin[fin.index('на') - 1])] = []
ex[str(fin[fin.index('на') - 1])].append(str(fin[fin.index('Максимальное') + 5]) + ' ' +
            str(fin[fin.index('Максимальное') + 6]))
ex[str(fin[fin.index('на') - 1])].append(str(fin[fin.index('Максимальное') + 7])[1:-2])
ex[str(fin[fin.index('на') - 1])].append(str(fin[fin.index('них') + 3]))


'''
info.append("дата - " + str(fin[fin.index('на') - 1]))
info.append("природных пожаров c активным горением - " + str(fin[fin.index('природных') - 1]))
info.append("горячие точки - " + str(fin[fin.index('горячие') - 1]))
info.append("активных  пожаров - " + str(fin[fin.index('активных') - 1]))
info.append("активных  пожаров лесов - " + str(fin[fin.index('точка).') - 2])[1:])
info.append("Максимальное число пожаров в - " + str(fin[fin.index('Максимальное') + 5]) + ' ' +
            str(fin[fin.index('Максимальное') + 6]) + ' ' + str(fin[fin.index('Максимальное') + 7])[1:-2])
info.append("На них было зарегистрировано (горячие точки) - " + str(fin[fin.index('них') + 3]))
'''
# print(text)
# print('\n'.join(info))

workbook = xlsxwriter.Workbook('Dataset.xlsx')
worksheet = workbook.add_worksheet()
data1 = [[a, *i] for a, i in ex.items()]
worksheet.add_table(0, 0, len(data1) + 1, 3, {'data': data1, 'columns': columns})
print(data1)
workbook.close()
