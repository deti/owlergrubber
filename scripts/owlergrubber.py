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

from owler.general import login_to_owler
from owler.search import iterate_through_search
from owler.profile import retrive_profiles
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


def _get_browser():
    return webdriver.Firefox()


def collect_profiles_links():
    browser = _get_browser()
    login_to_owler(browser)
    iterate_through_search(browser,
                           funds_from=10*ONE_M,
                           funds_to=50*ONE_M,
                           funds_gap=40*ONE_M,
                           funds_step=10*ONE_M,
                           year_from=0,
                           year_to=8,
                           year_gap=8,
                           year_step=1)
    browser.quit()


    # browser = _get_browser()
    # login_to_owler(browser)
    # iterate_through_search(browser,
    #                        funds_from=0,
    #                        funds_to=10*ONE_M,
    #                        funds_gap=2*ONE_M,
    #                        funds_step=ONE_M,
    #                        year_from=0,
    #                        year_to=8,
    #                        year_gap=2,
    #                        year_step=1)
    # browser.quit()
    # browser = _get_browser()
    # login_to_owler(browser)
    # iterate_through_search(browser,
    #                        funds_from=10*ONE_M,
    #                        funds_to=100*ONE_M,
    #                        funds_gap=10*ONE_M,
    #                        funds_step=10*ONE_M,
    #                        year_from=0,
    #                        year_to=8,
    #                        year_gap=2,
    #                        year_step=1)
    # browser.quit()

def get_profiles():
    browser = _get_browser()
    retrive_profiles(browser)
    browser.quit()

def main():
    config_logging()
    logging.info("-------- Start {} --------".format(conf.app_name))
    collect_profiles_links()
    get_profiles()
    logging.info("-------- Finish {} -------".format(conf.app_name))

if __name__=="__main__":
    main()


