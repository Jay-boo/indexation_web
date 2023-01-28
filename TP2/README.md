# :round_pushpin: Indexes Creation 

Create multiple indexes based on the urls in `crawled_urls.json`:
  - count Index
  - positional Index
 Moreover 2 options are available to tune your indexes. You can choose the html element to extract from each web pages with `--tag` and you can modify data preprocessing with `--stemmer` option
 
&rarr; The resulting indexes are stored in the `outputs` directory

***

# :rocket: Lauch

## Launch local
 
 ```
 git clone git@github.com:Jay-boo/indexation_web.git
 cd TP2
 pip install -r requirements.txt 
 python3 main.py --stemmer True --tag title
 ```
 You can pass 2 arguments when launching `main.py`
 - `--stemmer`:Use of stemming during data preprocessing. Default value : True
 - `--tag`:HTML element to extract from each document. Default value : title. *other example : h1*

## Launch with Docker

```
docker build -t image_tp2 .
docker run -v $(pwd)/outputs:/index/outputs image_tp2
```
... or open interactive terminal and play with argument
```
docker run -v $(pwd)/outputs:/index/outputs -it --entrypoint bash image_tp2
```
