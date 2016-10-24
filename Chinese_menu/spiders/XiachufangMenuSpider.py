import sys
import scrapy
from scrapy.xlib.pydispatch import dispatcher
from operator import itemgetter
import collections

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

class XiachufangMenuSpider(scrapy.Spider):
    name = "XiachufangMenu"
    characters = collections.Counter()

    start_urls = []
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 8
    }

    def __init__(self):
        dispatcher.connect(self.spider_closed, scrapy.signals.spider_closed)
        for i in xrange(101896732,101898732):
            self.start_urls.append("http://www.xiachufang.com/recipe/" + str(i) + "/")

    def spider_closed(self,spider):
        filename = "./results/Chinese_Xiachufang_menu2.txt"

        with open(filename, 'wb') as f:
            character_list = sorted(self.characters.items(), key=itemgetter(0))

            for character, count in character_list:
                if character != ' ' and character != '\r' and character != '\n':
                    f.write(character+'\n')
        f.close()

    def parse(self, response):

        title = response.xpath('//h1[@class="page-title"]/text()').extract()
        description = response.xpath('//div[@class="desc"]/text()').extract()
        steps = response.xpath('//li[@class="container"]/p/text()').extract()

        if len(title) > 0:
            for i in range(0,len(title[0])):
                self.characters[title[0][i]] += 1

        if len(description) > 0:
            for i in range(0,len(description)):
                for j in range(0,len(description[i])):
                    self.characters[description[i][j]] += 1

        if len(steps) > 0:
            for i in range(0,len(steps)):
                for j in range(0,len(steps[i])):
                    self.characters[steps[i][j]] += 1
