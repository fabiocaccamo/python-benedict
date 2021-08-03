# -*- coding: utf-8 -*-

import unittest

from benedict import benedict


class assign_test_case(unittest.TestCase):
    def test__assign__(self):
        required_fields_to_linkages = {
            "in_scope": {"output_key": "scope", "fields": ["pk"]},
            "out_network": {"output_key": "network", "fields": ["pk"]},
            "in_commonsite": {
                "output_key": "common_site",
                "fields": ["pk", "common_site_id_number"],
            },
            "out_activity": {"output_key": "activity", "fields": ["pk"]},
            "in_subproject": {"output_key": "sub_project", "fields": ["pk"]},
        }
        new_linkage = benedict({"list": {}})

        output_config = required_fields_to_linkages["in_scope"]
        output_key = output_config["output_key"]
        new_linkage["list"][output_key] = {}

        for output_field in output_config["fields"]:
            new_linkage["list"][output_key][output_field] = None
            self.assertTrue(True)


