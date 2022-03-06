from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

import json

keyword = input("Enter the keyword : ")

option = Options()
option.headless = False

driver = webdriver.Chrome(options=option)
driver.implicitly_wait(5)
baseUrl = "https://youtube.com/"


def getChannelUrl():
    driver.get(f"{baseUrl}/search?q={keyword}")
    time.sleep(3)
    allChannelList = driver.find_elements_by_css_selector(
        "#text.style-scope.ytd-channel-name a.yt-simple-endpoint.style-scope.yt-formatted-string")
    links = list(dict.fromkeys(
        map(lambda a: a.get_attribute("href"), allChannelList)))
    return links


def getChannelDetails(urls):
    details = []
    for url in urls:
        driver.get(f"{url}/about")
        cname = driver.find_element_by_css_selector(
            "#text.style-scope.ytd-channel-name").text
        cDess = driver.find_element_by_css_selector(
            "#description-container > yt-formatted-string:nth-child(2)").text
        clink = url
        otherLinkObj = driver.find_elements_by_css_selector(
            "#link-list-container.style-scope.ytd-channel-about-metadata-renderer a.yt-simple-endpoint.style-scope.ytd-channel-about-metadata-renderer")
        otherLinks = list(dict.fromkeys(
            map(lambda a: a.get_attribute("href"), otherLinkObj)))

        obj = {
            "cname": cname,
            "curl": clink,
            "cdesc": cDess,
            "otherLinks": otherLinks
        }
        details.append(obj)
    data = pd.DataFrame(details)
    data.to_excel("CategoryDB.xlsx")
    return details


if __name__ == "__main__":
    allChannelUrls = getChannelUrl()
    allChannelDetails = getChannelDetails(allChannelUrls)
    print(json.dumps(allChannelDetails, indent=4))
