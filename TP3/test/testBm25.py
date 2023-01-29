from math import log
from unittest import TestCase
import numpy as np

from query.bm25 import bm25

class TestBm25(TestCase):


    def test_get_query_tokens_freq(self):
        rf=bm25("test/testIndex_basics_index.json")
        tokenized_request=["patricia","wikipédia","token"]
        for id  in range(0,4):
            freqs=rf.get_query_tokens_freq(
                    {"id":id}
                    ,tokenized_request)
            if id==0:
                self.assertEqual(freqs,
                                 [0,0.5,0])
            elif id==1:
                self.assertEqual(freqs,
                                 [0.5,0.5,0])
            elif id==2:
                self.assertEqual(freqs,
                                 [0.5,0.5,0])
            elif id==3:
                self.assertEqual(freqs,
                                 [1/3,1/3,1/3])


        # With multi position in the same document and 
        # multi position in the tokenized query 
        rf=bm25("test/testIndex_multiple_position_index.json")
        tokenized_request=["wikipédia","patricia","avec","wikipédia"]
        for id  in range(0,4):
            freqs=rf.get_query_tokens_freq(
                    {"id":id}
                    ,tokenized_request)
            if id==0:
                self.assertEqual(freqs,
                                 [1/2,1/2,0,1/2])
            elif id==1:
                self.assertEqual(freqs,
                                 [2/3,1/3,0,2/3])

            elif id==2:
                self.assertEqual(freqs,
                                 [1/3,1/3,0,1/3])
            elif id==3:
                self.assertEqual(freqs,
                                 [2/3,1/3,0,2/3])



    def test_exception_raised(self):
        """
        Test if asking for not existing document raise a ValueError  in the bm25.get_query_tokens_freq
        """
        rf=bm25("test/testIndex_basics_index.json")
        tokenized_request=["patricia","wikipédia","token"]
        self.assertRaises(
                ValueError,rf.get_query_tokens_freq,{"id":4},tokenized_request
                ) 


    def test_get_index_stats(self):
        rf=bm25("test/testIndex_basics_index.json")
        N, avgFieldLen=rf.get_index_stats()
        self.assertEqual(N,4)
        self.assertEqual(avgFieldLen,np.mean([2,2,2,3]))

        rf=bm25("test/testIndex_multiple_position_index.json")
        N, avgFieldLen=rf.get_index_stats()
        self.assertEqual(N,4)
        self.assertEqual(avgFieldLen,np.mean([2,3,3,3]))
        


    def test_IDF(self):
        rf=bm25("test/testIndex_basics_index.json")
        N, avgFieldLen=rf.get_index_stats()

        # With a token appearing in each document
        idf=rf.IDF("wikipédia",N)
        n=4
        self.assertEqual(idf,log( (N-n+0.5)/(n+0.5)  ))

        # With a token appearing in only one document
        idf=rf.IDF("token",N)
        n=1
        self.assertEqual(idf,log( (N-n+0.5)/(n+0.5)  ))



        rf=bm25("test/testIndex_multiple_position_index.json")
        N, avgFieldLen=rf.get_index_stats()
        idf=rf.IDF("wikipédia",N)
        n=4
        print(idf)
        self.assertEqual(idf,log( (N-n+0.5)/(n+0.5)  ))

