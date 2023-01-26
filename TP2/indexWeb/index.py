import json
from tqdm import tqdm
from collections import Counter
import numpy as np
from indexWeb.utils import get_url_balise, tokenize, stemmer




class Index:

    def __init__(self,use_stemmer=True,content_tag="title"):
        self.urls=[]
        self.index={}
        self.positional_index={}
        self.flatten_doc_tokens=[]
        self.flatten_doc_tokens_stem=[]
        self.content_tag=content_tag
        self.use_stemmer=use_stemmer
        self.index_stem={}
        self.positional_index_stem={}



    def build_basic_index(self,tokens,url_id,dict_to_fill):
        """
        fill dict_to_fill using document tokens , and document id

        """
        counter_tokens=Counter(tokens)
        for token,count in counter_tokens.items():
            if token not in dict_to_fill.keys():
                dict_to_fill[token]={str(url_id):count}
            else:
                dict_to_fill[token][str(url_id)]=count


    def build_positional_index(self,tokens,url_id,dict_to_fill):
        pos=0
        for token in tokens :
            if token in dict_to_fill.keys():
                if str(url_id) in dict_to_fill[token]:
                    dict_to_fill[token][str(url_id)].append(pos)
                else:
                    dict_to_fill[token][str(url_id)]=[pos]
            else:
                dict_to_fill[token]={}
                dict_to_fill[token][str(url_id)]=[pos]
            pos+=1
        


    def build_indexes(self):
        """
        Wich url id use : The ids on the json or the ids in the filtered urls. The urls that will be used to make the index

        Here we consider the ids on the filtered urls.
        It means that document id 3 is not linked to the third url in crawled_urls.json if any url0,url1,url2 is not reachable. 
        If url0,url1 and url2 are reachable then url3 correspond to document 3
        """
        counter=0
        for doc_tokens in self.flatten_doc_tokens:
            tokens=doc_tokens
            self.build_basic_index(tokens,counter,self.index)
            self.build_positional_index(tokens,counter,self.positional_index)
            counter+=1

        counter=0
        for doc_tokens in self.flatten_doc_tokens_stem:
            tokens=doc_tokens
            self.build_basic_index(tokens,counter,self.index_stem)
            self.build_positional_index(tokens,counter,self.positional_index_stem)
            counter+=1
        

    def load_urls_from_json(self,filename:str,dir="outputs/"):
        """
        Create self.flatten_doc_tokens and self.flatten_doc_tokens_stem
        Moreover filtered urls keeping only reachable urls in outputs/filtered_crawled_urls.json

        Not keeped urls: 
            
            - Not reachable urls 
            - No html tag self.content_tag in the document

        """
        flag=False
        f=open(filename)
        self.urls=json.load(f)
        progressBar=tqdm(total=len(self.urls),desc=f"Looking at urls in {filename} ")
        filtered_urls=[]



        for url in self.urls:
            try:
                text=get_url_balise(url,self.content_tag)
                tokens=tokenize(text)
                if len(tokens)>0:
                    self.flatten_doc_tokens.append(tokens)
                    if self.use_stemmer:
                        stem_tokens=stemmer(text)
                        self.flatten_doc_tokens_stem.append(stem_tokens)
                    filtered_urls.append(url)
                else:
                    #url timeout or no content in this document so it s kick out of the DB 
                    flag=True
                    progressBar.update(1)
                    continue
            except:
                # print("error raised during the request.get")
                # If error raised here , its mean that get_url_balise raised an error 
                # requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeoutError, urllib3.exceptions.ConnectTimeoutError 
                # This erorr is due to request.get error
                flag=True
                progressBar.update(1)
                continue
            progressBar.update(1)
        progressBar.close()
        if flag:
            print("some urls are not reachable, the filtered crawled urls are store in filtered_crawled_urls.json")
        #----------------------
        #save reachable urls in a new json
        with open(f"{dir}filtered_crawled_urls.json", "w") as outfile:
            json.dump(
                   filtered_urls, 
                      outfile,
                      ensure_ascii=False,
                      indent=4
            )

        # Assert every kept crawled_urls has at least one token
        for doc in self.flatten_doc_tokens:
            assert (len(doc) >0)
    



        
    


    #--------------------------------------------
    # Get before index statistics
    def get_statistics(self):
        """
        return basic statistic about the index construction : 
            the number of urls , the number of urls used in the index, the number of tokens, ...
        """
        return len(self.urls),len(self.flatten_doc_tokens),sum([len(doc_tokens)for doc_tokens in self.flatten_doc_tokens]),np.mean([len(doc_tokens)for doc_tokens in self.flatten_doc_tokens])

        

    def save_statistics(self):
        tot_doc_in_db, doc_count,token_count,mean_token_by_doc=self.get_statistics()
        metadata={
                "before_index_stat":{
                    "tot_doc_in_db":tot_doc_in_db,
                    "used_doc_count":doc_count,
                    "token_count":token_count,
                    "mean_token_by_document":mean_token_by_doc,
                }
        }
        with open("outputs/metadata.json", "w") as outfile:
            json.dump(
                    metadata,
                      outfile,
                      ensure_ascii=False,
                      indent=4
        )




    
    def save_indexes(self):
        """
        Store basic index and positional index in two json
        """
        with open(f"outputs/{self.content_tag}.non_pos_index.json", "w") as outfile:
            json.dump(
                    self.index,
                      outfile,
                      ensure_ascii=False,
                      indent=4
        )
        with open(f"outputs/{self.content_tag}.pos_index.json", "w") as outfile:
            json.dump(
                    self.positional_index,
                      outfile,
                      ensure_ascii=False,
                      indent=4
        )
        with open(f"outputs/stem.{self.content_tag}.non_pos_index.json", "w") as outfile:
            json.dump(
                    self.index_stem,
                      outfile,
                      ensure_ascii=False,
                      indent=4
        )
        with open(f"outputs/stem.{self.content_tag}.pos_index.json", "w") as outfile:
            json.dump(
                    self.positional_index_stem,
                      outfile,
                      ensure_ascii=False,
                      indent=4
        )

    def run(self):
        self.load_urls_from_json("crawled_urls.json")
        self.save_statistics()
        self.build_indexes()
        self.save_indexes()


        




