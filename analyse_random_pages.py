import os
import sys
import time
# from flask import Flask
import urllib

# from urllib import urllib.parse
# import urllib.parse

import bs4
import requests

from logger import logger
from pprint import pprint

from collections import Counter
random_link_list = []

# http://localhost:8080/wikipedia_en_simple_all_nopic/A/
# http://localhost:8080/random?content=wikipedia_en_simple_all_nopic
#                      /random?content=wikipedia_en_simple_all_nopic
wikiname = "wikipedia_en_all_nopic"
if True:
    # start_url = "http://localhost:8080/index.php/Special:Random"
    # target_url = "http://localhost:8080/index.php/Philosophy"
    # site_url = "http://localhost:8080/"
    start_url = "http://localhost:8080/random?content={}".format(wikiname)
    # target_url = [
    #     # "http://localhost:8080/{}/A/Communication.html".format(wikiname),
    #     # "http://localhost:8080/{}/A/Philosophy.html".format(wikiname),
    #     # "http://localhost:8080/{}/A/Psychology.html".format(wikiname),
    #     # "http://localhost:8080/{}/A/Science.html".format(wikiname),
    #     # "http://localhost:8080/{}/A/Country.html".format(wikiname),
    #     # "http://localhost:8080/{}/A/Language.html".format(wikiname),
    #     ]

    site_url = "http://localhost:8080/{}/A/".format(wikiname)
else:
    start_url = "https://en.wikipedia.org/wiki/Special:Random"
    target_url = "https://en.wikipedia.org/wiki/Philosophy"
    site_url = "https://en.wikipedia.org/"


def run_crawler():
    for i in range(100):
        response = requests.get(start_url)
        logger.debug("{} --- {}".format(i, response.url))
        random_link_list.append(response.url)
        # time.sleep(3)  # Slow things down so as to not hammer Wikipedia's servers

    c = Counter(random_link_list)
    logger.info("-------------------------------------")
    pprint(c)
    logger.info("-------------------------------------")

if __name__ == "__main__":
    run_crawler()
