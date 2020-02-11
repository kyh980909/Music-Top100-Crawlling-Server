import requests
import json
from bs4 import BeautifulSoup
import time
import re
from multiprocessing import Pool


class Music:
    def __init__(self, rank, song, singer, like=None):
        self.rank = rank + 1
        self.song = song
        self.singer = singer
        self.like = like

    def to_json(self):
        if self.like is None:
            data = {"rank": self.rank, "song": self.song, "singer": self.singer}
            return data

        data = {
            "rank": self.rank,
            "song": self.song,
            "singer": self.singer,
            "like": self.like,
        }
        return data


def get_melon_like(header, album_id):
    url = "https://www.melon.com/album/detail.htm?albumId=" + str(album_id)

    req = requests.get(url, headers=header)
    soup = BeautifulSoup(req.text, "html.parser")
    like_selector = soup.select(
        "#frm > div > table > tbody > tr > td:nth-child(5) > div > button > span.cnt"
    )
    if like_selector == []:
        return None
    result = like_selector[0].text
    return re.findall("\d+", result)[0]


def crawlling(urls):
    data = {}
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    }

    if urls == "melon":
        data["melon"] = melon(header)
        return data
    else:
        data["genie"] = genie(header)
        return data


def melon(header):
    data = []
    url = "https://www.melon.com/chart/index.htm"
    req = requests.get(url, headers=header)
    soup = BeautifulSoup(req.text, "html.parser")
    like_page_check = True
    for rank, tr in enumerate(soup.select("#frm > div > table > tbody > tr")):
        tds = tr.select("td")
        td = tds[5]
        div = td.select_one('div[class="ellipsis rank01"]')
        song = div.text.strip()
        div = td.select_one('div[class="ellipsis rank02"]')
        singer = div.a.text.strip()
        if like_page_check:
            like = get_melon_like(header ,int(re.findall("\d+", tds[3].find("a")["href"])[0]))
            if like == None:
                like_page_check = False
        music = Music(rank, song, singer, like=like).to_json()
        data.append(music)
    return data


def genie(header):
    data = []
    urls = [
        "https://www.genie.co.kr/chart/top200",
        "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200129&hh=01&rtm=Y&pg=2",
    ]
    for url in urls:
        req = requests.get(url, headers=header)
        soup = BeautifulSoup(req.text, "html.parser")
        rank_start = 0
        for rank, tr in enumerate(
            soup.select("#body-content > div.newest-list > div > table > tbody > tr")
        ):
            tds = tr.select("td")
            td = tds[4]
            a = td.select_one('[class="title ellipsis"]')
            song = a.text.strip()
            a = td.select_one('[class="artist ellipsis"]')
            singer = a.text.strip()
            music = Music(rank + rank_start, song, singer).to_json()
            data.append(music)
        rank_start = 50
    return data


if __name__ == "__main__":
    start = time.time()
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    }
    kind = ["melon", "genie"]
    data = {}

    with Pool(4) as p:
        data = p.map(crawlling, kind)[0]

    data = json.dumps(data)

    print(json.loads(data))
    print("time : ", time.time() - start)

