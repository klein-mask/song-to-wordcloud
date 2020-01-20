import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import numpy as np
from PIL import Image


class LiricsToWordCloud:

    def __init__(self):
        self.song = ''
        self.artist = ''
        self.lirics = ''
        self.words = ''
        self.output_path = './output/'
    
    def get_lirics(self, *, url=''):
        error = None

        page = requests.get(url)

        try:
            soup = BeautifulSoup(page.text, "lxml")
        except:
            soup = BeautifulSoup(page.text, "html5lib")
        
        try:
            self.song = soup.find(class_='prev_pad').text.replace('\n','')
            self.artist = soup.find('span', itemprop='byArtist name').text.replace('\n','')
            self.lirics = soup.find('div', itemprop='lyrics').text.replace('\n','')

            df = pd.DataFrame(data=[[self.song, self.artist, self.lirics]], columns=['曲名', 'アーティスト名', '歌詞'])
            df.to_csv(self.output_path + 'lirics.csv', mode = 'w', encoding='utf-8')
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
            self.words = ' '.join(words)
            with open(self.output_path + 'words.txt', 'w', encoding='utf-8') as fp:
                fp.write(self.words)
        except Exception as e:
            error = e
        
        return error
    
    def create_word_cloud(self, img_color_path=''):
        font = '/System/Library/Fonts/ヒラギノ角ゴシック W1.ttc'

        stop_words = ['そう', 'ない', 'いる', 'する', 'まま', 'よう', 'てる', 'なる', 'こと', 'もう', 'いい', 'ある', 'ゆく', 'れる']

        wc = WordCloud( background_color='white', 
                        font_path=font,
                        width=800,
                        height=600, 
                        stopwords=set(stop_words),
                        mask=np.array(Image.open(img_color_path)),
                        collocations=False).generate(self.words)

        wc.to_file(self.output_path + '{0}.png'.format(self.song))


if __name__ == "__main__":
    args = sys.argv

    if len(args) >= 3:
        ltw = LiricsToWordCloud()
        error = ltw.get_lirics(url=args[1])

        if error is None:
            error = ltw.to_words()
            
            if error is None:
                ltw.create_word_cloud(args[2])

