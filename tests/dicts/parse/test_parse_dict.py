import unittest
from datetime import datetime
from decimal import Decimal

from benedict.dicts.parse import ParseDict


class parse_dict_test_case(unittest.TestCase):
    """
    This class describes a ParseDict test case.
    """

    def test_get_bool_default(self):
        d = {
            "n": None,
        }
        b = ParseDict(d)
        self.assertTrue(b.get_bool("n", True))
        self.assertFalse(b.get_bool("n", False))
        self.assertTrue(b.get_bool("d1", True))
        self.assertFalse(b.get_bool("d2", False))

    def test_get_bool_with_bool_values(self):
        d = {
            "b1": True,
            "b2": False,
        }
        b = ParseDict(d)
        self.assertTrue(b.get_bool("b1"))
        self.assertFalse(b.get_bool("b2"))

    def test_get_bool_with_int_values(self):
        d = {
            "i0": 0,
            "i1": 1,
            "i2": 2,
        }
        b = ParseDict(d)
        self.assertFalse(b.get_bool("i0"))
        self.assertTrue(b.get_bool("i1"))
        self.assertTrue(b.get_bool("i2", True))
        self.assertFalse(b.get_bool("i2", False))

    def test_get_bool_with_str_values(self):
        d = {
            "t1": "1",
            "t2": "YES",
            "t3": "True",
            "f1": "0",
            "f2": "NO",
            "f3": "False",
        }
        b = ParseDict(d)
        self.assertTrue(b.get_bool("t1"))
        self.assertTrue(b.get_bool("t2"))
        self.assertTrue(b.get_bool("t3"))
        self.assertFalse(b.get_bool("f1"))
        self.assertFalse(b.get_bool("f2"))
        self.assertFalse(b.get_bool("f3"))

    def test_get_bool_list(self):
        d = {
            "a": "1,YES,True,0,NO,False,XXX",
            "b": "1;YES;True;0;NO;False;XXX",
            "c": [
                "1",
                "YES",
                True,
                0,
                "NO",
                "False",
                "XXX",
            ],
        }
        b = ParseDict(d)
        self.assertEqual(
            b.get_bool_list("a"), [True, True, True, False, False, False, None]
        )
        self.assertEqual(b.get_bool_list("b"), [None])
        self.assertEqual(
            b.get_bool_list("b", separator=";"),
            [True, True, True, False, False, False, None],
        )
        self.assertEqual(
            b.get_bool_list("c"), [True, True, True, False, False, False, None]
        )
        self.assertEqual(b.get_bool_list("d", default=[False]), [False])

    def test_get_date_default(self):
        today = datetime.now().date()
        d = {
            "a": None,
        }
        b = ParseDict(d)
        self.assertEqual(b.get_date("a", today), today)
        self.assertEqual(b.get_date("b", today), today)

    def test_get_date_with_date_value(self):
        today = datetime.now().date()
        d = {
            "a": today,
        }
        b = ParseDict(d)
        self.assertEqual(b.get_date("a"), today)

    def test_get_date_list(self):
        d = {
            "a": ["2019-05-01", "2018-12-31", "Hello World"],
            "b": "2019-05-01,2018-12-31",
        }
        b = ParseDict(d)
        self.assertEqual(
            b.get_date_list("a"),
            [datetime(2019, 5, 1).date(), datetime(2018, 12, 31).date(), None],
        )
        self.assertEqual(
            b.get_date_list("b"),
            [datetime(2019, 5, 1).date(), datetime(2018, 12, 31).date()],
        )

    def test_get_datetime_default(self):
        now = datetime.now()
        d = {
            "a": None,
        }
        b = ParseDict(d)
        self.assertEqual(b.get_datetime("a", now), now)
        self.assertEqual(b.get_datetime("b", now), now)

    def test_get_datetime_with_datetime_value(self):
        now = datetime.now()
        d = {
            "a": now,
        }
        b = ParseDict(d)
        self.assertEqual(b.get_datetime("a"), now)

    def test_get_datetime_with_timestamp_int(self):
        now = datetime.now()
        ts = datetime.timestamp(now)
        d = {
            "a": ts,
        }
        b = ParseDict(d)
        self.assertEqual(b.get_datetime("a"), datetime.fromtimestamp(ts))

    def test_get_datetime_with_timestamp_string(self):
        now = datetime.now()
        ts = datetime.timestamp(now)
        d = {
            "a": str(ts),
        }
        b = ParseDict(d)
        self.assertEqual(b.get_datetime("a"), datetime.fromtimestamp(ts))

    def test_get_datetime_with_valid_format(self):
        d = {
            "a": "2019-05-01",
        }
        b = ParseDict(d)
        r = datetime(2019, 5, 1, 0, 0)
        self.assertEqual(b.get_datetime("a", format="%Y-%m-%d"), r)

    def test_get_datetime_with_invalid_format(self):
        now = datetime.now()
        d = {
            "a": "2019-05-01",
        }
        b = ParseDict(d)
        self.assertEqual(b.get_datetime("a", format="%Y/%m/%d"), None)
        self.assertEqual(
            b.get_datetime(
                "a",
                now,
                format="%Y/%m/%d",
            ),
            now,
        )

    def test_get_datetime_without_format(self):
        d = {
            "a": "2019-05-01",
        }
        b = ParseDict(d)
        r = datetime(2019, 5, 1, 0, 0)
        self.assertEqual(b.get_datetime("a"), r)

    def test_get_datetime_list(self):
        d = {
            "a": ["2019-05-01", "2018-12-31", "Hello World"],
            "b": "2019-05-01,2018-12-31",
        }
        b = ParseDict(d)
        self.assertEqual(
            b.get_datetime_list("a"),
            [datetime(2019, 5, 1, 0, 0), datetime(2018, 12, 31, 0, 0), None],
        )
        self.assertEqual(
            b.get_datetime_list("b"),
            [datetime(2019, 5, 1, 0, 0), datetime(2018, 12, 31, 0, 0)],
        )

    def test_get_decimal(self):
        d = {
            "a": 1,
            "b": True,
            "c": Decimal("4.25"),
        }
        b = ParseDict(d)
        self.assertEqual(b.get_decimal("a"), Decimal("1.0"))
        self.assertEqual(b.get_decimal("b"), Decimal("0.0"))
        self.assertEqual(b.get_decimal("b", Decimal("2.5")), Decimal("2.5"))
        self.assertEqual(b.get_decimal("c"), Decimal("4.25"))

    def test_get_decimal_with_choices(self):
        d = {
            "a": Decimal("0.25"),
            "b": Decimal("0.35"),
        }
        b = ParseDict(d)
        o = [
            Decimal("0.0"),
            Decimal("0.25"),
            Decimal("0.5"),
            Decimal("0.75"),
            Decimal("1.0"),
        ]
        self.assertEqual(b.get_decimal("a", Decimal("0.5"), choices=o), Decimal("0.25"))
        self.assertEqual(b.get_decimal("b", Decimal("0.5"), choices=o), Decimal("0.5"))

    def test_get_decimal_list(self):
        d = {
            "a": ["0.0", "0.5", "1.0", "Hello World"],
            "b": "0.0,0.5,1.0",
        }
        b = ParseDict(d)
        self.assertEqual(
            b.get_decimal_list("a"),
            [Decimal("0.0"), Decimal("0.5"), Decimal("1.0"), None],
        )
        self.assertEqual(
            b.get_decimal_list("b"), [Decimal("0.0"), Decimal("0.5"), Decimal("1.0")]
        )

    def test_get_dict(self):
        d = {
            "a": {"x": 1, "y": 2},
            "b": {},
        }
        b = ParseDict(d)
        self.assertEqual(b.get_dict("a"), {"x": 1, "y": 2})
        self.assertEqual(b.get_dict("b"), {})
        self.assertEqual(b.get_dict("b", {"default": True}), {})
        self.assertEqual(b.get_dict("c"), {})
        self.assertEqual(b.get_dict("c", {"default": True}), {"default": True})

    def test_get_dict_from_json(self):
        d = {
            "a": '{"numbers": ["0", "1", "2", "3", "4"], "letters": ["a", "b", "c", "d", "e"]}',
            "b": '["0", "1", "2", "3", "4"]',
            "c": "{}",
            "d": "[]",
            "e": "",
            "f": '{"invalid::json"}',
        }
        b = ParseDict(d)
        self.assertEqual(
            b.get_dict("a"),
            {
                "numbers": ["0", "1", "2", "3", "4"],
                "letters": ["a", "b", "c", "d", "e"],
            },
        )
        self.assertEqual(b.get_dict("b"), {})
        self.assertEqual(b.get_dict("c"), {})
        self.assertEqual(b.get_dict("c", {"default": True}), {})
        self.assertEqual(b.get_dict("d", {"default": True}), {"default": True})
        self.assertEqual(b.get_dict("e"), {})
        self.assertEqual(b.get_dict("f"), {})
        self.assertEqual(b.get_dict("g", {"default": True}), {"default": True})

    def test_get_float(self):
        d = {
            "a": 1.0,
            "b": True,
            "c": float(4.25),
        }
        b = ParseDict(d)
        self.assertEqual(b.get_float("a"), float(1.0))
        self.assertEqual(b.get_float("b"), float(0.0))
        self.assertEqual(b.get_float("b", float(2.5)), float(2.5))
        self.assertEqual(b.get_float("c"), float(4.25))

    def test_get_float_with_choices(self):
        d = {
            "a": float(0.25),
            "b": float(0.35),
        }
        b = ParseDict(d)
        o = [float(0.0), float(0.25), float(0.5), float(0.75), float(1.0)]
        self.assertEqual(b.get_float("a", float(0.5), choices=o), float(0.25))
        self.assertEqual(b.get_float("b", float(0.5), choices=o), float(0.5))

    def test_get_float_list(self):
        d = {
            "a": ["0.0", "0.5", "1.0", "Hello World"],
            "b": "0.0,0.5,1.0",
        }
        b = ParseDict(d)
        self.assertEqual(b.get_float_list("a"), [0.0, 0.5, 1.0, None])
        self.assertEqual(b.get_float_list("b"), [0.0, 0.5, 1.0])

    def test_get_email(self):
        d = {
            "a": "fabio@caccamo.com",
            "b": "fabio@@caccamo.com",
            "c": "fabio.caccamo@mailinator.com",
            "d": "",
        }
        b = ParseDict(d)
        # valid
        self.assertEqual(b.get_email("a"), d.get("a"))
        # valid (don't check blacklist)
        self.assertEqual(b.get_email("a", check_blacklist=False), d.get("a"))
        # invalid
        self.assertEqual(b.get_email("b"), "")
        # invalid (don't check blacklist)
        self.assertEqual(b.get_email("b", check_blacklist=False), "")
        # valid but disposable
        self.assertEqual(b.get_email("c"), "")
        # valid but disposable (don't check blacklist)
        self.assertEqual(b.get_email("c", check_blacklist=False), d.get("c"))
        # invalid email (empty)
        self.assertEqual(b.get_email("d"), "")
        # invalid key
        self.assertEqual(b.get_email("e"), "")

    def test_get_int(self):
        d = {
            "a": 1,
            "b": None,
            "c": int(4),
            "d": True,
            "e": False,
            "f": "3",
            "g": "3.5",
        }
        b = ParseDict(d)
        self.assertEqual(b.get_int("a"), 1)
        self.assertEqual(b.get_int("b"), 0)
        self.assertEqual(b.get_int("b", 2), 2)
        self.assertEqual(b.get_int("c"), 4)
        self.assertEqual(b.get_int("d", 2), 1)
        self.assertEqual(b.get_int("e", 2), 0)
        self.assertEqual(b.get_int("f", 2), 3)
        self.assertEqual(b.get_int("g", 2), 2)

    def test_get_int_with_choices(self):
        d = {
            "a": 25,
            "b": 35,
        }
        b = ParseDict(d)
        o = [0, 25, 50, 75, 100]
        self.assertEqual(b.get_int("a", 50, choices=o), 25)
        self.assertEqual(b.get_int("b", 50, choices=o), 50)

    def test_get_int_list(self):
        d = {
            "a": ["0", "1", "2", "Hello World"],
            "b": "0,1,2",
            "c": "0",
            "d": "1",
            "e": "",
            "f": None,
        }
        b = ParseDict(d)
        self.assertEqual(b.get_int_list("a"), [0, 1, 2, None])
        self.assertEqual(b.get_int_list("b"), [0, 1, 2])
        self.assertEqual(b.get_int_list("c"), [0])
        self.assertEqual(b.get_int_list("d"), [1])
        self.assertEqual(b.get_int_list("e"), [])
        self.assertEqual(b.get_int_list("f"), [])

    def test_get_list(self):
        d = {
            "a": (0, 1, 2, 3),
            "b": [0, 1, 2, 3],
            "c": [],
            "d": "{}",
            "e": "[]",
            "f": "",
        }
        b = ParseDict(d)
        self.assertEqual(b.get_list("a"), [0, 1, 2, 3])
        self.assertEqual(b.get_list("b"), [0, 1, 2, 3])
        self.assertEqual(b.get_list("c"), [])
        self.assertEqual(b.get_list("c", [0]), [])
        self.assertEqual(b.get_list("d"), [])
        self.assertEqual(b.get_list("e"), [])
        self.assertEqual(b.get_list("f"), [])
        self.assertEqual(b.get_list("g", [0]), [0])

    def test_get_list_from_json(self):
        d = {
            "a": '{"numbers": ["0", "1", "2", "3", "4"], "letters": ["a", "b", "c", "d", "e"]}',
            "b": '["0", "1", "2", "3", "4"]',
            "c": "[]",
        }
        b = ParseDict(d)
        self.assertEqual(b.get_list("a"), [])
        self.assertEqual(b.get_list("b"), ["0", "1", "2", "3", "4"])
        self.assertEqual(b.get_list("c"), [])
        self.assertEqual(b.get_list("c", [0]), [])
        self.assertEqual(b.get_list("d", [0]), [0])

    def test_get_list_with_separator(self):
        d = {
            "a": "0,1,2,3,4",
            "b": "5|6|7|8|9",
            "c": "",
        }
        b = ParseDict(d)
        self.assertEqual(b.get_list("a", separator=","), ["0", "1", "2", "3", "4"])
        self.assertEqual(b.get_list("b", separator="|"), ["5", "6", "7", "8", "9"])
        self.assertEqual(b.get_list("b"), ["5|6|7|8|9"])
        self.assertEqual(b.get_list("c", separator=","), [])
        self.assertEqual(b.get_list("d", separator=","), [])
        self.assertEqual(b.get_list("e", [0], separator=","), [0])

    def test_get_list_item(self):
        d = {
            "a": (1, 2, 3, 4, 5),
            "b": [6, 7, 8, 9, 0],
            "c": {},
        }
        b = ParseDict(d)
        self.assertEqual(b.get_list_item("a"), 1)
        self.assertEqual(b.get_list_item("a", index=1), 2)
        self.assertEqual(b.get_list_item("a", index=-1), 5)
        self.assertEqual(b.get_list_item("a", index=10), None)
        self.assertEqual(b.get_list_item("b"), 6)
        self.assertEqual(b.get_list_item("b", index=1), 7)
        self.assertEqual(b.get_list_item("b", index=-1), 0)
        self.assertEqual(b.get_list_item("b", index=10), None)
        self.assertEqual(b.get_list_item("c", index=1), None)

    def test_get_phonenumber(self):
        d = {
            "b": " (0039) 3334445566 ",  # valid phone number with 00 prefix
            "c": "+393334445566  ",  # valid phone number with + prefix
            "d": "+39333444556677889900",  # invalid phone number
            "e": "3334445566",  # valid phone number without prefix
            "y": "",
        }
        r = {
            "e164": "+393334445566",
            "international": "+39 333 444 5566",
            "national": "333 444 5566",
        }
        b = ParseDict(d)

        # valid phone number with 00 prefix
        p = b.get_phonenumber("b")
        self.assertEqual(p, r)

        # valid phone number with + prefix
        p = b.get_phonenumber("c")
        self.assertEqual(p, r)

        # invalid phone number
        p = b.get_phonenumber("d")
        self.assertEqual(p, {})

        # valid phone number without prefix, without country code
        p = b.get_phonenumber("e")
        self.assertEqual(p, {})

        # valid phone number without prefix, with lowercase alpha_2 country code
        p = b.get_phonenumber("e", country_code="it")
        self.assertEqual(p, r)

        # valid phone number without prefix, with uppercase alpha_2 uppercase
        p = b.get_phonenumber("e", country_code="IT")
        self.assertEqual(p, r)

        # valid phone number without prefix, with lowercase alpha_3 country code
        p = b.get_phonenumber("e", country_code="ita")
        self.assertEqual(p, r)

        # valid phone number without prefix, with uppercase alpha_3 uppercase
        p = b.get_phonenumber("e", country_code="ITA")
        self.assertEqual(p, r)

        # valid phone number without prefix, with wrong country code
        p = b.get_phonenumber("e", country_code="fr")
        self.assertEqual(p, {})

        # invalid phone number (empty)
        p = b.get_phonenumber("y")
        self.assertEqual(p, {})

        # invalid phone number dict key
        p = b.get_phonenumber("z")
        self.assertEqual(p, {})

    def test_get_slug(self):
        d = {
            "a": " Hello World ",
            "b": 1,
        }
        b = ParseDict(d)
        self.assertEqual(b.get_slug("a"), "hello-world")
        self.assertEqual(b.get_slug("b", "none"), "1")
        self.assertEqual(b.get_slug("c", "none"), "none")

    def test_get_slug_with_choices(self):
        d = {
            "a": "Sunday",
            "b": "Noneday",
        }
        b = ParseDict(d)
        self.assertEqual(b.get_slug("a", choices=["sunday", "saturday"]), "sunday")
        self.assertEqual(
            b.get_slug("b", choices=["sunday", "saturday"], default="saturday"),
            "saturday",
        )
        self.assertEqual(
            b.get_slug("c", choices=["sunday", "saturday"], default="saturday"),
            "saturday",
        )

    def test_get_slug_list(self):
        d = {
            "a": ["Hello World", " See you later ", 99.9],
            "b": "Hello World, See you later, 99.9",
        }
        b = ParseDict(d)
        self.assertEqual(b.get_slug_list("a"), ["hello-world", "see-you-later", "99-9"])
        self.assertEqual(b.get_slug_list("b"), ["hello-world", "see-you-later", "99-9"])

    def test_get_str(self):
        d = {
            "a": "Hello World",
            "b": "Hello  World",
            "c": 1,
        }
        b = ParseDict(d)
        self.assertEqual(b.get_str("a"), "Hello World")
        self.assertEqual(b.get_str("b"), "Hello World")
        self.assertEqual(b.get_str("c"), "1")

    def test_get_str_fix_encoding(self):
        d = {
            "a": "Sexâ\x80\x99n Drug",
            "b": "Localit\xe0",
        }
        b = ParseDict(d)
        self.assertEqual(b.get_str("a"), "Sex'n Drug")
        self.assertEqual(b.get_str("b"), "Località")

    def test_get_str_list(self):
        d = {
            "a": ["Hello World", "See you later", 99.9],
            "b": "Hello World,See you later,99.9",
        }
        b = ParseDict(d)
        self.assertEqual(b.get_str_list("a"), ["Hello World", "See you later", "99.9"])
        self.assertEqual(b.get_str_list("b"), ["Hello World", "See you later", "99.9"])

    def test_get_str_with_choices(self):
        d = {
            "a": "Sunday",
            "b": "Noneday",
        }
        b = ParseDict(d)
        self.assertEqual(b.get_str("a", choices=["Sunday", "Saturday"]), "Sunday")
        self.assertEqual(
            b.get_str("b", choices=["Sunday", "Saturday"], default="Saturday"),
            "Saturday",
        )
        self.assertEqual(
            b.get_str("c", choices=["Sunday", "Saturday"], default="Saturday"),
            "Saturday",
        )

    def test_get_uuid(self):
        d = {
            "a": "CA761232-ED42-11CE-BACD-00AA0057B223",
            "b": " CA761232-ED42-11CE-BACD-00AA0057B223 ",
            "c": " CA761232ED4211CEBACD00AA0057B223 ",
            "d": " ca761232ed4211cebacd00aa0057b223 ",
            "e": "CA761232ED4211CEBACD00AA0057B223",
            "f": "CA761232ED4211CEBACD00AA0057B2233",  # invalid too long
            "g": "CA761232ED4211CEBACD00AA0057B22x",  # invalid chars
            "h": "CA761232ED4211CEBACD00AA0057B22",  # invalid too short
            "i": "CA761232-ED42-11CE-BACD-00AA0057B2234",  # invalid too long
        }
        b = ParseDict(d)
        self.assertEqual(b.get_uuid("a"), "CA761232-ED42-11CE-BACD-00AA0057B223")
        self.assertEqual(b.get_uuid("b"), "CA761232-ED42-11CE-BACD-00AA0057B223")
        self.assertEqual(b.get_uuid("c"), "CA761232ED4211CEBACD00AA0057B223")
        self.assertEqual(b.get_uuid("d"), "ca761232ed4211cebacd00aa0057b223")
        self.assertEqual(b.get_uuid("e"), "CA761232ED4211CEBACD00AA0057B223")
        self.assertEqual(b.get_uuid("f"), "")
        self.assertEqual(b.get_uuid("f", "none"), "none")
        self.assertEqual(b.get_uuid("g"), "")
        self.assertEqual(b.get_uuid("h"), "")
        self.assertEqual(b.get_uuid("i"), "")

    def test_get_uuid_list(self):
        d = {
            "a": [
                "CA761232-ED42-11CE-BACD-00AA0057B223",
                " FB761232-ED42-314E-BFCA-00AA0057B118 ",
                99.9,
            ],
            "b": "Hello World, See you later, 99.9",
        }
        b = ParseDict(d)
        self.assertEqual(
            b.get_uuid_list("a"),
            [
                "CA761232-ED42-11CE-BACD-00AA0057B223",
                "FB761232-ED42-314E-BFCA-00AA0057B118",
                None,
            ],
        )
        self.assertEqual(b.get_uuid_list("b"), [None, None, None])
