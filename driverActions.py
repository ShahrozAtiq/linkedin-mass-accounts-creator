from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


import random
from time import sleep


def create_driver():
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values': {'images': 2,
                                                        'geolocation': 2,
                                                        'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                                        'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                        'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                                                        'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                                                        'durable_storage': 2}}
    options.add_experimental_option('prefs', prefs)
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_extension('meta.xpi')
    driver = webdriver.Chrome(
        executable_path='chromedriver.exe', options=options)
    return driver


class DriverActions():
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def random_wait(low, high):
        time_wait = random.uniform(low, high)
        sleep(time_wait)

    def get_el(self, xpath, wait=30):
        element = WebDriverWait(self.driver, wait).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        return element

    def click(self, xpath, wait=30):
        element = WebDriverWait(self.driver, wait).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()

    def human_typer(self, xpath, text: str, wait=30):
        element = WebDriverWait(self.driver, wait).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        for key in text:
            element.send_keys(key)
            self.random_wait(0.05, 0.5)

    def js_click(self, xpath, wait=30):
        element = WebDriverWait(self.driver, wait).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].click();", element)

    def select_by_value(self, xpath, value, wait=30):
        element = WebDriverWait(self.driver, wait).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        select = Select(element)
        select.select_by_value(value)
        return True

    def wait_until_new_tab_open(self, prev_tabs, wait=30):
        return WebDriverWait(self.driver, wait).until(lambda driver: len(prev_tabs) != len(self.driver.window_handles))

    def wait_until(self, func, wait=30):
        WebDriverWait(self.driver, wait).until(func)

    def set_attr(self, xpath, value, attr='value', wait=30):
        WebDriverWait(self.driver, wait).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        script = """
            (() => {
                let element = document.evaluate('{xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
                element.{attr} = '{value}'
            })()
        """.format(xpath=xpath, attr=attr, value=value)
        self.driver.execute_script(script)
        return True

    def send_keys_js(self, xpath, value, wait=30):
        element = WebDriverWait(self.driver, wait).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.execute_script(f"arguments[0].value = '{value}';", element)

    def send_keys(self, xpath, value, wait=30):
        element = WebDriverWait(self.driver, wait).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        element.clear()
        element.send_keys(value)

    def switch_to_window(self, window=-1):
        self.driver.switch_to.window(self.driver.window_handles[window])

    def wait_until_element_non_empty(self, xpath, wait=30):
        WebDriverWait(self.driver, 15).until(
            lambda x: self.get_el(xpath).get_attribute('value') != ''
        )
        return True
    # def force_click(self, xpath, max_try=5, wait=5):
    #     for _ in range(max_try):
    #         element = WebDriverWait(self.driver, wait).until(
    #             EC.presence_of_element_located((By.XPATH, xpath)))
    #         element.click()
