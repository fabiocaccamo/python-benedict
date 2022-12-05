from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_ini_test_case(io_dict_test_case):
    """
    This class describes an IODict / ini test case.
    """

    def test_from_ini_with_valid_data(self):
        s = """
[DEFAULT]
ServerAliveInterval = 45
Compression = yes
CompressionLevel = 9
ForwardX11 = yes

[bitbucket.org]
User = hg

[topsecret.server.com]
Port = 50022
ForwardX11 = no
"""
        # static method
        r = {
            "serveraliveinterval": 45,
            "compression": True,
            "compressionlevel": 9,
            "forwardx11": True,
            "bitbucket.org": {
                "user": "hg",
                "serveraliveinterval": 45,
                "compression": True,
                "compressionlevel": 9,
                "forwardx11": True,
            },
            "topsecret.server.com": {
                "port": 50022,
                "forwardx11": False,
                "serveraliveinterval": 45,
                "compression": True,
                "compressionlevel": 9,
            },
        }
        d = IODict.from_ini(s)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)
        # constructor
        d = IODict(s, format="ini")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)

    def test_from_ini_with_invalid_data(self):
        s = "Lorem ipsum est in ea occaecat nisi officia."
        # static method
        with self.assertRaises(ValueError):
            IODict.from_ini(s)
        # constructor
        with self.assertRaises(ValueError):
            IODict(s, format="ini")

    def test_from_ini_with_valid_file_valid_content(self):
        filepath = self.input_path("valid-content.ini")
        # static method
        d = IODict.from_ini(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="ini")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_ini_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path("valid-content.base64")
        with self.assertRaises(ValueError):
            d = IODict.from_ini(filepath)
        filepath = self.input_path("valid-content.json")
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        filepath = self.input_path("valid-content.plist")
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        filepath = self.input_path("valid-content.qs")
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        filepath = self.input_path("valid-content.toml")
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        filepath = self.input_path("valid-content.xml")
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        filepath = self.input_path("valid-content.yml")
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)

    def test_from_ini_with_valid_file_invalid_content(self):
        filepath = self.input_path("invalid-content.ini")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="ini")

    def test_from_ini_with_invalid_file(self):
        filepath = self.input_path("invalid-file.ini")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="ini")

    # def test_from_ini_with_valid_url_valid_content(self):
    #     url = self.input_url('valid-content.ini')
    #     # static method
    #     d = IODict.from_ini(url)
    #     self.assertTrue(isinstance(d, dict))
    #     # constructor
    #     d = IODict(url, format='ini')
    #     self.assertTrue(isinstance(d, dict))
    #     # constructor with format autodetection
    #     d = IODict(url)
    #     self.assertTrue(isinstance(d, dict))

    def test_from_ini_with_valid_url_invalid_content(self):
        url = "https://github.com/fabiocaccamo/python-benedict"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_ini(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="ini")

    def test_from_ini_with_invalid_url(self):
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_ini(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="ini")

    def test_to_ini(self):
        d = IODict(
            {
                "serveraliveinterval": 45,
                "compression": True,
                "compressionlevel": 9,
                "forwardx11": True,
                "bitbucket.org": {
                    "user": "hg",
                    "serveraliveinterval": 45,
                    "compression": True,
                    "compressionlevel": 9,
                    "forwardx11": True,
                },
                "topsecret.server.com": {
                    "port": 50022,
                    "forwardx11": False,
                    "serveraliveinterval": 45,
                    "compression": True,
                    "compressionlevel": 9,
                },
            }
        )
        s = d.to_ini()
        self.assertEqual(d, IODict.from_ini(s))

    def test_to_ini_file(self):
        d = IODict(
            {
                "serveraliveinterval": 45,
                "compression": True,
                "compressionlevel": 9,
                "forwardx11": True,
                "bitbucket.org": {
                    "user": "hg",
                    "serveraliveinterval": 45,
                    "compression": True,
                    "compressionlevel": 9,
                    "forwardx11": True,
                },
                "topsecret.server.com": {
                    "port": 50022,
                    "forwardx11": False,
                    "serveraliveinterval": 45,
                    "compression": True,
                    "compressionlevel": 9,
                },
            }
        )
        filepath = self.output_path("test_to_ini_file.ini")
        d.to_ini(filepath=filepath)
        self.assertFileExists(filepath)
        self.assertEqual(d, IODict.from_ini(filepath))
