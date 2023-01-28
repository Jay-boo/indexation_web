from unittest import TestCase
from query.utils import load_document_db, load_index_from_json
from query.query import Query


class TestFilterDocuments(TestCase):

    def test_filter_all_tokens_in_document(self):
        query=Query("wikipédia")
        query.index=load_index_from_json("test/testIndex_basics_index.json")
        query.document_DB=load_document_db("test/testIndex_basics_documents.json")
        self.assertEqual(len(query.filter_documents()),4)# All document tilte contain wikipédia
        query.request="karine"
        self.assertEqual(len(query.filter_documents()),1)# Only one get karine token
        karine_doc=query.filter_documents()

        query.request="karine wikipédia"
        self.assertEqual(len(query.filter_documents()),1)# Assert tis the same than karine one
        self.assertEqual(query.filter_documents(),karine_doc)

        query.request="patricia wikipédia"
        self.assertEqual(len(query.filter_documents()),3)





        query.request="token"
        self.assertEqual(len(query.filter_documents()),1)
        token_doc=query.filter_documents()


        query.request="patricia token"
        self.assertEqual(len(query.filter_documents()),1)
        self.assertEqual(token_doc,query.filter_documents())


        query.request="patricia wikipédia token"
        self.assertEqual(token_doc,query.filter_documents())
