import os
import sys
import time
# from flask import Flask
import urllib
import threading
import time
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

main_dict_lock = threading.Lock()
target_count_list_lock = threading.Lock()

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
        logger.debug("Exception while parsing html. {}".format(e))
        return (None, None)

    if not article_link:
        return (None, None)

    # Build a full url from the relative article_link url
    first_link = urllib.parse.urljoin(site_url, article_link)

    return (first_link, response.url)


def continue_crawl(search_history, target_url, max_steps=25):
    if search_history[-1] in target_url:
        logger.debug("We've found the target article!")
        with target_count_list_lock:
            target_count_list.append(target_url[-1])
        return False
    elif len(search_history) > max_steps:
        logger.debug("The search has gone on suspiciously long, aborting search!")
        return False
    elif search_history[-1] in search_history[:-1]:
        logger.debug("We've arrived at an article we've already seen, aborting search!")
        return False
    else:
        return True


def run_crawler(loop_count):
    article_chain = [start_url]
    for i in range(loop_count):
        count = 0
        random_resp_url = None
        while continue_crawl(article_chain, target_url):
            logger.debug("{} - Article to crawl - {}".format(count, article_chain[-1]))
            first_link, resp_url = find_first_link(article_chain[-1])
            if not first_link:
                logger.debug("We've arrived at an article with no links, aborting search!")
                break
            if count == 0:
                random_resp_url = resp_url
            article_chain.append(first_link)
            count = count + 1
            # time.sleep(3)  # Slow things down so as to not hammer Wikipedia's servers
        logger.debug("-------------------------------------")
        with main_dict_lock:
            main_dict[random_resp_url] = count
        logger.debug("| {} --- {}".format(random_resp_url, count))
        logger.debug("-------------------------------------")

if __name__ == "__main__":
    time_data_dict = {}
    main_count = 10
    l = [1]
    l.extend(range(2, main_count+2, 2))
    for j in l:
        start_time = time.time()
        total_iteration = 10
        block_count = j
        main_loop = total_iteration // block_count
        threads = list()
        for i in range(main_loop):
            logger.debug(">>>>>>>>>>>>>>>>>")
            logger.debug(">>>>>>>>>>>>>>>>> {} <<<<<<<<<<<<<<<<<<<<".format(i))
            logger.debug(">>>>>>>>>>>>>>>>>")
            x = threading.Thread(target=run_crawler, args=(block_count,))
            threads.append(x)
            x.start()
            # article_chain = [start_url]

            # run_crawler(block_count)
        for index, thread in enumerate(threads):
            thread.join()
        time_data_dict[j] = time.time() - start_time
        logger.info("#Threads {} --- #URL {} --- Time {}".format(main_loop, block_count, time_data_dict[j]))
        # logger.info("-------------------------------------")
        # with main_dict_lock:
        #     pprint(main_dict)
        # logger.info("-------------------------------------")
        # logger.info("-------------------------------------")
        # pprint(target_count_list)
        # with target_count_list_lock:
        #     c = Counter(target_count_list)
        # pprint(c)
        # logger.info("-------------------------------------")
        # pprint(time_data_dict)
        # time.sleep(5)

    logger.info("====================================================")
    logger.info("====================================================")
    pprint(time_data_dict)
    logger.info("====================================================")
    logger.info("====================================================")
