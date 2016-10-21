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
        page = response.url.split("/")
        
        if nha_dat_ban in page or nha_dat_cho_thue in page:
            property_detail_url = response.css("div.vip0.search-productItem div.p-title a::attr(href)").extract()
            
            for relative_url in property_detail_url:
                if relative_url is not None:
                    url = response.urljoin(relative_url)
                    yield scrapy.Request(url, callback=self.parse_property)
                    
            # to crawl the next page
            next_urls = response.css("div.background-pager-right-controls a::attr(href)").extract()
            for next_url in next_urls:
                if next_url is not None:
                    url = response.urljoin(next_url)
                    yield scrapy.Request(url, callback=self.parse)
        
        elif du_an_bat_dong_san in page:
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
        content = product_detail.css("div.pm-content").extract_first()
        features = response.css("div.left-detail div div.right::text").extract()
        address = features[1]
        post_type = features[3]
        created_date = features[4]
        expiry_date = features[5]
        
        contact_name = response.css("div#LeftMainContent__productDetail_contactName div.right::text").extract_first()
        contact_mobile = response.css("div#LeftMainContent__productDetail_contactMobile div.right::text").extract_first()
        contact_phone = response.css("div#LeftMainContent__productDetail_contactPhone div.right::text").extract_first()
        contact_email = response.css("div#LeftMainContent0e05fc061426e8ce153b00323aad41525656ab3b__productDetail_contactEmail div.right::text").extract_first()
        contact_address = response.css("div#LeftMainContent__productDetail_contactAddress div.right::text").extract_first()
        contact_info = {
            "name" : clean_text(contact_name),
            "address" : clean_text(contact_address),
            "mobile_no" : clean_text(contact_mobile),
            "phone" : clean_text(contact_phone),
            "email" : clean_text(contact_email)
        }
        
        similar_product_list = response.css("div#lstProductSimilar div div.p-title a::attr(href)").extract()
        for similar_product_url in similar_product_list:
            if similar_product_url is not None:
                yield scrapy.Request(response.urljoin(similar_product_url), callback=self.parse_property)
        
        property = Property(
                        url = response.url,
                        project_url = response.urljoin(project_url),
                        title = clean_text(title), 
                        price = clean_text(more_details[0]),
                        square = clean_text(more_details[1]),
                        origin_id = clean_text(origin_id),
                        created_date = clean_text(created_date),
                        expiry_date = clean_text(expiry_date),
                        post_type = clean_text(post_type),
                        address = clean_text(address),
                        contact_info = contact_info,
                        content = content
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
        
        