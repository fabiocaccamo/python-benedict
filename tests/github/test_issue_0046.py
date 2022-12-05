import json
import unittest

from benedict import benedict


class github_issue_0046_test_case(unittest.TestCase):
    """
    This class describes a github issue 0046 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/46

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0046
    """

    def test_json_dumps_with_cloned_instance(self):
        d = {
            "id": "37e4f6e876",
            "meta": {
                "data": {
                    "category": "category0",
                    "id": "data_id",
                    "title": "A title",
                },
                "id": "37e4f6e876",
                "k0": {
                    "ka": {
                        "key1": "",
                        "key2": "value2",
                        "key3": "value3",
                        "key4": True,
                    },
                    "kb": {
                        "key1": "",
                        "key2": "value2",
                        "key3": "value3",
                        "key4": True,
                    },
                    "kc": {
                        "extra_key2": "value2",
                        "key1": "",
                        "key2": "value2",
                        "key3": "value3",
                        "key4": True,
                    },
                    "kd": {
                        "key1": "",
                        "key2": "value2",
                        "key3": "value3",
                        "key4": True,
                    },
                    "ke": {
                        "key1": "",
                        "key2": "value2",
                        "key3": "value3",
                        "key4": True,
                    },
                    "kf": {
                        "key1": "",
                        "key2": "value2",
                        "key3": "separated",
                        "key4": True,
                    },
                },
                "language": "en",
                "name": "name_value",
            },
        }
        keypaths = ["id", "meta.k0.kc", "meta.language"]
        d = benedict(d)
        d_new = benedict()
        d_new = d.subset(keypaths)

        # patch the json module to force the use of the python encoder - #46
        # import json
        # json.encoder.c_make_encoder = None
        json_encoder = None
        json_dumps = lambda d: json.dumps(d, sort_keys=True, cls=json_encoder)

        d_new_raw = {
            "id": "37e4f6e876",
            "meta": {
                "k0": {
                    "kc": {
                        "extra_key2": "value2",
                        "key1": "",
                        "key2": "value2",
                        "key3": "value3",
                        "key4": True,
                    }
                },
                "language": "en",
            },
        }
        self.assertEqual(d_new, d_new_raw)
        self.assertEqual(json_dumps(d_new), json_dumps(d_new_raw))
        self.assertEqual(
            d_new.to_json(sort_keys=True, cls=json_encoder), json_dumps(d_new_raw)
        )

        d_new_cloned = d_new.clone()
        self.assertEqual(d_new, d_new_cloned)
        self.assertEqual(json_dumps(d_new), json_dumps(d_new_cloned))
        self.assertEqual(
            d_new.to_json(sort_keys=True), d_new_cloned.to_json(sort_keys=True)
        )
