# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import datetime
from baidu_search import settings
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class BaiduSearchPipeline(object):
    def process_item(self, item, spider):
        return item

class DownloadImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        url = item['url']
        if not url.endswith('.php'):
            name = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S')
            index = str(item['index'])
            name = name + '_' + index + '.jpg'
            item['img_name'] = name
            yield Request(url, meta={'name': name, 'dir': 'Full'})
        else:
            raise DropItem('valid img url:' + url)

    def item_completed(self, results, item, info):
        for ok, x in results:
            if ok:
                item['save_path'] = os.path.join(settings.IMAGES_STORE, x['path'])
                return item
            else:
                print('Download Error: ' + str(item))
                print(x)
                raise DropItem('download error:')

    def file_path(self, request, response=None, info=None):
        name = request.meta['name']
        return name

class RecorderPipeline(object):
    def __init__(self):
        self.file = open('download_list.dat', 'wb')

    def process_item(self, item, spider):
        line = '%s:   %s 【%s】' % (item['img_name'], item['url'], item['web_url']) + '\n'
        self.file.write(line.encode('utf-8'))
        return item
