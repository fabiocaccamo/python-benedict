# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer

from openpyxl import load_workbook


class XLSSerializer(AbstractSerializer):
    """
    This class describes a xls serializer.
    """

    def __init__(self):
        super(XLSSerializer, self).__init__()

    def decode(self, s, **kwargs):
        columns = kwargs.pop("columns", None)
        columns_row = kwargs.pop("columns_row", True)
        sheet_index = kwargs.pop("sheet_index", 0)

        # load the worksheet
        workbook = load_workbook(filename=data_path, read_only=True)

        # read the sheets
        sheets = [sheet for sheet in workbook]
        sheet = sheets[sheet_index]

        # create columns if not passed as argument
        if not columns:
            columns_iterator = sheet.iter_cols(min_row=1, max_row=1)
            if columns_row:
                # if first row is for column names read the names
                columns = [cell.value for cell in columns_iterator]
            else:
                # otherwise use columns indexes as column names
                columns = [index for index in range(len(columns_iterator))]

        # build list of dicts, one for each row
        items = []
        items_row_index = 2 if columns_row else 1
        for row in sheet.iter_rows(min_row=items_row_index):
            values = list([cell.value for cell in row])
            items.append(dict(zip(columns, values)))

        # close the worksheet
        workbook.close()

        return items

    def encode(self, d, **kwargs):
        raise NotImplementedError
