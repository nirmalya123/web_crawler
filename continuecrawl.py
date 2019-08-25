import os
import sys
import time
# from flask import Flask
import urllib

# from urllib import urllib.parse
# import urllib.parse

import bs4
import requests
from pprint import pprint

from logger import logger

from collections import Counter


# http://localhost:8080/wikipedia_en_simple_all_nopic/A/
# http://localhost:8080/random?content=wikipedia_en_simple_all_nopic
#                      /random?content=wikipedia_en_simple_all_nopic

main_dict = {}  # URL - Count
target_count_list = []

wikiname = "wikipedia_en_all_nopic"
if True:
    # start_url = "http://localhost:8080/index.php/Special:Random"
    # target_url = "http://localhost:8080/index.php/Philosophy"
    # site_url = "http://localhost:8080/"
    start_url = "http://localhost:8080/random?content={}".format(wikiname)
    target_url = [
        "http://localhost:8080/{}/A/Communication.html".format(wikiname),
        "http://localhost:8080/{}/A/Philosophy.html".format(wikiname),
        "http://localhost:8080/{}/A/Psychology.html".format(wikiname),
        "http://localhost:8080/{}/A/Science.html".format(wikiname),
        "http://localhost:8080/{}/A/Country.html".format(wikiname),
        "http://localhost:8080/{}/A/Language.html".format(wikiname),
        ]

    site_url = "http://localhost:8080/{}/A/".format(wikiname)
else:
    start_url = "https://en.wikipedia.org/wiki/Special:Random"
    target_url = "https://en.wikipedia.org/wiki/Philosophy"
    site_url = "https://en.wikipedia.org/"


def find_first_link(url):
    try:
        response = requests.get(url)
        html = response.text
        # logger.debug(">>>>>> {}".format(response.url))
        soup = bs4.BeautifulSoup(html, "html.parser")

        # This div contains the article's body
        # (June 2017 Note: Body nested in two div tags)
        # content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")
        # content_div = soup.find(id="mw-content-text")  # [ND]
        content_div = soup.find("div", {"class": "mw-content-text"})
        # logger.debug("{}".format(content_div))
        content_section = soup.find("section", {"data-mw-section-id": "0"})

        # stores the first link found in the article, if the article contains no
        # links this value will remain None
        article_link = None

        # Find all the direct children of content_div that are paragraphs
        # for element in content_div.find_all("p", recursive=False):
        for element in content_section.find_all("p", recursive=False):
            # Find the first anchor tag that's a direct child of a paragraph.
            # It's important to only look at direct children, because other types
            # of link, e.g. footnotes and pronunciation, could come before the
            # first link to an article. Those other link types aren't direct
            # children though, they're in divs of various classes.
            if element.find("a", recursive=False):
                article_link = element.find("a", recursive=False).get('href')
                break
    except Exception as e:
        logger.error("Exception while parsing html. {}".format(e))
        return (None, None)

    if not article_link:
        return (None, None)

    # Build a full url from the relative article_link url
    first_link = urllib.parse.urljoin(site_url, article_link)

    return (first_link, response.url)


def continue_crawl(search_history, target_url, max_steps=25):
    if search_history[-1] in target_url:
        logger.info("We've found the target article!")
        target_count_list.append(target_url[-1])
        return False
    elif len(search_history) > max_steps:
        logger.warning("The search has gone on suspiciously long, aborting search!")
        return False
    elif search_history[-1] in search_history[:-1]:
        logger.warning("We've arrived at an article we've already seen, aborting search!")
        return False
    else:
        return True

# article_chain = [start_url]


def run_crawler():
    count = 0
    random_resp_url = None
    while continue_crawl(article_chain, target_url):
        logger.info("{} - Article to crawl - {}".format(count, article_chain[-1]))
        first_link, resp_url = find_first_link(article_chain[-1])
        if not first_link:
            logger.warning("We've arrived at an article with no links, aborting search!")
            break
        if count == 0:
            random_resp_url = resp_url
        article_chain.append(first_link)
        count = count + 1
        # time.sleep(3)  # Slow things down so as to not hammer Wikipedia's servers
    logger.info("-------------------------------------")
    main_dict[random_resp_url] = count
    logger.info("| {} --- {}".format(random_resp_url, count))
    logger.info("-------------------------------------")

if __name__ == "__main__":
    for i in range(100):
        logger.info(">>>>>>>>>>>>>>>>>")
        logger.info(">>>>>>>>>>>>>>>>> {} <<<<<<<<<<<<<<<<<<<<".format(i))
        logger.info(">>>>>>>>>>>>>>>>>")
        article_chain = [start_url]
        run_crawler()

    logger.info("-------------------------------------")
    pprint(main_dict)
    logger.info("-------------------------------------")
    logger.info("-------------------------------------")
    # pprint(target_count_list)
    c = Counter(target_count_list)
    pprint(c)
    logger.info("-------------------------------------")


