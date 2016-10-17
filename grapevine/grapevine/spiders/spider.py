# -*- coding: utf-8 -*-
import scrapy


class GrapevineSpider(scrapy.Spider):
    name = "grapevine"
    allowed_domains = ["hanoigrapevine.com"]
    start_urls = (
        'http://www.hanoigrapevine.com/',
    )

    # parse the main page
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
            
            # return data to output file
            yield {
                'category_label' : category_label,
                'posts' : extracted_posts
            }

        category_links = response.css("ul.sub-menu li a::attr(href)").extract()
        for category_link in category_links:
            if category_link is not None:
                yield scrapy.Request(category_link, callback=self.parse_category)

    # parse the category page
    def parse_category(self, response):
        item_detail_links = response.css("div.item-details div.more-link-wrap a::attr(href)").extract()
        for item_detail_link in item_detail_links:
            if item_detail_link is not None:
                yield scrapy.Request(item_detail_link, callback=self.parse_article)

        page_nav_links = response.css("div.page-nav a::attr(href)").extract()
        for page_nav_link in page_nav_links:
            if page_nav_link is not None:
                yield scrapy.Request(page_nav_link, callback=self.parse_category)

    # parse artist page


    # parse calendar page


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
            # define header to set charset UTF-8 to the page
            html_header = '''<head>
                                <meta charset="UTF-8">
                            </head>'''
            # write to the html file for each article
            # need to encode the content because it's in html format
            f.write(u' '.join((html_header, output.get('content'))).encode('utf-8').strip())
        yield output

        # for the article has continue reading links
        continue_reading_links = output.get('continue_reading_links')
        for next_article_page in continue_reading_links:
            if next_article_page is not None:
                yield scrapy.Request(next_article_page, callback=self.parse_article)

        # go to related links
        links_in_sidebar = response.css("div.td-post-sidebar div.td_block_wrap div.td_block_inner div.td_mod_wrap div.item-details h3 a::attr(href)").extract()
        for link in links_in_sidebar:
            if link is not None:
                yield scrapy.Request(link, callback=self.parse_article)

        
