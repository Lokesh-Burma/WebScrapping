from bs4 import BeautifulSoup
import requests
import csv

# opening csv file
csv_file = open('BlueTomato_data.csv', 'w', encoding='utf-8-sig', newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Name', 'Brand_Name', 'Price', 'Product_URL', 'Image_URL'])  # row-1 Titles
csv_file.close()


# Save data to csv
def writeToCsv(name, brand, price, product_link, img_url):
    csv_file = open('BlueTomato_data.csv', 'a', encoding='utf-8-sig', newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([name, brand, price, product_link, img_url])
    csv_file.close()

base = 'https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/?page={}'
page = 1

# Iterating over all 35 pages
while page < 35:
    url = requests.get(base.format(page)).text
    soup = BeautifulSoup(url, 'html5lib')

    for product in soup.find_all('li', class_='productcell'):  # iterating over items list
        product_info = product.find('a', class_='name track-click track-load-producttile')

        name = product_info['data-productname']
        brand = product_info['data-brand']

        price = (product.find('span', class_='price').text).split('statt')
        price = price[0].replace('\xa0', ''.replace('\n','')).strip()  # cleaning price

        product_url = product_info['href']
        product_link = f'https://www.blue-tomato.com{product_url}'

        img = product.find('img')
        img_url = img.get('data-src')
        # image url is either in 'src' or 'data-src' of img tag
        if img_url is None:
            img_url = img.get('src')
        img_url = f'https:{img_url}'

        data = {
            "Name": name,
            "Brand": brand,
            "Price": price,
            "Product_link": product_link,
            "Img_url": img_url
        }

        print(data)
        # writing output row wise and column separated
        writeToCsv(name,brand,price,product_link,img_url)

    page += 1   # incrementing page number
