import scrapy 

class LandSpider(scrapy.Spider):
    name = 'Land Spider'
    start_urls = ['http://batdongsan.com.vn']

    def parse(self, response):
        menu_nha_dat_ban = response.css("div#page-navigative-menu ul li.lv0 a::attr(href)").extract()
        
        for title in responsemenu_nha_dat_ban:
            yield {'title': title.css('a ::text').extract_first()}

        next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
 
        
  