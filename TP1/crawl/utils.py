from datetime import datetime
from htmldate import find_date

def url_date(url):
    """
    Get the date of a web page
    """
    try:
        return find_date(url)
    except:
        return ''

