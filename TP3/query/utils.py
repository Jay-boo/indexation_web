import re
import json

# def load_index_from_json(filename:str):
#     f=open(filename)
#     return json.load(f)
#
def load_index_from_json(filename:str):
    with open(filename,'r')as file:
        data=json.load(file)
    return data 

def clean_text(text):
    text=re.sub(r"[^\w\s]","",text.lower())
    return text

def tokenize(text):
    text=clean_text(text)
    tokens=text.split()
    return tokens

def load_document_db(filename:str):
    with open(filename,'r')as file:
        data=json.load(file)
    return data 


def export_result_in_json(filename:str,data):
    with open(filename,"w") as outfile:
        json.dump(
                data,
                outfile,
                ensure_ascii=False,
                indent=4
                )
    
    


