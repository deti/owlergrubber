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
from functools import wraps
from sqlitedict import SqliteDict
from selenium import webdriver

from owler.general import login_to_owler
from owler.search import iterate_through_search
from owler.profile import get_profile
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
                           funds_from=10 * ONE_M,
                           funds_to=50 * ONE_M,
                           funds_gap=40 * ONE_M,
                           funds_step=10 * ONE_M,
                           year_from=0,
                           year_to=8,
                           year_gap=8,
                           year_step=1)
    browser.quit()


    # browser = _get_browser()
    # login_to_owler(browser)
    # iterate_through_search(browser,
    # funds_from=0,
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


def collect_profiles_data():
    profiles = SqliteDict(conf.db.db_file, autocommit=True)
    browser = _get_browser()
    login_to_owler(browser)

    for url in profiles.keys():
        if not profiles[url][TAG_PROCESSED]:
            profiles[url].update(get_profile(browser, url))
            profiles[url][TAG_PROCESSED] = True
    browser.quit()
    profiles.close()


def main():
    config_logging()
    logging.info("-------- Start {} --------".format(conf.app_name))
    # collect_profiles_links()
    collect_profiles_data()
    logging.info("-------- Finish {} -------".format(conf.app_name))


if __name__ == "__main__":
    main()


