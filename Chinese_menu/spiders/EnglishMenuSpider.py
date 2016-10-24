import sys
import scrapy
from scrapy.xlib.pydispatch import dispatcher
import collections

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

class EnglishMenuSpider(scrapy.Spider):
	name = "EnglishMenu"
	start_urls = []
	words = collections.Counter()

	def __init__(self):
		dispatcher.connect(self.spider_closed, scrapy.signals.spider_closed)
		for i in xrange(1,400):
			self.start_urls.append("http://allrecipes.com/recipes/?grouping=all&page=" + str(i))

	def spider_closed(self,spider):
    	
		filename = "./results/English_menu_sentences.txt"

		with open(filename, 'wb') as f:
			words_list = sorted(self.words.items(), key=lambda w: len(w[0]), reverse=True)

			for word, count in words_list:
				f.write(word + '\n')
		f.close()

	def parse(self, response):

		for href in response.xpath('//article[@class="grid-col--fixed-tiles"]/a[@data-internal-referrer-link="hub recipe"][1]/@href'):
			url = response.urljoin(href.extract())

			yield scrapy.Request(url,self.parse_dir_contents)

	def parse_dir_contents(self,response):

		title = response.xpath('//section[@class="recipe-summary clearfix"]/h1/text()').extract()
		description = response.xpath('//section[@class="recipe-summary clearfix"]/div[@class="submitter"]/div[@itemprop="description"]/text()').extract()
		
		if len(title) != 0:
			self.words[title[0]] += 1
		
		if len(description) != 0:
			self.words[description[0]] += 1

		for ingredient in response.xpath('//ul[@id="lst_ingredients_1"]/li/label/span/text()').extract():

			if len(ingredient) != 0:
				self.words[ingredient[0]] += 1

		for ingredient in response.xpath('//ul[@id="lst_ingredients_2"]/li/label/span/text()').extract():

			if len(ingredient) != 0:
				self.words[ingredient[0]] += 1

		for sel in response.xpath('//ol[@class="list-numbers recipe-directions__list"]/li'):
			direction = sel.xpath('/span/text()').extract()

			if len(direction) != 0:
				self.words[direction[0]] += 1