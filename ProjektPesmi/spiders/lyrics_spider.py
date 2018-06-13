import itertools
import re

import scrapy
import pandas as pd

class LyricSpyder(scrapy.Spider):
    # Tako poimenujemo spider-ja v komandni vrstici
    name = 'lyrics_data'
    DOWNLOAD_DELAY = 1

    # Dovoljene domene, da ne zabluzi
    allowed_domains = ['azlyrics.com']

    # Lahko to uporabimo namesto start_requests metode
    # Če uporabljamo ta način, moramo obvezno implementirati metodo z imenom parse
    # start_urls = ['http://www.avto.net/Ads/search_makes.asp']

    def start_requests(self):

        df = pd.read_csv("song_list.csv")
        num = 0

        for artist, title in zip(df['artist'], df['title']):

            artist = artist.replace(" ", "").lower()
            artist = re.sub(r'[^a-zA-Z0-9 ]',r'', artist)
            title = title.replace(" ", "").lower()
            title = re.sub(r'[^a-zA-Z0-9 ]', r'', title)

            url = 'https://www.azlyrics.com/lyrics/'+artist+'/'+title+'.html'

            request = scrapy.Request(url=url, callback=self.parse_lyrics)
            yield request


    def parse_lyrics(self, response):
        title = response.css('div.main-page div.row div.col-lg-8 b::text').extract()[1].replace('"', "")

        if(title):
            lyrics = response.css('div.main-page div.row div.col-lg-8 div::text').extract()
            artist = response.css('div.main-page div.row div.col-lg-8 form#addsong input[name="artist"]::attr(value)').extract_first()
            text = ""
            parameters = {}

            for lyric in lyrics:
                text = text+" "+lyric.replace('\n', "").replace('\r', "").replace('\t', "")

            parameters['lyrics'] = text
            parameters['title'] = title
            parameters['artist'] = artist

        yield parameters