import requests
import pandas as pd


def readData():
    df = pd.read_csv('Task4_Data.csv')
    google_search_codes = df['Google Search Code'].values.tolist()
    # returns search codes as list
    return google_search_codes


def savedata(product_url):
    # storing data to csv
    df = pd.read_csv("Task4_Data.csv")
    df["Product URL"] = product_url
    df.to_csv("Task4_Data.csv", index=False)


def extracturl():
    # specific parameters for api request
    params = {
        'access_key': '7b0f8ec10e1309197d2d23079cae5e8b',
        'engine': 'google',
        'location': 'france',
        'google_domain': 'google.com',
        'gl': 'fr',    # country code = fr
        'hl': 'fr'     # host language = fr
    }

    product_url = []
    # Iterate over google search codes
    for code in readData():
        api_result = requests.get(f'http://api.serpstack.com/search?&query={code}', params)
        api_response = api_result.json()

        flag = False
        # check if url is of oneill.com/fr from api results
        for result in api_response['organic_results']:
            if 'www.oneill.com/fr/fr' in result['url']:
                product_url.append(result['url'])        # if proper url found exit form loop
                flag = True
                break

        # did not get url for some products so appending not available string
        if flag is False:
            product_url.append('Not Available')

    savedata(product_url)

extracturl()