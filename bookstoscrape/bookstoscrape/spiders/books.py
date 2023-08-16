import scrapy; import re
from scrapy.linkextractors import LinkExtractor
from bookstoscrape.items import BookstoscrapeItem

def find_element_with_parentheses(lst):
    for element in lst:
        if '(' in element and ')' in element:
            return element
    return None

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['http://books.toscrape.com']

    # custom_settings = {
    #     "IMAGES_STORE": "my_images"
    # }

    def parse(self, response):
        for book in response.css('h3 a::attr(href)'):
            book_url = response.urljoin(book.extract())
            yield scrapy.Request(book_url, callback=self.parse_book)

        next_page = response.css('.next a::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    
    def parse_book(self, response):
        #Get availability info
        availability_strings = response.css('.instock.availability::text').extract()
        instock_str = find_element_with_parentheses(availability_strings).strip() if availability_strings else None
        instock_number  = re.search(r'\d+', instock_str).group() if instock_str else None


        #Get Price info
        price_with_pound = response.css('.price_color::text').extract_first()
        price = price_with_pound.replace('£', '') if price_with_pound else None
        
        #Get Rating info
        rating_text = response.css('.star-rating::attr(class)').re_first(r'star-rating ([A-Za-z]+)')
        rating_mapping = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5,
        }
        rating = rating_mapping.get(rating_text, None)

        img_links=[]
        for img in response.css('.thumbnail img::attr(src)').getall():
            img_links.append(response.urljoin(img))
            
        item = BookstoscrapeItem()
        item['title'] = response.css('h1::text').extract_first()
        item['price'] = price
        item['availability']=instock_number
        item['rating'] = rating 
        item['genre'] = response.css(".breadcrumb li:nth-child(3) a::text").extract_first(),
        item['image_urls'] = img_links
        yield item
