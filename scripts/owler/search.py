import conf
import logging
import time
from sqlitedict import SqliteDict
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element

from scripts.constants import *

def collect_profile_from_search(browser):
    """
    Collect search results
    :param browser: valid browser object with open search results page
    :return: dict with name-profile pairs
    """
    search_company_table = browser.find_element_by_id("searchCompanyTable")
    time.sleep(1) #Some how doesn't work without delay here
    company_body = search_company_table.find_element_by_tag_name("tbody")
    rows = company_body.find_elements_by_tag_name("tr")
    logging.info("Found {} rows in search page".format(len(rows)))

    profiles = dict()
    for r in rows:
        name = r.find_element_by_class_name("ellipsis").text
        profile = r.find_element_by_class_name("company_profile").get_attribute("href")
        url = r.find_elements_by_tag_name("a")[1].get_attribute("href")
        logging.info("Got: {}\t{}\t{}".format(name, url, profile))
        profiles[profile] = {
            TAG_PROFILE : profile,
            TAG_NAME : name,
            TAG_URL : url,
            TAG_PROCESSED: False
        }
    return profiles


def wait_for_processed(browser):
    def is_processed(some): # Check if request for new results finished
        processing = browser.find_element_by_id("searchCompanyTable_processing")
        return not processing.is_displayed()
    WebDriverWait(browser,30).until( is_processed )

def wait_for_advanced_search(browser, text):
    WebDriverWait(browser,30).until(
        text_to_be_present_in_element(
            (By.ID,"advancesearch_container"),
            text
        )
    )

def walk_through_search(browser):
    """
    Walk through search pages
    :param browser:
    :return:
    """
    profiles = SqliteDict(conf.db.db_file, autocommit=True)

    pages_txt = browser.find_element_by_class_name("paginate_of").text
    #filter numbers
    pages = int( ''.join(c for c in pages_txt if c.isdigit() ) )
    logging.info("Found {} pages".format(pages))

    # for p in range(20):
    for p in range(pages):
        logging.info("------- Process page #{} -------".format(p))
        profiles.update( collect_profile_from_search(browser) )
        browser.find_element_by_id("searchCompanyTable_next").click()
        wait_for_processed(browser)

    profiles.close()


def make_advanced_search(browser, funds_from, funds_to, year_from, year_to):
    funding_min = browser.find_element_by_id("funding_min")
    funding_max = browser.find_element_by_id("funding_max")
    companyAge_min = browser.find_element_by_id("companyAge_min")
    companyAge_max = browser.find_element_by_id("companyAge_max")

    def set_value(element, value): # Set value to hidden element
        browser.execute_script(
            "arguments[0].setAttribute('value', arguments[1])",
            element,
            value
        )

    if year_to >= 10: year_to = "*"
    if funds_to >= 100*ONE_M: funds_to = "*"

    set_value(funding_min, funds_from)
    set_value(funding_max, funds_to)
    set_value(companyAge_min, year_from)
    set_value(companyAge_max, year_to)

    browser.find_element_by_id("showResults").click()
    wait_for_advanced_search(browser, "Advanced Search Results")

    select = Select(browser.find_element_by_name("searchCompanyTable_length"))
    select.select_by_value("100")
    wait_for_processed(browser)




def iterate_through_search(browser,
                           funds_from,
                           funds_to,
                           funds_gap,
                           funds_step,
                           year_from,
                           year_to,
                           year_gap,
                           year_step):
    """
    Make advanced search request
    :param browser: valid browser object
    :return: browser object with applied search
    """
    advanced_search = browser.find_element_by_class_name("advncd-search")
    advanced_search.click()
    funds_l = funds_from
    funds_r = funds_from + funds_gap

    while funds_r <= funds_to:
        year_l = year_from
        year_r = year_from+year_gap
        while year_r <= year_to:

            make_advanced_search(browser, funds_l, funds_r, year_l, year_r)
            dataTables_info = browser.find_element_by_class_name("dataTables_info")
            logging.info("Years from {} to {}, Funds from {} to {}, {}".format(
                year_l, year_r, funds_l, funds_r, dataTables_info.text
            ))

            print("Years from {} to {}, Funds from {} to {}, {}".format(
                year_l, year_r, funds_l, funds_r, dataTables_info.text
            ))

            walk_through_search(browser)

            browser.find_element_by_link_text("< BACK TO MY SEARCH CRITERIA").click()
            wait_for_advanced_search(browser, "Advanced Search")

            year_l += year_step
            year_r += year_step
        funds_l += funds_step
        funds_r += funds_step

