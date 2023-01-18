import unittest


class stackoverflow_question_60276839_test_case(unittest.TestCase):
    def test_stackoverflow_question_60276839(self):
        """
        https://stackoverflow.com/questions/60276839/merge-list-of-nested-dictionaries
        """
        from benedict import benedict as bdict

        data_input = [
            {"9940542": {"Invalid Adjust(Platform Fee)": "-1.00"}},
            {"9940542": {"Invalid Adjust(Media Fee)": "-2.00"}},
            {"10315065": {"Invalid Adjust(Platform Fee)": "-1.00"}},
            {"10315065": {"Invalid Adjust(Media Fee)": "-3.00"}},
            {"11211744": {"Invalid Adjust(Platform Fee)": "-290.00"}},
            {"11211744": {"Invalid Adjust(Media Fee)": "-3403.00"}},
            {"11309685": {"Invalid Adjust(Platform Fee)": "-57.00"}},
            {"11309685": {"Invalid Adjust(Media Fee)": "-670.00"}},
            {"12103490": {"Media Fee": "709472.00"}},
            {"12103490": {"Platform Fee": "22703.00"}},
            {"12103490": {"Invalid Adjust(Platform Fee)": "-30.00"}},
            {"12103490": {"TrueView Budget Adjust (Platofrm Fee)": "-301.00"}},
            {"12103490": {"Invalid Adjust(Media Fee)": "-348.00"}},
            {"12103490": {"TrueView Budget Adjust (Media Fee)": "-9376.00"}},
            {"12160150": {"Media Fee": "549173.00"}},
            {"12160150": {"Platform Fee": "17573.00"}},
        ]
        data_output = bdict()
        data_output.merge(*data_input)
        # print(data_output.dump())

        expected_data_output = {
            "10315065": {
                "Invalid Adjust(Media Fee)": "-3.00",
                "Invalid Adjust(Platform Fee)": "-1.00",
            },
            "11211744": {
                "Invalid Adjust(Media Fee)": "-3403.00",
                "Invalid Adjust(Platform Fee)": "-290.00",
            },
            "11309685": {
                "Invalid Adjust(Media Fee)": "-670.00",
                "Invalid Adjust(Platform Fee)": "-57.00",
            },
            "12103490": {
                "Invalid Adjust(Media Fee)": "-348.00",
                "Invalid Adjust(Platform Fee)": "-30.00",
                "Media Fee": "709472.00",
                "Platform Fee": "22703.00",
                "TrueView Budget Adjust (Media Fee)": "-9376.00",
                "TrueView Budget Adjust (Platofrm Fee)": "-301.00",
            },
            "12160150": {
                "Media Fee": "549173.00",
                "Platform Fee": "17573.00",
            },
            "9940542": {
                "Invalid Adjust(Media Fee)": "-2.00",
                "Invalid Adjust(Platform Fee)": "-1.00",
            },
        }
        self.assertEqual(data_output, expected_data_output)
