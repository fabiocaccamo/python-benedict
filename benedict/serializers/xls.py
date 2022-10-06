# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer
from openpyxl import load_workbook
from slugify import slugify
from xlrd import open_workbook
import fsutil


class XLSSerializer(AbstractSerializer):
    """
    This class describes a xls serializer.
    """

    def __init__(self):
        super(XLSSerializer, self).__init__(
            extensions=[
                "xls",
                "xlsx",
                "xlsm",
            ],
        )

    def _get_sheet_index_and_name(self, **kwargs):
        sheet_index_or_name = kwargs.pop("sheet", 0)
        sheet_index = 0
        sheet_name = ""
        if isinstance(sheet_index_or_name, int):
            sheet_index = sheet_index_or_name
        elif isinstance(sheet_index_or_name, str):
            sheet_name = sheet_index_or_name
        return (sheet_index, sheet_name)

    def _decode_legacy(self, s, **kwargs):
        filepath = s

        # load the worksheet
        workbook = open_workbook(filename=filepath)

        # get sheet by index or by name
        sheet_index, sheet_name = self._get_sheet_index_and_name(**kwargs)
        if sheet_name:
            sheet_names = workbook.sheet_names()
            try:
                sheet_index = sheet_names.index(slugify(sheet_name))
            except ValueError:
                raise Exception(f"Invalid sheet name '{sheet_name}', sheet not found.")
        sheet = workbook.sheet_by_index(sheet_index)
        sheet_columns_range = range(sheet.ncols)

        # get columns
        columns = kwargs.pop("columns", None)
        columns_row = kwargs.pop("columns_row", True)
        columns_standardized = kwargs.pop("columns_standardized", columns is None)
        if not columns:
            if columns_row:
                # if first row is for column names read the names
                # for row in sheet.iter_rows(min_row=1, max_row=1):
                columns = [
                    sheet.cell_value(0, col_index) for col_index in sheet_columns_range
                ]
            else:
                # otherwise use columns indexes as column names
                # for row in sheet.iter_rows(min_row=1, max_row=1):
                columns = [col_index for col_index in sheet_columns_range]

        # standardize column names, eg. "Date Created" -> "date_created"
        if columns_standardized:
            columns = [slugify(column, separator="_") for column in columns]

        # build list of dicts, one for each row
        items = []
        items_row_start = 1 if columns_row else 0
        for row_index in range(items_row_start, sheet.nrows):
            row = {}
            for col_index in sheet_columns_range:
                col_key = columns[col_index]
                value = sheet.cell_value(row_index, col_index)
                row[col_key] = value
            items.append(row)

        # print(items)
        return items

    def _decode(self, s, **kwargs):
        filepath = s

        # load the worksheet
        workbook = load_workbook(filename=filepath, read_only=True)

        # select sheet by index or by name
        sheet_index, sheet_name = self._get_sheet_index_and_name(**kwargs)
        sheets = [sheet for sheet in workbook]
        if sheet_name:
            sheet_names = [slugify(sheet.title) for sheet in sheets]
            try:
                sheet_index = sheet_names.index(slugify(sheet_name))
            except ValueError:
                raise Exception(f"Invalid sheet name '{sheet_name}', sheet not found.")
        sheet = sheets[sheet_index]
        sheet_columns_cells = list(sheet.iter_rows(min_row=1, max_row=1))[0]

        # get columns
        columns = kwargs.pop("columns", None)
        columns_row = kwargs.pop("columns_row", True)
        columns_standardized = kwargs.pop("columns_standardized", columns is None)
        if not columns:
            if columns_row:
                # if first row is for column names read the names
                # for row in sheet.iter_rows(min_row=1, max_row=1):
                columns = [cell.value for cell in sheet_columns_cells]
            else:
                # otherwise use columns indexes as column names
                # for row in sheet.iter_rows(min_row=1, max_row=1):
                columns = [index for index in range(len(sheet_columns_cells))]

        # standardize column names, eg. "Date Created" -> "date_created"
        if columns_standardized:
            columns = [slugify(column, separator="_") for column in columns]

        # build list of dicts, one for each row
        items = []
        items_row_start = 2 if columns_row else 1
        for row in sheet.iter_rows(min_row=items_row_start):
            values = list([cell.value for cell in row])
            items.append(dict(zip(columns, values)))

        # close the worksheet
        workbook.close()

        # print(items)
        return items

    def decode(self, s, **kwargs):
        extension = fsutil.get_file_extension(s)
        if extension in ["xlsx", "xlsm"]:
            return self._decode(s, **kwargs)
        elif extension in ["xls", "xlt"]:
            return self._decode_legacy(s, **kwargs)

    def encode(self, d, **kwargs):
        raise NotImplementedError
