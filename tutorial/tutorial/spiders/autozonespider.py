import scrapy
from scrapy import log
import json


class AutoZoneZoneSpider(scrapy.Spider):
    name = 'wwwautozonecom'
    allowed_domains = ['autozone.com', 'www.autozone.com']
    base_url = 'https://{0}'.format(allowed_domains[1])
    store_search_url = (
        '{0}/rest/bean/autozone/diy/storelocator/StoreLocatorTools/'
        'findNearestLocationsByPlace?atg-rest-depth=1'.format(base_url)
    )

    def start_requests(self):
        body_data = 'arg1=95370&arg2=true'
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        import ipdb; ipdb.set_trace()
        yield scrapy.Request(
            self.store_search_url,
            headers=headers,
            method='POST',
            callback=self.parse_search_result,
            body=body_data,
            dont_filter=True
        )

    def parse_search_result(self, response):
        if response.status == 204:
            zone = response.meta['zip_code']
            log.msg('ZONE {0} IS INVALID'.format(zone), level=log.ERROR)
            log.msg('STATUS CODE 204: NO CONTENT', level=log.ERROR)
            return
        import ipdb;
        ipdb.set_trace()
        store_data = json.loads(response.body).get('locList')
        store_number = store_data[0].get('storeNum')
        print(store_number)
