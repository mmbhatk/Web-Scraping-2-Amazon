import scrapy
from ..items import AmazonbooksItem

class AmazonBooks(scrapy.Spider):

    name = "amazonbooks"
    start_urls = ['https://www.amazon.in/Books-Last-30-days/s?rh=n%3A976389031%2Cp_n_publication_date%3A2684819031']
    item = AmazonbooksItem()
    next_page_number = 2

    def parse(self, response):
        all_divs = response.css('.s-latency-cf-section')
        
        for book in all_divs:
            AmazonBooks.item['title'] = book.css('.a-color-base.a-text-normal::text').get()
            AmazonBooks.item['author'] = book.css('.a-color-secondary .a-size-base+ .a-size-base::text').get()
            AmazonBooks.item['price'] = book.css('.a-spacing-top-small .a-price-whole::text').get()    
            AmazonBooks.item['image_link'] = book.css('.s-image-fixed-height img::attr(src)').get()
            AmazonBooks.item['page_number'] = AmazonBooks.next_page_number - 1
            yield AmazonBooks.item

        next_page = 'https://www.amazon.in/Books-Last-30-days/s?i=stripbooks&rh=n%3A976389031%2Cp_n_publication_date%3A2684819031&page=' + str(AmazonBooks.next_page_number) + '&qid=1589131922&ref=sr_pg_2'

        if AmazonBooks.next_page_number < 75:
            AmazonBooks.next_page_number += 1
            print("--------------------" + AmazonBooks.next_page_number + "----------------------")
            yield response.follow(next_page, callback = self.parse)