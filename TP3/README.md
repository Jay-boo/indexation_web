# :round_pushpin: Ranking Functions

Return the list of documents from the two json files according to a query :
 - `index.json` : index 
 -  `documents.json` : contains information on each document

***


## Prerequis

- `index.json` containing index in the following form:
```
{
  "token1" :{
    "doc_id_0":{"positions":[list_position_index],"count":count_int},
    ...
  },
  ...
}
```
and with the following preprocessing: **tokenize with space splits + lower text** *(query and documents need to be similarly preprocessed)*


- `documents.json` containing documents content and urls int the following form:

```
[
  {
    "url":"url_1",
    "id":id,
    "title":"title_1"
  },
  ...
]
```

*used files provided in the repository*


***

# :rocket: Launch 

## Launch local

```
git clone git@github.com:Jay-boo/indexation_web.git
cd indexation_web/TP3
pip install -r requirements.txt 
python3 main.py 
```

You can pass 3 arguments when launching `main.py`:
- `--Q`: Your query. If no argument passed , it will be ask with `input()`
- `--filter_all_tokens`= False : Keep only document containing every query tokens
- `--bm25` = False : if True bm25 will be use as ranking function. Else if False the [`CustomLinearFunction`](query/customLinearFunction.py) will be used  


## Launch with Docker

```
#Launch in TP3 directory
bash  launch_docker.sh
```
***

# CustomLinearFunction

Rank documents focusing on the order of the query tokens in documents.
A document that respect query token order will be rate better than another that doesn't respect query tokens order. 



**Moreover stopwords are lighter in score calculation that others in `CustomLinearFunction`**


