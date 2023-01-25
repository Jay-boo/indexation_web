import re
from nltk.stem.snowball import FrenchStemmer
from bs4 import BeautifulSoup
import requests

def clean_text(text):
    text=re.sub(r"[^\w\s]","",text.lower())
    return text

def get_url_title(url):
    resp=requests.get(url)
    if resp.ok:
        soup=BeautifulSoup(resp.text,'html.parser')
        title=soup.find_all('title')[0].get_text()
        return title

def get_url_balise(url,balise:str):
    resp=requests.get(url)
    if resp.ok:
        soup=BeautifulSoup(resp.text,'html.parser')
        found_balise=soup.find_all(balise)
        print(found_balise)
        if found_balise: 
            concat_text=''
            for balise in found_balise:
                concat_text+=balise.get_text()+" "
            return concat_text
        else:
            return ''
        


def tokenize(text):
    text=clean_text(text)
    tokens=text.split()
    return tokens

def stemmer(text):
    fs=FrenchStemmer()
    tokens=tokenize(text)
    return [fs.stem(token) for token in tokens]
    

if __name__ == "__main__":
    url="https://nvchad.com/"
    ps=FrenchStemmer()
    word=["irait","ira"]
    print(ps.stem("boulangerie"))

    # url="https://ensai.fr."
    # print(get_url_title(url))
    # print("---------")
    # print(get_url_balise(url,"h1"))
    # print("---------")

    # Need to concat all h1 balise in get_url_balise






