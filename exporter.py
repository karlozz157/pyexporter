#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datasource import MongoDataSource
import xlsxwriter
import json

class ExcelExporter(object):
    def export(self, data):
        self.header_columns = []
        filename = '%s_%s.xlsx' % (data['db'], data['collection'])
        self.workbook = xlsxwriter.Workbook(filename)
        self.worksheet = self.workbook.add_worksheet()
        self.__write_header(data['data'])
        self.__write_body(data['data'])
        self.workbook.close()
        return filename

    def __write_header(self, data):
        columns = []
        [[columns.append(column) if '_id' != column else '' for column in rows.keys()] for rows in data]
        columns = list(set(columns))
        columns.sort()
        column_count = 0
        for column in columns:
            self.header_columns.append(column)
            self.worksheet.write(0, column_count, column, self.workbook.add_format({'bold': True}))
            column_count += 1

    def __write_body(self, data):
        row_count = 1
        for rows in data:
            column_count = 0
            for header in self.header_columns:
                if header not in rows.keys():
                    column_value = ''
                else:
                    column_value = rows[header]
                if type(column_value) in [list, dict]:
                    json_dumped = json.dumps(column_value)
                    column_value = self.__to_string(json_dumped)
                self.worksheet.write(row_count, column_count, column_value)
                column_count += 1
            row_count += 1

    def __to_string(self, json_dumped):
        json_loaded = json.loads(json_dumped)
        string = ''
        if type(json_loaded) is dict:
            string += self.__dict_to_string(json_loaded)
        elif type(json_loaded) is list:
            for key in json_loaded:
                if type(key) == dict:
                    string += self.__dict_to_string(key)
                    string += '\n=========================\n'
                else: 
                    string += '%s, ' % str(key)
        return string

    def __dict_to_string(self, dictionary):
        array = ['%s: %s' % (key, dictionary[key]) for key in dictionary]
        return '\n'.join(array)
