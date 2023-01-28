from nltk.corpus import stopwords
from query.rankingFunction import RankingFunction


class bm25(RankingFunction):
    def __init__(self,filename_attached_index:str):
        super().__init__(filename_attached_index)
    

    def calculate_score(self,doc,tokenized_request):
        """
        implementation of the bm25 ranking function
        """
        pass
