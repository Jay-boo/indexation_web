import requests
from bs4 import BeautifulSoup
import socket
import json
import re

from indexWeb.index import Index





# f=open("crawled_urls.json")
# urls=json.load(f)
#
#
#
# index={}
# counter=0
# for url in urls[0:20]:
#     print(url)
#     counter+=1
#     try:
#         resp=requests.get(url)
#         if resp.ok:
#             soup=BeautifulSoup(resp.text,'html.parser')
#             title=soup.find_all('title')[0].get_text()
#             title = clean_text(title)
#             tokens=title.split()
#             print(tokens)
#             # tokens.remove('')
#
#             for token in tokens   :
#                 if token not in index.keys():
#                     index[token]=[counter]
#                 else:
#                     index[token].append(counter)
#
#
#     except:
#         
#         continue
# print(index)
if __name__ == "__main__":
    ind=Index()
    ind.load_urls_from_json("crawled_urls.json")
    ind.build_index()
    ind.save_index()
    print(ind.tokens_count())
    print(ind.positional_index)

    
