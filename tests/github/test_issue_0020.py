import unittest
from typing import Any

import yaml
from yaml import Node

from benedict import benedict


class GetAtt(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!GetAtt"

    def __init__(self, val: Any) -> None:
        self.val = val

    @classmethod
    def from_yaml(cls, loader: Any, node: Node) -> Any:
        return cls(node.value)

    def __repr__(self) -> str:
        return f"GetAtt({self.val})"


yaml.add_constructor("!GetAtt", GetAtt.from_yaml)


class github_issue_0020_test_case(unittest.TestCase):
    """
    This class describes a github issue 0020 test case.
    """

    def test_github_issue_0020(self) -> None:
        """
        https://github.com/fabiocaccamo/python-benedict/issues/20
        """
        yaml_str = """
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Outputs:
    Description: "LoremIpsum Ex nisi incididunt occaecat dolor."
    Value: !GetAtt LoremIpsum.Arn
        """

        # r = {
        #     "AWSTemplateFormatVersion": "2010-09-09",
        #     "Transform": "AWS::Serverless-2016-10-31",
        #     "Outputs": {
        #         "Description": "LoremIpsum Ex nisi incididunt occaecat dolor.",
        #         "Value": GetAtt("LoremIpsum.Arn"),
        #     },
        # }

        b = benedict(yaml_str, format="yaml")
        # print(b.dump())

        self.assertEqual(b["AWSTemplateFormatVersion"], "2010-09-09")
        self.assertEqual(b["Transform"], "AWS::Serverless-2016-10-31")
        self.assertEqual(
            b["Outputs.Description"], "LoremIpsum Ex nisi incididunt occaecat dolor."
        )
        self.assertTrue(isinstance(b["Outputs.Value"], GetAtt))
        # self.assertEqual(b["Outputs.Value"], r["Outputs"]["Value"])
        # self.assertEqual(b, r)
