import xlrd
import xlwt
import re


# 读取excel
class ExcelReadHelper:
    # 文件名称
    file_name = ""
    current_raw = 1
    pcd_col = 4
    et_col = 2
    size_col = 1
    seperator_ = '*'
    invalid_raw_index_list = []

    def __init__(self, file_name):
        self.file_name = file_name
        self.wb = xlrd.open_workbook(file_name)
        self.sh = self.wb.sheet_by_index(0)  # 第一个表
        self.all_raw = self.sh.nrows
        self.all_col = self.sh.ncols

    def get_next_raw(self):
        while True:
            if self.current_raw < self.all_raw:
                self.current_raw = self.current_raw + 1
                raw_data = self.sh.row_values(self.current_raw)
                if self.test_data(raw_data):
                    return raw_data
                else:
                    self.invalid_raw_index_list.append(self.current_raw)

            else:
                return

    # 行数据预校验
    def test_data(self, raw_data):
        # 直径和宽度校验
        size_ = str(raw_data[self.size_col])
        if re.match(r'^\d{2}[*](\d+(\.\d+)?)$', size_) is None:
            print("直径或宽度不合法")
            return False
        # et校验
        et = str(raw_data[self.et_col])
        if re.match(r'^\d{2}(\.\d+)?$', et) is None:
            print("ET 不合法")
            return False
        # 校验pcd
        pcd = str(raw_data[self.pcd_col])
        if re.match(r'^\d{1}[*](\d+(\.\d+)?)$', pcd) is None:
            print("pcd 不合法")
            return False
        return True

    # 获取pcd
    def get_pcd(self, raw_data):
        return raw_data[self.pcd_col]

    # 获取et
    def get_et(self, raw_data):
        return raw_data[self.et_col]

    # 轮毂宽度
    def get_rim_width(self, raw_data):
        if raw_data[self.size_col].find('*') != -1:
            return raw_data[1].split('*')[1]
        else:
            print("宽度不合法,行数据：")
            print(raw_data)

    # 获取轮毂直径
    def get_rim_diameter(self, raw_data):
        if raw_data[self.size_col].find('*') != -1:
            return raw_data[self.size_col].split('*')[0]
        else:
            print("直径不合法，行数据:")
            print(raw_data)


def test_excel_read():
    '''
    测试方法
    '''

    em = ExcelReadHelper("test.xls")
    for i in range(0, 10):
        raw = em.get_next_raw()
        print(em.get_rim_width(raw), em.get_rim_diameter(raw))


class ExcelWriteHelper:
    '''
    Excel写操作
    '''

    file_name = ""

    def __init__(self, file_name, title_list):
        self.file_name = file_name
        self.title_list = title_list
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet("Sheet 1")
        self.set_title()

    def set_title(self):
        title_style = xlwt.easyxf('font: bold 1')
        for i in range(len(self.title_list)):
            self.sheet.col(i).width = 1000 * (len(self.title_list[i]) + 1)
            self.sheet.write(0, i, self.title_list[i], title_style)

    def save(self):
        self.workbook.save(self.file_name)

    def write_raw(self, raw_index, raw_data):
        for i in range(len(raw_data)):
            self.sheet.write(raw_index, i, str(raw_data[i]))


def test_write_excel():
    '''
    写测试
    '''
    writer = ExcelWriteHelper("mytest.xls", ['姓名', '学号', '数学成绩'])
    writer.save()
