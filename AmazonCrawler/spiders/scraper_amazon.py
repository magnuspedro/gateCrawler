# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ..items import AmazoncrawlerItem
import hashlib 


class BotAmazonSraper(scrapy.Spider):
    name = "botamazon"
    allowed_domain = 'www.amazon.com.br'
    start_urls = [
        'https://www.amazon.com.br/xiaomi-Celulares-e-Smartphones-Desbloqueados-Comunica%C3%A7%C3%A3o/s?k=xiaomi&i=electronics&rh=n%3A16243890011%2Cp_n_condition-type%3A13862762011&dc&pf_rd_i=16243890011&pf_rd_m=A3RN7G7QC5MWSZ&pf_rd_p=0838205f-62f8-4999-8714-b5d906838dae&pf_rd_r=45JZZE4N8SCBEE5TWWSE&pf_rd_s=merchandised-search-5&pf_rd_t=101&qid=1564689920&rnid=13862761011&ref=sr_nr_p_n_condition-type_1',
    ]

    def parse(self, response):
        items = AmazoncrawlerItem()
        all_products = response.css('.s-result-item')
        for products in all_products:
            product = products.css('.a-color-base.a-text-normal::text').extract()
            price = products.css('.a-price-whole::text').extract()
            shipping = products.css(
                '.s-align-children-center span::text').extract()
            small_price = products.css(
                '.a-color-secondary .a-color-base::text').extract()
            link = products.css(
                '.a-color-secondary .a-link-normal').xpath('@href').extract()
            
            unique_code = hashlib.md5(product[0].encode())  
            items['code'] = unique_code.hexdigest()
            items['product'] = self.clear_text(product[0]) if product else ''
            items['price'] = self.clear_text(price[0]) if price else ''
            items['shipping'] = self.clear_text(shipping[0]) if shipping else ''
            items['small_price'] = self.clear_text(small_price[0]) if small_price else ''
            items['link'] = self.clear_text(link[0]) if link else ''
            
            yield items    
        next_page = response.css('.a-last a').xpath('@href').extract_first()

        
        

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

