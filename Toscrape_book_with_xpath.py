import requests
from requests import Session
from bs4 import BeautifulSoup as bs
# from collections import ChainMap
from lxml import html
import pandas as pd
import re
s = Session()
s.headers['user-agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:10Gecko/20100101 Firefox/104.0'


def detailPage(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    Title = tree.xpath('//h1//text()'.strip())
    Price = tree.xpath('//div[@class="col-sm-6 product_main"]//p[@class = "price_color"]//text()'.strip())
    Stock = tree.xpath('//div[@class="col-sm-6 product_main"]//p[@class = "instock availability"]//text()'.strip())
    Warning_ = tree.xpath('//div[@class ="alert alert-warning"]//text()'.strip())
    Product_Description = tree.xpath('//article[@class="product_page"]//p[not(@class) and not(@id)]//text()')
    img = ''.join(tree.xpath('//div[@class ="item active"]//img/@src'))
    image = 'http://books.toscrape.com/'+img.replace('..','').replace('//','')

    data_detail ={
        'Title':Title,
        'Price':Price,
        'Stock':Stock,
        'Warning_':Warning_,
        'Product_Description':Product_Description,
        'image':image
    }
    return data_detail


all_data = []
def listpage(url):
    NextPage = url
    while NextPage:
        r = s.get(NextPage)
        tree = html.fromstring(r.text)

        NextLink = ''.join(tree.xpath('//li[@class="next"]//a/@href'))
        NextPage = 'http://books.toscrape.com/catalogue/'+ NextLink
        if NextLink:
            All_product = tree.xpath('//li[@class = "col-xs-6 col-sm-4 col-md-3 col-lg-3"]')
            for product in All_product:
                Pro_link = ''.join(product.xpath('.//h3//a/@href'))
                links = 'http://books.toscrape.com/catalogue/'+Pro_link
                # print(links)


                detail = detailPage(links)
                data = {
                    'Landing_Url':NextPage,
                    'Pro_link':links,
                    'Title':detail['Title'],
                    'Price':detail['Price'],
                    'Stock':detail['Stock'],
                    'Warning_':detail['Warning_'],
                    'Product_Description':detail['Product_Description'],
                    'image':detail['image']            
                }
                # data.update(data_detail)
                # combine_dict = ChainMap(data,data_detail)
                all_data.append(data)
        else:
            break

        print(data)
url = 'http://books.toscrape.com/catalogue/page-1.html'
listpage(url)
df = pd.DataFrame(all_data)
df.to_excel('Books_xpath.xlsx',index=False)



