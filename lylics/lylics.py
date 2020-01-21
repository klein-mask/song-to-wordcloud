
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image

import requests
import sys
import os


class LyricsToWordCloud:

    def __init__(self):
        self.song = ''
        self.artist = ''
        self.lyrics = ''
        self.words = ''
        self.output_path = os.path.dirname(__file__) + '/output/'
    
    def generate(self, *, url, source_image):
        try:
           self.get_lyrics(url=url)
        except:
            print('歌詞の取得に失敗しました')
        
        try:
            self.to_words()
        except:
            print('歌詞の分割に失敗しました')
        
        try:
            self.create_word_cloud(source_image=source_image)
            print('Success!!')
        except:
            print('wordcloudの作成に失敗しました')
        
    def get_lyrics(self, *, url):
        page = requests.get(url)

        try:
            soup = BeautifulSoup(page.text, "lxml")
        except:
            soup = BeautifulSoup(page.text, "html5lib")
        
        self.song = soup.find(class_='prev_pad').text.replace('\n','')
        self.artist = soup.find('span', itemprop='byArtist name').text.replace('\n','')
        self.lyrics = soup.find('div', itemprop='lyrics').text.replace('\n','')

        df = pd.DataFrame(data=[[self.song, self.artist, self.lyrics]], columns=['曲名', 'アーティスト名', '歌詞'])
        df.to_csv(self.output_path + 'lirics.csv', mode = 'w', encoding='utf-8')


    def to_words(self):
        t = Tokenizer()
        tokens = t.tokenize(self.lyrics)

        words = []
        for token in tokens:
            hinshi = token.part_of_speech.split(',')[0]

            if hinshi in ['名詞', '形容詞', '動詞', '副詞']:
                words.append(token.surface)
        
        self.words = ' '.join(words)
        with open(self.output_path + 'words.txt', 'w', encoding='utf-8') as fp:
            fp.write(self.words)


    def create_word_cloud(self, *, source_image):
        font = '/System/Library/Fonts/ヒラギノ角ゴシック W1.ttc'

        stop_words = ['それ', 'そう', 'ない', 'の', 'いる', 'する', 'まま', 'よう', 'てる', 'なる', 'こと', 'もう', 'いい', 'ある', 'ゆく', 'れる']

        img_color = np.array(Image.open(source_image))
        wc = WordCloud( background_color='white', 
                        font_path=font,
                        width=800,
                        height=600, 
                        stopwords=set(stop_words),
                        mask=img_color,
                        collocations=False).generate(self.words)

        wc.recolor(color_func=ImageColorGenerator(img_color))
        wc.to_file(self.output_path + '{0}.png'.format(self.song))


if __name__ == "__main__":
    args = sys.argv

    if len(args) >= 3:
        ltw = LyricsToWordCloud()
        error = ltw.generate(url=args[1], source_image=args[2])
