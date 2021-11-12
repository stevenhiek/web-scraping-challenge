from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import pandas as pd

def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_dict = {}

    ### Generate Latest News Title and Descriptions
    mars_news_url = 'https://redplanetscience.com/'
    browser.visit(mars_news_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find(class_='content_title').text
    news_p = soup.find(class_="article_teaser_body").text

    ### Generate Featured Image ###
    featured_image_url = 'https://spaceimages-mars.com/'
    browser.visit(featured_image_url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_relative_path = soup.find('img',class_="fancybox-image")['src']
    featured_image_url = featured_image_url + featured_image_relative_path

    ### Generate Mars Table ###
    mars_table_url = 'https://galaxyfacts-mars.com/'
    browser.visit(mars_table_url)
    mars_df = pd.read_html(mars_table_url)
    mars_df = mars_df[0]
    mars_df.columns = mars_df.iloc[0]
    mars_df = mars_df.iloc[1:]
    # mars_df_to_list = mars_df.to_dict(orient="list")
    mars_html = mars_df.to_html()

    ### Generate Mars Hemispheres ###
    mars_hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(mars_hemispheres_url)
    hemispheres_list = []
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres_results = soup.find_all('div',class_='item')
    for hemisphere in hemispheres_results:
        browser.links.find_by_partial_text(hemisphere.h3.text).click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_title = soup.h2.text
        image_url = mars_hemispheres_url + soup.find('img',class_="wide-image")['src']
        browser.visit(mars_hemispheres_url)
        image_dict = {'title':image_title,'image_url':image_url}
        hemispheres_list.append(image_dict)

    ### Add to Mars Dictionary ###
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p
    mars_dict['feature_image_url'] = featured_image_url
    mars_dict['mars_df'] = mars_html
    mars_dict['mar_hemispheres'] = hemispheres_list

    # Quit the browser
    browser.quit()

    return mars_dict
