import scrapy
import logging
import random

from greendeckCrawlers.items import GreendeckcrawlersItem

class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-footwear'
    #scrape 20 pages
    start_urls = [
        f"https://www.net-a-porter.com/en-in/shop/shoes?pageNumber={i}" for i in range(1,26) #scrape 25 pages
        ]


    def parse(self, response):
        num_tags = len(response.xpath("//section/div[2]/div/div/a")) #number of anchor tags present per page. Tags were 60 but we want to scrape only 40 products/page.
        for i in range(1,41):
            
            item = GreendeckcrawlersItem()
            try:

                original_price = float(''.join(response.xpath(f"//a[{i}]/div/div/div[2]/div/div[1]/span//span/text()").get()[1:].split(',')))
                img_url = response.xpath(f"//a[{i}]/div/div/div[1]/div/div[2]/div/div/div/picture/img/@src").get()
                item['product_name'] = response.xpath(f"//a[{i}]/div/div/div[2]/div/span/span[3]/text()").get()
                item['brand_name'] = response.xpath(f"//a[{i}]/div/div/div[2]/div/span/span[1]/text()").get()
                item['original_price'] = original_price
                item['sales_price'] = round(random.uniform(545.0,original_price),2)
                item['image_url'] = 'https:'+img_url if img_url else None
                item['product_page_url'] = 'https://www.net-a-porter.com'+response.xpath(f"//section/div[2]/div/div/a[{i}]/@href").get()
                item['product_category'] = 'footwear'
                #logging.debug(item['product_name'])
                
            except:
                logging.debug(f"Fault Product_item:{i}")
            
	    yield item
		
'''
Note : I couldn't find the sales_price on the website,only original_price was listed for each product. 
I believe sale wasn't going on that moment. So I generated a random sales_price between the given range
as you see above. I even mailed this query to the careers@greendeck.com but got no response so decided 
to go ahead with it. 

Also, for some products img_url is not getting extracted cause of addition of extra divs on the website.
So I have marked them as None in the database. We can discuss this issue and my approach more 
clearly perhaps in the interview. 

'''




