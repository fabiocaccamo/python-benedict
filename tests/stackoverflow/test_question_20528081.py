import unittest


class stackoverflow_question_20528081_test_case(unittest.TestCase):
    def test_stackoverflow_question_20528081(self):
        """
        https://stackoverflow.com/questions/20528081/performance-of-calculations-on-large-flattened-dictionary-with-implied-hierarchy
        """
        from benedict import benedict as bdict

        d = {
            "guy1_arm_param1": 23.0,
            "guy1_arm_param2_low": 2.0,
            "guy1_arm_param2_high": 3.0,
            "guy1_arm_param3": 20.0,
            "guy1_leg_param1": 40.0,
            "guy1_leg_param2_low": 2.0,
            "guy1_leg_param2_high": 3.0,
            "guy1_leg_param3": 20.0,
            "guy2_arm_param1": 23.0,
            "guy2_arm_param2_low": 2.0,
            "guy2_arm_param2_high": 3.0,
            "guy2_arm_param3": 20.0,
            "guy2_leg_param1": 40.0,
            "guy2_leg_param2_low": 2.0,
            "guy2_leg_param2_high": 3.0,
            "guy2_leg_param3": 20.0,
            "another_guy_param1": 3.0,
        }
        b = bdict(d)
        u = b.unflatten()
        # print(u.dump())
        r = {
            "another": {
                "guy": {
                    "param1": 3.0,
                },
            },
            "guy1": {
                "arm": {
                    "param1": 23.0,
                    "param2": {
                        "high": 3.0,
                        "low": 2.0,
                    },
                    "param3": 20.0,
                },
                "leg": {
                    "param1": 40.0,
                    "param2": {
                        "high": 3.0,
                        "low": 2.0,
                    },
                    "param3": 20.0,
                },
            },
            "guy2": {
                "arm": {
                    "param1": 23.0,
                    "param2": {
                        "high": 3.0,
                        "low": 2.0,
                    },
                    "param3": 20.0,
                },
                "leg": {
                    "param1": 40.0,
                    "param2": {
                        "high": 3.0,
                        "low": 2.0,
                    },
                    "param3": 20.0,
                },
            },
        }
        self.assertEqual(u, r)
