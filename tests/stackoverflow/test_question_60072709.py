import unittest


class stackoverflow_question_60072709_test_case(unittest.TestCase):
    def test_stackoverflow_question_60072709(self):
        """
        https://stackoverflow.com/questions/60072709/i-want-to-convert-sample-json-data-into-nested-json-using-specific-key-value-in
        """
        from benedict import benedict as bdict

        json_input = """
        {
            "1": {
                "amount": 0,
                "breakdown": [
                    {
                        "amount": 169857,
                        "id": 4,
                        "name": "Website Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 8709,
                        "id": 5,
                        "name": "Mobile App Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 80862,
                        "id": 6,
                        "name": "DevOps",
                        "parent_id": "1"
                    },
                    {
                        "amount": 51479,
                        "id": 7,
                        "name": "Wireframing",
                        "parent_id": "2"
                    },
                    {
                        "amount": 37204,
                        "id": 8,
                        "name": "UI Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 13141,
                        "id": 9,
                        "name": "Brochure Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 39591,
                        "id": 10,
                        "name": "Social Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 41385,
                        "id": 11,
                        "name": "Print Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 92801,
                        "id": 12,
                        "name": "Payment Gateway License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 77056,
                        "id": 13,
                        "name": "JavaScript Plugin License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 3412,
                        "id": 14,
                        "name": "Google Play Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 5297,
                        "id": 15,
                        "name": "Apple App Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 75020,
                        "id": 16,
                        "name": "Servers",
                        "parent_id": "6"
                    },
                    {
                        "amount": 1217,
                        "id": 17,
                        "name": "Domain Name",
                        "parent_id": "6"
                    },
                    {
                        "amount": 4625,
                        "id": 18,
                        "name": "SSL Certificate",
                        "parent_id": "6"
                    }
                ],
                "id": 1,
                "name": "Project 1"
            },
            "2": {
                "amount": 0,
                "breakdown": [
                    {
                        "amount": 205822,
                        "id": 4,
                        "name": "Website Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 12132,
                        "id": 5,
                        "name": "Mobile App Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 56235,
                        "id": 6,
                        "name": "DevOps",
                        "parent_id": "1"
                    },
                    {
                        "amount": 72901,
                        "id": 7,
                        "name": "Wireframing",
                        "parent_id": "2"
                    },
                    {
                        "amount": 33750,
                        "id": 8,
                        "name": "UI Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 10547,
                        "id": 9,
                        "name": "Brochure Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 53946,
                        "id": 10,
                        "name": "Social Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 38910,
                        "id": 11,
                        "name": "Print Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 131750,
                        "id": 12,
                        "name": "Payment Gateway License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 74072,
                        "id": 13,
                        "name": "JavaScript Plugin License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 2585,
                        "id": 14,
                        "name": "Google Play Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 9547,
                        "id": 15,
                        "name": "Apple App Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 50087,
                        "id": 16,
                        "name": "Servers",
                        "parent_id": "6"
                    },
                    {
                        "amount": 1463,
                        "id": 17,
                        "name": "Domain Name",
                        "parent_id": "6"
                    },
                    {
                        "amount": 4685,
                        "id": 18,
                        "name": "SSL Certificate",
                        "parent_id": "6"
                    }
                ],
                "id": 2,
                "name": "Project 2"
            },
            "3": {
                "amount": 0,
                "breakdown": [
                    {
                        "amount": 253894,
                        "id": 4,
                        "name": "Website Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 11924,
                        "id": 5,
                        "name": "Mobile App Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 54651,
                        "id": 6,
                        "name": "DevOps",
                        "parent_id": "1"
                    },
                    {
                        "amount": 82045,
                        "id": 7,
                        "name": "Wireframing",
                        "parent_id": "2"
                    },
                    {
                        "amount": 46000,
                        "id": 8,
                        "name": "UI Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 9835,
                        "id": 9,
                        "name": "Brochure Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 45660,
                        "id": 10,
                        "name": "Social Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 25984,
                        "id": 11,
                        "name": "Print Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 162184,
                        "id": 12,
                        "name": "Payment Gateway License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 91710,
                        "id": 13,
                        "name": "JavaScript Plugin License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 2596,
                        "id": 14,
                        "name": "Google Play Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 9328,
                        "id": 15,
                        "name": "Apple App Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 48171,
                        "id": 16,
                        "name": "Servers",
                        "parent_id": "6"
                    },
                    {
                        "amount": 1550,
                        "id": 17,
                        "name": "Domain Name",
                        "parent_id": "6"
                    },
                    {
                        "amount": 4930,
                        "id": 18,
                        "name": "SSL Certificate",
                        "parent_id": "6"
                    }
                ],
                "id": 3,
                "name": "Project 3"
            },
            "4": {
                "amount": 0,
                "breakdown": [
                    {
                        "amount": 215166,
                        "id": 4,
                        "name": "Website Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 11030,
                        "id": 5,
                        "name": "Mobile App Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 60883,
                        "id": 6,
                        "name": "DevOps",
                        "parent_id": "1"
                    },
                    {
                        "amount": 82842,
                        "id": 7,
                        "name": "Wireframing",
                        "parent_id": "2"
                    },
                    {
                        "amount": 26713,
                        "id": 8,
                        "name": "UI Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 13305,
                        "id": 9,
                        "name": "Brochure Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 47650,
                        "id": 10,
                        "name": "Social Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 41266,
                        "id": 11,
                        "name": "Print Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 130015,
                        "id": 12,
                        "name": "Payment Gateway License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 85151,
                        "id": 13,
                        "name": "JavaScript Plugin License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 2341,
                        "id": 14,
                        "name": "Google Play Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 8689,
                        "id": 15,
                        "name": "Apple App Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 55320,
                        "id": 16,
                        "name": "Servers",
                        "parent_id": "6"
                    },
                    {
                        "amount": 1399,
                        "id": 17,
                        "name": "Domain Name",
                        "parent_id": "6"
                    },
                    {
                        "amount": 4164,
                        "id": 18,
                        "name": "SSL Certificate",
                        "parent_id": "6"
                    }
                ],
                "id": 4,
                "name": "Project 4"
            },
            "5": {
                "amount": 0,
                "breakdown": [
                    {
                        "amount": 257678,
                        "id": 4,
                        "name": "Website Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 11908,
                        "id": 5,
                        "name": "Mobile App Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 69707,
                        "id": 6,
                        "name": "DevOps",
                        "parent_id": "1"
                    },
                    {
                        "amount": 80342,
                        "id": 7,
                        "name": "Wireframing",
                        "parent_id": "2"
                    },
                    {
                        "amount": 25483,
                        "id": 8,
                        "name": "UI Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 12735,
                        "id": 9,
                        "name": "Brochure Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 47972,
                        "id": 10,
                        "name": "Social Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 39871,
                        "id": 11,
                        "name": "Print Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 133534,
                        "id": 12,
                        "name": "Payment Gateway License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 124144,
                        "id": 13,
                        "name": "JavaScript Plugin License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 2083,
                        "id": 14,
                        "name": "Google Play Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 9825,
                        "id": 15,
                        "name": "Apple App Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 63413,
                        "id": 16,
                        "name": "Servers",
                        "parent_id": "6"
                    },
                    {
                        "amount": 1437,
                        "id": 17,
                        "name": "Domain Name",
                        "parent_id": "6"
                    },
                    {
                        "amount": 4857,
                        "id": 18,
                        "name": "SSL Certificate",
                        "parent_id": "6"
                    }
                ],
                "id": 5,
                "name": "Project 5"
            },
            "6": {
                "amount": 0,
                "breakdown": [
                    {
                        "amount": 202257,
                        "id": 4,
                        "name": "Website Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 11990,
                        "id": 5,
                        "name": "Mobile App Development",
                        "parent_id": "1"
                    },
                    {
                        "amount": 67792,
                        "id": 6,
                        "name": "DevOps",
                        "parent_id": "1"
                    },
                    {
                        "amount": 78702,
                        "id": 7,
                        "name": "Wireframing",
                        "parent_id": "2"
                    },
                    {
                        "amount": 32707,
                        "id": 8,
                        "name": "UI Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 10431,
                        "id": 9,
                        "name": "Brochure Design",
                        "parent_id": "2"
                    },
                    {
                        "amount": 28636,
                        "id": 10,
                        "name": "Social Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 43055,
                        "id": 11,
                        "name": "Print Media Marketing",
                        "parent_id": "3"
                    },
                    {
                        "amount": 101200,
                        "id": 12,
                        "name": "Payment Gateway License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 101057,
                        "id": 13,
                        "name": "JavaScript Plugin License",
                        "parent_id": "4"
                    },
                    {
                        "amount": 3081,
                        "id": 14,
                        "name": "Google Play Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 8909,
                        "id": 15,
                        "name": "Apple App Store Fees",
                        "parent_id": "5"
                    },
                    {
                        "amount": 60790,
                        "id": 16,
                        "name": "Servers",
                        "parent_id": "6"
                    },
                    {
                        "amount": 1612,
                        "id": 17,
                        "name": "Domain Name",
                        "parent_id": "6"
                    },
                    {
                        "amount": 5390,
                        "id": 18,
                        "name": "SSL Certificate",
                        "parent_id": "6"
                    }
                ],
                "id": 6,
                "name": "Project 6"
            }
        }
        """

        json_output = """
        [
          {

                "id": 1,
                "name": "Project 1",
                "amount": 442228,
                "breakdown": [
                  {
                    "id": 1,
                    "name": "Development",
                    "amount": 259428,
                    "breakdown": [
                      {
                        "id": 4,
                        "name": "Website Development",
                        "amount": 169857,
                        "breakdown": [
                          {
                            "id": 12,
                            "name": "Payment Gateway License",
                            "amount": 92801,
                            "breakdown": []
                          },
                          {
                            "id": 13,
                            "name": "JavaScript Plugin License",
                            "amount": 77056,
                            "breakdown": []
                          }
                        ]
                      },
                      {
                        "id": 5,
                        "name": "Mobile App Development",
                        "amount": 8709,
                        "breakdown": [
                          {
                            "id": 14,
                            "name": "Google Play Store Fees",
                            "amount": 3412,
                            "breakdown": []
                          },
                          {
                            "id": 15,
                            "name": "Apple App Store Fees",
                            "amount": 5297,
                            "breakdown": []
                          }
                        ]
                      },
                      {
                        "id": 6,
                        "name": "DevOps",
                        "amount": 80862,
                        "breakdown": [
                          {
                            "id": 16,
                            "name": "Servers",
                            "amount": 75020,
                            "breakdown": []
                          },
                          {
                            "id": 17,
                            "name": "Domain Name",
                            "amount": 1217,
                            "breakdown": []
                          },
                          {
                            "id": 18,
                            "name": "SSL Certificate",
                            "amount": 4625,
                            "breakdown": []
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "id": 2,
                    "name": "Designing",
                    "amount": 101824,
                    "breakdown": [
                      {
                        "id": 7,
                        "name": "Wireframing",
                        "amount": 51479,
                        "breakdown": []
                      },
                      {
                        "id": 8,
                        "name": "UI Design",
                        "amount": 37204,
                        "breakdown": []
                      },
                      {
                        "id": 9,
                        "name": "Brochure Design",
                        "amount": 13141,
                        "breakdown": []
                      }
                    ]
                  },
                  {
                    "id": 3,
                    "name": "Marketing",
                    "amount": 80976,
                    "breakdown": [
                      {
                        "id": 10,
                        "name": "Social Media Marketing",
                        "amount": 39591,
                        "breakdown": []
                      },
                      {
                        "id": 11,
                        "name": "Print Media Marketing",
                        "amount": 41385,
                        "breakdown": []
                      }
                    ]
                  }

            ]
          }
        ]
        """

        data = bdict.from_json(json_input)
        keys = list(data.keys())
        items = []
        for key in keys:
            item = bdict(data.get(key))
            # move all items to the top level
            items += list(item["breakdown"])
            item["breakdown"] = []
            items.append(item)
            break

        # convert all parent_id values to int to allow comparison
        for item in items:
            if "parent_id" in item:
                item["parent_id"] = int(item["parent_id"])

        items_dict = bdict({"items": items})
        items_dict["items_nested"] = items_dict.nest(
            "items", id_key="id", parent_id_key="parent_id", children_key="breakdown"
        )
        # print(items_dict.dump())
