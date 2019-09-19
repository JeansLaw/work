import xlwt

class ExcelUtil(object):
    """
    使用步骤：

    1、setWorkBook  创建Excel文件

    2、setSheet     在Excel文件中创建表格

    3、getWorkBook  获取Excel文件(如wb=WorkBook)

    4、writeXls     进行数据写入

    5、wb.save(path)路径要以xls结尾，如wb.save("xxx.xls")
    """
    __count = 0
    __wb = None
    __sheet = None
    __arr = []

    def setWorkBook(self):
        """
        创建Excel文档
        """
        self.__wb = xlwt.Workbook()

    def getWorkBook(self):
        """
        获取Excel文档
        """
        return self.__wb

    def setSheet(self, sheetName):
        """ 
        :param sheetName:新建表格名称
        """
        self.sheet = self.__wb.add_sheet(sheetName)

    def writeXls(self, path="", arr=[]):
        """
        :param path: 保存Excel的路径
        :param arr: 输出到Excel的数据
        :return:
        """
        for i in range(len(arr)):
            self.sheet.write(self.__count, i, arr[i])
        self.__count = self.__count + 1

        try:
            self.__wb.save(path)
        except Exception as e:
            print("Excel保存路径设置不正确！")
            return
