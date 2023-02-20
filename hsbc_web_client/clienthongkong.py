import os
import time

from hsbc_web_client.clientbase import HSBCwebClient
from hsbc_web_client.account import Account
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

class HSBCwebClientHK(HSBCwebClient):
    def __init__(self, *args, **kwargs):
        URL = 'https://www.hsbc.com.hk/ways-to-bank/internet'
        super().__init__(URL, *args, **kwargs)

    def logon(self, login=None, password=None):

        if login:
            self._login = login
        if password:
            self._password = password

        self._logger.info("stage LOGON")

        WebDriverWait(self._driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Log on')]"))).click()
        self._logger.debug("menu for log on is clickable")

        menu_item = WebDriverWait(self._driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Log on')]")))
        self._logger.debug("menu for log on is visible")

        ActionChains(self._driver).move_to_element(menu_item).perform()
        self._logger.debug("menu for log on is clicked")

        WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'HSBC Online Banking')]"))).click()
        self._logger.debug("menu item for log on is clicked")

        self._logger.info("stage IDENTIFICATION")

        WebDriverWait(self._driver, 15).until(EC.title_contains("Log on to Internet Banking: Username | HSBC"))
        self._logger.debug(f'loaded page: "{self._driver.title}"')

        element = WebDriverWait(self._driver, 30).until(EC.presence_of_element_located((By.ID, "Username1")))
        self._logger.debug("found element: Username1")

        element.send_keys(self._login)
        element.submit()
        self._logger.debug("user name submitted")

        self._logger.info("stage SECURITY")

        WebDriverWait(self._driver, 15).until(EC.title_contains(
            "| Log on | HSBC"))
        self._logger.debug(f'loaded page: "{self._driver.title}"')

        WebDriverWait(self._driver, 15).until(EC.presence_of_element_located((By.ID, "app-root")))
        self._logger.debug("found element: app-root")

        time.sleep(5)
        self._logger.debug("quick pause")

        if "Security code" in self._driver.title:
            actions = ActionChains(self._driver)
            actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            self._logger.debug("selected login with password")
            WebDriverWait(self._driver, 15).until(EC.title_contains("Password | Log on | HSBC"))
            self._logger.debug(f'loaded page: "{self._driver.title}"')

            WebDriverWait(self._driver, 30).until(EC.presence_of_element_located(
                (By.ID, "app-root")))
            self._logger.debug("found element: app-root")

        self._logger.info("stage AUTHENTICATION")

        time.sleep(2)
        self._logger.debug("quick pause")

        actions = ActionChains(self._driver)
        actions.send_keys(self._password)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        self._logger.debug("password submitted")
        self._logged_on = True

    def fetch(self):
        WebDriverWait(self._driver, 15).until(EC.title_contains("Homepage | HSBC"))
        time.sleep(10)
        self._logger.debug(f'loaded page: "{self._driver.title}"')
        self._logger.info("stage FETCHING")
        self._screenshot('accounts-hk.png')
#        self._print('accounts-hk.pdf')
        self._export('accounts-hk.csv')

    def _export(self, filename):
        elements = self._driver.find_elements("xpath", "//div[contains(@class, 'account-card-container')]")

        account = Account()

        with open(filename, 'w') as f:
            f.write('TITLE,NUMBER,BALANCE,CURRENCY\n')

            for element in elements:
                title = account.get_title(self, element)
                number = account.get_account_number(self, element)
                balance = account.get_balance(self, element)
                currency = account.get_currency(self, element)

                f.write(f'{title},{number},{balance},{currency}\n')

        self._logger.debug("exported as HTML tags")

    def get_account_info(self):
        WebDriverWait(self._driver, 15).until(
            EC.title_contains("Homepage | HSBC"))
        time.sleep(10)

        elements = self._driver.find_elements(
            "xpath", "//div[contains(@class, 'account-card-container')]")

        for element in elements:
            account = Account()

            account.title = account.get_title(self, element)
            account.number = account.get_account_number(self, element)
            account.balance = account.get_balance(self, element)
            account.currency = account.get_currency(self, element)
            self.accounts.append(account)

    def logoff(self):
        self._logger.info("stage LOGOFF")

        element = self._driver.find_element(
            "xpath",
            "//button[contains(@class, 'cpi-masthead-logoff__button')]")

        if element.get_attribute("innerHTML") == "Log off":
            element.click()
            self._logger.debug("log off")
        else:
            raise RuntimeError("found unexpected element")

        WebDriverWait(self._driver, 15).until(
            EC.title_contains("Log-off Page - HSBC HK"))
        self._logger.debug(f'loaded page: "{self._driver.title}"')

