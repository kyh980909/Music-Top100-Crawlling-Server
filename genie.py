from base import Base
import re


class Genie(Base):
    def __init__(self):
        self.url = ["https://www.genie.co.kr/chart/top200",
                    "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200212&hh=17&rtm=Y&pg=2",
                    "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200212&hh=17&rtm=Y&pg=3",
                    "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200212&hh=17&rtm=Y&pg=4"]

    def page_parse(self):
        soups = Base.page_parse(self)
        start_rank = 1
        for soup in soups:
            for rank, tr in enumerate(soup.select(
                    "#body-content > div.newest-list > div > table > tbody > tr"), start=start_rank):
                album_photo = 'https:' + tr.select('img')[0]['src']
                if tr.select('td.number > span.rank > span.rank > span.rank-up'):
                    rank_change = {'up': re.findall("\d+", tr.select(
                        'td.number > span.rank > span.rank > span.rank-up')[0].text)[0]}
                elif tr.select('td.number > span.rank > span.rank > span.rank-down'):
                    rank_change = {'up': re.findall("\d+", tr.select(
                        'td.number > span.rank > span.rank > span.rank-down')[0].text)[0]}
                else:
                    rank_change = {'none': 0}
                song = tr.select('td.info > a')[0].text.strip()
                singer = tr.select('td.info > a')[1].text.strip()

                print(rank_change)
                print(rank)
                print(album_photo)
                print(song)
                print(singer)
            start_rank += 50
