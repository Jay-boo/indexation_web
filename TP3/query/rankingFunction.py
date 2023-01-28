from abc import ABC, abstractmethod
from collections import Counter
import nltk
from nltk.corpus import stopwords

from query.utils import load_index_from_json

class RankingFunction(ABC):
    def __init__(self,filename_attached_index:str):
        self.attached_index=load_index_from_json(filename_attached_index)
        nltk.download('stopwords')
    
    @abstractmethod
    def calculate_score(self,doc,tokenized_request):
        pass

