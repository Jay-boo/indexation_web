from time import time
from crawl import Crawler

# url="https://ensai.fr/"
# url="https://twitter.com/"
url="https://docs.python.org/fr/3/library/urllib.robotparser.html#module-urllib.robotparser"
# crawler=Crawler(url,200)
# start_oneThread=time()
# crawler.crawl()
# end_oneThread=time()
# print(len(crawler.output))
#
#
crawler=Crawler(url,200)

start_multiThread=time()
crawler.multiThread_crawl()
end_multiThread=time()
print(len(crawler.output))
crawler.write_output_urls_in_text_file()
# print(f"Duration one thread : {end_oneThread - start_oneThread}")
print(f"Duration multi thread : {end_multiThread - start_multiThread}")

# crawler.save_in_RDB()
# crawler.write_output_urls_in_text_file()

