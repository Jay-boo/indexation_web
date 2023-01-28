from query.query import Query
import argparse
import distutils.util
import distutils
# query=input("Requetes Utilisateur :")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--Q")
    parser.add_argument("--filter_all_tokens",type=lambda x:bool(distutils.util.strtobool(x)),default='False')
    args = parser.parse_args()
    Q = args.Q
    filter_all_tokens = args.filter_all_tokens
    print(Q,filter_all_tokens)
    if Q==None:
        Q=input(" Requête :")
        #Valeur par default =True

    query=Query(Q,filter_all_tokens)
    query.run()
