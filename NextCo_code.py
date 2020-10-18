import json
import scrapy


class T4Spider(scrapy.Spider):
    name = 'nextco'
    start_urls = ['https://www.next.co.uk/clearance/search?w=*&af=gender:men%20']

    # request headers
    headers = {
            "Accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US, en; q = 0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://www.next.co.uk/clearance/search?w=*&af=gender:men%20",
            "gender": "men % 20",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 85.0.4183.121Safari / 537.36Edg / 85.0.564.70",
            "x-requested-with": "XMLHttpRequest",
    }

    def parse(self, response, **kwargs):
        url = 'https://www.next.co.uk/clearance/all/search?w=*&af=gender:men%20gender:men%20'
        # collecting XHR get request from page as this is a dynamic website
        request = scrapy.Request(url, callback=self.parse_api, headers=self.headers)
        yield request

    def parse_api(self, response):
        # convert data to json object
        raw_data = response.body
        data = json.loads(raw_data)

        for product in data['Items']:
            brand = product["Brand"]
            name = product["Name"]
            image_url = product["SearchImage"]

            priceinfo = product["ItemOptions"][0]
            originalprice = priceinfo['OriginalPrice']
            discountprice = priceinfo['Price']

            yield {
                    'Brand': brand,
                    'Name': name,
                    'OriginalPrice (Euros)': originalprice,
                    'DiscountPrice (Euros)': discountprice,
                    'Img': f'https://xcdn.next.co.uk/COMMON/Items/Default/Default/ItemImages/Sale{image_url}'
                    }

        # Extract current page number and total results
        product = data['Items'][0]
        page = int(product['PageNo'])
        total_items = int(data['SearchConfig']['TotalResults'])
        # each page has 24 items listed
        # find total pages by dividing total results by no. of item in each page
        # srt = page item start count eg. for page 1, items = 0-23; page 2, srt = 24-47; ...
        if page < total_items//24:
            srt = (page)*24             # page 1 , srt=0*24 => 0; page 2, srt=1*24 => 24
            next = f'https://www.next.co.uk/clearance/all/search?w=*&af=gender:men%20gender:men%20&srt={srt}'
            yield scrapy.Request(next, callback=self.parse_api)