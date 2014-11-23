# -*- coding: utf-8 -*-

import scrapy
from creep.items import WaterfallItem
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector





class WaterfallsHamiltonSpider(CrawlSpider):
    name = "waterfalls_hamilton"
    allowed_domains = ["waterfalls.hamilton.ca"]
    start_urls = (
        'http://www.waterfalls.hamilton.ca/default.asp?sort=1',
        'http://www.waterfalls.hamilton.ca/default.asp?sort=2',
        'http://www.waterfalls.hamilton.ca/default.asp?sort=3',

    )
    rules = (

    Rule(
        LinkExtractor(
            allow=('default.asp?waterfall=(\w+)',)),
            callback='parse_item'),
    )

    def _get_words(self, raw, regexp):
        return Selector(
                body=raw[0]
            ).xpath('//text()').re(regexp)

    def _get_latlng(self, raw):
        res = self._get_words(raw, '([\w|\.]+)')
        return (res[0], res[2],)

    def _get_type(self, raw):
        return ' '.join(self._get_words(raw, '(\w+)'))

    def parse_item(self, response):
        self.log('waterfall found: %s ' % response.url)
        outer = response.xpath('//div[@class="span6"]')
        span3 =  outer.xpath('.//div[@class="span3"]')

        height, width = span3.re('(\d+)\xa0metres')
        lat, lng = self._get_latlng(span3.re('Coordinates:(.*)'))
        classification = self._get_type(span3.re('Classification:(.*)'))

        ownership = self._get_type(outer.re("Ownership(.*)"))
        accessibility  = self._get_access(outer.re('Accessibility -(\w+)'))
        #output
        waterfall = WaterfallItem()

        waterfall['name'] =  outer.xpath('.//div[@class="span5"]/h3/text()').extract()
        waterfall['lat'] = lat
        waterfall['lng'] = lng
        waterfall['classification_type'] = classification
        waterfall['height'] , waterfall['width']  = height, width
        waterfall['ownership'] = ownership # (public/priate)
        waterfall['accessibility'] = accessibility

