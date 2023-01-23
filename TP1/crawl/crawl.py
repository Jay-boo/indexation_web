import requests
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from crawl.utils import url_date
from crawl.database import Pages, init,engine
from threading import Thread
from urllib.request import urlopen
import time
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse
import socket
from requests.exceptions import TooManyRedirects
from urllib.error import URLError



socket.setdefaulttimeout(1)

class crawlerThread(Thread):
    def __init__(self,crawler,url,session):
        Thread.__init__(self)
        self.crawler=crawler
        self.url=url
        self.new_pages=[]
        self.session=session

    def run(self):
        print(f"crawling ------------- {self.url}")
        new_urls=self.crawler.get_allowed_urls_with_sitemaps(self.session,self.url)
        self.new_pages+=new_urls

        new_urls=self.crawler.get_allowed_urls_with_robots(self.session,self.url)
        self.new_pages+=new_urls
        time.sleep(5)
        print(f"end------------- {self.url}:  count new pages : {len(self.new_pages)}")
        






class Crawler:
    def __init__(self,seed:str,stop:int=50):
        init()
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
        is_completed=False
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
                is_completed=self.add_page_to_db(session,loc,requests.get(loc).text,url_date(loc))
                if is_completed:
                    print("is break")
                    break
                pages.append(loc)
            if is_completed:
                break
                    
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
        first_allowed_urls=list(set(self.get_allowed_urls_with_sitemaps(session,self.seed)))
        time.sleep(5)
        print(first_allowed_urls)
        self.frontier=first_allowed_urls
        self.output=first_allowed_urls
        if  len(self.frontier)>=self.stop :
            print("out")
            return self.output[0:self.stop]
        while  True:
            flag=True
            new_outputs=[]
            waiting_url_output=self.output
            
            for url in self.frontier:
                print(f"----------------------looking at {url} in frontier")
                #-----------------------
                new_urls=self.get_allowed_urls_with_sitemaps(session,url)
                new_outputs+=new_urls
                if len(new_urls) >0:
                    waiting_url_output.remove(url)
                if len(list(set(new_outputs+waiting_url_output))) >= self.stop:
                    print("flag is False")
                    flag=False
                    break
                print(f"Total size of the outputs: {len(list(set(new_outputs+waiting_url_output)))}")
                time.sleep(5)#Time page crawling

            final_output=list(set(waiting_url_output+new_outputs))
            difference=True
            for x in set(final_output +self.output):
                if final_output.count(x)!=self.output.count(x):
                    difference= False
            if difference:
                print("No more urls to explore")
                flag=False

            self.frontier=final_output
            self.output=final_output
            
            if not flag:
                print("----------------finish-----------------")
                break
                
        session.commit()
        self.output=self.output[0:self.stop]
        return self.output



    def multiThread_crawl(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        first_allowed_urls=list(set(self.get_allowed_urls_with_sitemaps(session,self.seed)))
        time.sleep(5)
        self.frontier=first_allowed_urls
        self.output=first_allowed_urls
        if  len(self.frontier)>=self.stop :
            return self.output[0:self.stop]
        
        while True:
            threads=list()
            flag=True
            waiting_url_output=self.output
            new_outputs=[]
            root_urls_in_thread=[]#WE don't want the same sit to be crawled in two parallele thread

            for url in self.frontier:

                root_url=urlparse(url).scheme + "://"+ urlparse(url).hostname

                if root_url not in root_urls_in_thread:
                    x=crawlerThread(self,url,session)
                    threads.append(x)
                    x.start()
                    root_urls_in_thread.append(root_url)
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
                        root_urls_in_thread=[]
                else:
                    pass

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
        session.commit()
        self.output=self.output[0:self.stop]
        return self.output    





    def add_page_to_db(self,session,url:str,document,date):
        """
        Add pages to the session query verifying the urls are unique
        and return boolean to know if db is complet

        """
        count=session.query(Pages).count()
        print(count)
        if count>= self.stop: # If we have enough urls
            return True
        if date !='': 
            date=datetime.strptime(date,"%Y-%m-%d")
        else:
            date=None
        res=(
            session.query(Pages).filter(Pages.url==url).all()
        )
        if res==[]:
            # assert url not already in session
            page=Pages(url=url,document=document,date=date)
            session.add(page)
        return False


        
    def write_output_urls_in_text_file(self):
        """
        Write crawler urls in crawled_webpages.txt
        """
        with open("crawled_webpages.txt","w") as f:
            for line in self.output[0:self.stop]:
                f.write(line+"\n")

