# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import scrapy

from scrapy_splash import SplashRequest
from mm99.items import Mm99Item


class A99mmSpider(scrapy.Spider):
    name = '99mm'
    allowed_domains = ['99mm.me']
    start_urls = ['http://www.99mm.me/xinggan/']

    def parse(self, response):
        for href in response.xpath('//*[@id="piclist"]/li/dl/dt/a/@href'):
            yield SplashRequest(url=response.urljoin(href.extract()), callback=self.parse_suite_page,
                                args={'wait': 1}, endpoint='render.html')

        if response.url in self.start_urls:
            max_page = int(response.xpath(r'//div[@class="page"]//a[@class="all"]/text()').extract_first()[3:])
            page_url_pattern = response.xpath(r'//div[@class="page"]//a[@class="all"]/@href').extract_first()
            for page_index in range(2, max_page+1):
                # <a href="mm_3_7.html">7</a>
                url = page_url_pattern
                url = url[:url.rindex('_') + 1] + str(page_index) + url[url.rindex('.'):]
                yield SplashRequest(url=response.urljoin(url), callback=self.parse,
                                    args={'wait': 1}, endpoint='render.html')

    def parse_suite_page(self, response):
        item = Mm99Item()
        item['name'] = response.xpath('//div[@class="title"]//h2/text()').extract_first()
        item['url'] = response.xpath('//div[@id="picbox"]//img/@src').extract_first()
        item['page_url'] = response.url
        yield item

        if response.url.find('?') == -1:
            max_page = int(response.xpath(r'//div[@class="page"]//a[@class="all"]/text()').extract_first()[3:])
            page_url_pattern = response.xpath(r'//div[@class="page"]//a[@class="all"]/@href').extract_first()
            for page_index in range(2, max_page+1):
                # <a href="/qingchun/2923.html?url=2">2</a>
                url = page_url_pattern
                url = url[:url.rindex('=') + 1] + str(page_index)
                yield SplashRequest(url=response.urljoin(url), callback=self.parse_suite_page,
                                    args={'wait': 1}, endpoint='render.html')
