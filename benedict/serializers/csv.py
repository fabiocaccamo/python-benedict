# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer
from benedict.utils import type_util

from io import StringIO

import csv


class CSVSerializer(AbstractSerializer):
    """
    This class describes a csv serializer.
    """

    def __init__(self):
        super(CSVSerializer, self).__init__(
            extensions=[
                "csv",
            ],
        )

    def decode(self, s, **kwargs):
        # kwargs.setdefault('delimiter', ',')
        if kwargs.pop("quote", False):
            # TODO: add tests coverage
            kwargs.setdefault("quoting", csv.QUOTE_ALL)
        columns = kwargs.pop("columns", None)
        columns_row = kwargs.pop("columns_row", True)
        f = StringIO(s)
        r = csv.reader(f, **kwargs)
        ln = 0
        data = []
        for row in r:
            if ln == 0 and columns_row:
                if not columns:
                    columns = row
                ln += 1
                continue
            d = dict(zip(columns, row))
            data.append(d)
            ln += 1
        return data

    def encode(self, d, **kwargs):
        ls = d
        # kwargs.setdefault('delimiter', ',')
        if kwargs.pop("quote", False):
            kwargs.setdefault("quoting", csv.QUOTE_ALL)
        kwargs.setdefault("lineterminator", "\n")
        columns = kwargs.pop("columns", None)
        columns_row = kwargs.pop("columns_row", True)
        if not columns and len(ls) and type_util.is_dict(ls[0]):
            keys = [str(key) for key in ls[0].keys()]
            columns = list(sorted(keys))
        f = StringIO()
        w = csv.writer(f, **kwargs)
        if columns_row and columns:
            w.writerow(columns)
        for item in ls:
            if type_util.is_dict(item):
                row = [item.get(key, "") for key in columns]
            elif type_util.is_collection(item):
                # TODO: add tests coverage
                row = item
            else:
                # TODO: add tests coverage
                row = [item]
            w.writerow(row)
        data = f.getvalue()
        return data
