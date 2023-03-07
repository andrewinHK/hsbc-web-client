import time
from datetime import datetime

from hsbc_web_client.clientbase import HSBCwebClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait

class Property:
    def __init__(self, client, url, zone, district, estate, block,
                 floor, flat, label, mortgage=None):

        self.logger = client._logger
        self.driver = None      # assign after client is launched
        self.url = url
        self.zone = zone
        self.district = district
        self.estate = estate
        self.block = block
        self.floor = floor
        self.flat = flat
        self.mortgage = mortgage
        self.label = label
        self.valuation = 0.0
        self.address = None
        self.gross = 0
        self.saleable = 0
        self.age = None
        self.valuation_date = None

    def open_valuation(self, client):
        self.logger.info('page to be open: <{self.url}>')
        self.driver.get(self.url)
        time.sleep(10)
        self.logger.debug("web page is open")

    def _choose_item(self, parent, menu, value):
        time.sleep(5)
        element = wait(self.driver, 10).until(EC.element_to_be_clickable((
            By.ID, parent)))
        element.click()
        self.logger.debug("Clicked on %s", parent)

        element = wait(self.driver, 10).until(EC.presence_of_element_located((
            By.ID, menu)))
        self.logger.debug("Found %s", menu)

        item = ".//*[contains(text(), '%s')]" % value
        element.find_element("xpath", item).click()
        self.logger.info("Selected %s", value)
    def get_valuation(self, client):
        self.logger.info("Selecting Zone")
        self._choose_item("tools_form_1_selectized", "tools_form_1_menu",
                          self.zone)
        self.logger.info("Selecting District")
        self._choose_item("tools_form_2_selectized", "tools_form_2_menu",
                          self.district)
        self.logger.info("Selecting Estate")
        self._choose_item("tools_form_3_selectized", "tools_form_3_menu",
                          self.estate)
        if self.block:
            self.logger.info("Selecting Block/Building")
            self._choose_item("tools_form_4_selectized", "tools_form_4_menu",
                              self.block)
        if self.floor:
            self.logger.info("Selecting Floor")
            self._choose_item("tools_form_5_selectized", "tools_form_5_menu",
                              self.floor)
        if self.flat:
            self.logger.info("Selecting Flat")
            self._choose_item("tools_form_6_selectized", "tools_form_6_menu",
                              self.flat)

        self.logger.info("Getting valuation")
        element = wait(self.driver, 5).until(EC.element_to_be_clickable((
            By.CLASS_NAME, "A-BTNP-RW-ALL.search-button")))
        element.click()
        self.parse_results()

    def parse_results(self):
        time.sleep(2)
        element = wait(self.driver, 10).until(EC.presence_of_element_located((
            By.CLASS_NAME, "sm-12.md-12.lg-6.results")))
        details = element.text.split('\n')
        self.address = details[2].split(':')[1]
        self.logger.info("Address: %s", self.address)
        self.valuation = float(details[4].replace(',', ''))
        self.logger.info("Valuation: %s", details[4])
        self.gross = details[6]
        self.logger.info("Gross: %s", details[6])
        self.saleable = details[8]
        self.logger.info("Saleable: %s", details[8])
        self.age = int(details[10])
        self.logger.info("Age (in years): %s", details[10])
        self.valuation_date = datetime.strptime(details[12], '%d %b %Y')
        self.logger.info("Valuation Date: %s", self.valuation_date)



