
from selenium.common.exceptions import NoSuchElementException
import math

class Account:
    def __init__(self):
        self.title = None
        self.number = ""
        self.balance = 0
        self.currency = ""

    def get_title(self, client, element):
        subelement = element.find_element(
            "xpath", ".//*[contains(@class, 'account-title')]")
        title = subelement.get_attribute("innerText")
        client.elements = subelement
        client._logger.info(f'account title: {title}')
        return title

    def get_account_number(self, client, element):
        try:
            subelement = element.find_element(
                "xpath", ".//*[contains(@class, 'account-number')]")
            number = subelement.get_attribute(
                "innerText").split('\n')[0].replace('Account number ', '')
            client._logger.info(f'account number: {number}')
        except NoSuchElementException:
            client._logger.info("No account number on this account")
            number = ""

        return number

    def get_balance(self, client, element):
        try:
            subelement = element.find_element(
                "xpath", ".//*[contains(@class, 'amount-balance')]")
            balance = subelement.get_attribute(
                "innerText").replace('Balance\n', '').replace(',', '')

            client._logger.info(f'account balance: {balance}')
        except NoSuchElementException:
            client._logger.info(f'No balance found for this account')
            balance = math.nan
        balance = float(balance)
        return balance

    def get_currency(self, client, element):
        try:
            subelement = element.find_element(
                "xpath", ".//*[contains(@class, 'amount-currency')]")
            currency = subelement.get_attribute("innerText")
            client._logger.info(f'account currency: {currency}')
        except NoSuchElementException:
            client._logger.info(f'No currency found for this account')
            currency = ""

        return currency


