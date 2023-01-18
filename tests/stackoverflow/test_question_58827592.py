import unittest


class stackoverflow_question_58827592_test_case(unittest.TestCase):
    def test_stackoverflow_question_58827592(self):
        """
        https://stackoverflow.com/questions/58827592/is-there-a-way-to-convert-csv-columns-into-hierarchical-relationships
        """
        from benedict import benedict as bdict

        data_source = """
RecordID,kingdom,phylum,class,order,family,genus,species
1,Animalia,Chordata,Mammalia,Primates,Hominidae,Homo,Homo sapiens
2,Animalia,Chordata,Mammalia,Carnivora,Canidae,Canis,Canis
3,Plantae,nan,Magnoliopsida,Brassicales,Brassicaceae,Arabidopsis,Arabidopsis thaliana
4,Plantae,nan,Magnoliopsida,Fabales,Fabaceae,Phaseoulus,Phaseolus vulgaris
"""
        data_input = bdict.from_csv(data_source)
        data_output = bdict()

        ancestors_hierarchy = [
            "kingdom",
            "phylum",
            "class",
            "order",
            "family",
            "genus",
            "species",
        ]
        for value in data_input["values"]:
            data_output[
                ".".join([value[ancestor] for ancestor in ancestors_hierarchy])
            ] = bdict()

        # print(data_output.dump())
        keypaths = sorted(
            data_output.keypaths(), key=lambda item: len(item.split(".")), reverse=True
        )

        data_output["children"] = []

        def transform_data(d, key, value):
            if isinstance(value, dict):
                value.update({"name": key, "children": []})

        data_output.traverse(transform_data)

        for keypath in keypaths:
            target_keypath = ".".join(keypath.split(".")[:-1] + ["children"])
            data_output[target_keypath].append(data_output.pop(keypath))

        # print(data_output.dump())
