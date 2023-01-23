import requests
from requests.api import request
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util.langhelpers import NoneType
from database  import engine 


from threading import Thread
from urllib.request import urlopen
import sqlite3
import time
import pandas as pd
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse
import socket
from htmldate import find_date
from requests.exceptions import TooManyRedirects
from urllib.error import URLError
socket.setdefaulttimeout(1)


def url_date(url):
    try:
        return find_date(url)
    except:
        return ''# to do later


class crawlerThread(Thread):
    def __init__(self,crawler,url):
        Thread.__init__(self)
        self.crawler=crawler
        self.url=url
        self.new_pages=[]

    def run(self):
        print(f"crawling ------------- {self.url}")
        new_urls=self.crawler.get_allowed_urls_with_sitemaps(self.url)
        self.new_pages+=new_urls

        new_urls=self.crawler.get_allowed_urls_with_robots(self.url)
        self.new_pages+=new_urls
        time.sleep(5)
        print(f"end------------- {self.url}: new pages : {len(self.new_pages)}")
        






class Crawler:
    def __init__(self,seed:str,stop:int=100):
        self.seed=seed
        self.stop=stop
        self.frontier=[]
        self.output=[]
        self.visited_sitemaps=[]

    def get_allowed_urls_with_sitemaps(self,session,url):
        """
        Get new urls with sitemaps attached to the url
        """
        pages=[]
        rp=urllib.robotparser.RobotFileParser()
        rp.set_url(urlparse(url).scheme + "://"+ urlparse(url).hostname +"/robots.txt")
        try: 
            rp.read()
        except URLError:
            print("URL Error raise")
            return []

        sitemaps=rp.site_maps()

        if sitemaps is None:
            return []

        sitemaps_not_exploit=[sitemap for sitemap in sitemaps if sitemap not in self.visited_sitemaps ]
        for sitemap in sitemaps_not_exploit :
            print(f"----------looking at sitemap {sitemap}")
            try:
                response=urlopen(sitemap)
            except:
                continue

            xml=BeautifulSoup(response,'lxml-xml',from_encoding=response.info().get_param('charset'))
            if xml.find_all('sitemapindex'):
                #We want to explore sitemaps giving urls , not the other sitemaps
                continue
            urls=xml.find_all("url")
            for url in urls:
                loc=url.findNext("loc").text
                pages.append(loc)
                self.add_page_to_db(session,loc,None,url_date(loc))
        self.visited_sitemaps+=sitemaps_not_exploit
        return pages

    def get_allowed_urls_with_robots(self,session,url):
        """
        Get new url checking robots.txt and urls in the url page
        """
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
                    self.add_page_to_db(session,link,response.text,url_date(link))

            except:
                pass
        return list(set(pages))


    def crawl(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        first_allowed_urls=list(set(self.get_allowed_urls_with_sitemaps(session,self.seed) +self.get_allowed_urls_with_robots(session,self.seed)))
        time.sleep(5)
        print(first_allowed_urls)
        self.frontier=first_allowed_urls
        self.output=first_allowed_urls
        if  len(self.frontier)>=self.stop :
            return self.output[0:self.stop]

        while  True:
            flag=True
            new_outputs=[]
            waiting_url_output=self.output
            
            for url in self.frontier:
                print(f"----------------------looking at {url} in frontier")
                #-----------------------
                new_urls=self.get_allowed_urls_with_sitemaps(url)
                new_outputs+=new_urls
                if len(new_urls) >0:
                    waiting_url_output.remove(url)

                if len(list(set(new_outputs+waiting_url_output))) >= self.stop:
                    flag=False
                    break

                #-------------
                # Getting new urls from robots and links in page
                new_urls=self.get_allowed_urls_with_robots(url)
                new_outputs+=new_urls

                print(f"Total size of the outputs: {len(list(set(new_outputs+waiting_url_output)))}")

                #------------------
                # Test if we have enough outputs :
                if len(list(set(new_outputs+waiting_url_output))) >= self.stop:
                    flag=False
                    break

                time.sleep(5)#Time page crawling

            print("----- See every url in the actual output")
            #------------------------
            # update attribute
            final_output=list(set(waiting_url_output+new_outputs))

            #--------------------------
            # Put every url in database
            
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
                
        self.output=self.output[0:self.stop]
        return self.output



    def multiThread_crawl(self):
        first_allowed_urls=list(set(self.get_allowed_urls_with_sitemaps(self.seed) +self.get_allowed_urls_with_robots(self.seed)))
        time.sleep(5)
        print(first_allowed_urls)
        self.frontier=first_allowed_urls
        self.output=first_allowed_urls
        if  len(self.frontier)>=self.stop :
            return self.output[0:self.stop]
        
        while True:
            threads=list()
            flag=True
            waiting_url_output=self.output
            new_outputs=[]
            for url in self.frontier:
                root_url=urlparse(url).scheme + "://"+ urlparse(url).hostname
                x=crawlerThread(self,url)
                threads.append(x)
                x.start()
                if (len(threads)>=5 or url==self.frontier[-1]) :
                    for index, thread in enumerate(threads):
                        thread.join()
                    print(waiting_url_output)
                    for index, thread in enumerate(threads):
                        new_outputs+=thread.new_pages
                        if len(thread.new_pages) >0:
                            waiting_url_output.remove(thread.url)
                    new_outputs=list(set(new_outputs))
                    if(len(list(set(waiting_url_output+new_outputs)))>=self.stop):
                        print("Enough URL")
                        flag=False
                        break
                    threads=list()
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
        self.output=self.output[0:self.stop]
        return self.output    

    def add_page_to_db(self,session,url:str,document:str|NoneType,date):
        """
        Add pages to the session query verifying the urls are unique
        """
            # new_urls[url] = WebPageDB(url=url, creation_date=self.find_date(url))

        for each in session.query(WebPageDB).filter(WebPageDB.url.in_(new_urls.keys())).all():
            session.merge(new_urls.pop(each.url))
        # Only add those posts which did not exist in the database 

        session.add_all(new_urls.values())

        # Now we commit our modifications (merges) and inserts (adds) to the database!
        session.commit()
        


        



    def write_output_urls_in_text_file(self):
        with open("crawled_webpages.txt","w") as f:
            for line in self.output[0:self.stop]:
                f.write(line+"\n")

    def save_in_RDB(self):
        data_to_stock=pd.DataFrame({
                'url':self.output,
                'date':[url_date(url) for url in self.output]}
                )
        conn=sqlite3.connect("urls.db")
        data_to_stock.to_sql("my_data",conn,if_exists="replace")
        conn.execute(
        """
        create table urlTable as 
        select * from my_data;
        """)
