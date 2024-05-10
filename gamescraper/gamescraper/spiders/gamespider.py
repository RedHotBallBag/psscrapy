import scrapy


class GameSpider(scrapy.Spider):
    name = 'ps4'
    start_urls = ['https://dlpsgame.com/']

    def parse(self, response):
        for games in response.css('div.post-body.entry-content'):
            yield  {
                'name': games.css('a').attrib['href'].replace('https://dlpsgame.com/category/ps4/','').replace('-download-free/','').replace('-',' '),
                'url':games.css('a').attrib['href'],
                'image':games.css('img').attrib['src']
            }
        next_page = response.css('a.nextpostslink').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)