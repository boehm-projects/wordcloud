import urllib.request
from urllib.error import URLError
import bs4
from bs4 import BeautifulSoup as bs
import logging

class Scraper:
    def __init__(self, f):
        self.f = f
        self.html = ""
        with urllib.request.urlopen(self.f) as response:
            try:
                self.html = response.read()
                self.html = bs(self.html, 'html.parser')
                logging.info("Scrapping done.")
            except urllib.error.URLError as e:
                logging.critical("Scrapping failed!")
                
    def get_bs_item(self):
        return self.html
