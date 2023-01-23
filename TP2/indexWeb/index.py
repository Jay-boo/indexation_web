import json

from indexWeb.utils import get_url_title, tokenize




class Index:

    def __init__(self):
        self.urls=[]
        self.index={}
        self.positional_index={}
        self.counter=0


    def build_basic_index(self,tokens):
        for token in tokens   :
            if token not in self.index.keys():
                self.index[token]=[self.counter]
            else:
                self.index[token].append(self.counter)


    def build_positional_index(self,tokens):
        pos=0
        for token in tokens :
            if token in self.positional_index.keys():
                if self.counter in self.positional_index[token]:
                    self.positional_index[token][self.counter].append(pos)
                else:
                    self.positional_index[token][self.counter]=[pos]
            else:
                self.positional_index[token]={}
                self.positional_index[token][self.counter]=[pos]
            pos+=1
        


    def build_index(self):
        for url in self.urls[0:6]:
            print(f"-------------------{url}")
            try:
                tokens=tokenize(get_url_title(url))
                self.build_basic_index(tokens)
                self.build_positional_index(tokens)
                self.counter+=1
            except:
                continue



    def add_document_to_index(self,new_urls):
        pass

    def load_urls_from_json(self,filename:str):
        f=open(filename)
        self.urls=json.load(f)
    

    def get_document_count(self):
        return self.counter

    def tokens_count(self):
        res=0
        for key in self.positional_index.keys():
            for subkey in self.positional_index[key].keys():
                res+=len(self.positional_index[key][subkey])
        return  res




    
    def save_index(self):
        with open("title.non_pos_index.json", "w") as outfile:
            json.dump(
                    self.index,
                      outfile,
                      ensure_ascii=False,
                      indent=4
            )

        




