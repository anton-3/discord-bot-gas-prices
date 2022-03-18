import requests
from lxml import html
from cssselect import GenericTranslator

class Scraper:
    def __init__(self, name, url):
        self.url = url
        self.name = name
        # request doesn't go through unless you pass headers in the get request
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}
        self.last_prices = {} # prices the last time it was checked
        self.get_response() # test url so it throws an error if it's invalid

    def get_response(self):
        response = requests.get(self.url, headers=self.headers)
        if response.ok:
            return response
        else:
            raise Exception('HTML request error, status code ' + str(response.status_code))

    # get the current listed prices for the gas station
    # right now only works for links to costco locations
    def get_prices(self):
        response = self.get_response()
        document = html.fromstring(response.content)
        # xpath expression for the price elements
        prices_exp = GenericTranslator().css_to_xpath('.h3-style-guide') + '/text()'
        prices_list = document.xpath(prices_exp)
        prices = {'regular': prices_list[0], 'premium': prices_list[1], 'diesel': prices_list[2]}
        self.last_prices = prices
        return prices

