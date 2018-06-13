import pandas as pd
import wikipedia as wiki
import scrapy

class GenreSpider(scrapy.Spider):
    # Tako poimenujemo spider-ja v komandni vrstici
    name = 'music_genre'

    # Dovoljene domene, da ne zabluzi
    allowed_domains = ['wikipedia.org']

    # Lahko to uporabimo namesto start_requests metode
    # Če uporabljamo ta način, moramo obvezno implementirati metodo z imenom parse
    # start_urls = ['http://www.avto.net/Ads/search_makes.asp']

    def start_requests(self):
        df = pd.read_csv("song_list.csv", index_col=0)

        urls = []
        num = 0

        for artist in df['artist']:

            if "featuring" in artist:
                artist = artist.split("featuring")[0]

            try:
                wiki_url = wiki.page(artist)
                if "&" in artist:
                    if not wiki_url:
                        artist = artist.split("&")[0]
                        wiki_url = wiki.page(artist)

                request = scrapy.Request(url=wiki_url.url, callback=self.parse_genres)
                yield request

            except Exception as e:
                print("URL not found")



    def parse_genres(self, response):
        parameters = {}
        genre = ""

        genre_info = response.css('div.mw-content-ltr div.mw-parser-output table.infobox tr th[scope="row"]::text').extract()
        artist = response.css('div.mw-content-ltr div.mw-parser-output table.infobox tr th span.fn::text').extract_first()

        if not artist:
            artist = response.css('div.mw-content-ltr div.mw-parser-output table.infobox tr th::text').extract_first()

        parameters['artist'] = artist

        if "Genres" in genre_info:
            genre = response.css('div.mw-content-ltr div.mw-parser-output table.infobox tr td div.hlist ul li a::text').extract_first()

            if genre != "file":
                parameters['genre'] = genre
            else:
                genre = ""

            if not genre:
                rows = response.css('div.mw-content-ltr div.mw-parser-output table.infobox tr:contains("Genres") td a::text').extract()

                for row in rows:
                    if "[" not in row:
                        genre = row
                        print("ROWS HELOU ---->", genre)
                        break

                if genre:
                    parameters['genre'] = genre
                else:
                    parameters['genre'] ="/"

        else:
            parameters['genre'] = "/"

        yield parameters