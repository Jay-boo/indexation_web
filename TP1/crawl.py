import requests
import time
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse
import os
import socket

def get_page_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    res=soup.find_all('a')
    return res


socket.setdefaulttimeout(1)


class Crawler:
    def __init__(self,seed:str,stop:int=1000):
        self.seed=seed
        self.stop=stop
        self.frontier=[]
        self.output=[]


    def filter_allowed_urls(self,urls):
        """
        Check robot.tx
        """
        output=[]
        print("In url filter method:")
        print([url.get('href') for url in urls])
        for link in urls: 
            link=link.get('href')
            rp=urllib.robotparser.RobotFileParser()
            try:
                rp.set_url(urlparse(link).scheme + "://"+ urlparse(link).hostname +"/robots.txt")
                rp.read()
                if rp.can_fetch("*",link):
                    output.append(link)
            except:
                pass
            

        return output




    def run(self):
        
        links=get_page_url(self.seed)
        self.frontier=links
        self.output=self.filter_allowed_urls(self.frontier)
        
        if len(self.output)>= self.stop:
            return
        print('------------- outputs')
        print(self.output)
        print('---------------------------')

        self.frontier=self.output
            

        while True: 
            
            flag=False
            new_frontier=[]
            output_maj=self.output
            for url in self.frontier:
                print(f'-----------------------------------------crawled :{url}')
                links=get_page_url(url)
                new_frontier.append(links)
                new_output=self.filter_allowed_urls(links)
                print(new_output)
                output_maj.remove(url)
                output_maj.extend(new_output)
                print('------------------OUTPUT LEN')
                print(len(output_maj))

                if len(output_maj) >=self.stop :
                    print(url)
                    flag=True
                    break

                time.sleep(5)

            print('-----------------------------end of first urls')
            self.output=output_maj
            self.frontier=self.output
                
            if flag:
                break
        print(self.output)
        print(len(self.output))

            
                    



if __name__ == "__main__":
    # url="https://ensai.fr/"
    url="https://twitter.com/"
    crawler=Crawler(url,500)

    crawler.run()

