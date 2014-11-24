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
                allow=('waterfall=(\d+)',)),
                callback='parse_item'
            ),
    )
    #some helper functions
    #wraps string returned from a regex in a selector and then strips html tags and applies a final regex
    #lazy way to ignore all the html entities that are in the waterfall template
    def _get_words(self, raw, regexp):
        try:
            return Selector(
                    text=raw[0]
                ).xpath('//text()').re(regexp)
        except IndexError:
            self.log('could not get words from: {0}'.format(str(raw)))

    def _get_latlng(self, raw):
        res = self._get_words(raw, '([\w|\.]+)')
        try:
            return (res[0], res[2],)
        except:
            return (None, None)
            
    def _get_type(self, raw):
        return ' '.join(self._get_words(raw, '(\w+)'))

    def _get_access(self, raw):
        try:
            return self._get_words(raw, '\w+')[1]
        except IndexError:
            return self._get_words(raw, '\w+')[0]

    def parse_item(self, response):
        self.log('waterfall found: %s ' % response.url)
        outer = response.xpath('//div[@class="span6"]')
        span3 =  outer.xpath('.//div[@class="span3"]')

        height, width = span3.re('(\d+)\xa0metres')
        lat, lng = self._get_latlng(span3.re('Coordinates:(.*)'))
        classification = self._get_type(span3.re('Classification:(.*)'))
        ownership = self._get_type(outer.re("Ownership(.*)"))
        accessibility  = self._get_access(outer.re('Accessibility -(.*)'))
        
        waterfall = WaterfallItem()

        waterfall['name'] =  outer.xpath('.//div[@class="span5"]/h3/text()').extract()[0]
        waterfall['lat'] = lat
        waterfall['lng'] = lng
        waterfall['classification_type'] = classification
        waterfall['height'] , waterfall['width']  = height, width
        waterfall['ownership'] = ownership # (public/priate)
        waterfall['accessibility'] = accessibility
        return waterfall
