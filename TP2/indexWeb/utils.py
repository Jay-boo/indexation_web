import re
from nltk.stem.snowball import FrenchStemmer
from bs4 import BeautifulSoup
import requests

def clean_text(text):
    text=re.sub(r"[^\w\s]","",text.lower())
    return text


def get_url_balise(url,balise:str):
    resp=requests.get(url,timeout=5)
    if resp.ok:
        #timeout response will not pass here

        soup=BeautifulSoup(resp.text,'html.parser')
        found_balise=soup.find_all(balise)
        if found_balise: 
            concat_text=''
            for balise in found_balise:
                concat_text+=balise.get_text()+" "
            return concat_text
        else:
            return ''# Return by docuemnt whitout the asked content asked
    return ''# Return by timeout urls
        


def tokenize(text):
    text=clean_text(text)
    tokens=text.split()
    return tokens

def stemmer(text):
    fs=FrenchStemmer()
    tokens=tokenize(text)
    return [fs.stem(token) for token in tokens]
    

