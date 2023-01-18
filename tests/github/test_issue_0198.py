import unittest

from decouple import config

from benedict import benedict


class github_issue_0198_test_case(unittest.TestCase):
    """
    This class describes a github issue 0198 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/198

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0198
    """

    def test_constructor_with_s3_url_and_s3_options_with_file_json(self):
        aws_access_key_id = config("AWS_ACCESS_KEY_ID", default=None)
        aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY", default=None)
        if not all([aws_access_key_id, aws_secret_access_key]):
            # don't use s3 on GH CI
            return
        s3_options = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        }
        d = benedict(
            "s3://python-benedict/valid-content.json",
            s3_options=s3_options,
        )
        expected_dict = {"a": 1, "b": 2, "c": 3, "x": 7, "y": 8, "z": 9}
        self.assertEqual(d, expected_dict)

    def test_constructor_with_s3_url_and_s3_options_with_file_xlsx(self):
        aws_access_key_id = config("AWS_ACCESS_KEY_ID", default=None)
        aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY", default=None)
        if not all([aws_access_key_id, aws_secret_access_key]):
            # don't use s3 on GH CI
            return
        s3_options = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        }
        d = benedict(
            "s3://python-benedict/valid-content.xlsx",
            s3_options=s3_options,
        )
        expected_dict = {
            "values": [
                {
                    "mon": 10,
                    "tue": 11,
                    "wed": 12,
                    "thu": 13,
                    "fri": 14,
                    "sat": 15,
                    "sun": 16,
                },
                {
                    "mon": 20,
                    "tue": 21,
                    "wed": 22,
                    "thu": 23,
                    "fri": 24,
                    "sat": 25,
                    "sun": 26,
                },
                {
                    "mon": 30,
                    "tue": 31,
                    "wed": 32,
                    "thu": 33,
                    "fri": 34,
                    "sat": 35,
                    "sun": 36,
                },
            ]
        }
        self.assertEqual(d, expected_dict)
