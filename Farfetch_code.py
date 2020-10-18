import scrapy


class Task1(scrapy.Spider):
    name = 'farfetch'

    start_urls = ['https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx?']

    def parse(self, response, **kwargs):
        product_info = response.css('[data-test="productCard"]')

        img_url = []
        # //img/@src didn't work here so extracting image info from meta tag
        for image in response.xpath('//meta/@content').extract():
            # finding list of proper img urls
            if '.jpg' in image:
                img_url.append(image)

        # each product has a display image and a hover image
        # extracting display images from list (in odd positions)
        img_url = img_url[::2]
        i = -1      # counter for images

        for product in product_info:
            name = product.css('[itemprop="name"]::text').get()
            brand = product.css('h3::text').get()
            price = product.css('[data-test="price"]::text').get()
            pro_url = product.css('[class="_5ce6f6"]').xpath("@href").get()

            i += 1
            yield {
                "Name": name, "Brand": brand, "Price (in Euros)": price,
                "Product_url": f'https://www.farfetch.com{pro_url}',
                "img": img_url[i]
            }

        # moving to next page, total pages 176
        for page in range(2,177):
            next_page = f'https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx?page={page}'
            yield scrapy.Request(next_page)