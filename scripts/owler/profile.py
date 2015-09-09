__author__ = 'deti'

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

test_profiles = [
    "https://www.owler.com/iaApp/1855459/lodging-opportunity-fund-company-profile",
    "https://www.owler.com/iaApp/4733500/springpath-company-profile",
    "https://www.owler.com/iaApp/716945/minesto-company-profile",
    "https://www.owler.com/iaApp/223273/acfun-company-profile",
    "https://www.owler.com/iaApp/1574811/graymatter-company-profile",
    "https://www.owler.com/iaApp/219185/modumetal-company-profile"
]


def retrive_profiles(browser):
    """
    Retrive Owler profiles
    :param browser: logged to Owler browser
    """
    url = "https://www.owler.com/iaApp/219185/modumetal-company-profile"


