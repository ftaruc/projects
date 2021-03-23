#Import packages
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import re
import time
import sys
import requests
import datefinder
import pickle
#selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
#bs4
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

COOKIES_PATH = r"C:\Users\ferdi\Downloads\projects\grailed\cookies.pkl"
DIRECTORY_PATH = r"C:\Users\ferdi\Downloads\projects\grailed"
WEBDRIVER_PATH = r'C:\Users\ferdi\Downloads\projects\grailed\chromedriver.exe'

#pip install --target "C:\Users\ferdi\AppData\Local\Programs\Python\Python39\Lib\site-packages"
#alias python='winpty "C:\Users\ferdi\AppData\Local\Programs\Python\Python39/python.exe"'

#driver.get_screenshot_as_file(r"C:\Users\ferdi\Downloads\projects\grailed\screenshot.png") -> Use to troubleshoot selenium
"""
FUTURE PLANS

* add follower count as a feature
* can add average feedback as well from profile
"""

#############################################################

"""
You need to log-in to a Grailed Account to access all the filters to see past listings that were sold.
This function saves the cookies so it can be accessed in the future.
"""

def first_run():
    ##Initialize Selenium
    options = Options()
    options.add_argument("user-data-dir=selenium")
    url = "https://www.grailed.com/users/sign_up"
    driver = webdriver.Chrome(WEBDRIVER_PATH, options=options)
    driver.get(url)
    time.sleep(2)

    #Login to account
    email = "grailedscraper@gmail.com"
    pw = "grailedscraper123"

    og_logxpath = "/html/body/div[3]/div[7]/div/div/div[2]/div/div/p[2]/a"
    login_xpath = "/html/body/div[3]/div[7]/div/div/div[2]/div/div/button[4]"
    driver.find_element_by_xpath(og_logxpath).click()
    time.sleep(1)
    driver.find_element_by_xpath(login_xpath).click()
    time.sleep(1)

    email_xpath = "/html/body/div[3]/div[7]/div/div/div[2]/div/div/form/div[1]/input"
    pw_xpath = "/html/body/div[3]/div[7]/div/div/div[2]/div/div/form/div[2]/input"
    driver.find_element_by_xpath(email_xpath).send_keys(email)
    driver.find_element_by_xpath(pw_xpath).send_keys(pw)
    final_login_xpath = "/html/body/div[3]/div[7]/div/div/div[2]/div/div/form/button"
    driver.find_element_by_xpath(final_login_xpath).click()

    #save cookies
    #time.sleep(5)
    pickle.dump(driver.get_cookies() , open(COOKIES_PATH,"wb"))

def scrape(user_input, display_amount):

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("disable-infobars"); # disabling infobars
    options.add_argument("--disable-extensions"); # disabling extensions
    options.add_argument("--disable-gpu"); # applicable to windows os only
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
    options.add_argument('--headless')

    #to not look like a bot
    ua = UserAgent()
    userAgent = ua.random
    #print(str(userAgent))
    options.add_argument(f'user-agent={userAgent}')

    url = "https://www.grailed.com/"
    driver = webdriver.Chrome(WEBDRIVER_PATH, options=options)
    driver.get(url)

    #load past cookies
    cookies = pickle.load(open(COOKIES_PATH, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    #Searching User Input
    driver.find_element_by_id("globalheader_search").send_keys(user_input + Keys.RETURN)

    time.sleep(1)

    #get containers of all items
    driver, display_amount = check_unlimited_scroll(display_amount, driver)
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    containers = bs.find_all("div", class_="feed-item")
    time.sleep(1)

    print("Saving Results...")
    num_empty = len(bs.find_all("div", class_="feed-item empty-item")) #ignore empty feed items

    #write to new .csv file
    links, item_df = get_item_df(containers, display_amount, num_empty, user_input, False)
    #item_df.to_csv(user_input + "-item.csv", index = False)
    seller_df = scrape_seller(links, False)
    #seller_df.to_csv(user_input + "-seller.csv", index = False)

    final_df = item_df.merge(seller_df, how = 'inner', on = 'Link')
    return final_df
    #final_df.to_csv(user_input + "-final.csv", index = False)

def scrape_filter_sold(user_input, display_amount):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("disable-infobars"); # disabling infobars
    options.add_argument("--disable-extensions"); # disabling extensions
    options.add_argument("--disable-gpu"); # applicable to windows os only
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
    options.add_argument('--headless')

    #to not look like a bot
    from fake_useragent import UserAgent
    ua = UserAgent()
    userAgent = ua.random
    #print(str(userAgent))
    options.add_argument(f'user-agent={userAgent}')

    url = "https://www.grailed.com/"
    driver = webdriver.Chrome(WEBDRIVER_PATH, options=options)
    driver.get(url)

    cookies = pickle.load(open(COOKIES_PATH, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    #Searching User Input
    driver.find_element_by_id("globalheader_search").send_keys(user_input + Keys.RETURN)

    #Filtering by "Sold Only"
    time.sleep(2)

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

    collapse_show = "//*[@id=\"shop\"]/div/div/div[3]/div[1]/div/div[8]/div[1]/div"
    check_sold = "/html/body/div[3]/div[7]/div/div/div[3]/div[1]/div/div[8]/div[2]/div/div/ul/li/label/div/input"
    check_sold_2 = "/html/body/div[3]/div[7]/div/div/div[3]/div[1]/div/div[8]/div[2]/div/div/ul/li[2]/label/div/input"
    check_sold_3 = "/html/body/div[3]/div[7]/div/div/div[3]/div[1]/div/div[8]/div[2]/div/div/ul/li[3]/label/div/input"
    check_sold_4 = "/html/body/div[3]/div[7]/div/div/div[3]/div[1]/div/div[8]/div[2]/div/div/ul/li[4]/label/div/input"

    driver.find_element_by_xpath(collapse_show).click()
    driver.implicitly_wait(1)
    if len(driver.find_elements_by_xpath(check_sold)) > 0:
        driver.find_element_by_xpath(check_sold).click()
    elif len(driver.find_elements_by_xpath(check_sold_2)) > 0:
        driver.find_elements_by_xpath(check_sold_2)[0].click()
    elif len(driver.find_elements_by_xpath(check_sold_3)) > 0:
        driver.find_element_by_xpath(check_sold_3).click()
    else:
        driver.find_elements_by_xpath(check_sold_4).click()
    time.sleep(1)
    driver, display_amount = check_unlimited_scroll(display_amount, driver)

    #get containers of all items

    bs = BeautifulSoup(driver.page_source, 'html.parser')
    containers = bs.find_all("div", class_="feed-item")
    time.sleep(1)

    print("Saving Sold Results...")
    num_empty = len(bs.find_all("div", class_="feed-item empty-item")) #ignore empty feed items

    #write to new .csv file
    links, item_df = get_item_df(containers, display_amount, num_empty, user_input, True)
    #item_df.to_csv(user_input + "-sold-item.csv", index = False)
    seller_df = scrape_seller(links, True)
    #seller_df.to_csv(user_input + "-sold-seller.csv", index = False)

    final_df = item_df.merge(seller_df, how = 'inner', on = 'Link')
    return final_df
    #final_df.to_csv(DIRECTORY_PATH + user_input + "-sold-final.csv", index = False)

def scrape_seller(links, is_sold):
    print("Scraping Seller...")
    # headless: so chrome doesn't open
    options = webdriver.ChromeOptions()

    from fake_useragent import UserAgent
    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')

    options.add_argument('--headless')
    options.add_argument('--lang=en_US')
    options.add_argument("--start-maximized") #fullscreen
    options.add_argument("disable-infobars"); # disabling infobars
    options.add_argument("--disable-extensions"); # disabling extensions
    options.add_argument("--disable-gpu"); # applicable to windows os only
    options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
    #options.add_argument("--no-sandbox");
    driver = webdriver.Chrome(WEBDRIVER_PATH, options=options)

    # column lists for dataframe
    username_list = []
    shipping_list = []
    amt_sold = []
    amt_feedback = []
    amt_listings = []
    amt_likes = []
    desc_list = []
    profile_links = []
    feedback_links = []
    amt_followercount = []
    full_size_desc = []
    location_list = []
    amt_pictures = []
    avg_feeback_list = []

    ### Start Process. links from save_results
    for link in links:
        new_link = "https://www.grailed.com" + link
        driver.get(new_link)
        bs = BeautifulSoup(driver.page_source, 'html.parser')

        #usernames
        try:
            user_name = driver.find_element_by_xpath('//span[@class="-username"]').text
            username_list.append(user_name)
        except NoSuchElementException:
            username_list.append("")

        #amount of items they sold
        try:
            sold = driver.find_element_by_xpath('//a[@class="-link"]/span[2]').text
            amt_sold.append(sold.replace('-','').replace('–', '')) #sold
        except NoSuchElementException:
            amt_sold.append("0")

        #amount of likes
        try:
            likes = driver.find_element_by_xpath('//*[@id="listing-likes"]/button/span').text#sold
            amt_likes.append(likes)
        except NoSuchElementException:
            amt_likes.append("0")

        #amount of feedback received
        try:
            feedback = driver.find_element_by_xpath('//span[@class="-feedback-count"]').text
            amt_feedback.append(feedback.replace("Feedback", "")) #feedback

            #print(avg_feedback)
        except NoSuchElementException:
            amt_feedback.append("0")
            #avg_feeback_list.append("")

        #amount of listings currently posted
        try:
            currentlisting = driver.find_element_by_xpath('//a[@class="-for-sale-link"]').text
            amt_listings.append(currentlisting.replace("Listings for Sale", "").replace("Listing for Sale", "")) #currentlistings
        except NoSuchElementException:
            amt_listings.append("0")

        #description of listing
        try:
            description = driver.find_element_by_xpath('//div[@class="listing-description"]').text
            desc_list.append(description) #description
        except NoSuchElementException:
            desc_list.append("NA")

        #links to their profile
        try:
            profilelink=driver.find_element_by_xpath('//span[@class="Username"]/a').get_attribute("href")
            profile_links.append(profilelink) #profilelink
        except NoSuchElementException:
            profile_links.append("NA")

        #links to their feedback
        try:
            feedbacklink=driver.find_element_by_xpath('//div[@class="-details"]/a').get_attribute("href")
            feedback_links.append(feedbacklink) #feedbacklink
        except NoSuchElementException:
            feedback_links.append("NA")

        #amount of followers
        try:
            followercount=driver.find_element_by_xpath('//p[@class="-follower-count"]').text
            amt_followercount.append(followercount) #followercount not working since you would have to go to profile
        except NoSuchElementException:
            amt_followercount.append("NA")

        try:
            fullsize = driver.find_element_by_xpath('//h2[@class="listing-size sub-title"]').text
            full_size_desc.append(fullsize) #fullsize
        except NoSuchElementException:
            full_size_desc.append("NA")

        try:
            na_shipping = driver.find_elements_by_xpath("//*[contains(text(), 'shipping')]")
            h_shipping = driver.find_elements_by_xpath("//*[contains(text(), 'Shipping')]")
            if is_sold or (len(na_shipping) > 0 and len(na_shipping[0].text.split()) > 0):
                location_list.append("NA")
                shipping_list.append("NA")
            elif len(h_shipping) > 0 and len(h_shipping[0].text.split()) > 0 and is_sold == False:
                final_text = h_shipping[0].text.split()
                shipping = final_text[0].replace("+", "")
                location = final_text[2]
                location_list.append(location)
                shipping_list.append(shipping)
            else:
                location_list.append("NA")
                shipping_list.append("NA")

        except NoSuchElementException:
            location_list.append("NA")
            shipping_list.append("NA")

        numPics = len(bs.find_all("img", class_="PhotoGallery--Thumbnail"))
        amt_pictures.append(numPics) #picture number

    # Turn it into DataFrame
    #cols = [username_list, amt_sold, amt_feedback, amt_listings, desc_list, profile_links, feedback_links, amt_followercount, full_size_desc, location_list, amt_pictures, amt_transactions]

    seller_df = pd.DataFrame(zip(username_list,shipping_list, amt_sold, amt_feedback, amt_listings, desc_list, amt_likes, profile_links, feedback_links, full_size_desc, location_list, amt_pictures, links),
    columns = ['uname', 'ship_cost', 'amt_sold', 'amt_feedback', 'amt_listings', 'desc', 'amt_likes', 'prf_link', 'feed_link', 'size_desc', 'loc', 'amt_pics', 'Link'])
    return seller_df

def merge_df(user_input, unsold_df, sold_df):
    combined_df = unsold_df.append(sold_df)
    #combined_df.to_csv(DIRECTORY_PATH + "/data/" + user_input" + ".csv", index = False)
    return combined_df


"""
HELPER FUNCTIONS

"""
def extract_brand_name(container):
    brand_container = container.find_all("p", class_="listing-designer")
    brand = brand_container[0].text.strip()
    #brand = re.sub(r'[^a-zA-Z ]+', '', brand)
    brand = " ".join(brand.split())
    return brand

def extract_title(container):
    import string
    title_container = container.find_all("p", class_="listing-title")
    title = title_container[0].text.strip()
    title = " ".join(title.split())
    title = string.capwords(title)
    return title

def extract_date(container):
    #date_container = container.find_all("p", class_="listing-age")
    new_date = container.find_all("span", class_ = "date-ago")[0]
    new = new_date.text.strip().replace('about','').replace('ago', '')

    if container.find_all("span", class_="bumped date-ago"):
        old_date = container.find_all("span", class_ = "bumped date-ago")[0]
        old = old_date.text.strip().replace('(','').replace(')','').replace('about', '')
        return new,old
    else:
        old = "NA"
        return new,old

    return new,old

def extract_product_id(container):
    product_id_container = container.find_all("button", class_="heart-follow")
    #print(len(product_id_container))
    if len(product_id_container) > 0:
        pid = product_id_container[0].get('id')
    #print(pid)
        pid = pid[2:]
    else:
        pid = "NA"
    return pid

def extract_product_size(container):
    product_size_container = container.find_all("p", class_="listing-size")
    ps = product_size_container[0].text.strip()
    return ps

def extract_product_desc(container, user_input):
    product_desc_container = container.find_all("div", class_="truncate")
    pd = product_desc_container[0].text.strip()
    user_input = re.sub('-', ' ', user_input)
    for name in list(map(''.join, product(*(sorted({c.upper(), c.lower()} for c in user_input))))):
        pd = re.sub(name, '', pd)
    pd = re.sub(r'([^\s\w]|_)+', '', pd)
    pd = " ".join(pd.split()) #remove bad spacing between words
    return pd

def extract_price(container):
    original_price_container = container.find_all("p", class_="original-price")
    op = original_price_container[0].text.strip()
    if container.find_all("p", class_="new-price"):
        new_price_container = container.find_all("p", class_="new-price")
        np = new_price_container[0].text.strip()
        return op, np
    else:
        np = "NA"
        return op, np

def extract_sold_price(container):
    if container.find_all("p", class_="sold-price"):
        sold_price_container = container.find_all("p", class_="sold-price")
        sold = sold_price_container[0].text.strip()
        return sold
    else:
        sold = "NA"
        return sold

def calculate_price_reduction(old_price, new_price):
    if new_price != "NA":
        old_price = re.sub(r'[^0-9]', '', old_price)
        new_price = re.sub(r'[^0-9]', '', new_price)
        percentage = round(((1 - (float(new_price) / float(old_price))) * 100), 2)
        percentage = str(percentage) + "%"
        return percentage
    return "NA"

def get_image(listing, is_sold):
    total_link = "https://www.grailed.com" + listing
    if is_sold:
        xpath = "/html/body/div[9]/div/div[2]/div[2]/div/div/div[1]/div[2]/ul/li[1]/div/img"
    else:
        xpath = "/html/body/div[8]/div/div[2]/div[2]/div/div/div[1]/div[2]/ul/li[1]/div/img"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("disable-infobars"); # disabling infobars
    options.add_argument("--disable-extensions"); # disabling extensions
    options.add_argument("--disable-gpu"); # applicable to windows os only
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
    options.add_argument('--headless')

    #to not look like a bot
    from fake_useragent import UserAgent
    ua = UserAgent()
    userAgent = ua.random
    #print(str(userAgent))
    options.add_argument(f'user-agent={userAgent}')
    driver = webdriver.Chrome(WEBDRIVER_PATH, options=options)
    driver.get(total_link)
    image_link = driver.find_element_by_xpath(xpath).get_attribute("src")
    return image_link


def get_item_df(containers, display_amount, num_empty, user_input, is_sold):
    item_number = 1
    link_list = []
    product_id_list = []
    brand_name_list = []
    product_size_list = []
    title_list = []
    original_price_list = []
    new_price_list = []
    sold_price_list = []
    new_date_list = []
    old_date_list = []
    price_change_list = []
    is_sold_list = []

    for container in containers:
        #get features
        link_id = str(container.find('a', class_ = "listing-item-link")['href'])
        #print(link_id)
        product_id_list.append(extract_product_id(container))
        brand_name_list.append(extract_brand_name(container))
        product_size_list.append(extract_product_size(container))
        title_list.append(extract_title(container))
        new_date, old_date = extract_date(container)
        new_date_list.append(new_date)
        old_date_list.append(old_date)
        link_list.append(link_id)
        is_sold_list.append(is_sold)

        if is_sold:
            original_price_list.append("NA")
            new_price_list.append("NA")
            price_change_list.append( "NA")
            sold_price_list.append(extract_sold_price(container))
        else:
            original_price, new_price = extract_price(container)
            sold_price_list.append("NA")
            original_price_list.append(original_price)
            new_price_list.append(new_price)
            price_change = calculate_price_reduction(original_price, new_price)
            price_change_list.append(price_change)
        #stopping condition
        item_number +=1
        if item_number == (display_amount - num_empty + 1): #automatically subtracts 3
            item_df = pd.DataFrame(zip(product_id_list, brand_name_list, title_list, product_size_list, original_price_list, new_price_list, sold_price_list,is_sold_list, old_date_list, new_date_list, price_change_list, link_list),
            columns = ['pid', 'b_name', 'title', 'size', 'og_price', 'new_price', 'sold_price', 'is_sold', 'old_date', 'new_date', '%p_change', 'Link'])
            return link_list, item_df


def check_unlimited_scroll(display_amount, driver):
    item_count = 0
    loop_count = 0
    check_repeated = []
    while item_count < display_amount:

        bs = BeautifulSoup(driver.page_source, 'html.parser')
        item_count = len(bs.find_all("div", class_="feed-item"))
        check_repeated.append(item_count)

        """Not enough items to refresh"""
        """TODO: FIX"""
        if len(set(check_repeated)) != len(check_repeated):
            return driver, item_count

        loop_count = loop_count + 1

        print("Infinite Scroll Refresh iteration: " + str(loop_count) +
              " current item count: " + str(item_count) +
              " display amount: " + str(display_amount))

        page_length = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        while match == False:
            last_count = page_length
            time.sleep(3)
            page_length = driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if last_count == page_length:
                match = True
            break
    return driver, display_amount

    def test_html():
        options = webdriver.ChromeOptions()
        from fake_useragent import UserAgent
        ua = UserAgent()
        userAgent = ua.random
        options.add_argument(f'user-agent={userAgent}')
        #options.add_argument('--headless')
        options.add_argument('--lang=en_US')
        options.add_argument("--start-maximized") #fullscreen
        options.add_argument("disable-infobars"); # disabling infobars
        options.add_argument("--disable-extensions"); # disabling extensions
        options.add_argument("--disable-gpu"); # applicable to windows os only
        options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
        #options.add_argument("--no-sandbox");
        driver = webdriver.Chrome(WEBDRIVER_PATH, options=options)
        #link = "https://www.grailed.com/listings/20859074-supreme-supreme-box-logo-stickers-protection-sleeve-bogo"
        link = "https://www.grailed.com/listings/16759582-nike-x-vintage-nike-air-force-1"
        driver.get(link)

        bs = BeautifulSoup(driver.page_source, 'html.parser')

        #t = driver.find_element_by_xpath("/html/body/div[16]/div/span[1]").text
        t = driver.find_element_by_xpath("/html/body/div[16]/div/span[1]").text
        #print(t)


if __name__ == '__main__':
    """
    Run  - 1
    First time authentication and save cookies: first_run()

    Run  - 2
    Reuse cookies and use logged-in session: scrape()
    """
    input_name = sys.argv[1]
    amount_scrape = int(sys.argv[2]) #automatically subtracts 3

    #scrape_filter_sold(input_name, amount_scrape)

    unsold_df = scrape(input_name, amount_scrape)
    sold_df = scrape_filter_sold(input_name, amount_scrape)
    merge_df(input_name, unsold_df, sold_df)
