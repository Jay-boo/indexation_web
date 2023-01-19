import requests
import time
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse
import socket
from htmldate import find_date

from requests.api import get
from requests.exceptions import TooManyRedirects

socket.setdefaulttimeout(1)


def url_date(url):
    find_date(url)



def get_allowed_urls(url):
    pages=[]
    try:
        response = requests.get(url)
    except TooManyRedirects:
        print("We find a Too manyRedirect error while navigating through urls")
        return []


    soup = BeautifulSoup(response.text, 'html.parser')
    links=soup.find_all('a')
    
    for link in links:
        link=link.get('href')
        rp=urllib.robotparser.RobotFileParser()
        try:
            rp.set_url(urlparse(link).scheme + "://"+ urlparse(link).hostname +"/robots.txt")
            rp.read()
            if rp.can_fetch("*",link):
                pages.append(link)
        except:
            pass
    return list(set(pages))

            







class Crawler:
    def __init__(self,seed:str,stop:int=100):
        self.seed=seed
        self.stop=stop
        self.frontier=[]
        self.output=[]

    def crawl(self):
        first_allowed_urls=get_allowed_urls(self.seed)
        print(first_allowed_urls)
        self.frontier=first_allowed_urls
        self.output=first_allowed_urls
        if  len(self.frontier)>=self.stop :
            return self.output[0:self.stop]

        while  True:
            print("in  while loop")
            flag=True
            new_outputs=[]
            waiting_url_output=self.output
            
            for url in self.frontier:
                print(f"----------------------looking at {url} in frontier")
                #-----------------------
                new_outputs+=get_allowed_urls(url)
                print(f"Total size of the outputs: {len(list(set(new_outputs+waiting_url_output)))}")

                #------------------
                # Test if we have enough outputs :
                waiting_url_output.remove(url)
                if len(list(set(new_outputs+waiting_url_output))) >= self.stop:
                    flag=False
                    break;

                time.sleep(5)#Time page crawling

            print("----- See every url in the actual output")
            #------------------------
            # update attribute
            final_output=list(set(waiting_url_output+new_outputs))
            
            #-----------------
            # Detect when we have no more url
            difference=True
            for x in set(final_output +self.output):
                if final_output.count(x)!=self.output.count(x):
                    difference= False
            if difference:
                print("no more urls")
                flag=False

            self.frontier=final_output
            self.output=final_output
            
            if not flag:
                print("We have enough output or there is no more url ")
                break
                
        return self.output[0:self.stop]


    def write_output_urls_in_text_file(self):
        with open("crawled_webpages.txt","w") as f:
            for line in self.output[0:self.stop]:
                f.write(line+"\n")

    def save_in_RDB(self):
        pass

if __name__ == "__main__":
    # url="https://ensai.fr/"
    url="https://twitter.com/"
    crawler=Crawler(url,100)

    crawler.crawl()
    crawler.write_output_urls_in_text_file()


