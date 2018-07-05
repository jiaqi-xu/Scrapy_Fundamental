# -*- coding: utf-8 -*-
import scrapy
from collectips.items import CollectipsItem


class XicispiderSpider(scrapy.Spider):
    name = 'XiciSpider'
    allowed_domains = ['xicidaili.com']

    start_urls = ['http://xicidaili.com/']

    def start_requests(self):
        reqs = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36'
        }
        for i in range(1,3):
            yield scrapy.Request('http://www.xicidaili.com/nn/%s'%i, headers=headers)


    def parse(self, response):

        ip_list = response.xpath('//table[@id="ip_list"]')
        trs = ip_list[0].xpath('tr')
        items = []
        for ip in trs[1:]:
            pre_item = CollectipsItem()
            pre_item['IP'] = ip.xpath('td[2]/text()')[0].extract()
            pre_item['PORT'] = ip.xpath('td[3]/text()')[0].extract()
            pre_item['POSITION'] = ip.xpath('string(td[4])')[0].extract().strip()
            pre_item['TYPE'] = ip.xpath('td[6]/text()')[0].extract()
            pre_item['SPEED'] = ip.xpath('td[7]/div[@class="bar"]/@title') \
                                .re('\d{0,2}\.\d*')[0]
            pre_item['LAST_CHECK_TIME'] = ip.xpath('td[10]/text()')[0].extract()
            yield pre_item
