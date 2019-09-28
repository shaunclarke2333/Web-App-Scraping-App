from splinter import Browser
from bs4 import BeautifulSoup as bs
import cssutils
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

     # Scrape NASA Mars News

    url_nasa_mars_news = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url_nasa_mars_news)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    latest_article = soup.find('li', class_="slide")

    news_title = latest_article.find('div', class_='content_title').get_text()
    news_p = latest_article.find('div', class_='article_teaser_body').get_text()

    
    
    # Scrape JPL Mars Space Images - Featured Image

    url_jpl_mars_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl_mars_images)

    time.sleep(1)

    html = browser.html
    soup = bs(html,'html.parser')

    featured = soup.find('article', class_='carousel_item')
    style=cssutils.parseStyle(featured['style'])
    img_url = style['background-image']
    img_url = img_url.replace('url(', '').replace(')', '')

    featured_image_url = 'https://www.jpl.nasa.gov' + img_url


    # Scrape Mars Weather

    url_tweet = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_tweet)

    time.sleep(1)

    html = browser.html
    soup = bs(html,'html.parser')

    tweet_box = soup.find('div', class_="tweet")
    tweet = tweet_box.find('div',class_="js-tweet-text-container")
    tweet_p = tweet.find('p')
    mars_weather = tweet_p.get_text()

    # Scrape Mars Facts

    url_mars_fact = 'https://space-facts.com/mars/'

    tables = pd.read_html(url_mars_fact)

    df = tables[1]
    df.columns = ['', 'value']
    df.set_index('', inplace=True)

    df.to_html('table.html')

    # Mars Hemispheres

    url_hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemisphere)

    hemisphere_image_urls = []

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_="item")

    for result in results:
        html = browser.html
        soup = bs(html, 'html.parser')
        title = result.find('h3').get_text()

        hemisphere_dict = {
            'title': title
        }

        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = bs(html, 'html.parser')
        img = soup.find('div', class_='downloads').find('a')['href']
        hemisphere_dict.update({'img_url':img})
        hemisphere_image_urls.append(hemisphere_dict)
        browser.back()

    # Quite the browser after scraping
    browser.quit()

    scraped_data = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "mars_weather":mars_weather,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    # Return results
    return scraped_data
