from unittest import TestCase
from indexWeb.index import Index



class testStatistics(TestCase):

    def testGetStatistics(self):
        flatten_token=[
                ["Paul","mange","une","pomme","dans","le","jardin"],
                ["Jean","mange","une","poire","dans","la","cuisine"]
        ]
        index=Index()
        index.urls=["url1","url2"]
        index.flatten_doc_tokens=flatten_token
        tot_doc_in_db,doc_count,token_count,mean_token_by_doc=index.get_statistics()

        self.assertEqual(2,tot_doc_in_db)
        self.assertEqual(2,doc_count)
        self.assertEqual(14,token_count)
        self.assertEqual(7,mean_token_by_doc)
                


