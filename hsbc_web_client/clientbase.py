import argparse
import getpass
import logging
import os
import selenium
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


class HSBCwebClient:
    def __init__(self, url, login=None, password=None):
        self._url = url
        self._login = login
        self._password = password
        self._logged_on = False
        self._logger = logging.getLogger('hsbc-web-client')
        self.elements = []
        self.accounts = []
        self.properties = []

    def launch(self, *, verbose=True, gui=True, maximized=True):
        if verbose:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)

        options = Options()
        options.set_preference("print.always_print_silent", True)
        options.set_preference("print.printer_Mozilla_Save_to_PDF.print_to_file", True)
        options.set_preference("print_printer", "Mozilla Save to PDF")

        if gui:
            self._logger.info("the GUI will be displayed")
        else:
            self._logger.info("the GUI will not be displayed")
            options.add_argument("--headless")

        self._driver = selenium.webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        self._logger.info("the browser is launched")

        if maximized:
            self._driver.maximize_window()
            self._logger.debug("the browser window is now maximized")

    def open(self):
        self._logger.info(f'page to be open: <{self._url}>')
        self._driver.get(self._url)
        self._logger.debug("web page is open")

    def logon(self):
        raise NotImplemented("no generic logon: use derived classes instead")

    def fetch(self):
        raise NotImplemented("no generic fetch: use derived classes instead")

    def logoff(self):
        raise NotImplemented("no generic logoff: use derived classes instead")

    def quit(self):
        self._driver.quit()
        self._logger.info("the browser has exited")

    def _screenshot(self, filename):
        self._driver.save_screenshot(filename)
        self._logger.debug("exported as screenshot")

    def _print(self, filename):
        self._driver.execute_script("window.print();")
        while True:
            try:
                time.sleep(1)
                os.rename('mozilla.pdf', filename)
                self._logger.debug("exported as PDF")
                break
            except FileNotFoundError:
                pass

