import unittest

import yaml

from benedict import benedict


class github_issue_0025_test_case(unittest.TestCase):
    """
    This class describes a github issue 0025 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/25

    To run this specific test:
    - For each method comment @unittest.skip decorator
    - Run python -m unittest tests.github.test_issue_0025
    """

    @staticmethod
    def load_dict():
        yaml_str = """
SERVER:
    S01:
        alias: s01_alias
        ssh_port: s01_port
        host: s01_host
        credentials:
            username: s01_user
            password: s01_passw
        location:
            building: s01_building
            floar: s01_floar
            room: s01_room
        """
        servers = yaml.safe_load(yaml_str)
        return servers

    def test_pointers_with_dict(self):
        servers = dict(self.load_dict())
        s01_ptr = servers["SERVER"]["S01"]
        s01_ptr["alias"] = "ptr_alias"
        s01_ptr["location"]["building"] = "ptr_building"
        s01_ptr["credentials"]["username"] = "ptr_unsername"
        self.assertEqual(s01_ptr, servers["SERVER"]["S01"])

    def test_pointers_with_benedict_casting(self):
        d = self.load_dict()
        servers = benedict(d)
        s01_ptr = servers["SERVER.S01"]
        self.assertTrue(isinstance(s01_ptr, benedict))
        self.assertEqual(type(s01_ptr), benedict)
        s01_ptr["alias"] = "ptr_alias"
        s01_ptr["location"]["building"] = "ptr_building"
        s01_ptr["credentials"]["username"] = "ptr_unsername"
        self.assertEqual(s01_ptr, servers["SERVER.S01"])

    def test_pointers_after_pointer_update(self):
        d = self.load_dict()
        b = benedict(d)
        d["SERVER"]["S01"]["alias"] = "new_alias"
        d["SERVER_2"] = "server_2"
        self.assertEqual(b, d)
        self.assertEqual(b.dict(), d)

    def test_pointers_after_pointer_clear(self):
        d = self.load_dict()
        b = benedict(d)
        d.clear()
        self.assertEqual(b, d)
        self.assertEqual(b.dict(), d)
