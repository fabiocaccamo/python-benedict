from argparse import ArgumentError, ArgumentParser
from collections import Counter
from re import finditer

from benedict.serializers.abstract import AbstractSerializer
from benedict.utils import type_util


class CLISerializer(AbstractSerializer):
    """
    This class describes a CLI serializer.
    """

    regex_keys_with_values = r"-+\w+(?=\s[^\s-])"
    """
    Regex string.
    Used to search for keys (e.g. -STRING or --STRING)
    that *aren't* followed by another key

    Example input: script.py --username example --verbose -d -e email@example.com
    - Matches: --username, -e
    - Doesn't match: script.py, example, --verbose, -d, email@example.com
    """

    regex_all_keys = r"-+\w+"
    """
    Regex string.
    Used to search for keys (e.g. -STRING or --STRING)
    no matter if they are followed by another key

    Example input: script.py --username example --verbose -d -e email@example.com
    - Matches: --username, --verbose, -d, -e
    - Doesn't match: script.py, example, email@example.com
    """

    def __init__(self):
        super().__init__(
            extensions=["cli"],
        )

    @staticmethod
    def parse_keys(regex, string):
        # For some reason findall didn't work
        results = [match.group(0) for match in finditer(regex, string)]
        return results

    """Helper method, returns a list of --keys based on the regex used"""

    @staticmethod
    def _get_parser(options):
        parser = ArgumentParser(**options)
        return parser

    def decode(self, s=None, **kwargs):
        parser = self._get_parser(options=kwargs)

        keys_with_values = set(self.parse_keys(self.regex_keys_with_values, s))
        all_keys = Counter(self.parse_keys(self.regex_all_keys, s))
        for key in all_keys:
            count = all_keys[key]

            try:
                # If the key has a value...
                if key in keys_with_values:
                    # and is defined once, collect the values
                    if count == 1:
                        parser.add_argument(
                            key,
                            nargs="*",
                            # This puts multiple values in a list
                            # even though this won't always be wanted
                            # This is adressed after the dict is generated
                            required=False,
                        )
                    # and is defined multiple times, collect the values
                    else:
                        parser.add_argument(key, action="append", required=False)

                # If the key doesn't have a value...
                else:
                    # and is defined once, store as bool
                    if count <= 1:
                        parser.add_argument(key, action="store_true", required=False)
                    # and is defined multiple times, count how many times
                    else:
                        parser.add_argument(key, action="count", required=False)

            except ArgumentError as error:
                raise ValueError from error

        try:
            args = parser.parse_args(s.split())
        except BaseException as error:
            raise ValueError from error

        dict = vars(args)
        for key in dict:
            value = dict[key]
            # If only one value was written,
            # return that value instead of a list
            if type_util.is_list(value) and len(value) == 1:
                dict[key] = value[0]

        return dict

    def encode(self, d, **kwargs):
        raise NotImplementedError
