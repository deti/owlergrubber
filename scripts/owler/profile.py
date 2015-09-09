__author__ = 'deti'

import logging

from selenium.common.exceptions import NoSuchElementException
from scripts.constants import *


test_profiles = [
    "https://www.owler.com/iaApp/1855459/lodging-opportunity-fund-company-profile",
    "https://www.owler.com/iaApp/4733500/springpath-company-profile",
    "https://www.owler.com/iaApp/716945/minesto-company-profile",
    "https://www.owler.com/iaApp/223273/acfun-company-profile",
    "https://www.owler.com/iaApp/1574811/graymatter-company-profile",
    "https://www.owler.com/iaApp/219185/modumetal-company-profile"
]


def get_profile(browser, url):
    browser.get(url)

    try:
        description = browser.find_element_by_id("description").text
    except NoSuchElementException:
        description = None

    try:
        founded_year = browser.find_element_by_id("foundedYear").text
    except NoSuchElementException:
        founded_year = None

    try:
        funding_total = browser.find_element_by_id("fundingTotal").text.replace("TOTAL", "")
    except NoSuchElementException:
        funding_total = None

    try:
        funding_table = browser.find_element_by_id("fundingTable")
        details = funding_table.find_elements_by_class_name("details")
    except NoSuchElementException:
        details = ()

    last_amt = None
    last_date = None
    last_source = None
    last_investors = None
    if details:
        last_amt = details[0].find_element_by_class_name("amt").text
        last_date = details[0].find_element_by_class_name("date").text
        last_source = details[0].find_element_by_class_name("invsource").get_attribute("href")
        last_investors = details[0].find_element_by_class_name("investors").text

    previous_amt = None
    previous_date = None
    previous_source = None
    previous_investors = None
    if len(details) > 1:
        previous_amt = details[1].find_element_by_class_name("amt").text
        previous_date = details[1].find_element_by_class_name("date").text
        previous_source = details[1].find_element_by_class_name("invsource").get_attribute("href")
        previous_investors = details[1].find_element_by_class_name("investors").text

    # print("---------------------------------------------------------------------")
    # print("url: {}".format(url))
    # print("description: {}".format(description))
    # print("founded_year: {}".format(founded_year))
    # print("funding_total: {}".format(funding_total))
    # print("last_amt: {}".format(last_amt))
    # print("last_date: {}".format(last_date))
    # print("last_source: {}".format(last_source))
    # print("last_investors: {}".format(last_investors))
    # print("previous_amt: {}".format(previous_amt))
    # print("previous_date: {}".format(previous_date))
    # print("previous_source: {}".format(previous_source))
    # print("previous_investors: {}".format(previous_investors))

    profile = {
        TAG_DESCRIPTION: description,
        TAG_FOUNDED_YEAR: founded_year,
        TAG_FUNDING_TOTAL: funding_total,
        TAG_LAST_AMT: last_amt,
        TAG_LAST_DATE: last_date,
        TAG_LAST_INVESTORS: last_investors,
        TAG_LAST_SOURCE: last_source,
        TAG_PREVIOUS_AMT: previous_amt,
        TAG_PREVIOUS_DATE: previous_date,
        TAG_PREVIOUS_INVESTORS: previous_investors,
        TAG_PREVIOUS_SOURCE: previous_source
    }
    # logging.info(profile)
    return profile

