# # Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time

def init_browser():
    executable_path = {'executable_path':'c:/users/ktauf/desktop/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # # Scrape NASA website for latest Mars news
    url1 = 'https://mars.nasa.gov/news/'
    response = requests.get(url1)
    soup = bs(response.text, 'html.parser')
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text
    time.sleep(2)

    # # Scrape NASA for feateured Mars image URL
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    button = browser.find_by_id('full_image')
    button.click()
    button2 = browser.find_by_text('more info     ')
    button2.click()
    figure = browser.find_by_css('.main_image')
    featured_image_url = figure['src']
    time.sleep(2)
    
    # # Scrape Mars Weather Twitter feed to gather latest weather update
    url3 = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url3)
    soup = bs(response.content, 'html.parser')
    results = soup.find_all('div', class_='js-tweet-text-container')
    mars_weather = ''
    for result in results:
        if 'InSight sol' in result.text:
            mars_weather = result.text
        break
    time.sleep(2)
    
    # # Scrape USGS website to get images of Mars' four hemispheres
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    button = browser.find_by_text('Cerberus Hemisphere Enhanced')
    button.click()
    cerberus_image = browser.find_by_css('.wide-image')['src']
    cerberus_title = browser.find_by_css('.title').text
    time.sleep(2)
    
    browser.visit(url5)
    button = browser.find_by_text('Syrtis Major Hemisphere Enhanced')
    button.click()
    syrtis_major_image = browser.find_by_css('.wide-image')['src']
    syrtis_major_title = browser.find_by_css('.title').text
    time.sleep(2)

    browser.visit(url5)
    button = browser.find_by_text('Schiaparelli Hemisphere Enhanced')
    button.click()
    schiaparelli_image = browser.find_by_css('.wide-image')['src']
    schiaparelli_title = browser.find_by_css('.title').text
    time.sleep(2)

    browser.visit(url5)
    button = browser.find_by_text('Valles Marineris Hemisphere Enhanced')
    button.click()
    valles_marineris_image = browser.find_by_css('.wide-image')['src']
    valles_marineris_title = browser.find_by_css('.title').text

    # # Create dataframe of Mars information
    mars_data = {
        'news_title' : news_title, 
        'news_subtitle': news_p, 
        'featured_image_url': featured_image_url, 
        'mars_weather' : mars_weather,
        "valles_marineris_title": valles_marineris_title, 
        "valles_marineris_img_url": valles_marineris_image,
        "cerberus_title": cerberus_title, 
        "cerberus_img_url": cerberus_image,
        "schiaparelli_title": schiaparelli_title, 
        "schiaparelli_img_url": schiaparelli_image,
        "syrtis_major_title": syrtis_major_title, 
        "syrtis_major_img_url": syrtis_major_image}
    
    return mars_data

init_browser()
scrape()