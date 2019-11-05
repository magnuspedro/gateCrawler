# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import hashlib 
from ..items import AmericanasItem


class BotShoptimeSraper(scrapy.Spider):
    name = "botshoptime"
    allowed_domain = 'www.amazon.com.br'
    start_urls = [
        'https://www.submarino.com.br/busca/xiaomi',
    ]

    def parse(self, response):
        items = AmericanasItem()
        products = response.css('#content-middle .card-product')
        
        for product in products:
            
            product_name = product.css('.card-product-name::text').extract()
            price = product.css('.value+ .value::text').extract()
            link = products.css(
                '.card-product-url').xpath('@href').extract()
                        
            unique_code = hashlib.md5(product_name[0].encode())  
            items['code'] = unique_code.hexdigest()
            items['product'] = self.clear_text(product_name[0]) if product else ''
            items['price'] = price[0]
            items['link'] = self.clear_text(link[0]) if link else ''
            
            yield items    
        next_page = response.css('#content-middle li:nth-child(10) a').xpath('@href').extract_first()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def clear_text(self, text):
        return text.replace('  ', '').replace('\n', '').replace('R$','')

    # def options_parse(self, response):
    #     asin = response.url.split('/')
    #     price = response.css('.olpOfferPrice::text').extract()
    #     shipping = response.css(
    #         '.a-color-secondary :nth-child(1)::text').extract()
    #     color = response.css('#variationsTwister .a-text-bold::text').extract()
    #     next_page = response.css('.a-last a').xpath('@href').extract_first()

    #     yield {
    #         'asin': asin.pop(),
    #         'price': price,
    #         'shipping': shipping,
    #         'color': color,
    #     }
    #     if next_page is not None:
    #         yield response.follow(next_page, callback=self.options_parse)

