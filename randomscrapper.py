import urllib.request
from urllib.error import URLError
import bs4
from bs4 import BeautifulSoup as bs


class Scraper:
    def __init__(self, f):
        self.f = f
        self.html = ""
        print(self.f)
        with urllib.request.urlopen(self.f) as response:
            try:
                self.html = response.read()
                self.html = bs(self.html, 'html.parser')
                print("i did it")
            except urllib.error.URLError as e:
                print("oh no" + e)

    def get_bs_item(self):
        return self.html
