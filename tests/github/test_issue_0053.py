import unittest

from benedict import benedict


class github_issue_0053_test_case(unittest.TestCase):
    """
    This class describes a github issue 0053 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/53

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0053
    """

    def test_toml_dump_circular_reference(self):
        toml_str = """[build-system]
requires = [ "poetry-core>=1.0.0",]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "hermes"
version = "0.5.21"
description = "CI tool using Poetry"
authors = [ "Francisco Algaba <...>",]
readme = "README.md"

[tool.poetry.scripts]
hermes = "hermes.main:app"

[tool.poetry.dependencies]
python = ">=3.6.1,<4.0.0"
python-benedict = "^0.23.2"
mkdocs-material = "^7.1.2"
mkdocstrings = "^0.15.0"
mkdocs = "^1.1.2"
shiv = "^0.4.0"
pytest-json-report = "^1.2.4"
cruft = "^2.8.0"

[tool.poetry.dev-dependencies]
pytest = "^5.2"
Pygments = "^2.8.1"
pre-commit = "^2.12.0"
isort = "^5.8.0"

[tool.poetry.dependencies.typer]
extras = [ "all",]
version = "^0.3.2"

[tool.poetry.dev-dependencies.black]
version = "^20.8b1"
allow-prereleases = true
"""
        toml_dict = benedict.from_toml(toml_str)
        toml_dict["tool.poetry.name"] = "new name with custom value"
        # print(toml_dict.dump())
        toml_str_new = toml_dict.to_toml()
        # print(toml_str_new)
        self.assertTrue("new name with custom value" in toml_str_new)
