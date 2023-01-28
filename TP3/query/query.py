from query.customLinearFunction import customLinearFunction
from query.rankingFunction import RankingFunction
from query.utils import load_index_from_json, tokenize, load_document_db,export_result_in_json
import nltk
from nltk.corpus import stopwords
import os

class Query:

    def __init__(self,request,doc_contains_all_tokens=True,ranking_function:RankingFunction=customLinearFunction("index.json")):
        self.request=request
        self.index=load_index_from_json("index.json")
        self.document_DB=load_document_db("documents.json")
        self.doc_contains_all_tokens=doc_contains_all_tokens
        self.rankingFunction=ranking_function

    def tokenize_request(self):
        return tokenize(self.request)


    def filter_document_with_token(self,token):
        """
        get documents containing the token
        Return:
            List of document index containing the token
        
        """
        try:
            documents=self.index[token].keys()
            return documents
        except KeyError:
            return []

    def filter_documents_with_at_least_one_token(self):
        """
        On conserve les documents avec au moins un token de la requete
        """
        tokens= self.tokenize_request()
        doc= self.filter_document_with_token(tokens[0])
        for token in tokens[1:len(tokens)]:
            doc_new=self.filter_document_with_token(token)
            doc=list(set(doc).union(doc_new))
        doc=list(doc)
        return [self.get_document_data_with_id(int(doc_i))for doc_i in doc]

    def filter_documents(self):
        """
        On conserve les documents avec tout les token de la requete

        Return:
            List of dictionnary  with the following keys {"id", "title","url"} 
        """
        tokens= self.tokenize_request()
        doc= self.filter_document_with_token(tokens[0])
        for token in tokens[1:len(tokens)]:
            doc_new=self.filter_document_with_token(token)
            doc=list(set(doc).intersection(doc_new))
        doc=list(doc)
        return [self.get_document_data_with_id(int(doc_i))for doc_i in doc]






    def get_document_data_with_id(self,id):
        for doc in self.document_DB:
            if doc["id"]==id:
                return {"id":id,"title":doc["title"],"url":doc["url"]}


    def setRankingFunction(self,rf:RankingFunction):
        self.rankingFunction=rf


    def run(self):
        #-------------------------------
        # Filter document
        if self.doc_contains_all_tokens:
            docs=self.filter_documents()
        else:
            docs=self.filter_documents_with_at_least_one_token()

        print("------------filter")
        print(docs)
        print("-------------------")
        
        #-------------------------------
        # Calculate score for each doc
        tokenized_request=self.tokenize_request()
        for doc in docs:
            doc["score"]=self.rankingFunction.calculate_score(doc,tokenized_request)
        docs.sort(key=lambda doc:doc["score"],reverse=True)
        export_result_in_json("results.json",docs)
        print("results export to results.json")
        return docs 
    



                
                







    def __str__(self):
        return str(self.index)
