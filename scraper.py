import requests
from lxml import html
from cssselect import GenericTranslator

class Scraper:
    def __init__(self, url):
        self.url = url
        # throws a 403 unless you pass headers in the get request
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}

        self.location = self.get_location()

    def get_response(self):
        response = requests.get(self.url, headers=self.headers)
        if response.ok:
            return response
        else:
            raise Exception('HTML request error, status code ' + str(response.status_code))

    # get the location of the gas station
    def get_location(self):
        response = self.get_response()
        document = html.fromstring(response.content)
        # xpath expression for the location name
        heading_exp = GenericTranslator().css_to_xpath('h1') + '/text()'
        heading = document.xpath(heading_exp)
        location = ''.join(heading)
        return location

    # get the current listed prices for the gas station
    def get_prices(self):
        response = self.get_response()
        document = html.fromstring(response.content)
        # xpath expression for the price elements
        prices_exp = GenericTranslator().css_to_xpath('.FuelTypePriceDisplay-module__price___3iizb') + '/text()'
        prices = document.xpath(prices_exp)
        regular = prices[0]
        premium = prices[1]
        diesel = prices[2]
        return {'regular': regular, 'premium': premium, 'diesel': diesel}

