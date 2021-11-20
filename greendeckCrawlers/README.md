<h3>Repository for the footwear and topwear scrawler of website https://www.net-a-porter.com/en-in/ as part of my application for Greendeck.</h3>


<h4>Project Structure</h4>

After you do ```scrapy startproject greendeckCrawlers```, scrapy creates the folders in the following structure.
-insert outermost image

In the greendeckCrawlers folder, you can see the spiders folder and different files scrapy provides us for data processing and pipeline.
-insert outermost image

In the spiders folder,we have the two crawlers for our usage : 
1. **toscrape-footwear.py** to scrape shoes from the website.
2. **toscrape-topwear.py** to scrape tops from the website.

We can use mongo atlas free tier for storing the scraped data into the collections 'flipkart' and you can interact with your 
database via the UI on the website or using mongo shell (<a href="https://docs.mongodb.com/mongodb-shell/install/"/>I have used this one to fire the queries</a>).

After scrapy following things are done:
1. The scraped data is stored in the items object scrapy provides by editing the *items.py* file.
2. Then we can insert each item which is in the form of key,value pairs into the collections with
   the help of *pipelines.py* file. 
3. You can get all the mongo database credentials in the *settings.py* file.
4. Leave the *middlewares.py* file as it is since its not needed for current problem statment.


<h4>Scraping</h4>
1. Mention the url you want to scrape in the ```start_url``` list.
2. Each product is scraped by using the xpath selector.
3. Each product is present in an anchor tag so you can loop over all anchor tags and get each product one by one
   ```python
	for i in range(1,41):
            item = GreendeckcrawlersItem()
            try:
                img_url = response.xpath(f"//a[{i}]/div/div/div[1]/div/div[2]/div/div/div/picture/img/@src").get()
                item['product_name'] = response.xpath(f"//a[{i}]/div/div/div[2]/div/span/span[3]/text()").get()
                item['brand_name'] = response.xpath(f"//a[{i}]/div/div/div[2]/div/span/span[1]/text()").get()
                #rest of the fields
            except:
                logging.debug(f"Fault Product_item:{i}")
            
	    yield item```
      
4. Next page is navigated by generating the next pages in the ```start_url``` list as follows:
   ```python f"https://www.net-a-porter.com/en-in/shop/clothing/tops?pageNumber={i}" for i in range(1,26) #scrape 25 pages```


<h4>Run your crawlers</h4>
You can run the footwear crawler as follows
```scrapy crawl toscrape-footwear.py```


You can run the topwear crawler as follows:
```scrapy crawl toscrape-footwear.py```



<h4>Future Scope</h4>
We can further make changes to the project by:
1. Add the database credentials to the config file,parse it instead of openly displaying your credentials and
   then add the config file to .gitgnore
2. Convert the crawler into a REST-API or integrate it into an existing one as per your needs.
