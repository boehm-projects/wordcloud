import randomscrapper
import bs4
from bs4 import BeautifulSoup, CData
import nltk
from nltk.corpus import stopwords
import os
# Libraries
from wordcloud import WordCloud
import matplotlib.pyplot as plt
 


class BuzzwordMap:
    #init methode - clears data
    def __init__(self, argument):
        self.argument = argument
        #fetch new data
        self.scrapped_data = randomscrapper.Scraper("https://www.gamestar.de/news/rss/news.rss").get_bs_item()
        #strip data from all punctuation and only return headlines
        self.data = self.get_headlines(self.scrapped_data)
        self.stripped_data =self.remove_stopwords()

        #save as string in textfile
        self.inner_data = BeautifulSoup(self.stripped_data, 'html.parser')
        self.save_to_file("------",self.inner_data)

        #read from file as 1d array
        self.data_from_file = self.open_file(os.path.join('E:/Neuer Ordner',"HeadlineFile.html"))
        self.data_by_index = self.data_from_file.split("------")

        #create wordcloud from newest data
        if self.argument == "new":
            self.display_word_cloud(" ".join(self.get_word_counts(self.data_by_index[-1])))

        #create wordcloud from array index
        elif self.argument in range(0, 100):
            x = int(self.argument)
            try:
                self.display_word_cloud(" ".join(self.get_word_counts(self.data_by_index[x])))
            except:
                print("This is no valid argument")
        #create wordcloud composed of the top words in all of the array
        elif self.argument == "top":
            self.display_word_cloud(" ".join(self.get_word_counts("".join(self.data_by_index))))

    def get_headlines(self, data):    
        dat  = data
        rows = dat.findAll('item')
        list_of_elements = []
        for item in rows:
            try:
                l = item.find(text=lambda tag: isinstance(tag, bs4.CData)).string.strip()
                list_of_elements.append(l)
            except:
                continue
        return " ".join(list_of_elements)

    def get_word_counts(self,data):
        words = nltk.tokenize.word_tokenize(data)        
        #print(words)
        fdist = nltk.FreqDist(words)
        return fdist

    def save_to_file(self, delimiter, data): 
        f = open(os.path.join('E:/Neuer Ordner',"HeadlineFile.html"), "a")
        f.write(delimiter + str(data) )
       
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
    
    test = BuzzwordMap("top")