from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_csv_test_case(io_dict_test_case):
    """
    This class describes an IODict / csv test case.
    """

    def test_from_csv_with_valid_data(self):
        s = """id,name,age,height,weight
1,Alice,20,62,120.6
2,Freddie,21,74,190.6
3,Bob,17,68,120.0
4,François,32,75,110.05
"""
        r = {
            "values": [
                {
                    "id": "1",
                    "name": "Alice",
                    "age": "20",
                    "height": "62",
                    "weight": "120.6",
                },
                {
                    "id": "2",
                    "name": "Freddie",
                    "age": "21",
                    "height": "74",
                    "weight": "190.6",
                },
                {
                    "id": "3",
                    "name": "Bob",
                    "age": "17",
                    "height": "68",
                    "weight": "120.0",
                },
                {
                    "id": "4",
                    "name": "François",
                    "age": "32",
                    "height": "75",
                    "weight": "110.05",
                },
            ],
        }
        # static method
        d = IODict.from_csv(s)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)
        # constructor
        d = IODict(s, format="csv")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)

    # def test_from_csv_with_invalid_data(self):
    #     s = 'Lorem ipsum est in ea occaecat nisi officia.'
    #     # static method
    #     with self.assertRaises(ValueError):
    #         print(IODict.from_csv(s))
    #     # constructor
    #     with self.assertRaises(ValueError):
    #         IODict(s, format='csv')

    def test_from_csv_with_valid_file_valid_content(self):
        filepath = self.input_path("valid-content.csv")
        # static method
        d = IODict.from_csv(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="csv")
        self.assertTrue(isinstance(d, dict))

    # def test_from_csv_with_valid_file_valid_content_invalid_format(self):
    #     filepath = self.input_path('valid-content.base64')
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)
    #     filepath = self.input_path('valid-content.qs')
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)
    #     filepath = self.input_path('valid-content.toml')
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)
    #     filepath = self.input_path('valid-content.xml')
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)
    #     filepath = self.input_path('valid-content.yml')
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)

    # def test_from_csv_with_valid_file_invalid_content(self):
    #     filepath = self.input_path('invalid-content.csv')
    #     # static method
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)
    #     # constructor
    #     with self.assertRaises(ValueError):
    #         IODict(filepath, format='csv')

    def test_from_csv_with_invalid_file(self):
        filepath = self.input_path("invalid-file.csv")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_csv(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="csv")

    # TODO: python 2.7 max compatibility
    # def test_from_csv_with_valid_url_valid_content(self):
    #     url = self.input_url('valid-content.csv')
    #     # static method
    #     d = IODict.from_csv(url)
    #     self.assertTrue(isinstance(d, dict))
    #     # constructor
    #     d = IODict(url, format='csv')
    #     self.assertTrue(isinstance(d, dict))

    # def test_from_csv_with_valid_url_invalid_content(self):
    #     url = 'https://github.com/fabiocaccamo/python-benedict'
    #     # static method
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(url)
    #     # constructor
    #     with self.assertRaises(ValueError):
    #         IODict(url, format='csv')

    def test_from_csv_with_invalid_url(self):
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_csv(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="csv")

    def test_to_csv(self):
        d = IODict(
            {
                "values": [
                    {
                        "id": "1",
                        "name": "Alice",
                        "age": "20",
                        "height": "62",
                        "weight": "120.6",
                    },
                    {
                        "id": "2",
                        "name": "Freddie",
                        "age": "21",
                        "height": "74",
                        "weight": "190.6",
                    },
                    {
                        "id": "3",
                        "name": "Bob",
                        "age": "17",
                        "height": "68",
                        "weight": "120.0",
                    },
                    {
                        "id": "4",
                        "name": "François",
                        "age": "32",
                        "height": "75",
                        "weight": "110.05",
                    },
                ],
            }
        )
        s = d.to_csv()
        r = """age,height,id,name,weight
20,62,1,Alice,120.6
21,74,2,Freddie,190.6
17,68,3,Bob,120.0
32,75,4,François,110.05
"""
        self.assertEqual(s, r)

    def test_to_csv_with_custom_columns(self):
        d = IODict(
            {
                "values": [
                    {
                        "id": "1",
                        "name": "Alice",
                        "age": "20",
                        "height": "62",
                        "weight": "120.6",
                    },
                    {
                        "id": "2",
                        "name": "Freddie",
                        "age": "21",
                        "height": "74",
                        "weight": "190.6",
                    },
                    {
                        "id": "3",
                        "name": "Bob",
                        "age": "17",
                        "height": "68",
                        "weight": "120.0",
                    },
                    {
                        "id": "4",
                        "name": "François",
                        "age": "32",
                        "height": "75",
                        "weight": "110.05",
                    },
                ],
            }
        )
        s = d.to_csv(
            key="values",
            columns=["id", "name", "family_name", "age", "height", "gender", "weight"],
        )
        r = """id,name,family_name,age,height,gender,weight
1,Alice,,20,62,,120.6
2,Freddie,,21,74,,190.6
3,Bob,,17,68,,120.0
4,François,,32,75,,110.05
"""
        self.assertEqual(s, r)

    def test_to_csv_with_custom_delimiter_and_quotes(self):
        d = IODict(
            {
                "values": [
                    {
                        "id": "1",
                        "name": "Alice",
                        "age": "20",
                        "height": "62",
                        "weight": "120.6",
                    },
                    {
                        "id": "2",
                        "name": "Freddie",
                        "age": "21",
                        "height": "74",
                        "weight": "190.6",
                    },
                    {
                        "id": "3",
                        "name": "Bob",
                        "age": "17",
                        "height": "68",
                        "weight": "120.0",
                    },
                    {
                        "id": "4",
                        "name": "François",
                        "age": "32",
                        "height": "75",
                        "weight": "110.05",
                    },
                ],
            }
        )
        s = d.to_csv(
            columns=["id", "name", "age", "height", "weight"], delimiter=";", quote=True
        )
        r = """"id";"name";"age";"height";"weight"
"1";"Alice";"20";"62";"120.6"
"2";"Freddie";"21";"74";"190.6"
"3";"Bob";"17";"68";"120.0"
"4";"François";"32";"75";"110.05"
"""
        self.assertEqual(s, r)

    def test_to_csv_with_custom_key_valid(self):
        d = IODict(
            {
                "results": [
                    {
                        "id": "1",
                        "name": "Alice",
                        "age": "20",
                        "height": "62",
                        "weight": "120.6",
                    },
                    {
                        "id": "2",
                        "name": "Freddie",
                        "age": "21",
                        "height": "74",
                        "weight": "190.6",
                    },
                    {
                        "id": "3",
                        "name": "Bob",
                        "age": "17",
                        "height": "68",
                        "weight": "120.0",
                    },
                    {
                        "id": "4",
                        "name": "François",
                        "age": "32",
                        "height": "75",
                        "weight": "110.05",
                    },
                ],
            }
        )
        s = d.to_csv("results", columns=["id", "name", "age", "height", "weight"])
        r = """id,name,age,height,weight
1,Alice,20,62,120.6
2,Freddie,21,74,190.6
3,Bob,17,68,120.0
4,François,32,75,110.05
"""
        self.assertEqual(s, r)

    def test_to_csv_with_custom_key_invalid(self):
        d = IODict(
            {
                "values": [
                    {
                        "id": "1",
                        "name": "Alice",
                        "age": "20",
                        "height": "62",
                        "weight": "120.6",
                    },
                    {
                        "id": "2",
                        "name": "Freddie",
                        "age": "21",
                        "height": "74",
                        "weight": "190.6",
                    },
                    {
                        "id": "3",
                        "name": "Bob",
                        "age": "17",
                        "height": "68",
                        "weight": "120.0",
                    },
                    {
                        "id": "4",
                        "name": "François",
                        "age": "32",
                        "height": "75",
                        "weight": "110.05",
                    },
                ],
            }
        )
        with self.assertRaises(KeyError):
            s = d.to_csv(
                "invalid_values", columns=["id", "name", "age", "height", "weight"]
            )

    def test_to_csv_file(self):
        d = IODict(
            {
                "values": [
                    {
                        "id": "1",
                        "name": "Alice",
                        "age": "20",
                        "height": "62",
                        "weight": "120.6",
                    },
                    {
                        "id": "2",
                        "name": "Freddie",
                        "age": "21",
                        "height": "74",
                        "weight": "190.6",
                    },
                    {
                        "id": "3",
                        "name": "Bob",
                        "age": "17",
                        "height": "68",
                        "weight": "120.0",
                    },
                    {
                        "id": "4",
                        "name": "François",
                        "age": "32",
                        "height": "75",
                        "weight": "110.05",
                    },
                ],
            }
        )
        filepath = self.output_path("test_to_csv_file.csv")
        d.to_csv(filepath=filepath)
        self.assertFileExists(filepath)
        self.assertEqual(d, IODict.from_csv(filepath))
