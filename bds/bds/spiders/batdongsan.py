# -*- coding: utf-8 -*-
import scrapy
import pymongo
from bds.items import Property
from bds.items import Project

nha_dat_ban = "nha-dat-ban"
nha_dat_cho_thue = "nha-dat-cho-thue"
du_an_bat_dong_san = "du-an-bat-dong-san"

# to remove all special character out of the text
def clean_text(text):
    cleaned_text = ""
    if text is not None:
        cleaned_text = text.replace('\n', '').replace('\r', '').strip()
    return cleaned_text

class BatdongsanSpider(scrapy.Spider):
    name = "batdongsan"
    # allowed_domains = ["batdongsan.com.vn"]
    
    # custom_settings = {
    #     "DOWNLOAD_DELAY" : 1.35,
    # }
    
    start_urls = (
        'http://www.batdongsan.com.vn/nha-dat-ban',
        'http://www.batdongsan.com.vn/nha-dat-cho-thue',
        'http://www.batdongsan.com.vn/du-an-bat-dong-san',
    )

    def parse(self, response):
        page = response.url.split("/")[-1]
        
        if page == nha_dat_ban or page == nha_dat_cho_thue:
            property_detail_url = response.css("div.vip0.search-productItem div.p-title a::attr(href)").extract()
            
            for relative_url in property_detail_url:
                if relative_url is not None:
                    url = response.urljoin(relative_url)
                    yield scrapy.Request(url, callback=self.parse_property)
        
        elif page == du_an_bat_dong_san:
            project_items = response.css("div.prj-items")
            project_details_links = project_items.css("ul li div.below-img div.prj-name a::attr(href)").extract()
        
            for project_link in project_details_links:
                if project_link is not None:
                    yield scrapy.Request(response.urljoin(project_link), callback=self.parse_project)
        
    def parse_property(self, response):
        product_detail = response.css("div#product-detail")
        title = product_detail.css("div.pm-title h1::text").extract_first()
        more_details = product_detail.css("div.kqchitiet span span strong::text").extract()
        project_url = product_detail.css("span.diadiem-title a::attr(href)").extract_first()
        origin_id = product_detail.css("div.pm-content.stat::attr(cid)").extract_first()
        
        features = response.css("div.left-detail div div.right::text").extract()
        created_date = features[4]
        
        property = Property(
                        url = response.url,
                        project_url = response.urljoin(project_url),
                        title = clean_text(title), 
                        price = clean_text(more_details[0]),
                        square = clean_text(more_details[1]),
                        origin_id = clean_text(origin_id),
                        created_date = clean_text(created_date)
                    )
        yield property
        
    def parse_project(self, response):
        project_details = response.css("div.prj-detail")
        project_name = project_details.css("h1::text").extract_first()
        project_other_name = project_details.css("span.prj-othername::text").extract_first()

        project = Project(
                    url = response.url,
                    other_name = clean_text(project_other_name),
                    name = clean_text(project_name)
                )
                
        yield project
        
        