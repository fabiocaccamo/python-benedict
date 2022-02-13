# -*- coding: utf-8 -*-

from benedict import benedict

import time
import unittest


class github_issue_0039_test_case(unittest.TestCase):
    """
    This class describes a github issue 0039 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/39

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0039
    """

    def test_performance(self):
        b = benedict()

        i_iterations = 500
        j_iterations = 100

        t = time.time()
        for i in range(0, i_iterations):
            for j in range(0, j_iterations):
                b.set("{}.{}".format(i, j), "text-{}-{}".format(i, j))
        # print(b.dump())
        e = time.time() - t
        # print('benedict set: {} seconds'.format(e))
        # self.assertTrue(e < 5)

        t = time.time()
        for i in range(0, i_iterations):
            for j in range(0, j_iterations):
                b.get("{}.{}".format(i, j), None)
        e = time.time() - t
        # print('benedict get: {} seconds'.format(e))
        # self.assertTrue(e < 5)

        b.clear()
        t = time.time()
        for i in range(0, i_iterations):
            for j in range(0, j_iterations):
                b.get("{}.{}".format(i, j), None)
        e = time.time() - t
        # print('benedict get (default): {} seconds'.format(e))
        # self.assertTrue(e < 5)
