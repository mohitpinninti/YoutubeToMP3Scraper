import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import wget
# imports for try block
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# path to web driver
driver_path = "C:/Program Files (x86)/chromedriver.exe"

print("Welcome to the Youtube to MP3 Downloader Tool")

while 1:
    # ask for input for search term
    search_term = input("What video would you like to download an MP3 of? (Type \"nothing\" if nothing is needed: ")
    if search_term.lower() == "nothing":
        break
    search_term = search_term.replace(" ", "+")
    # print(search_term)

    # navigating to youtube
    driver = webdriver.Chrome(driver_path)
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
        # goal of this try block is to click the download button once it appears
        buttons_div = driver.find_element_by_id("buttons")
        download_link = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, "Download")))
        download_link = download_link.get_attribute("href")
        print("Download Link: " + download_link)

        # next few lines are intermission of try block to get the name of the downloadable element before download
        name_of_downloadable = driver.find_element_by_id("title").text
        print("Name of downloadable: " + name_of_downloadable)

        os.chdir("C:\\Users\\pinni\\Downloads\\")
        retval = os.getcwd()
        print("Current working directory %s" % retval)
        wget.download(download_link)
        print("Download Complete!")

    except Exception as e:
        print("Unable to Download " + name_of_downloadable)
        logging.exception(e)
        driver.quit()
        exit()

    driver.quit()

print("Sounds like you're done. Have fun listening!")
