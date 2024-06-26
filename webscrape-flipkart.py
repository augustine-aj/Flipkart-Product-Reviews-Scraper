# using xpath
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd


path = "C:/Users/ugus/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe"
website = 'https://www.flipkart.com/apple-iphone-15-blue-256-gb/product-reviews/itm986f66c53cae4?pid=MOBGTAGPNEZZY2YR&lid=LSTMOBGTAGPNEZZY2YRE1FCIG&marketplace=FLIPKART'
nextPage_link = ''
nextPage_xpath = '//div[@class="_1G0WLw mpIySA"]/nav/a[@class="_9QVEpD"]'

xpaths_review = {
    'customer_rating': '//div[@class="XQDdHH Ga3i8K"]',
    'customer_reviewTitle': '//div/p[@class="z9E0IG"]',
    'customer_review': '//div[@class="ZmyHeo"]',
    'customer_name': '//div/p[@class="_2NsDsF AwS1CA"]',
    'customer_place': '//div/p[@class="MztJPv"]/span[2]',
    'customer_postedDate': '//div/p[@class="_2NsDsF"]',
    'customer_reviewLikes': '//div[@class="_6kK6mk"]/span[@class="tl9VpF"]',
    'customer_reviewDislikes': '//div[@class="_6kK6mk aQymJL"]/span[@class="tl9VpF"]',

}

review_dict = {
    'customer_rating': [],
    'customer_reviewTitle': [],
    'customer_review': [],
    'customer_name': [],
    'customer_place': [],
    'customer_postedDate': [],
    'customer_reviewLikes': [],
    'customer_reviewDislikes': [],
}

service = Service(excutable_path=path)
driver = webdriver.Chrome(service=service)


def browse_link(link):
    return driver.get(link)


def get_elements():
    for keys, values in xpaths_review.items():
        elements = driver.find_elements(by='xpath', value=values)
        if keys == 'customer_place':
            text_list = [element.text.split(',')[-1].strip() for element in elements]
        elif keys == 'customer_review':
            text_list = [element.text.replace('\n', '.') for element in elements]
        else:
            text_list = [element.text for element in elements]
        review_dict[keys].extend(text_list)


def get_link():
    global nextPage_link
    elements = driver.find_elements(by='xpath', value=nextPage_xpath)
    for element in elements:
        nextPage_link = element.get_attribute('href')


browse_link(website)
get_elements()
get_link()

for i in range(5):
    browse_link(nextPage_link)
    get_elements()
    get_link()

for keys, values in review_dict.items():
    print(f'{keys} : {len(values)}')

review_dict_df = pd.DataFrame(review_dict)
print(review_dict_df)
review_dict_df.to_csv('review_data.csv', index=False)

