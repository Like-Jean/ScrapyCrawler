import sys
import scrapy
from scrapy.xlib.pydispatch import dispatcher
from operator import itemgetter
from scrapy.selector import Selector
import collections
import time

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

class ChineseMenuSpider(scrapy.Spider):
    name = "ChineseMenu"
    handle_httpstatus_list = [302]
    #start_urls = [
    #"https://www.ele.me/premium/wtw371yhtc7",
    #"https://www.ele.me/place/wx4g43ebyjn",
    #"https://www.ele.me/place/ws0ee5exnm5",
    #"https://www.ele.me/place/ws105wt73ch",
    #"https://www.ele.me/place/wtms6rwx4cd",
    #"https://www.ele.me/place/wtsqqvzz9n2"
    #]
    start_urls = [
    "http://waimai.meituan.com/home/wx4g416mzxh9",
    "http://waimai.meituan.com/home/wtsqqun2hx83",
    "http://waimai.meituan.com/home/wtw3sjrwsgzb",
    "http://waimai.meituan.com/home/ws0edup2jmgw",
    "http://waimai.meituan.com/home/ws10m42brm5c",
    "http://waimai.meituan.com/home/wtmkq80cvbw5",
    "http://waimai.meituan.com/home/yb4h6fvc7xm0",
    "http://waimai.meituan.com/home/wt3q08n1wweb",
    "http://waimai.meituan.com/home/wt027hh8be0c",
    "http://waimai.meituan.com/home/wx4g45r716vu",
    "http://waimai.meituan.com/home/wm6n2npmrw7d",
    "http://waimai.meituan.com/home/wqj6z039n2r9",
    "http://waimai.meituan.com/home/ws7grbn54905",
    "http://waimai.meituan.com/home/wx4g49uspt9y",
    "http://waimai.meituan.com/home/wx4g42vjzs8z",
    "http://waimai.meituan.com/home/wx4g424sj2wt",
    "http://waimai.meituan.com/home/wx4ffq8dv7hu",
    "http://waimai.meituan.com/home/wx4g1eyd55ds",
    "http://waimai.meituan.com/home/wx4g1exuejw9",
    "http://waimai.meituan.com/home/wx4exf9n3tbv",
    "http://waimai.meituan.com/home/wttccs9x39ue",
    "http://waimai.meituan.com/home/wtte749yhzz6",
    "http://waimai.meituan.com/home/wtw3uepk5zuw",
    "http://waimai.meituan.com/home/wtw371v55jgg",
    "http://waimai.meituan.com/home/wtmkq8nknkkp",
    "http://waimai.meituan.com/home/wtmkmm94x8cy",
    "http://waimai.meituan.com/home/wtmkwt54nx3d",
    "http://waimai.meituan.com/home/wtmsb3k0xf40",
    "http://waimai.meituan.com/home/wtmkns3ukrut",
    "http://waimai.meituan.com/home/wtmkm4hy32cd",
    "http://waimai.meituan.com/home/ws9dzrtf89zp",
    "http://waimai.meituan.com/home/w7jzu5ucqj3z",
    "http://waimai.meituan.com/home/ws0e9d647e4k",
    "http://waimai.meituan.com/home/ws0ee0bhthyk",
    "http://waimai.meituan.com/home/ws0e3ujrcyju",
    "http://waimai.meituan.com/home/ws0e94932654"
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 6,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1
    }
    characters = collections.Counter()

    def __init__(self):
    	dispatcher.connect(self.spider_closed, scrapy.signals.spider_closed)

    def spider_closed(self,spider):
        filename = "./results/Chinese_menu.txt"

        with open(filename, 'wb') as f:
            character_list = sorted(self.characters.items(), key=itemgetter(0))

            for character, count in character_list:
                if character != ' ' and character != '\r' and character != '\n':
                    f.write(character+'\n')
        f.close()

    def start_requests(self):
        for i,url in enumerate(self.start_urls):
            yield scrapy.Request(url,meta={'dont_redirect':True}, callback=self.parse)
            print url

    def parse(self, response):
        for href in response.xpath('//div[@class="restaurant"]/a[@class="rest-atag"]/@href'):
            url = response.urljoin(href.extract())

            yield scrapy.Request(url,meta={'dont_redirect':True}, callback=self.parse_dir_contents)
            print url

    def parse_dir_contents(self,response):

        for sel in response.xpath('//div[@class="category"]'):
            title = sel.xpath('h3/@title').extract()
            description = sel.xpath('div[@class="food-cate-desc"]/text()').extract()
            picture_description = sel.xpath('div[@class="pic-food-cont clearfix"]/div[@class="j-pic-food pic-food  pic-food-rowlast"]/div[@class="np clearfix"]/span/text()').extract()
            food_content = sel.xpath('div[@class="text-food-cont"]/div[@class="j-text-food text-food clearfix"]/div[@class="fl description"]').extract()

            for i in range(0,len(title[0])):
            	self.characters[title[0][i]] += 1

            if len(description) != 0:
                for i in range(0,len(description)):
                    for j in range(0,len(description[i])):
                        self.characters[description[i][j]] += 1

            if len(picture_description) != 0:
                for i in range(0,len(picture_description)):
                    for j in range(0,len(picture_description[i])):
                        self.characters[picture_description[i][j]] += 1

            if len(food_content) != 0:
                for i in range(0,len(food_content)):
                    if len(food_content[i]) != 0:
                        for j in range(0,len(food_content[i])):
                            self.characters[food_content[i][j]] += 1
            #print food_content
