import unittest


class stackoverflow_question_60066331_test_case(unittest.TestCase):
    def test_stackoverflow_question_60066331(self):
        """
        https://stackoverflow.com/questions/60066331/find-elements-in-python-dict
        """
        from benedict import benedict as bdict

        d = bdict(
            {
                "ResponseMetadata": {"NOT IMPORTANT"},
                "hasMoreResults": True,
                "marker": '{"NOT IMPORTANT"}',
                "pipelineIdList": [
                    {"id": "df-0001", "name": "Blue"},
                    {"id": "df-0002", "name": "Orange"},
                    {"id": "df-0003", "name": "Green"},
                    {"id": "df-0004", "name": "Red"},
                    {"id": "df-0005", "name": "Purple"},
                ],
            }
        )
        results = d.search(
            "red", in_keys=False, in_values=True, exact=True, case_sensitive=False
        )
        # for item, key, value in results:
        #     print(item) # {'id': 'df-0004', 'name': 'Red'}
        #     print(key) # 'name'
        #     print(value) # 'Red'

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0],
            (
                {"id": "df-0004", "name": "Red"},
                "name",
                "Red",
            ),
        )
