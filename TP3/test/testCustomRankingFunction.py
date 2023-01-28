from unittest import TestCase
from query.customLinearFunction import customLinearFunction


class TestCustomRankingFunction(TestCase):


    def testLinearRankingFunction_basics(self):
        rf=customLinearFunction("test/testIndex_basics_index.json")
        tokenized_request=["patricia","wikipédia"]

        score_doc0=rf.calculate_score(
                {"id":0,"title":"karine wikipédia","url":"https://ensai.fr"},
                tokenized_request
        )
        score_doc1=rf.calculate_score(
                {"id":1,"title":"patricia wikipédia","url":"https://ensai.fr"},
                tokenized_request
        )
        score_doc2=rf.calculate_score(
                {"id":2,"title":"wikipédia patricia ","url":"https://ensai.fr"},
                tokenized_request
        )
        score_doc3=rf.calculate_score(
                {"id":3,"title":"wikipédia patricia token","url":"https://ensai.fr"},
                tokenized_request
        )
        
        expected_score_0=0 
        expected_score_1=2*0.8 +2*0.8
        print(score_doc1,score_doc2)
        self.assertEqual(expected_score_0,score_doc0)
        self.assertEqual(expected_score_1,score_doc1)
        self.assertGreater(score_doc1,score_doc0)
        self.assertGreater(score_doc1,score_doc2)
        self.assertEqual(score_doc2,score_doc3)


    def testLinearRankingFunction_multiple_position(self):
        """
        Test dealing with multiple token position in the same document or in the request 
        """
        print("test multiple")
        rf=customLinearFunction("test/testIndex_multiple_position_index.json")
        tokenized_request=["wikipédia","patricia","avec","wikipédia"]

        score_doc0=rf.calculate_score(
                {"id":0,"title":" wikipédia patricia","url":"https://ensai.fr"},
                tokenized_request
        )
        score_doc1=rf.calculate_score(
                {"id":1,"title":" wikipédia patricia wikipédia","url":"https://ensai.fr"},
                tokenized_request
        )
        score_doc2=rf.calculate_score(
                {"id":2,"title":" wikipédia cherche patricia ","url":"https://ensai.fr"},
                tokenized_request
        )
        score_doc3=rf.calculate_score(
                {"id":3,"title":" wikipédia wikipédia patricia ","url":"https://ensai.fr"},
                tokenized_request
        )
        print(score_doc0)
        self.assertGreater(score_doc1,score_doc0)
        self.assertEqual(score_doc0,score_doc3)
        self.assertEqual(score_doc2,score_doc3)




