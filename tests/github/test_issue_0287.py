from benedict import benedict
from tests.dicts.io.test_io_dict import io_dict_test_case


class github_issue_0287_test_case(io_dict_test_case):
    """
    This class describes a github issue 0287 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/287

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0287
    """

    def test_sources_argument_with_all_list(self):
        filepath = self.input_path("valid-content.json")
        _ = benedict(filepath, sources=["*"])
        _ = benedict.from_json(filepath, sources=["*"])

        _ = benedict(filepath, sources=["all"])
        _ = benedict.from_json(filepath, sources=["all"])

        _ = benedict(filepath, sources=["auto"])
        _ = benedict.from_json(filepath, sources=["auto"])

    def test_sources_argument_with_all_string(self):
        filepath = self.input_path("valid-content.json")
        _ = benedict(filepath, sources="*")
        _ = benedict.from_json(filepath, sources="*")

        _ = benedict(filepath, sources="all")
        _ = benedict.from_json(filepath, sources="all")

        _ = benedict(filepath, sources="auto")
        _ = benedict.from_json(filepath, sources="auto")

    def test_sources_argument_with_list(self):
        filepath = self.input_path("valid-content.json")

        _ = benedict(filepath, sources=["file"])
        with self.assertRaises(ValueError):
            _ = benedict(filepath, sources=["url"])
        with self.assertRaises(ValueError):
            _ = benedict(filepath, sources=["s3"])
        with self.assertRaises(ValueError):
            _ = benedict(filepath, sources=["data"])

        _ = benedict.from_json(filepath, sources=["file"])
        with self.assertRaises(ValueError):
            _ = benedict.from_json(filepath, sources=["url"])
        with self.assertRaises(ValueError):
            _ = benedict.from_json(filepath, sources=["s3"])
        with self.assertRaises(ValueError):
            _ = benedict.from_json(filepath, sources=["data"])

    def test_sources_argument_with_string(self):
        filepath = self.input_path("valid-content.json")

        _ = benedict(filepath, sources="file")
        with self.assertRaises(ValueError):
            _ = benedict(filepath, sources="url")
        with self.assertRaises(ValueError):
            _ = benedict(filepath, sources="s3")
        with self.assertRaises(ValueError):
            _ = benedict(filepath, sources="data")

        _ = benedict.from_json(filepath, sources="file")
        with self.assertRaises(ValueError):
            _ = benedict.from_json(filepath, sources="url")
        with self.assertRaises(ValueError):
            _ = benedict.from_json(filepath, sources="s3")
        with self.assertRaises(ValueError):
            _ = benedict.from_json(filepath, sources="data")
