from collections import Counter
from nltk.corpus import stopwords
from query.rankingFunction import RankingFunction

class customLinearFunction(RankingFunction):
    def __init__(self,filename_attached_index:str):
        super().__init__(filename_attached_index)
    

    def calculate_score(self,doc,tokenized_request):
        """
        Focus on similar token order than request
        doc is a dictionary {"id","title","url"}
        """
        stopw=set(stopwords.words('french'))
        last_position=-1
        score=0
        passed_token=Counter()
        for token in  tokenized_request:
            if token in stopw:
                weight=0.2
            else:
                weight=0.8
            
            passed_token[token]+=1
            #-------------------
            #Calculate token  document position 
            try:
                position_in_doc=self.attached_index[token][str(doc["id"])]["positions"][passed_token[token]-1]
            except (KeyError,IndexError) as error:
                if isinstance(error,IndexError):
                    msg="Token appear multiple time in request  and appears less time in document"
                else :
                    msg= "Token not in index"
                # print(msg)
                position_in_doc= -1

            if last_position < position_in_doc:
                score+=weight*2
                last_position=position_in_doc
            else:
                score -= weight*2
            

        return score 

