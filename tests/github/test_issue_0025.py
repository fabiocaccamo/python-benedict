# -*- coding: utf-8 -*-

from benedict import benedict

import unittest


class github_issue_0025_test_case(unittest.TestCase):

    """
    https://github.com/fabiocaccamo/python-benedict/issues/25

    To run this specific test:
    - For each method comment @unittest.skip decorator
    - Run python -m unittest tests.github.test_issue_0025
    """

    @staticmethod
    def load_dict():
        yaml_str ="""
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
        servers = benedict.from_yaml(yaml_str)
        # print(servers.dump())
        return dict(servers)

    # @unittest.skip('testing main_dict and pointers failure')
    def test_pointers_with_dict(self):
        servers = dict(self.load_dict())
        # s01_ptr=dict(servers['SERVER']['S01'])
        s01_ptr=servers['SERVER']['S01']
        s01_ptr['alias']='ptr_alias'
        s01_ptr['location']['building']='ptr_building'
        s01_ptr['credentials']['username']='ptr_unsername'
        self.assertEqual(s01_ptr, servers['SERVER']['S01'])

    # @unittest.skip('testing copy and pointers failure')
    def test_pointers_with_benedict_casting(self):
        servers = benedict(self.load_dict())
        # s01_ptr=benedict(servers['SERVER.S01'])
        s01_ptr=servers['SERVER.S01']
        s01_ptr['alias']='ptr_alias'
        s01_ptr['location']['building']='ptr_building'
        s01_ptr['credentials']['username']='ptr_unsername'
        self.assertEqual(s01_ptr, servers['SERVER.S01'])
