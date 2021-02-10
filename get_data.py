import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen

ticker = input(str('Enter a Ticker: '))
url = ('https://finviz.com/quote.ashx?t='+ ticker +'&ty=c&p=d&b=1')

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
html = soup(webpage, "html.parser")


fundamentals = pd.read_html(str(html), attrs = {'class': 'snapshot-table2'})[0]

fundamentals.to_csv('table.csv')  
print(fundamentals)