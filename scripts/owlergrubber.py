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
from selenium.webdriver.common.keys import Keys

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

def main():
    config_logging()
    logging.info("-------- Start {} --------".format(conf.app_name))
    try_seleinum()
    logging.info("-------- Finish {} -------".format(conf.app_name))

if __name__=="__main__":
    main()


