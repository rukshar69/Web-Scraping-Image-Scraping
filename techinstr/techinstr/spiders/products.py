import scrapy
from techinstr.items import ProductItem  # Import your Item class from items.py


class ProductsSpider(scrapy.Spider):
    name = "products"
    custom_settings = {
        #'LOG_LEVEL': 'INFO',  # Set the log level to INFO to reduce terminal output
        #'CONCURRENT_REQUESTS': 8,  # Adjust the number of concurrent requests
        #'DOWNLOAD_DELAY': 1,  # Add a delay between requests
    }

    start_urls = ['https://techinstr.myshopify.com/collections/all']

    def parse(self, response):
        for link in response.xpath('//*[contains(@class,"product-card")]/a/@href').getall():
            yield response.follow(link, callback=self.parse_product)
            #print(link)
        
        next_link = response.xpath('//span[contains(text(),"Next page")]/../@href').get()
        if next_link:
            yield response.follow(next_link)

    def parse_product(self, response):
        img_links=[]
        for img in response.xpath('//*[@id="FeaturedImage-product-template"]/@src').getall():
            img_links.append(response.urljoin(img))

        #Get Price info
        price_with_pound = response.xpath('normalize-space(//*[contains(@class,"price-item--regular")]/text())').get()
        price = price_with_pound.replace('£', '') if price_with_pound else None
            
        item = ProductItem()
        item['title'] = response.xpath('normalize-space(//h1/text())').get()
        item['price'] = price
        item['image_urls'] = img_links
        yield item
        
        # yield {
        #     'title': response.xpath('normalize-space(//h1/text())').get(),
        #     'price': response.xpath('normalize-space(//*[contains(@class,"price-item--regular")]/text())').get(),
        #     'image_urls': img_links,
        #     'Link': response.url
        # }