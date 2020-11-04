import xlwt
from public import config
xls = xlwt.Workbook()
sht1 = xls.add_sheet("report_modules")

xls.save('r', config.src_path+'/report/')


