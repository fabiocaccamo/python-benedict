import unittest
from unittest.mock import MagicMock, patch

from benedict.serializers import XLSSerializer


class xls_cleanup_test_case(unittest.TestCase):
    def test_modern_workbooks_close_on_row_error(self) -> None:
        book = MagicMock()
        sheet = MagicMock()
        sheet.iter_rows.side_effect = RuntimeError("unreadable worksheet")
        book.__iter__.return_value = iter([sheet])
        with patch("benedict.serializers.xls.load_workbook", return_value=book):
            with self.assertRaisesRegex(RuntimeError, "unreadable worksheet"):
                XLSSerializer()._decode("example.xlsx")
        book.close.assert_called_once_with()
        book.vba_archive.close.assert_called_once_with()

    def test_legacy_workbooks_release_resources_on_error(self) -> None:
        book = MagicMock()
        book.sheet_by_index.side_effect = IndexError("sheet does not exist")
        with patch("benedict.serializers.xls.open_workbook", return_value=book):
            with self.assertRaisesRegex(IndexError, "sheet does not exist"):
                XLSSerializer()._decode_legacy("example.xls", sheet=2)
        book.release_resources.assert_called_once_with()
