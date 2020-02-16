from base import Base
import re

from music import Music


class Melon(Base):
    def __init__(self):
        self.url = ['https://www.melon.com/chart/index.htm']

    def page_parse(self):
        soups = Base.page_parse(self)

        data = []

        for soup in soups:
            for rank, tr in enumerate(soup.select('#frm > div > table > tbody > tr'), start=1):
                tds = tr.select('td')
                if tds[2].select('span.up'):
                    rank_change = {'up': int(tds[2].select('span.up')[0].text)}
                elif tds[2].select('span.down'):
                    rank_change = {'down': int(
                        tds[2].select('span.down')[0].text)}
                else:
                    rank_change = {'none': 0}
                album_id = re.findall("\d+", tds[3].select('a')[0]['href'])[0]
                album_photo = tds[3].select('img')[0]['src']
                song = tds[5].select_one(
                    'div[class="ellipsis rank01"]').text.strip()
                singer = tds[5].select_one(
                    'div[class="ellipsis rank02"]').select('a')[0].text.strip()

                data.append(Music(rank, rank_change, album_photo, song, singer).to_json())
        return data
