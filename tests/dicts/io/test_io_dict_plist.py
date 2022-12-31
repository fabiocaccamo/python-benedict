import datetime as dt
import plistlib

from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_plist_test_case(io_dict_test_case):
    """
    This class describes an IODict / plist test case.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dict = dict(
            aString="Doodah",
            aList=[
                "A",
                "B",
                12,
                32.1,
                [1, 2, 3],
            ],
            aFloat=0.1,
            anInt=728,
            aDict=dict(
                anotherString="<hello & hi there!>",
                aThirdString="M\xe4ssig, Ma\xdf",
                aTrueValue=True,
                aFalseValue=False,
            ),
            someData=bytes("<binary gunk>", encoding="utf-8"),
            someMoreData=bytes("<lots of binary gunk>" * 10, encoding="utf-8"),
            aDate=dt.datetime(
                1985, 4, 3, 23, 55
            ),  # dt.datetime.fromtimestamp(481413300),
        )
        # self._dict = {
        #     'aString': 'Doodah',
        #     'aList': ['A', 'B', 12, 32.1, [1, 2, 3]],
        #     'aFloat': 0.1,
        #     'anInt': 728,
        #     'aDict': {
        #         'anotherString': '<hello & hi there!>',
        #         'aThirdString': 'M\xe4ssig, Ma\xdf',
        #         'aTrueValue': True,
        #         'aFalseValue': False,
        #     },
        #     'someData': b'<binary gunk>',
        #     'someMoreData': b'<lots of binary gunk>' * 10,
        #     'aDate': dt.datetime.fromtimestamp(481406100),
        # }
        self._plist = """
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>aDate</key>
    <date>1985-04-03T23:55:00Z</date>
    <key>aDict</key>
    <dict>
        <key>aFalseValue</key>
        <false/>
        <key>aThirdString</key>
        <string>Mässig, Maß</string>
        <key>aTrueValue</key>
        <true/>
        <key>anotherString</key>
        <string>&lt;hello &amp; hi there!&gt;</string>
    </dict>
    <key>aFloat</key>
    <real>0.1</real>
    <key>aList</key>
    <array>
        <string>A</string>
        <string>B</string>
        <integer>12</integer>
        <real>32.1</real>
        <array>
            <integer>1</integer>
            <integer>2</integer>
            <integer>3</integer>
        </array>
    </array>
    <key>aString</key>
    <string>Doodah</string>
    <key>anInt</key>
    <integer>728</integer>
    <key>someData</key>
    <data>
    PGJpbmFyeSBndW5rPg==
    </data>
    <key>someMoreData</key>
    <data>
    PGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMgb2Yg
    YmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5IGd1
    bms+PGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMg
    b2YgYmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5IGd1bms+PGxvdHMgb2YgYmluYXJ5
    IGd1bms+
    </data>
</dict>
</plist>
"""

    def test_from_plist_with_valid_data(self):
        j = self._plist
        # static method
        d = IODict.from_plist(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d.get("aDate"), self._dict.get("aDate"))
        self.assertEqual(d, self._dict)
        # constructor
        d = IODict(j, format="plist")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, self._dict)

    def test_from_plist_with_invalid_data(self):
        j = "Lorem ipsum est in ea occaecat nisi officia."
        # static method
        with self.assertRaises(ValueError):
            IODict.from_plist(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format="plist")

    def test_from_plist_with_valid_file_valid_content(self):
        filepath = self.input_path("valid-content.plist")
        # static method
        d = IODict.from_plist(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="plist")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_plist_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path("valid-content.base64")
        with self.assertRaises(ValueError):
            IODict.from_plist(filepath)
        filepath = self.input_path("valid-content.csv")
        with self.assertRaises(ValueError):
            IODict.from_plist(filepath)
        filepath = self.input_path("valid-content.json")
        with self.assertRaises(ValueError):
            IODict.from_plist(filepath)
        filepath = self.input_path("valid-content.pickle")
        with self.assertRaises(ValueError):
            IODict.from_plist(filepath)
        filepath = self.input_path("valid-content.qs")
        with self.assertRaises(ValueError):
            IODict.from_plist(filepath)
        filepath = self.input_path("valid-content.toml")
        with self.assertRaises(ValueError):
            IODict.from_plist(filepath)
        filepath = self.input_path("valid-content.xml")
        with self.assertRaises(ValueError):
            IODict.from_plist(filepath)
        filepath = self.input_path("valid-content.yml")
        with self.assertRaises(ValueError):
            IODict.from_plist(filepath)

    def test_from_plist_with_valid_file_invalid_content(self):
        filepath = self.input_path("invalid-content.plist")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_plist(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="plist")

    def test_from_plist_with_invalid_file(self):
        filepath = self.input_path("invalid-file.plist")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_plist(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="plist")

    def test_from_plist_with_valid_url_valid_content(self):
        url = self.input_url("valid-content.plist")
        # static method
        d = IODict.from_plist(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format="plist")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(url)
        self.assertTrue(isinstance(d, dict))

    def test_from_plist_with_valid_url_invalid_content(self):
        url = "https://github.com/fabiocaccamo/python-benedict"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_plist(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="plist")

    def test_from_plist_with_invalid_url(self):
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_plist(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="plist")

    def test_to_plist(self):
        # example data taken from:
        # https://docs.python.org/3/library/plistlib.html#examples
        d = IODict(self._dict)
        s = d.to_plist()
        # print(s)
        self.assertEqual(d, IODict.from_plist(s))

    def test_to_plist_file(self):
        d = IODict(self._dict)
        filepath = self.output_path("test_to_plist_file.plist")
        d.to_plist(filepath=filepath)
        self.assertFileExists(filepath)
        self.assertEqual(d, IODict.from_plist(filepath))
