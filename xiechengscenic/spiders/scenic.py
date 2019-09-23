# -*- coding: utf-8 -*-
import scrapy
from xiechengscenic.items import XiechengscenicItem


class ScenicSpider(scrapy.Spider):
    name = 'scenic'
    allowed_domains = ['ctrip.com']
    id = 0
    page = 1
    base_urls = 'http://you.ctrip.com/sight/guangzhou152/s0-p{}.html'
    start_urls = [base_urls.format(str(page))]

    def parse(self, response):
        base_url = 'https://piao.ctrip.com/ticket/dest/'
        node_list = response.xpath('//div[@class="list_mod2"]')
        for node in node_list:
            self.id += 1
            item = XiechengscenicItem()
            item['preview'] = node.xpath('.//a/img/@src').extract()[0]
            item['id'] = self.id
            url_1 = node.xpath('.//a/@href').extract()[0]
            num = url_1.split("/")[-1]
            url = base_url + 't' + num

            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_info)

    def parse_info(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//h2[@data-reactid="38"]/text()').extract()[0]
        item['location'] = response.xpath('//li[1]/span/text()').extract()[0]
        item['score'] = float(response.xpath('//div[@class="score"]/span/i[@class="num"]/text()').extract()[0])
        item['spot_introduction'] = response.xpath('//div[3][@class="content-wrapper"]').extract()[0]
        item['traffic_information'] = response.xpath('//div[@class="traffic-content"]').extract()[0]

        yield item

        if self.page <= 10:
            self.page += 1
            yield scrapy.Request(self.base_urls.format(str(self.page)), callback=self.parse)
        else:
            pass

