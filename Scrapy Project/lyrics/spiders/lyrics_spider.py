from scrapy.spiders import SitemapSpider


class LyricsSpider(SitemapSpider):
    name = "lyrics"
    allowed_domains = ['lyricslk.com']
    sitemap_urls = [
        'http://lyricslk.com/sitemap.xml'
    ]
    sitemap_rules = [('^(?!.*).*$', 'parse')]

   
    def parse(self, response):
        song_lines = response.xpath('//*[@id="lyricsBody"]/text()').getall()
        song = ''
        for line in song_lines:
            song_line = line.split('\n')[1].strip()
            song = song + " " + song_line
        yield {
            'track_id': response.xpath('//*[@id="lyricsTitle"]/h2/text()')[0].get().split(' - ')[0],
            'track_name': response.xpath('//*[@id="lyricsTitle"]/h2/text()')[0].get().split(' - ')[1],
            'track_rating': response.xpath('//*[@id="lyricsTitle"]/h2/text()')[0].get().split(' - ')[2],
            'album_name': response.xpath('//*[@id="lyricsTitle"]/h2/text()')[0].get().split(' - ')[3],
            'artist_name': response.xpath('//*[@id="lyricsSinger"]/h2/text()')[0].get().split(' - ')[4],
            'artist_rating': response.xpath('//*[@id="lyricsSinger"]/h2/text()')[0].get().split(' - ')[5],
            'song' : song
        }