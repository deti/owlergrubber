__author__ = 'deti'

import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located


from constants import *

test_profiles = [
    "https://www.owler.com/iaApp/1855459/lodging-opportunity-fund-company-profile",
    "https://www.owler.com/iaApp/4733500/springpath-company-profile",
    "https://www.owler.com/iaApp/716945/minesto-company-profile",
    "https://www.owler.com/iaApp/223273/acfun-company-profile",
    "https://www.owler.com/iaApp/1574811/graymatter-company-profile",
    "https://www.owler.com/iaApp/219185/modumetal-company-profile"
]


def get_text_by_id(element, _id):
    try:
        txt = element.find_element_by_id(_id).text
    except NoSuchElementException:
        txt = None
    return txt


def get_text_by_class_name(element, class_name):
    try:
        txt = element.find_element_by_class_name(class_name).text
    except NoSuchElementException:
        txt = None
    return txt


def get_href_by_class_name(element, class_name):
    try:
        href = element.find_element_by_class_name(class_name).get_attribute("href")
    except NoSuchElementException:
        href = None
    return href



def get_profile(browser, url):
    browser.get(url)

    WebDriverWait(browser,30).until(
        presence_of_element_located(
            (By.ID,"fundings")
        )
    )


    company_name = get_text_by_id(browser, "companyName")
    description = get_text_by_id(browser, "description")
    founded_year = get_text_by_id(browser, "foundedYear")
    funding_total = get_text_by_id(browser, "fundingTotal")
    if funding_total:
        funding_total = funding_total.replace("TOTAL", "")

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
        last_amt = get_text_by_class_name(details[0], "amt")
        last_date = get_text_by_class_name(details[0],"date")
        last_source = get_href_by_class_name(details[0], "invsource")
        last_investors = get_text_by_class_name(details[0],"investors")

    previous_amt = None
    previous_date = None
    previous_source = None
    previous_investors = None
    if len(details) > 1:
        previous_amt = get_text_by_class_name(details[1],"amt")
        previous_date = get_text_by_class_name(details[1],"date")
        previous_source = get_href_by_class_name(details[1], "invsource")
        previous_investors = get_text_by_class_name(details[1],"investors")

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
        TAG_COMPANY_NAME : company_name,
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

