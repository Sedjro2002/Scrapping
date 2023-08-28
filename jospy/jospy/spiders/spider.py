from pathlib import Path
import scrapy
import time

class Spider(scrapy.Spider):
    name = 'spider'
    
    def start_requests(self):
        self.logger.info('Starting spider')
        url="https://marches-publics.bj/plan-de-passation"
        yield scrapy.Request(url=url, callback=self.parse)
        # print(scrapy.Request.body)

    def parse(self, response):
        # filename = 'marches-publics.html'
        # Path(filename).write_bytes(response.body)
        time.sleep(10)
        table = response.css('div.full-width')
        print(table)
