# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem

class QuotesSpiderSpider(scrapy.Spider):
    name = 'quotes_spider'
    allowed_domains = ['quotes.toscrape.com/']
    start_urls = ['http://quotes.toscrape.com//']

    def parse(self, response):
        #filename = response.url.split('.')[-2] + '.html'
        #with open(filename, 'wb') as fp:
            #fp.write(response.body)
        element_list = response.xpath('//div[@class="quote"]')
        #import ipdb; ipdb.set_trace()
        for element in element_list:
            #import ipdb; ipdb.set_trace()
            Item = TutorialItem()
            Item['content'] = element.xpath('.//span[@class="text"]/text()').extract()[0]
            Item['author'] = element.xpath('.//small[@class="author"]/text()').extract()[0]
            Item['link'] = element.xpath('.//a[contains(text(),"(about)")]/@href').extract()[0]
            #Item['tags'] = element.xpath('')
            yield Item
