from unittest import TestCase

from nltk.stem.snowball import FrenchStemmer
from indexWeb.index import Index
from indexWeb.utils import stemmer


class testPreProcessing(TestCase):
    
    def test_filterReachableUrls(self):
        """
        Assure timeout urls and error raised request.get(url) are 
        not in the filtered URls DB
        """
        # url_timeout="http://www.amisducadrenoir.fr/"
        # url_error_raised="http://www.corriges.net"
        index=Index()
        index.load_urls_from_json("test/test_preprocessing_urls.json",dir="test/")
        self.assertEqual(len(index.flatten_doc_tokens),2)


    def test_flatten_doc_tokens(self):
        """
        Assure token list are well positionalized in flatten_doc_tokens
        """
        #IF loading few URLS with some of then unreachable
        index=Index()
        index.load_urls_from_json("test/test_preprocessing_urls.json",dir="test/")

        # THEN unreachable urls don't appears in flatten_doc_token and flatten_doc_tokens_stem
        expected_flatten_token=[['karine','lacombe','wikipédia'],['nuit','de','cristal','wikipédia']]
        self.assertEqual(expected_flatten_token,index.flatten_doc_tokens)

        expected_stem_flatten_token=[[FrenchStemmer().stem(doc_token) for doc_token in doc]for doc in expected_flatten_token]
        self.assertEqual(expected_stem_flatten_token,index.flatten_doc_tokens_stem)
                




