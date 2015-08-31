__author__ = 't846432'
import unittest
from BeautifulSoup import BeautifulSoup as bs
from urllib2 import urlopen
import sys

class TestCase(unittest.TestCase):
    def Test1(self):
        BASE_URL = "https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_Oslo_Stock_Exchange"
        #BASE_URL = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'

        html = urlopen(BASE_URL).read()
        try:
            data = []
            soup = bs(html)
            table = soup.find('table', attrs={'class':'wikitable sortable'})
            table_body = table.find('tbody')

            rows = table.findAll("tr")
            for row in rows:
                cols = row.findAll('td')
                cols = [ele.text.strip() for ele in cols]
                try:
                    ticker = str(cols[1][4:])+'.OL'
                    data.append(ticker)
                except:
                    pass
             # Get rid of empty values
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()

    def Test2(self):
        #BASE_URL = "https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_Oslo_Stock_Exchange"
        BASE_URL = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'

        html = urlopen(BASE_URL).read()
        try:
            data = []
            soup = str(bs(html))
            rows = soup.split('\r\n')

            for row in rows:
                i =row.find('|')
                try:
                    ticker = str(row[:i])
                    if(ticker != 'Symbol'):
                        data.append(ticker)
                except:
                    pass
             # Get rid of empty values
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
        t = len(data)
        print(data)
