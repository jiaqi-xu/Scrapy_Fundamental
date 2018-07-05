# -*- coding: utf-8 -*-
import scrapy
from tmallspider.items import TmallGoodsItem
from scrapy.pipelines import images

class TmallSpider(scrapy.Spider):
    name = 'tmall_spider'
    allowed_domains = ['www.tmall.com/']
    start_urls = ['https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.4.4aa3d905RKuMMl&cat=50025135&q=%C5%AE%D7%B0&sort=d&style=g&from=mallfp..pc_1_searchbutton']

    #记录处理的页数
    count = 0

    def parse(self, response):

        TmallSpider.count += 1
        divs = response.xpath('//div[@id="J_ItemList"]//div[@class="product-iWrap"]')
        for div in divs:
            item = TmallGoodsItem()
            item['GOODS_PRICE'] = div.xpath('p[@class="productPrice"]/em/@title')[0].extract()
            item['GOODS_NAME'] = div.xpath('p[@class="productTitle"]/a/@title')[0].extract()
            pre_goods_url = div.xpath('p[@class="productTitle"]/a/@href')[0].extract()
            item['GOODS_URL'] = pre_goods_url if "http:" in pre_goods_url else ("http:" + pre_goods_url)

            # Picture Url
            try:
                import ipdb; ipdb.set_trace()
                picture_url = div.xpath('//div[@class="productImg-wrap"]/a/img/@src')[0].extract()
                # have to be a list of pircture urls
                item['PICTURE_URL'] = ['http:' + picture_url]
            except Exception, e:
                print 'ERROR:', e

            yield scrapy.Request(
                url=item['GOODS_URL'], meta={'item':item}, callback=self.parse_detail,
                dont_filter=True
            )

            break # avoid getting block, just crawl one product

    def parse_detail(self, response):
        div = response.xpath('//div[@class="slogo"]/a[@class="slogo-shopname"]')
        if not div:
            self.log('List page error %s'%response.url)

        item = response.meta['item']
        item['SHOP_NAME'] = div.xpath('.//text()')[0].extract()
        pre_shop_url = div.xpath('@href')[0].extract()
        item['SHOP_URL'] = pre_shop_url if "http:" in pre_shop_url else ("http:" + pre_shop_url)
        yield item
