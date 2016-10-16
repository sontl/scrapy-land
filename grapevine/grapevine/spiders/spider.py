# -*- coding: utf-8 -*-
import scrapy


class GrapevineSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["hanoigrapevine.com"]
    start_urls = (
        'http://www.hanoigrapevine.com/',
    )

    def parse(self, response):
        for category_block in response.css("div.td_block_wrap"):
            category_label = category_block.css("h4.block-title a::text").extract_first()
            
            posts = category_block.css("div.td_mod5")
            extracted_posts = []
            for post in posts:
                extracted_post = {
                    'thumbnail' : post.css("div.td_mod5 div.thumb-wrap a img.entry-thumb::attr(src)").extract_first(),
                    'title' : post.css("h3.entry-title a::text").extract_first(),
                    'created_date' : post.css("div.meta-info time::text").extract_first(),
                    'text_excerpt' : post.css("div.td-post-text-excerpt::text").extract_first(),
                }
                extracted_posts.append(extracted_post)
            yield {
                'category_label' : category_label,
                'posts' : extracted_posts
            }
        
        
