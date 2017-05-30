from datasource import MongoDataSource
import xlsxwriter
import json

class ExcelExporter(object):
    def export(self, data):
        filename = '%s_%s.xlsx' % (data['db'], data['collection'])
        self.workbook = xlsxwriter.Workbook(filename)
        self.worksheet = self.workbook.add_worksheet()
        self.__write_header(data['data'])
        self.__write_body(data['data'])
        self.workbook.close()
        return filename

    def __write_header(self, data):
        headers = data[0].keys()
        column_count = 0
        for header in headers:
            if '_id' == header:
                continue
            self.worksheet.write(0, column_count, header, self.workbook.add_format({'bold': True}))
            column_count += 1

    def __write_body(self, data):
        row_count = 1
        for rows in data:
            column_count = 0
            for column in rows:
                if '_id' == column:
                    continue
                column_value = rows[column]
                if type(column_value) in [list, dict]:
                    column_value = json.dumps(column_value)
                self.worksheet.write(row_count, column_count, column_value)
                column_count += 1
            row_count += 1
