import datetime as dt

from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_pickle_test_case(io_dict_test_case):
    """
    This class describes an IODict / pickle test case.
    """

    @staticmethod
    def _get_pickle_decoded():
        return {
            "date": dt.datetime(year=1985, month=4, day=3),
        }

    @staticmethod
    def _get_pickle_encoded():
        return "gAJ9cQBYBAAAAGRhdGVxAWNkYXRldGltZQpkYXRldGltZQpxAmNfY29kZWNzCmVuY29kZQpxA1gLAAAAB8OBBAMAAAAAAABxBFgGAAAAbGF0aW4xcQWGcQZScQeFcQhScQlzLg=="

    def test_from_pickle_with_valid_data(self):
        j = self._get_pickle_encoded()
        r = self._get_pickle_decoded()
        # static method
        d = IODict.from_pickle(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)
        # constructor
        d = IODict(j, format="pickle")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)

    def test_from_pickle_with_invalid_data(self):
        j = "Lorem ipsum est in ea occaecat nisi officia."
        # static method
        with self.assertRaises(ValueError):
            IODict.from_pickle(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format="pickle")

    def test_from_pickle_with_valid_file_valid_content(self):
        filepath = self.input_path("valid-content.pickle")
        # static method
        d = IODict.from_pickle(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="pickle")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_pickle_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path("valid-content.json")
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        filepath = self.input_path("valid-content.qs")
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        filepath = self.input_path("valid-content.toml")
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        filepath = self.input_path("valid-content.xml")
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        filepath = self.input_path("valid-content.yml")
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)

    def test_from_pickle_with_valid_file_invalid_content(self):
        filepath = self.input_path("invalid-content.pickle")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="pickle")

    def test_from_pickle_with_invalid_file(self):
        filepath = self.input_path("invalid-file.pickle")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="pickle")

    def test_from_pickle_with_valid_url_valid_content(self):
        url = self.input_url("valid-content.pickle")
        # static method
        d = IODict.from_pickle(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format="pickle")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(url)
        self.assertTrue(isinstance(d, dict))

    def test_from_pickle_with_valid_url_invalid_content(self):
        url = "https://github.com/fabiocaccamo/python-benedict"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_pickle(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="pickle")

    def test_from_pickle_with_invalid_url(self):
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_pickle(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="pickle")

    def test_to_pickle(self):
        d = IODict(self._get_pickle_decoded())
        s = d.to_pickle()
        self.assertEqual(IODict.from_pickle(s), self._get_pickle_decoded())

    def test_to_pickle_file(self):
        d = IODict({"date": self._get_pickle_decoded()})
        filepath = self.output_path("test_to_pickle_file.pickle")
        d.to_pickle(filepath=filepath)
        self.assertFileExists(filepath)
        self.assertEqual(d, IODict.from_pickle(filepath))
