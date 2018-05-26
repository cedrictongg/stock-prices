"""High level imports for this and that"""
from bs4 import BeautifulSoup
import requests


def filter_tags(company):
    """Returns the symbol for the specified company"""
    site = requests.get(f'https://www.google.com/search?q={company}+stock+symbol')
    soup = BeautifulSoup(site.text, 'lxml')
    potential_links = soup.find_all('cite')
    return potential_links


def get_symbol(links):
    """
    Grab the first link with matching phrase and take
    the symbol from the link
    """
    symbol = None
    for i in links:
        if '/quote/' in i.text:
            begin = [j for j in range(0, len(i.text)) if i.text[j:].startswith('/')]
            end = len(i.text)-1
            symbol = i.text[begin[-2]+1:end]
            break
    return symbol
