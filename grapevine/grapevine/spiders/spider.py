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
                    'link_to_article' : post.css("h3.entry-title a::attr(href)").extract_first()
                }
                extracted_posts.append(extracted_post)
                # follow links to article
                next_article_page = extracted_post.get('link_to_article')
                if next_article_page is not None:
                    yield scrapy.Request(next_article_page, callback=self.parse_article)
            
            yield {
                'category_label' : category_label,
                'posts' : extracted_posts
            }

    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()
        
        article = response.css('article')

        output = {
            'id' : response.css('article::attr(id)').extract_first(),
            'title' : article.css('header h1::text').extract_first(),
            'category' : article.css('header div ul li a::text').extract(),
            'posted_on' : article.css('header div time::text').extract_first(),
            'comment_count' : article.css('header div.meta-info div.entry-comments-views::text').extract_first(),
            'content' : article.css('div.td-post-text-content').extract_first(),
            'continue_reading_links' : article.css('div.td-post-text-content div.main-post-list div#latest-posts p.entry-summary a::attr(href)').extract()
        }

        filename = 'article-%s.html' % output.get('id')
        with open(filename, 'wb') as f:
            html_header = '''<head>
                                <meta charset="UTF-8">
                            </head>'''
            f.write(u' '.join((html_header, output.get('content'))).encode('utf-8').strip())
        yield output

        continue_reading_links = output.get('continue_reading_links')
        for next_article_page in continue_reading_links:
            if next_article_page is not None:
                yield scrapy.Request(next_article_page, callback=self.parse_article)

        
        
