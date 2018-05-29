"""High level imports for this and that"""
from bs4 import BeautifulSoup
import requests


def filter_tags(company):
    """Returns the symbol for the specified company"""
    print(company)
    site = requests.get(f'https://www.google.com/search?q={company}+stock+symbol')
    print(site.status_code)
    if site.status_code == 200:
        soup = BeautifulSoup(site.text, 'html.parser')
        potential_links = soup.find_all('cite')
        return potential_links

def get_symbol(links):
    """
    Grab the first link with matching phrase and returns
    the symbol from the link
    """
    symbol = None
    for i in links:
        print(i.text)
        if '/quote/' in i.text:
            begin = [j for j in range(0, len(i.text)) if i.text[j:].startswith('/')]
            end = len(i.text)-1
            symbol = i.text[begin[-2]+1:end]
            break
        elif '/symbol/' in i.text:
            begin = [j for j in range(0, len(i.text)) if i.text[j:].startswith('/')]
            end = len(i.text)
            symbol = i.text[begin[-1]+1:end].upper()
            break
    return symbol
