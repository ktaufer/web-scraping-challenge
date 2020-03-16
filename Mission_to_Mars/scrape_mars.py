# # Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time

def scrape_mars():
    # # Scrape NASA website for latest Mars news
    url1 = 'https://mars.nasa.gov/news/'
    response = requests.get(url1)
    soup = bs(response.text, 'html.parser')
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text
    time.sleep(2)

    # # Scrape NASA for feateured Mars image URL
    executable_path = {'executable_path':'c:/users/ktauf/desktop/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    button = browser.find_by_id('full_image')
    button.click()
    button2 = browser.find_by_text('more info     ')
    button2.click()
    figure = browser.find_by_css('.main_image')
    featured_image_url = figure['src']
    time.sleep(2)
    
    # # Scrape Mars Weather Twitter feed to gather latest weather update
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    results = soup.find_all('div', class_='js-tweet-text-container')
    for result in results:
        if 'InSight sol' in result.text:
        mars_weather = result.text
        break
    time.sleep(2)

    # # Scrape space-facts.com to gather table of Mars factoids
    url = 'https://space-facts.com/mars/'
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    results = soup.find('table', id ='tablepress-p-mars-no-2')
    tbody = results.find('tbody')
    trow = tbody.find_all('tr')
    table_list = []
    for item in trow:
        column1 = item.find('td', class_='column-1').text
        column2 = item.find('td', class_='column-2').text
        table_list.append({'Measurement':column1, 'Data': column2}) 
    table_df = pd.DataFrame(table_list)
    table_df = table_df[['Measurement','Data']]
    table_df = table_df.set_index('Measurement')
    table_df.to_html('facts_table.html')
    time.sleep(2)
    
    # # Scrape USGS website to get images of Mars' four hemispheres
    executable_path = {'executable_path':'c:/users/ktauf/desktop/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    button = browser.find_by_text('Cerberus Hemisphere Enhanced')
    button.click()
    cerberus_image = browser.find_by_css('.wide-image')['src']
    cerberus_title = browser.find_by_css('.title').text
    time.sleep(2)
    
    executable_path = {'executable_path':'c:/users/ktauf/desktop/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    button = browser.find_by_text('Syrtis Major Hemisphere Enhanced')
    button.click()
    syrtis_major_image = browser.find_by_css('.wide-image')['src']
    syrtis_major_title = browser.find_by_css('.title').text
    time.sleep(1)

    executable_path = {'executable_path':'c:/users/ktauf/desktop/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    button = browser.find_by_text('Schiaparelli Hemisphere Enhanced')
    button.click()
    schiaparelli_image = browser.find_by_css('.wide-image')['src']
    schiaparelli_title = browser.find_by_css('.title').text

    executable_path = {'executable_path':'c:/users/ktauf/desktop/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    button = browser.find_by_text('Valles Marineris Hemisphere Enhanced')
    button.click()
    valles_marineris_image = browser.find_by_css('.wide-image')['src']
    valles_marineris_title = browser.find_by_css('.title').text
    
    # # Create dataframe of Mars hemispheres images
    hemisphere_image_urls = [
        {"title": valles_marineris_title, "img_url": valles_marineris_image},
        {"title": cerberus_title, "img_url": cerberus_image},
        {"title": schiaparelli_title, "img_url": schiaparelli_image},
        {"title": syrtis_major_title, "img_url": syrtis_major_image}]
        hemisphere_images = pd.DataFrame(hemisphere_image_urls)
    
    mars_data = [
        {'news_title' : news_title}, 
        {'news_p': news_p}, 
        {'featured_image_url': featured_image_url}, 
        {'mars_weather' : mars_weather}
        ]
    
    return hemisphere_image_urls, mars_data


scrape_mars()
