import conf
import time

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
