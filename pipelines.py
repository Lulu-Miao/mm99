# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re


class Mm99Pipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder = item['name']
        folder_strip = strip(folder)
        #  'url': 'http://fj.kanmengmei.com/2018/2869/23-m4.jpg'
        splits = request.url.split('/')
        if re.match('^\d{1,2}-.*', splits[-1]):
            image_guid = splits[-3] + '-' + splits[-2] + '-' + splits[-1][:splits[-1].find('-')] + splits[-1][splits[-1].rfind('.'):]
        else:
            image_guid = splits[-3] + '-' + splits[-2] + '-' + splits[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        return filename

    def get_media_requests(self, item, info):
        yield Request(item['url'], meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

def strip(path):
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path

