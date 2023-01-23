import re
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
        


def tokenize(text):
    text=clean_text(text)
    tokens=text.split()
    return tokens
    






