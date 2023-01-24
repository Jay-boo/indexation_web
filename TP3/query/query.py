from query.utils import load_index_from_json, tokenize, load_document_db,export_result_in_json
import nltk
from nltk.corpus import stopwords
import os

class Query:

    def __init__(self,request,doc_contains_all_tokens=True):
        self.request=request
        self.index=load_index_from_json("index.json")
        self.document_DB=load_document_db("documents.json")
        self.doc_contains_all_tokens=doc_contains_all_tokens

    def tokenize_request(self):
        return tokenize(self.request)


    def filter_document_with_token(self,token):
        """
        get documents containing the token
        
        """
        try:
            documents=self.index[token].keys()
            return documents
        except KeyError:
            return []

    def filter_document_bis(self):
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

    def filter_document(self):
        """
        On conserve les documents avec tout les token de la requete
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



    def apply_basic_linear_function(self,doc):
        """
        Return score
        """
        stopw=set(stopwords.words('french'))
        last_position=0
        score=0
        for token in self.tokenize_request() :
            if token in stopw:
                score_delta=5
            else:
                score_delta=10
            if last_position <= min(self.index[token][str(doc["id"])]["positions"] ):
                score+=score_delta
            else:
                return  score-=score_delta
        return score


    def add_score_to_not_stopword(self,doc):
        nltk.download('stopwords',download_dir=os.getcwd())
        stopw=set(stopwords.words('french'))
        print(stopw)


    def run(self):
        #-------------------------------
        # Filter document
        if self.doc_contains_all_tokens:
            docs=self.filter_document()
        else:
            docs=self.filter_document_bis()

        print("------------filter")
        print(docs)
        print("-------------------")
        
        #-------------------------------
        # Calculate score for each doc
        for doc in docs:
            doc["score"]=self.apply_basic_linear_function(doc) 
        docs.sort(key=lambda doc:doc["score"])
        print(docs)
        export_result_in_json("results.json",docs)
        print("finish run fct")
        return docs 
    



                
                







    def __str__(self):
        return str(self.index)
