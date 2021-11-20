# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GreendeckcrawlersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #defining storage containers for the data we plant to scrap.
    
    product_name = scrapy.Field()
    brand_name = scrapy.Field()
    original_price = scrapy.Field()
    sales_price = scrapy.Field()
    image_url = scrapy.Field()
    product_page_url = scrapy.Field()
    product_category = scrapy.Field()
    

