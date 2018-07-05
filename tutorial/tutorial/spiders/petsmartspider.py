import scrapy
from scrapy import log
import json

class PetSmartZoneSpider(scrapy.Spider):
    name = 'wwwpetsmartcom'
    allowed_domains = ['petsmart.com', 'www.petsmart.com']
    cookie_names = ['StoreCookie']
    download_delay = 0.1
    base_url = 'https://{0}'.format(allowed_domains[1])
    store_search_url = (
        '{0}/on/demandware.store/Sites-PetSmart-Site/default'
        '/StoreLocator-GetNearestStores'.format(base_url)
    )

    def start_requests(self):
        body_data = 'dwfrm_storelocator_postalCode=95370&searchradius=20' \
                    '&dwfrm_storelocator_distanceUnit=mi' \
                    '&dwfrm_storelocator_countryCode=US' \
                    '&dwfrm_storelocator_findbyzip=Search'
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
        import ipdb; ipdb.set_trace()
        store_data = json.loads(response.body)['storeData']['stores']
        store_number = store_data[0]['ID']
