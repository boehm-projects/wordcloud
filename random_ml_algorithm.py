import numpy
import pandas
import sqlite3
import randomscrapper
import bs4
from bs4 import BeautifulSoup, CData
import nltk
from nltk.corpus import stopwords
import numpy as np
import os
# Libraries
from wordcloud import WordCloud
import matplotlib.pyplot as plt
 


class BuzzwordMap:
    #init methode - clears data
    def __init__(self):
        self.scrapped_data = randomscrapper.Scraper("https://www.gamestar.de/news/rss/news.rss").get_bs_item()
        self.data = self.get_headlines(self.scrapped_data)
        self.stripped_data =self.remove_stopwords()
        
        self.inner_data = BeautifulSoup(self.stripped_data, 'html.parser')
        self.save_to_file(self.inner_data)
        self.data_from_file = self.open_file(os.path.join('E:/Neuer Ordner',"HeadlineFile.html"))
        

        self.display_word_cloud(" ".join(self.get_word_counts(self.data_from_file)))

       

    def get_headlines(self, data):    
        dat  = data
        rows = dat.findAll('item')
        list_of_elements = []
        for item in rows:
            try:
                l = item.find(text=lambda tag: isinstance(tag, bs4.CData)).string.strip()
                list_of_elements.append(l)
        #a = numpy.asarray(self.list_of_elements).reshape(1,len(self.list_of_elements))[0]
        #a = " ".join(a)
            except:
                continue
        return " ".join(list_of_elements)

    def get_word_counts(self,data):
        print(data)
        #data = self.scrapped_data.get_headlines()   
        words = nltk.tokenize.word_tokenize(data)        
        print(words)
        fdist = nltk.FreqDist(words)
        return fdist

    def save_to_file(self,data): 
        f = open(os.path.join('E:/Neuer Ordner',"HeadlineFile.html"), "a")
        f.write(str(data))
       
        f.close()

    def open_file(self, file):
        f = open(file, "r")
        return f.read()

    def remove_stopwords(self):
        
        german_stop_words = stopwords.words('german')
        text = ' '.join([word for word in self.data.split() if (word not in german_stop_words)])
        text = text.replace(" -","")
        text = text.replace("'", "")
        text = text.replace(".", "")
        text = text.replace("´", "")
        text = text.replace("`", "")
        text = text.replace(",", "")
        text = text.replace(":", "")
        text = text.replace("&", "")
        text = text.replace("?", "")
        text = text.replace("!", "")
        text = text.replace("(", "")
        text = text.replace(")", "")
        
        return text
    def display_word_cloud(self, data):
        wordcloud = WordCloud(width=1600, height=800, max_font_size=300, min_font_size=5).generate(data)
        plt.figure( figsize=(20,10), facecolor='k')
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.savefig(os.path.join('E:/Neuer Ordner','wordcloud.pdf'))


if __name__ == "__main__":
    
    test = BuzzwordMap()