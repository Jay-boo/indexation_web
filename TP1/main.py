from time import time
from crawl.crawl import Crawler
import distutils.util
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url")
    parser.add_argument("--limit_pages",type=int,default=50)
    parser.add_argument("--multithread",type=lambda x:bool(distutils.util.strtobool(x)),default='False')
    args = parser.parse_args()
    url = args.url
    limit_pages = args.limit_pages
    multithread = args.multithread
    print('------------prompt-------------------')
    print(f"seed:{url} \nmax urls:{limit_pages} \nmultithread:{multithread}") 
    print('-------------------------------------\n\n')
    crawler=Crawler(url,limit_pages)
    if url ==None:
       raise argparse.ArgumentTypeError("url need to be specified in --url argument") 
        
    start=time()
    if multithread:
        crawler.multiThread_crawl()
    else:
        crawler.crawl()
    end=time()
    crawler.write_output_urls_in_text_file()
    print(f"Timer : {end- start}")
