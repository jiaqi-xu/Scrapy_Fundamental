# -*- coding: utf-8 -*-
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'github_spider'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/']

    def parse(self, response):
        pass
