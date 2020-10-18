import scrapy
from scrapy.spiders import Spider
import pandas as pd

# To store price
price_list = []

class QuoteSpider(Spider):
    name = 'Oneill'
    # for allowing requests one by one
    custom_settings = {'CONCURRENT_REQUESTS': '1'}

    def start_requests(self):
        df = pd.read_csv('Task4_Data.csv')  # Get product url dataframe from csv file
        urls_list = df['Product URL'].values.tolist()  # convert product url values to list
        for url in urls_list:
            if url != 'Not Available':
                yield scrapy.Request(url, priority=1)   # check if product url is available for a product
            else:
                price_list.append("Not Available")

    def parse(self, response, **kwargs):

        price = response.xpath('//*[contains(concat( " ", @class," " ),concat( " ", "sales", " " ))]//*[contains(concat( " ",@ class , " " ), concat( " ", "value", " " ))]/text()').get()
        price = price.replace('\r', ''.replace('\n', ''))
        price = price.strip()

        price_list.append(price)

        # total 129 products
        if(len(price_list) is 129):
            df = pd.read_csv('Oneill_data.csv')
            df["Price"] = price_list
            df.to_csv('Task4_Data.csv', index=False)