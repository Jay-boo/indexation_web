# Minimal Crawler

## Install packages
```
pip install -r requirements
```
## Launch crawler
 Three arguments:
 - `--url`:`str` : seed of the crawler. 
 - `--limit_pages`:`int` Number of page to collect. **Default value = 50**
 - `--multithread`:`Boolean` : Use of multi thread **Default value = False**

```
python3 main.py --url https://ensai.fr/ --limit_pages 60 --multithread False
```

## Storage





Visualize sqlite local DB on browser : https://inloop.github.io/sqlite-viewer/
