import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


class LiricsToWordCloud:

    def __init__(self):
        self.lirics = ''
        self.artist = ''
        self.song = ''
    
    def get_lirics(self, *, url=''):
        res = requests.get(url)

        try:
            soup = BeautifulSoup(res.text, "lxml")
        except:
            soup = BeautifulSoup(res.text, "html5lib")
        
        self.song = soup.find(class_='prev_pad').text.replace('\n','')
        self.lirics = soup.find('div', itemprop='lyrics').text.replace('\n','')
        self.artist = soup.find('span', itemprop='byArtist name').text.replace('\n','')

        print(self.song)
        print(self.artist)


        # create dataframe
        df = pd.DataFrame(data=[[self.song, self.artist, self.lirics]], columns=['曲名', 'アーティスト名', '歌詞'])

        print(df)

        df.to_csv('lirics.csv', mode = 'a', encoding='utf-8')


if __name__ == "__main__":
    ltw = LiricsToWordCloud()
    ltw.get_lirics(url='https://www.uta-net.com/song/266648/')