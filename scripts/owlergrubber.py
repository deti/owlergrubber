__author__ = 'deti'
"""
API & documentation
https://github.com/toggl/toggl_api_docs
https://dev.evernote.com/doc/start/python.php

https://dev.evernote.com/doc/reference/
https://dev.evernote.com/doc/
"""
import conf
import logging
import time
from functools import wraps
from sqlitedict import SqliteDict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element

from constants import *

def config_logging():
    import os
    if not os.path.exists(conf.logging.log_dir):
        os.mkdir(conf.logging.log_dir)
    logging.basicConfig(filename=conf.logging.log_file,
                        format=conf.logging.format,
                        level=conf.logging.level)


def debug_decorator(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        logging.debug("{} called".format(func.__name__))
        result = func(*args, **kwargs)
        log_str = "{} finished".format(func.__name__)
        if result:
            log_str = "{}. Result: {}".format(log_str, result)
        logging.debug(log_str)
        return result
    return func_wrapper


def try_seleinum():
    browser = webdriver.Firefox()
    browser.get('http://www.yahoo.com')
    assert 'Yahoo' in browser.title
    elem = browser.find_element_by_name('p')  # Find the search box
    elem.send_keys('seleniumhq' + Keys.RETURN)
    browser.quit()

def _get_browser():
    return webdriver.Firefox()

def login_to_owler(browser):
    """
    Log in to Owler
    :param browser: object
    :return: Browser object with alive session into Owler
    """
    browser.get(conf.owler.url)
    assert "Owler: Competitive Intelligence for Better Business Decisions" in browser.title
    browser.find_element_by_id("signInLink").click()

    email_sign_in = browser.find_element_by_id("emailSignIn")
    email_sign_in.clear()
    email_sign_in.send_keys("detijazzz@yandex.ru")

    password_sign_in = browser.find_element_by_id("passwordSignIn")
    password_sign_in.clear()
    password_sign_in.send_keys("Ktpp2002%^")

    sign_in_submit = browser.find_element_by_id("signInSubmit")
    sign_in_submit.click()
    time.sleep(1)


def make_advanced_search_request(browser):
    """
    Make advanced search request
    :param browser: valid browser object
    :return: browser object with applied search
    """
    advanced_search = browser.find_element_by_class_name("advncd-search")
    advanced_search.click()

    company_age_slider = browser.find_element_by_xpath("//*[contains(text(), '10 YRS+')]")
    actions = ActionChains(browser)
    actions.move_to_element(company_age_slider)
    actions.click(company_age_slider)
    actions.key_down(Keys.ARROW_LEFT)
    actions.key_up(Keys.ARROW_LEFT)
    actions.perform()

    browser.find_element_by_id("showResults").click()
    time.sleep(5)

    select = Select(browser.find_element_by_name("searchCompanyTable_length"))
    select.select_by_value("100")
    time.sleep(2)


def collect_search_results(browser):
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
            PROFILE : profile,
            NAME : name,
            URL : url,
            PROCESSED: False
        }
    return profiles



def walk_through(browser):
    """
    Walk through passed pages
    :param browser:
    :return:
    """
    profiles = SqliteDict(conf.db.db_file, autocommit=True)

    pages_txt = browser.find_element_by_class_name("paginate_of").text
    #filter numbers
    pages = int( ''.join(c for c in pages_txt if c.isdigit() ) )
    logging.info("Found {} pages".format(pages))

    def is_processed(some):
        """ Check if request for new results finished """
        processing = browser.find_element_by_id("searchCompanyTable_processing")
        return not processing.is_displayed()

    # for p in range(20):
    for p in range(pages):
        logging.info("------- Process page #{} -------".format(p))
        profiles.update( collect_search_results(browser) )
        browser.find_element_by_id("searchCompanyTable_next").click()
        WebDriverWait(browser,30).until( is_processed )

    profiles.close()


def login_and_search():
    browser = _get_browser()
    login_to_owler(browser)
    time.sleep(2)
    make_advanced_search_request(browser)

    walk_through(browser)
    browser.quit()


def wait_for_advanced_search(browser, text):
    WebDriverWait(browser,30).until(
        text_to_be_present_in_element(
            (By.ID,"advancesearch_container"),
            text
        )
    )



def make_advanced_request(browser, funds_from, funds_to, year_from, year_to):
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

    set_value(funding_min, funds_from)
    set_value(funding_max, funds_to)
    set_value(companyAge_min, year_from)
    set_value(companyAge_max, year_to)

    browser.find_element_by_id("showResults").click()
    wait_for_advanced_search(browser, "Advanced Search Results")




def play_with_funding_sliders(browser):
    """
    Make advanced search request
    :param browser: valid browser object
    :return: browser object with applied search
    """
    advanced_search = browser.find_element_by_class_name("advncd-search")
    advanced_search.click()
    for funds in range (2):
        for year in range(2):
            f = funds*5*ONE_M
            make_advanced_request(
                browser, f , 10*ONE_M + f, year, 2+year
            )
            dataTables_info = browser.find_element_by_class_name("dataTables_info")
            print("-----------------")
            print("Funds from {}M to {}M".format(funds*5, 10+funds*5))
            print("Years from {} to {}".format(year, 2+year))
            print(dataTables_info.text)

            browser.find_element_by_link_text("< BACK TO MY SEARCH CRITERIA").click()
            # browser.find_element_by_link_text("BACK TO MY SEARCH CRITERIA").click()
            # browser.find_element_by_class_name("back").click()
            wait_for_advanced_search(browser, "Advanced Search")



def play_with_queries():
    browser = _get_browser()
    login_to_owler(browser)
    time.sleep(2)
    play_with_funding_sliders(browser)

def main():
    config_logging()
    logging.info("-------- Start {} --------".format(conf.app_name))
    # login_and_search()
    play_with_queries()
    logging.info("-------- Finish {} -------".format(conf.app_name))

if __name__=="__main__":
    main()


