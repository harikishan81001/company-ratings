"""
Base class for conversion, which takes as input a csv file
and gives as output a list of dictionaries.
The dictionary will contain header, value pairs.
The output will be a list of one such dictionary per row.
"""
import csv
import json
import xlrd


class InvalidFileFormat(Exception):
    pass



class File2Json(object):
    """
    Take as input a csv/xls/xlsx file and output json data
    """
    def __init__(self, file_name, *args, **kwargs):
        super(File2Json, self).__init__(*args, **kwargs)
        self.file_name = file_name
        self.file_extn = file_name.split('.')[-1]
        if self.file_extn == 'csv':
            self.converter = self.csv_converter
        elif self.file_extn == 'xls':
            self.converter = self.xls_converter
        elif self.file_extn == 'xlsx':
            self.converter = self.xlsx_converter
        else:
            raise InvalidFileFormat("Invalid file format.")

    def csv_converter(self):
        """
        csv to json converter
        """
        try:
            f = open(self.file_name, 'rb')
        except IOError:
            raise IOError("invalid file path, please check")
        reader = csv.reader(f)
        keys = reader.next()
        lines = []
        # encoding the data in ascii and if error comes in case of
        # ordinal characters not in range then encoding is done as punycode
        # which that ignores these type of characters
        for each in reader:
            line = []
            for cell in each:
                try:
                    line.append(cell.encode('ascii', 'ignore'))
                except UnicodeDecodeError:
                    line.append(cell.encode('punycode'))
            lines.append(line)
        out_dict = [dict(zip(keys, line)) for line in lines]
        # json_data = json.dumps(out_dict)
        return out_dict

    def xls_converter(self):
        """
        xls to json converter
        """
        try:
            xls = xlrd.open_workbook(self.file_name)
        except IOError:
            raise IOError("invalid file path, please check")
        data = {}
        sheets = xls.sheet_names()
        for sheet in sheets:
            work_sheet = xls.sheet_by_name(sheet)
            num_rows = work_sheet.nrows - 1
            curr_row = 0
            header_cells = work_sheet.row(0)
            # header values of the sheet
            header = [each.value for each in header_cells]
            out_list = []
            while curr_row < num_rows:
                curr_row += 1
                row = [each.value for each in work_sheet.row(curr_row)]
                out_list.append(dict(zip(header, row)))
            data[sheet] = out_list
        return data

    def xlsx_converter(self):
        """
        xlsx to json converter, currently no difference from xls converter
        """
        return self.xls_converter()

    def convert(self):
        """
        Call the converter as per the file format
        """
        return self.converter()
