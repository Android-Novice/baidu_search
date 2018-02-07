import random

import re
import urllib
import urllib.request
import requests
import scrapy
from baidu_search.items import BaiduSearchItem
from baidu_search.settings import USER_AGENTS
from scrapy import Request

class BaiduSpider(scrapy.Spider):
    name = 'baidu_search'
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }
    firstUrl = 'https://www.baidu.com/s?wd=%s&oq=%s'
    otherUrl = 'https://www.baidu.com/s?wd=%s&pn=%d&oq=%s'
    pageIndex = 0
    searchNoneCount = 0
    key_word = ''
    imgIndex = 0

    def start_requests(self):
        url = self.firstUrl % (self.key_word, self.key_word)
        yield Request(url, headers=self.headers, dont_filter=True)

    def parse(self, response):
        try:
            hrefElems = response.xpath('//h3[@class="t"]/a/@href')
            if len(hrefElems) > 0:
                for elem in hrefElems:
                    old_url = elem.extract()
                    src_url = self.getDirectUrl(old_url)
                    yield Request(src_url, headers=self.headers, callback=self.parse_other)
                self.pageIndex += 1
                next_url = self.otherUrl % (self.key_word, self.pageIndex, self.key_word)
                yield Request(next_url, headers=self.headers)
        except:
            pass

    def parse_other(self, response):
        imgElems = response.xpath('//img')
        if len(imgElems):
            for elem in imgElems:
                original_url = elem.xpath('@data-original').extract()
                if not original_url:
                    original_url = elem.xpath('@data-actualsrc').extract()
                    if not original_url:
                        original_url = elem.xpath('@data-src').extract()
                        if not original_url:
                            original_url = elem.xpath('@src').extract()
                if original_url:
                    original_url = self.filter_url(original_url[0], response.url)
                    if original_url:
                        self.imgIndex += 1
                        item = BaiduSearchItem()
                        item['index'] = self.imgIndex
                        item['url'] = original_url
                        item['web_url'] = response.url
                        yield item

        bodyElem = response.xpath('//body')
        if len(bodyElem):
            urlElems = bodyElem[0].xpath('//a')
            for urlElem in urlElems:
                url = urlElem.xpath('@data-href').extract()
                if not url:
                    url = urlElem.xpath('@href').extract()
                    if url:
                        url = self.filter_url(url[0], response.url)
                        yield Request(url, headers=self.headers, callback=self.parse_other)

    def filter_url(self, img_url, response_url):
        if img_url:
            if img_url.startswith('//'):
                img_url = 'http:' + img_url
            elif not img_url.startswith('http'):
                proto, rest = urllib.request.splittype(response_url)
                host, rest = urllib.request.splithost(rest)
                if host != None:
                    img_url = host + img_url
                    if not img_url.startswith('http'):
                        img_url = 'http://' + img_url
                else:
                    return None
        return img_url

    def getDirectUrl(self, redirectUrl):
        try:
            tmpPage = requests.get(redirectUrl, allow_redirects=False)
            if tmpPage.status_code == requests.codes.ok:
                ##此处代码有待验证，目前还没有进到这个里面，应该有问题；
                pageText = tmpPage.text.encode('utf-8')
                urlMatch = re.search(r'URL=\'(.*?)\'', tmpPage.text.encode('utf-8'), re.S)
                raise Exception('活捉验证码200的网页一个: ' + redirectUrl)
                # return urlMatch.group(1)
                # print(pageText)
            elif tmpPage.status_code == 302:
                directUrl = tmpPage.headers.get('location')
                print(directUrl)
                return directUrl
            return redirectUrl
        except Exception as error:
            print('********getDirectUrl error: ' + str(error))
        return None
