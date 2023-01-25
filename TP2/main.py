import argparse
import distutils.util
from indexWeb.index import Index


if __name__ == "__main__":
    parser =argparse.ArgumentParser()

    parser.add_argument("--stemmer",type=lambda x:bool(distutils.util.strtobool(x)),default='True')
    parser.add_argument("--tag",default="title")
    args=parser.parse_args()
    stemmer=args.stemmer
    tag=args.tag
    ind=Index(stemmer,tag)
    ind.run()

    
