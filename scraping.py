import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


if __name__ == "__main__":
    #スクレイピングしたデータを入れる表を作成
    list_df = pd.DataFrame(columns=['歌詞'])

    #曲ページ先頭アドレス
    base_url = 'https://www.uta-net.com'

    #歌詞一覧ページ
    url = 'https://www.uta-net.com/song/266648/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    song_lyrics = soup.find('div', itemprop='lyrics')
    song_lyric = song_lyrics.text
    song_lyric = song_lyric.replace('\n','')

    #取得した歌詞を表に追加
    tmp_se = pd.DataFrame([song_lyric], index=list_df.columns).T
    list_df = list_df.append(tmp_se)

    print(list_df)

    #csv保存
    list_df.to_csv('list.csv', mode = 'a', encoding='utf-8')