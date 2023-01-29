from math import log
import numpy as np
from nltk.corpus import stopwords
from query.rankingFunction import RankingFunction


class bm25(RankingFunction):
    def __init__(self,filename_attached_index:str):
        super().__init__(filename_attached_index)
    

    def calculate_score(self,doc,tokenized_request):
        """
        implementation of the bm25 ranking function
        """
        # Calcul  des frequence de chaque token de la requete
        freqs= self.get_query_tokens_freq(doc,tokenized_request)
        fieldLen=self.get_doc_total_nb_tokens(doc)
        k1=1.2
        b=0.75
        N,avgFieldLen=self.get_index_stats()

        score=0
        counter=0
        for token in tokenized_request:
            freq=freqs[counter]
            score += self.IDF(token,N) *((freq*(k1+1))/freq+k1*(1-b+b*(fieldLen/avgFieldLen)))
            counter+=1
        return score

        

    def get_query_tokens_freq(self,doc,tokenized_request):
        freqs=[]
        total_tokens_count=self.get_doc_total_nb_tokens(doc)
        if total_tokens_count==0:
            raise ValueError("Document id not in index")
            
        for token in tokenized_request:
            try: 
                token_count=self.attached_index[token][doc["id"]]["count"]
            except KeyError:
                token_count=0
            freqs.append(token_count/total_tokens_count)

        return freqs



    def get_doc_total_nb_tokens(self,doc):
        """
        Get document total number of tokens using index build
        """
        tot=0
        for  key,value in self.attached_index.items():
            if doc["id"] in  value.keys():
                tot += value[doc["id"]]["count"]
        return tot


    def number_of_doc_contain_token(self,token):
        """
        Return number of document containg token
        """
        return len(self.attached_index[token])


    def get_index_stats(self):
        """
        return doc_count,average_number_of_token_by_doc
        """
        doc_ids=[]
        for key , value in self.attached_index.items():
            tokens_documents=set([key for key in value.keys()])
            doc_ids=list(set(doc_ids).union(tokens_documents))


        avgFieldLen=np.mean([self.get_doc_total_nb_tokens({"id":str(doc_id)}) for doc_id in doc_ids])

            
        return len(doc_ids),avgFieldLen


    def IDF(self,token,N):
        n=self.number_of_doc_contain_token(token)
        return log((N-n+0.5)/(n+0.5))







