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
    time.sleep(2)

    password_sign_in = browser.find_element_by_id("passwordSignIn")
    password_sign_in.clear()
    password_sign_in.send_keys("Ktpp2002%^")
    time.sleep(2)

    sign_in_submit = browser.find_element_by_id("signInSubmit")
    sign_in_submit.click()


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
    actions.key_down(Keys.ARROW_LEFT)
    actions.perform()

    browser.find_element_by_id("showResults").click()

    # browser.find_element_by_name("searchCompanyTable_length").select_by_visible_text("100")
    # time.sleep(2)




def collect_search_results(browser):
    """
    Collect search results
    :param browser: valid browser object with open search results page
    :return:
    """
    search_company_table = browser.find_element_by_id("searchCompanyTable")
    time.sleep(1) #Some how doesn't work without delay here
    company_body = search_company_table.find_element_by_tag_name("tbody")
    rows = company_body.find_elements_by_tag_name("tr")
    print(len(rows))

    r = rows[1]
    # for r in rows:
    #     print("\n")
    #     print(r)
    # driver.get(self.base_url + "/iaApp/advancedsearch.htm")
    # Select(driver.find_element_by_name("searchCompanyTable_length")).select_by_visible_text("100")
    # driver.find_element_by_id("searchCompanyTable_next").click()
    # driver.find_element_by_id("searchCompanyTable_next").click()
    # driver.find_element_by_id("searchCompanyTable_next").click()
    # driver.find_element_by_id("searchCompanyTable_next").click()
    # driver.find_element_by_css_selector("#searchCompanyTable_paginate > input.validate").clear()
    # driver.find_element_by_css_selector("#searchCompanyTable_paginate > input.validate").send_keys("10")
    # driver.find_element_by_css_selector("#searchCompanyTable_paginate > input.validate").clear()
    # driver.find_element_by_css_selector("#searchCompanyTable_paginate > input.validate").send_keys("12")



def login_and_search():
    browser = _get_browser()
    login_to_owler(browser)
    time.sleep(5)
    make_advanced_search_request(browser)

    collect_search_results(browser)

    # browser.quit()

def main():
    config_logging()
    logging.info("-------- Start {} --------".format(conf.app_name))
    login_and_search()
    logging.info("-------- Finish {} -------".format(conf.app_name))

if __name__=="__main__":
    main()


