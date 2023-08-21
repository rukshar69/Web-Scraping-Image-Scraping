import scrapy
from quotefancy.items import QuotefancyItem


class QuoteImages2Spider(scrapy.Spider):
    name = "quote_images_2"
    allowed_domains = ['quotefancy.com']
    start_urls = ['https://quotefancy.com/motivational-quotes']

    async def close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

    def parse(self, response):
        yield scrapy.Request(response.url, callback=self.parse_quotes,
                             meta={
                                    "playwright": True,
                                    "playwright_include_page": True
                                },
                            errback=self.close_page)

    async def parse_quotes(self, response):
        page = response.meta['playwright_page']

        #GET IMAGE URLS
        #This query only returns the first image
        rel_img_urls =[]; first_url = response.xpath('//img/@src').get(); rel_img_urls.append(first_url)
        #This returns all other images
        rel_secondary_urls = response.css('img').xpath('@data-original').getall()
        rel_img_urls.extend(rel_secondary_urls)

        #GET AUTHOR QUOTE UPVOTE DOWNVOTE   
        quotes = response.xpath('//a[@class="quote-a"]/text()').getall()
        authors = response.xpath('//p[@class="author-p"]/a/text()').getall()
        upvotes = response.xpath('//p[contains(@id,"upvotes")]/text()').getall()
        downvotes = response.xpath('//p[contains(@id,"downvotes")]/text()').getall()

        for i in range(len(quotes)):
            item = QuotefancyItem()
            item['quote'] = quotes[i]; item['author'] = authors[i]
            item['image_urls'] = [rel_img_urls[i]]
            item['upvotes'] = upvotes[i]
            item['downvotes'] = downvotes[i]
            yield item

        # item = QuotefancyItem()
        # item['quote'] = quotes; item['author'] = authors
        # item['image_urls'] = rel_img_urls
        # item['upvotes'] = upvotes
        # item['downvotes'] = downvotes
        

        await page.close()
        # yield item

        next_page = response.xpath('//a[@class="loadmore page-next"]/@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_quotes,
                                 meta={
                                    "playwright": True,
                                    "playwright_include_page": True
                                },
                                errback=self.close_page)