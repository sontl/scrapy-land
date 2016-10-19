# -*- coding: utf-8 -*-
import scrapy
from Property import *

nha_dat_ban = "nha-dat-ban"
nha_dat_cho_thue = "nha-dat-cho-thue"
du_an_bat_dong_san = "du-an-bat-dong-san"

class BatdongsanSpider(scrapy.Spider):
    name = "batdongsan"
    allowed_domains = ["batdongsan.com.vn"]
    
    custom_settings = {
        "DOWNLOAD_DELAY" : 1.35     
    }
    
    start_urls = (
        'http://www.batdongsan.com.vn/nha-dat-ban',
        'http://www.batdongsan.com.vn/nha-dat-cho-thue',
        'http://www.batdongsan.com.vn/du-an-bat-dong-san',
    )

    def parse(self, response):
        page = response.url.split("/")[-1]
        property_detail_url = response.css("div.vip0.search-productItem div.p-title a::attr(href)").extract()
        for relative_url in property_detail_url:
            if relative_url is not None:
                url = response.urljoin(relative_url)
            
                if page == nha_dat_ban or page == nha_dat_cho_thue:
                    yield scrapy.Request(url, callback=self.parse_property)
                else:
                    yield scrapy.Request(url, callback=self.parse_project)
        
    def parse_property(self, response):
        product_detail = response.css("div#product-detail")
        title = product_detail.css("div.pm-title h1::text").extract_first()
        more_details = product_detail.css("div.kqchitiet span span strong::text").extract_first()
        property = Property(title=title, price=more_details)
        yield  
            dict(property)
        }
        
        
    def parse_project(self, response):
        pass