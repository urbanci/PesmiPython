import scrapy


class MusicSpider(scrapy.Spider):
    # Tako poimenujemo spider-ja v komandni vrstici
    name = 'music_data'

    # Dovoljene domene, da ne zabluzi
    allowed_domains = ['musicoutfitters.com']

    # Lahko to uporabimo namesto start_requests metode
    # Če uporabljamo ta način, moramo obvezno implementirati metodo z imenom parse
    # start_urls = ['http://www.avto.net/Ads/search_makes.asp']

    def start_requests(self):
        """
        To je dokumentacija metode start_requests.
        Ta metoda se kliče ob zagonu, le enkrat. Če je ta metoda implementirana, se ignorira start_urls list.
        """
        parameters = {}
        url = 'https://www.musicoutfitters.com/top-100-songs.htm'

        # Vse kar želimo da scrapy pregleda podamo z ukazom yield, mora pa biti tipa scrapy.Request
        # V argument callback podamo metodo, ki se zažene, ko se podan link pregleda
        request = scrapy.Request(url=url, callback=self.parse_glavna_stran)
        yield request




    def parse_glavna_stran(self, response):
        """
        Ta metoda se kliče, ko se naloži glavna stran z znamkami avtomobilov.
        """
        znamke = response.css('div.col-10 div.gutters div.col a::attr(href)').extract()

        for znamka in znamke:
            # Pripravimo URL za parsanje
            url = "https://www.musicoutfitters.com/"+znamka

            yield scrapy.Request(url, callback=self.parse_seznam_pesmi)



    def parse_seznam_pesmi(self, response):
        pesmi = response.css('div.col-6 a::text').extract()
        leto = response.css('div.row nav.breadcrumbs ul li span::text').extract()
        parameters = {}

        for pesem in pesmi:
            split = pesem.split(" - ")

            parameters['year'] = leto[0]
            parameters['artist'] = split[1]
            parameters['title'] = split[0]

            yield parameters

