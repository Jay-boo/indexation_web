from query.bm25 import bm25
from query.query import Query
import argparse
import distutils.util
import distutils
# query=input("Requetes Utilisateur :")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--Q")
    parser.add_argument("--filter_all_tokens",type=lambda x:bool(distutils.util.strtobool(x)),default='False')
    parser.add_argument("--bm25",type=lambda x:bool(distutils.util.strtobool(x)),default='False')
    args = parser.parse_args()
    Q = args.Q
    filter_all_tokens = args.filter_all_tokens
    use_bm25=args.bm25
    print(Q,filter_all_tokens,use_bm25)
    if Q==None:
        Q=input(" Requête :")
        #Valeur par default =True
    
    if use_bm25:
        rf=bm25("index.json")
        query=Query(Q,filter_all_tokens,ranking_function=rf)
        rf_str="BM25"
    else:
        query=Query(Q,filter_all_tokens)
        rf_str="CustomLinearRankingFunction"

    print("------prompt--------")
    print(f"Query :{Q}\nDocuments contains all query tokens :{filter_all_tokens}\nRanking Function :{rf_str}")
    print("--------------")
    query.run()
