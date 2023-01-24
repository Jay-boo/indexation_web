from query.query import Query
import argparse
import distutils
# query=input("Requetes Utilisateur :")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--Q")
    parser.add_argument("--doc_contains_all_tokens",type=int,default=1)
    args = parser.parse_args()
    Q = args.Q
    doc_contains_all_tokens = args.doc_contains_all_tokens
    print(Q,doc_contains_all_tokens)
    if Q==None:
        Q=input(" Requête :")
    if  doc_contains_all_tokens ==0:
        doc_contains_all_tokens=False
    else:
        doc_contains_all_tokens=True
        #Valeur par default =True

    query=Query(Q,doc_contains_all_tokens)
    query.test_stopwords()
    print(query.run())
