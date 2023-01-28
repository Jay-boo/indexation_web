from unittest import TestCase

from indexWeb.index import Index



flatten_token=[
        ["Paul","mange","une","pomme","dans","le","jardin"],
        ["Jean","mange","une","poire","dans","la","cuisine"]
]
flatten_token_bis=[
        ["Paul","mange","la","pomme","dans","la","chambre"],
        ["Jean","mange","la","poire","dans","la","cuisine"]
        ]


test_flatten_token_stem=[]

class testBuildIndex(TestCase):

    def testBasicIndex(self):
        index=Index()
        index.flatten_doc_tokens=flatten_token
        index.build_indexes()
        expected_index={
                        "Paul":{"0":1},
                        "mange":{"0":1,
                                 "1":1},
                        "une":{"0":1,"1":1},
                        "pomme":{"0":1},
                        "dans":{"0":1,"1":1},
                        "le":{"0":1},
                        "jardin":{"0":1},
                        "Jean":{"1":1},
                        "poire":{"1":1},
                        "la":{"1":1},
                        "cuisine":{"1":1}

        }
        
        self.assertEqual(len(index.index.keys()),len(expected_index.keys()))
        for key, value in index.index.items():
            self.assertEqual(value,expected_index[key])

        index=Index()
        index.flatten_doc_tokens=flatten_token_bis
        index.build_indexes()
        expected_index={
                        "Paul":{"0":1},
                        "mange":{"0":1,
                                 "1":1},
                        "pomme":{"0":1},
                        "dans":{"0":1,"1":1},
                        "chambre":{"0":1},
                        "Jean":{"1":1},
                        "poire":{"1":1},
                        "la":{"0":2,"1":2},
                        "cuisine":{"1":1}

        }
        
        self.assertEqual(len(index.index.keys()),len(expected_index.keys()))
        for key, value in index.index.items():
            self.assertEqual(value,expected_index[key])






    def testPositionalIndex(self):
        """
        Test positional index
        """
        index=Index()
        index.flatten_doc_tokens=flatten_token_bis
        index.build_indexes()
        expected_index={
                "Paul":{
                    "0":[0]
                    },
                "mange":{
                    "0":[1],
                    "1":[1]
                    },
                "la":{
                    "0":[2,5],
                    "1":[2,5]
                    },
                "pomme":{
                    "0":[3]
                    },
                "dans":{
                    "0":[4],
                    "1":[4]
                    },
                "chambre":{
                    "0":[6]
                    },
                "Jean":{
                    "1":[0]
                    },
                "poire":{
                    "1":[3]
                    },
                "cuisine":{
                    "1":[6]
                    }
        }
        self.assertEqual(len(index.positional_index.keys()),len(expected_index.keys()))
        for key, value in index.positional_index.items():
            self.assertEqual(value,expected_index[key])





