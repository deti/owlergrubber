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

from constants import *

from owler.general import login_to_owler
from owler.search import iterate_through_search
from owler.profile import get_profile

from os import path


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
    """
    Collect all profile links from Owler through search.
    Save all links to DB
    """
    browser = _get_browser()
    login_to_owler(browser)
    iterate_through_search(browser,
                           funds_start=conf.funds.start * ONE_M,
                           funds_finish=conf.funds.finish * ONE_M,
                           funds_gap=conf.funds.gap*ONE_M,
                           funds_step=conf.funds.step*ONE_M,
                           year_start=conf.year.start,
                           year_finish=conf.year.finish,
                           year_gap=conf.year.gap,
                           year_step=conf.year.step)
    browser.quit()


def collect_profiles_data():
    """
    Get profile data for profiles in DB
    """
    profiles = SqliteDict(conf.db.db_file, autocommit=True)
    browser = _get_browser()
    login_to_owler(browser)

    i = 1
    for url in profiles.keys():
        d = profiles[url]
        if not profiles[url][TAG_PROCESSED]:
            r = get_profile(browser, url)
            d.update(r)
            d[TAG_PROCESSED] = True
            profiles[url] = d
            logging.info("Processed {}: {}".format(i, profiles[url] ))
        i +=1

    browser.quit()
    profiles.close()

def export_db_to_csv(in_db, out_csv):
    """
    Export info from DataBase to CSV file
    :param in_db: path to database
    :param out_csv: path to output csv file
    """
    profiles = SqliteDict(in_db, autocommit=False)

    def get_values(values, tags):
        res = list()
        for tag in tags:
            s = values.get(tag, NO_VALUE) or  NO_VALUE
            res.append( s.replace("\n", ", "))
        return res

    out = open(out_csv, "w")

    values_tags = (
        TAG_NAME,
        TAG_DESCRIPTION,
        TAG_URL,
        TAG_PROFILE,
        TAG_FOUNDED_YEAR,
        TAG_FUNDING_TOTAL,
        TAG_LAST_AMT,
        TAG_LAST_DATE,
        TAG_LAST_SOURCE,
        TAG_LAST_INVESTORS,
        TAG_PREVIOUS_AMT,
        TAG_PREVIOUS_DATE,
        TAG_PREVIOUS_SOURCE,
        TAG_PREVIOUS_INVESTORS
    )

    out.write("{}\n".format(
            "\t".join( values_tags )
        ))

    i = 1
    total_count = 20
    for k in profiles.keys():
        profile = profiles[k]
        out.write("{}\n".format(
            "\t".join( get_values( profile, values_tags) )
        ))
        # if i > total_count: break
        # i += 1

    out.close()
    profiles.close()

def merge_dbs(input_list, output_file):
    """
    Merge several DBs into one output file
    :param input_list: list of paths to DBs
    :param output_file: path to result DB
    """
    outdb = SqliteDict(output_file, autocommit=True)
    for input_name in input_list:
        indb = SqliteDict(input_name, autocommit=False)
        outdb.update(indb)
        indb.close()
    outdb.close()

def search_and_save_csv(key_words, out_filename):
    """
    Search for key words in project description and save relevant rows to output csv file
    :param key_words: list of key words
    :param out_filename: output csv file name
    :return:
    """
    tmp_db_file_name = path.join(conf.db.db_dir, out_filename+".sqlite")
    tmpdb = SqliteDict(tmp_db_file_name, autocommit=True)
    indb = SqliteDict(conf.db.db_file, autocommit=False)

    key_words = [kw.lower() for kw in key_words]

    for k in indb.keys():
        description = indb[k][TAG_DESCRIPTION].lower()
        for word in key_words:
            if description.find(word) >= 0:
                tmpdb[k] = indb[k]
    tmpdb.close()
    indb.close()
    export_db_to_csv(tmp_db_file_name, out_filename+".csv")



def collect_profiles():
    config_logging()
    logging.info("-------- Start {} collect_profiles --------".format(conf.app_name))
    collect_profiles_links()
    collect_profiles_data()
    export_db_to_csv(conf.db.db_file, "out.csv")
    logging.info("-------- Finish {} collect_profiles -------".format(conf.app_name))


def search_for_words():
    config_logging()
    logging.info("-------- Start {} search_for_words --------".format(conf.app_name))
    for r in conf.requests:
        search_and_save_csv(conf.requests[r], r)
    logging.info("-------- Finish {} search_for_words -------".format(conf.app_name))

def main():
    config_logging()
    logging.info("-------- Start {} --------".format(conf.app_name))
    collect_profiles()
    search_for_words()
    logging.info("-------- Finish {} -------".format(conf.app_name))

if __name__ == "__main__":
    main()


