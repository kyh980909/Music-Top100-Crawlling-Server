class Music:
    def __init__(self, rank, rank_change, album_photo, song, singer):
        self.rank = rank
        self.rank_change = rank_change
        self.album_photo = album_photo
        self.song = song
        self.singer = singer

    def to_json(self):
        data = {
            "rank": self.rank,
            "rank_change": self.rank_change,
            "img": self.album_photo,
            "song": self.song,
            "singer": self.singer
        }

        return data
