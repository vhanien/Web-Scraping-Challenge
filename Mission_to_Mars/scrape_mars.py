# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser 
import pandas as pd 
import time 

# Initialize chromedriver.exe 
def init_browser():
    executable_path = {"executable_path": "C:/Users/verin/Desktop/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()


    # Visit NASA's website to scrape title and paragraph information
    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    # Scrape page into soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Retrieve latest news title and paragraph text
    news_title = soup.find_all("div", "content_title")[1].text
    news_p = soup.find_all("div", "article_teaser_body")[0].text

    # Visit NASA's website for images
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    # Retrieve the featured image by using the click function
    browser.click_link_by_partial_text('FULL IMAGE')
    # Add a timer between clicks 
    time.sleep(3)
    # Retrieve the featured image by using the click function
    browser.click_link_by_partial_text('more info')
    # Scrape page into soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Create link
    image = soup.find("img", class_ = 'main_image')['src']
    featured_image_url = "https://www.jpl.nasa.gov" + image

    # Visit Mars space facts
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    # Scrape the table with the planet profile 
    tables = pd.read_html(url)
    # Slice the dataframes we want
    df = tables[0]
    # Rename the columns 
    df.columns=['Description', "Mars"]
    # Set description as index
    df.set_index("Description", inplace=True)
    # Save as HTML file
    df_html = df.to_html()

    # Visit the USGS Astrogeology site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    # Scrape page into soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Retrieve information from the list 
    mars_hemispheres = soup.find_all("div", "item")
    # Create a dictionary to store information
    hemisphere_info = []
    # Create a loop to get title information and image link for all 4 pictures
    for hemisphere in mars_hemispheres:
        # Get the title
        title = hemisphere.find("h3").text
        # Create image link
        link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + link   
        # Visit image link, add a timer and scrape into soup
        browser.visit(image_link)
        time.sleep(1)
        html = browser.html
        soup = bs(html, "html.parser")
        # Retrieve full image 
        full_image = soup.find("div", "downloads")
        image_url = full_image.find("a")["href"]
        hemisphere_info.append({"title": title, "img_url": image_url})


    # Store data in a dictionary
    mars_data = {
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url" : featured_image_url,
        "df_html" : df_html,
        "hemisphere_info" : hemisphere_info
    }

    # Close the browser after scraping
    browser.quit()

    return mars_data