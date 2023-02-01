import unittest

from benedict.core import standardize as _standardize


class standardize_test_case(unittest.TestCase):
    """
    This class describes a standardize test case.
    """

    def test_standardize(self):
        d = {
            "CamelCase": 1,
            "CamelCamelCase": 1,
            "Camel2Camel2Case": 1,
            "getHTTPResponseCode": 1,
            "get2HTTPResponseCode": 1,
            "HTTPResponseCode": 1,
            "HTTPResponseCodeXYZ": 1,
            " LocationCoordinates ": {
                "Lat. ": 0.0,
                "Lng. ": 0.0,
            },
            " LocationHistoryCoordinates ": [
                {
                    "Lat. ": 0.0,
                    "Lng. ": 0.0,
                },
                {
                    "Lat. ": 0.0,
                    "Lng. ": 0.0,
                },
            ],
        }
        _standardize(d)
        r = {
            "camel_case": 1,
            "camel_camel_case": 1,
            "camel2_camel2_case": 1,
            "get_http_response_code": 1,
            "get2_http_response_code": 1,
            "http_response_code": 1,
            "http_response_code_xyz": 1,
            "location_coordinates": {
                "lat": 0.0,
                "lng": 0.0,
            },
            "location_history_coordinates": [
                {
                    "lat": 0.0,
                    "lng": 0.0,
                },
                {
                    "lat": 0.0,
                    "lng": 0.0,
                },
            ],
        }
        # print(_dump(d))
        # print(_dump(r))
        self.assertEqual(d, r)
