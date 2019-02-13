# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6
import requests
from parsel import Selector

class GoogleMerchantFeed:
    '''Фид для Google Merchant'''
    #url = 'https://marko.biz.ua/google_merchant_center.xml?hash_tag=63112d878cb232b7c77baadf6c68b955&product_ids=&group_ids=24728881&label_ids='
    url = 'https://marko.biz.ua/google_merchant_center.xml?hash_tag=63112d878cb232b7c77baadf6c68b955&product_ids=&group_ids=&label_ids=1197755'
    def __init__(self, gid, title, description, link, price, availability, image, mpn, brand):
        self.gid = gid
        self.title = title
        self.description = description
        self.link = link
        self.price = price
        self.availability = availability
        self.image = image
        self.mpn = mpn
        self.brand = brand
    
    def __repr__(self):
        return self.title
    
# Парсинг данных и сохранение в класс GoogleMerchantFeed
r = requests.get(GoogleMerchantFeed.url)
r.encoding = 'utf-8'
r = r.text
hub = []
sel = Selector(text=r, type='xml')
items = sel.xpath('//item')
for item in items:
    gid = item.xpath('./*[name()="g:id"]/text()').get()
    title = item.xpath('./*[name()="g:title"]/text()').get()
    description = item.xpath('./*[name()="g:description"]/text()').get().split('Основные размеры:')[0]
    link = item.xpath('./*[name()="g:link"]/text()').get()
    price = item.xpath('./*[name()="g:price"]/text()').get()
    availability = item.xpath('./*[name()="g:availability"]/text()').get()
    image = item.xpath('./*[name()="g:image_link"]/text()').get()
    brand = item.xpath('./*[name()="g:brand"]/text()').get()
    mpn = 'mpn'
    hub.append(GoogleMerchantFeed(gid, title, description, link, price, availability, image, mpn, brand))

# Запись данных в файл
my_file = open('google.xml', 'w')
my_file.write('<?xml version="1.0"?>\n<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">\n<channel>\n<title>Интернет-магазин «Марко»</title>\n<link>https://marko.biz.ua</link>\n<description>RSS 2.0 product data feed</description>\n')
for item in hub:
    my_file.write('<item>\n')
    my_file.write('<g:id>'+item.gid+'</g:id>\n')
    my_file.write('<g:title>'+item.title+'</g:title>')
    my_file.write('<g:description>'+item.description+'</g:description>\n')
    my_file.write('<g:link>'+item.link+'</g:link>\n')
    my_file.write('<g:image_link>'+item.image+'</g:image_link>\n')
    my_file.write('<g:condition>new</g:condition>\n')
    my_file.write('<g:availability>'+item.availability+'</g:availability>\n')
    my_file.write('<g:price>'+item.price+'</g:price>\n')
    my_file.write('<g:brand>'+item.brand+'</g:brand>\n')
    my_file.write('<g:mpn>'+item.mpn+'</g:mpn>\n')
    my_file.write('<g:product_type>Постельное белье</g:product_type>\n')
    my_file.write('<g:google_product_category>4171</g:google_product_category>\n')
    my_file.write('</item>\n')
my_file.write('</channel>\n</rss>')
my_file.close()
