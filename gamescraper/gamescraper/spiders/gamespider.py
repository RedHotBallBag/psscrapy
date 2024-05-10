import scrapy
import logging
import shutil

class GameSpider(scrapy.Spider):
    name = 'ps4'
    start_urls = ['https://dlpsgame.com/']

    def parse(self, response):
        # Add logging
        self.logger.info('Parsing page: %s', response.url)

        for games in response.css('div.post-body.entry-content'):
            yield {
                'name': games.css('a').attrib['href'].replace('https://dlpsgame.com/category/ps4/','').replace('-download-free/','').replace('-',' '),
                'url': games.css('a').attrib['href'],
                'image': games.css('img').attrib['src']
            }

        next_page = response.css('a.nextpostslink').attrib['href']
        if next_page is not None:
            # Add logging
            self.logger.info('Following next page: %s', next_page)
            yield response.follow(next_page, callback=self.parse)


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GameSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.closed, signal=signals.spider_closed)
        return spider
    
    
    def closed(self, reason):
        # Define source and destination paths
        src_path = '/path/to/output.csv'
        dest_path = '/var/www/html/output/output.csv'

        # Move the file to the destination folder
        try:
            shutil.move(src_path, dest_path)
            self.logger.info('Output file moved to %s', dest_path)
        except Exception as e:
            self.logger.error('Error moving output file: %s', e)
