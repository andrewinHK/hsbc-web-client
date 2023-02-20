from datetime import datetime

from hsbc_web_client.clientbase import HSBCwebClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait

class Property(HSBCwebClient):
    def __init__(self, client, url, zone, district, estate, block,
                 floor, flat, label, mortgage=None):
        super().__init__(url)

        self._url = url
        self._zone = zone
        self._district = district
        self._estate = estate
        self._block = block
        self._floor = floor
        self._flat = flat
        self._mortgage = mortgage
        self.label = label
        self.valuation = 0.0
        self.address = None
        self.gross = 0
        self.saleable = 0
        self.age = None
        self.valuation_date = None

    def open_valuation(self, client):
        self._logger.info(f'page to be open: <{self._url}>')
        self._driver.get(self._url)
        self._logger.debug("web page is open")

    def _choose_item(self, parent, menu, value):
        element = wait(self._driver, 5).until(EC.element_to_be_clickable((
            By.ID, parent)))
        element.click()
        self._logger.debug("Clicked on %s", parent)

        element = wait(self._driver, 5).until(EC.presence_of_element_located((
            By.ID, menu)))
        self._logger.debug("Found %s", menu)

        item = ".//*[contains(text(), '%s')]" % value
        element.find_element("xpath", item).click()
        self._logger.info("Selected %s", value)
    def get_valuation(self, client):
        self._logger.info("Selecting Zone")
        self._choose_item("tools_form_1_selectized", "tools_form_1_menu",
                          self._zone)
        self._logger.info("Selecting District")
        self._choose_item("tools_form_2_selectized", "tools_form_2_menu",
                          self._district)
        self._logger.info("Selecting Estate")
        self._choose_item("tools_form_3_selectized", "tools_form_3_menu",
                          self._estate)
        if self._block:
            self._logger.info("Selecting Block/Building")
            self._choose_item("tools_form_4_selectized", "tools_form_4_menu",
                              self._block)
        if self._floor:
            self._logger.info("Selecting Floor")
            self._choose_item("tools_form_5_selectized", "tools_form_5_menu",
                              self._floor)
        if self._flat:
            self._logger.info("Selecting Flat")
            self._choose_item("tools_form_6_selectized", "tools_form_6_menu",
                              self._flat)

        self._logger.info("Getting valuation")
        element = wait(self._driver, 5).until(EC.element_to_be_clickable((
            By.CLASS_NAME, "A-BTNP-RW-ALL.search-button")))
        element.click()
        self.parse_results()

    def parse_results(self):
        element = wait(self._driver, 10).until(EC.presence_of_element_located((
            By.CLASS_NAME, "sm-12.md-12.lg-6.results")))
        details = element.text.split('\n')
        self.address = details[2].split(':')[1]
        self._logger.info("Address: %s", self.address)
        self.valuation = float(details[4].replace(',', ''))
        self._logger.info("Valuation: %s", details[4])
        self.gross = details[6]
        self._logger.info("Gross: %s", details[6])
        self.saleable = float(details[8].replace(',', ''))
        self._logger.info("Address: %s", self.address)
        self.age = int(details[10])
        self._logger.info("Address: %s", self.address)
        self.valuation_date = datetime.strptime(details[12], '%d %b %Y')
        self._logger.info("Address: %s", self.address)



