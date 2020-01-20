import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
from janome.tokenizer import Tokenizer
import re

class LiricsToWordCloud:

    def __init__(self):
        self.lirics = ''
        self.artist = ''
        self.song = ''
    
    def get_lirics(self, *, url=''):
        error = None

        page = requests.get(url)

        try:
            soup = BeautifulSoup(page.text, "lxml")
        except:
            soup = BeautifulSoup(page.text, "html5lib")
        
        try:
            self.song = soup.find(class_='prev_pad').text.replace('\n','')
            self.lirics = soup.find('div', itemprop='lyrics').text.replace('\n','')
            self.artist = soup.find('span', itemprop='byArtist name').text.replace('\n','')

            print(self.song)
            print(self.artist)


            # create dataframe
            df = pd.DataFrame(data=[[self.song, self.artist, self.lirics]], columns=['曲名', 'アーティスト名', '歌詞'])

            print(df)

            df.to_csv('lirics.csv', mode = 'a', encoding='utf-8')
        except Exception as e:
            error = e

        return error

    def to_words(self):
        error = None

        t = Tokenizer()
        tokens = t.tokenize(self.lirics)

        words = []
        for token in tokens:
            try:
                hinshi = token.part_of_speech.split(',')[0]

                if hinshi in ['名詞', '形容詞', '動詞', '副詞']:
                    words.append(token.surface)
            except Exception as e:
                error = e
        
        try:
            words = ' '.join(words)
            with open('words.txt', 'w', encoding='utf-8') as fp:
                fp.write(words)
        except Exception as e:
            error = e


if __name__ == "__main__":
    args = sys.argv

    if len(args) >= 2:
        ltw = LiricsToWordCloud()
        error = ltw.get_lirics(url=args[1])
        if error is None:
            ltw.to_words()