# Minimal Crawler

A minimal crawler with a single-threaded version and a multi-threaded one using sitemaps respectfull of the politness.

***

## :rocket: How to use ?

### Launch local


#### Install packages
```
pip install -r requirements
```
#### ⮕ Launch crawler
 Three arguments:
 - `--url`:`str` : seed of the crawler. 
 - `--limit_pages`:`int` Number of page to collect. **Default value = 50**
 - `--multithread`:`Boolean` : Use of multi thread **Default value = False**

```
python3 main.py --url https://ensai.fr/ --limit_pages 60 --multithread False
```

### ⮕ Launch with docker
In TP1/ directory use the following commands to build and launch the docker image
```
docker build -t my_image_name .
docker run my_image_name
```
You can modify argument in the `Dockerfile` before building and launching the image

***

## Storage
There is 2 storage location :
- In `crawled_webpages.txt` : Store urls only.
- In DB : You can configure your DB in `crawl/database.py`. By default it use a sqlite database engine named "pages". The page url, date and html are stored in the DB.

Visualize sqlite local DB on browser : https://inloop.github.io/sqlite-viewer/

***
## Multi Threading
The number of thread is limited to 5, and to respect politness 2 web pages with similar root urls can't be in parallel threads.
This limits its effectiveness because it crawl urls using sitemaps.


