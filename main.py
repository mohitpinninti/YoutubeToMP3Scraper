import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# imports for try block
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# path to web driver
PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)

# ask for input for search term
search_term = input("What would you like to look for? ")
search_term = search_term.replace(" ", "+")
# print(search_term)

# navigating to youtube
driver.get("https://youtube.com/results?search_query=" + search_term)
print(driver.title)


try:
    # search_results is used to get all of the text data for the top result to display video name+channel name
    search_results = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "contents")))
    video_data = search_results.find_element_by_class_name("ytd-video-renderer")
    video_name = video_data.find_element_by_id("title-wrapper")
    channel_name = video_data.find_element_by_id("channel-info")
    print("VIDEO NAME AND CHANNEL NAME ONLY: " + video_name.text + "  -  " + channel_name.text)
    # getting video url
    video_url = video_data.find_element_by_id("thumbnail").get_attribute("href")
    if video_url is None:
        raise Exception("You done goofed")
    print("Video Link: " + video_url)

except Exception as e:
    logging.exception(e)
    driver.quit()
    exit()




# navigating to downloading website and pasting link
driver.get("https://ytmp3.cc/downloader/")
search_box = driver.find_element_by_tag_name("input")
print(search_box.text)
search_box.send_keys(video_url)
search_box.send_keys(Keys.RETURN)


try:
    buttons_div = driver.find_element_by_id("buttons")
    download_link = WebDriverWait(driver, 30).until(ec.element_to_be_clickable((By.LINK_TEXT, "Download")))
    download_link.click()

except Exception as e:
    logging.exception(e)
    driver.quit()
    exit()