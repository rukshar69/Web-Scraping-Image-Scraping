# Web-Scraping-Shopify-Image-Scraping
Scraping a Shopify site named Techinstr to scrape product images

## Data Scraping

- Used Scrapy to scrape product data from [Techinstr](https://techinstr.myshopify.com/collections/all) shopify site. The spider is in [products.py](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/techinstr/techinstr/spiders/products.py). 
- Even though the website is javascript-enabled, by disabling the javascript, the website shows simple pagination. Since disabled javascript is Scrapy's default behavior, we can implement a simple pagination traversal in the spider code.
- The images are scraped using a custom [image pipeline](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/techinstr/techinstr/pipelines.py). The custom pipeline changes the saved images' filenames. The filenames are slugified versions of product titles. This slugification is done using Python's **slugify** library
- Necessary changes have been added in [settings.py](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/techinstr/techinstr/settings.py) to accommodate the custom image pipeline
- The downloaded images were 1000x1000 which is too large. We downsized the image size to 100x100 by adding **IMAGES_THUMBS** variable in the *settings.py*. 
- Overall there are about 130 products spread about 15 pages
- The csv file includes product **title, price, and image info. like image file path**

## Streamlit App



## Reference
- [Scrapy image pipeline documentation](https://docs.scrapy.org/en/latest/topics/media-pipeline.html)
- [YouTube vid: Download All Images and other Data -Python Scrapy New Easier Method using Python Scrapy](https://www.youtube.com/watch?v=2BsvriLQuOs) 
