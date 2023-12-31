# Web-Scraping-Image-Scraping

## Techinstr
Scraping a Shopify site named Techinstr to scrape product images

### Data Scraping

- Used Scrapy to scrape product data from [Techinstr](https://techinstr.myshopify.com/collections/all) shopify site. The spider is in [products.py](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/techinstr/techinstr/spiders/products.py). 
- Even though the website is javascript-enabled, by disabling the javascript, the website shows simple pagination. Since disabled javascript is Scrapy's default behavior, we can implement a simple pagination traversal in the spider code.
- The images are scraped using a custom [image pipeline](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/techinstr/techinstr/pipelines.py). The custom pipeline changes the saved images' filenames. The filenames are slugified versions of product titles. This slugification is done using Python's **slugify** library
- Necessary changes have been added in [settings.py](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/techinstr/techinstr/settings.py) to accommodate the custom image pipeline
- The downloaded images were 1000x1000 which is too large. We downsized the image size to 100x100 by adding **IMAGES_THUMBS** variable in the *settings.py*. 
- Overall there are about 130 products spread about 15 pages
- The scraped data is saved in a [json file](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/techinstr/products.json) that  includes product **title, price, and image info. like image file path**
- The scraped images are save in a [folder](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/tree/main/techinstr/product_images) that is determined by **IMAGES_STORE** variable in *settings.py*.

### Streamlit App

Streamlit App Link: [https://image-mining.streamlit.app/](https://image-mining.streamlit.app/)

**Features**:

- Price distribution of item
- Top 10 cheapest and most expensive items
- 9 random scraped images from the site


## Books to Scrape

Scraping [bookstoscrape](http://books.toscrape.com/index.html) to scrape images of books and their info


### Data Scraping
- Framework: **Scrapy** 
- Scrapy spider: [books.py](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/tree/main/bookstoscrape/bookstoscrape/spiders)
- The spider scrapes the info. of 1000 books and saves the info. in [books.json ](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/bookstoscrape/books.json). The info. contains *price, title, genre, how many books are in stock, rating, image_url that is used to scrape the image, image meta data that has the path where the scraped images are saved*. The spider scrapes through 50 pages
- The images are scraped using a [custom image pipeline](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/bookstoscrape/bookstoscrape/pipelines.py). The custom pipeline changes the saved images' filenames. The filenames are slugified versions of book titles. This slugification is done using Python's slugify library. Necessary changes have been added in [settings.py](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/bookstoscrape/bookstoscrape/settings.py) to accommodate the custom image pipeline
- The scraped images are save in a [folder](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/tree/main/bookstoscrape/book_images/full) that is determined by IMAGES_STORE variable in settings.py.

### Streamlit App

Streamlit App Link: [https://image-mining.streamlit.app/](https://image-mining.streamlit.app/)

**Features**:

- Genre-based histogram and box plot for price and in_stock distribution
- Bar plot for genre-based ratings distribution
- Top 10 lists for most expensive, cheapest, highest and lowest rated books
- Genre-based Scatter Plot and Correlation Heatmap for Price vs Rating
- Bar plot for genre distribution
- Show the cover of a selected book along with its title, price, and other info.


## QuoteFancy

Scraping Top 100 Motivational Quotes from [quotefancy](https://quotefancy.com/motivational-quotes).

### Data Scraping
- Framework: **Scrapy** & **Playwright**. To use playwright with scrapy, [scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright) Python module had to be installed. 
- **Quotes images, quote texts, author names, upvotes, and downvotes** for quotes were scraped. The **upvotes and downvotes** used javascript. So, playwright was used to scrape **upvotes and downvotes**. The spider crawler is [image_scraper_2](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/quotefancy/quotefancy/spiders/quote_images_2.py)
- The scraped for 100 top quotes are saved in [quotes.json](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/quotefancy/quotes.json). The scraped image_quotes are saved in [downloads](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/tree/main/quotefancy/downloads) folder
- The quote text is further cleaned by removing stopwords using **nltk** library and by removing non-alphabetic symbols using *regex*. It's saved in [quote_filtered_text.json](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/quotefancy/quote_filtered_text.json). This text is later used to generate *world cloud* in the streamlit app. The code can be found in [create_clean_quote_text.py](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/quotefancy/create_clean_quote_text.py)

### Streamlit App

Streamlit App Link: [https://image-mining.streamlit.app/](https://image-mining.streamlit.app/)

**Features**:

- Showing chosen quote's associated image and other related info.
- Distribution of upvotes (box plot and histogram)
- Word cloud using the cleaned quote text data from [quote_filtered_text.json](https://github.com/rukshar69/Web-Scraping-Shopify-Image-Scraping/blob/main/quotefancy/quote_filtered_text.json) 
- Scatter plot between Upvotes and Downvotes

## Reference
- [Scrapy image pipeline documentation](https://docs.scrapy.org/en/latest/topics/media-pipeline.html)
- [YouTube vid: Download All Images and other Data -Python Scrapy New Easier Method using Python Scrapy](https://www.youtube.com/watch?v=2BsvriLQuOs) 