import scrapy


class ImagesSpider(scrapy.Spider):
    name = 'images'

    def start_requests(self):
        for pagenumber in range(25):
            base_url = f'https://www.blue-tomato.com/de-DE/products/categories/Snowboard+Shop-00000000/gender/men/?page={pagenumber}'
            yield scrapy.Request(base_url)

    def parse(self, response, **kwargs):
        raw_img_urls = response.css('img::attr(src)').getall()      # extracting image url info

        clean_img_urls = []
        # extracting only valid image urls, stripping other data which some img tags contains
        for img_url in raw_img_urls:
            if '.jpg' in img_url:
                clean_img_urls.append(response.urljoin(img_url))

        yield {'image_urls': clean_img_urls}