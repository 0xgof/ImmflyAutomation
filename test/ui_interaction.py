import configparser
import logging
import os
import sys
import time

import psutil
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import test.test_utils as test_utils

# Read the configuration files from root directory
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'settings.ini'))

# Get configuration variables
BROWSER_TYPE = config.get('BROWSERS', 'BROWSER_TYPE')
URL = 'https://highlifeshop.com/speedbird-cafe'

class BrowserManager:
    def __init__(self):
        assert isinstance(BROWSER_TYPE, str), "BROWSER_TYPE should be a string"
        self.browser_type = BROWSER_TYPE
        self.driver = None

    def initialize_ui(self):
        """
        Launches a Chrome browser with Selenium and navigates to the selected page URL.
        If a Chrome process is already running, it will terminate it before starting a new one.

        :return: The Selenium driver
        """
        if self.browser_type == 'chrome':
            logging.info('Terminating existing Chrome process')
            # Terminate all Chrome processes
            for process in psutil.process_iter():
                if process.name() == 'chrome.exe':
                    process.terminate()
                    time.sleep(1)

            # Set up the Selenium driver
            options = Options()
            options.add_argument("--display=:0.1")  # Replace this with the display number you want to use
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

            # Navigate to the URL
            logging.info(f'Navigating to: {URL}')
            driver.get(URL)

        # Remove the Cookies pop up
        for _ in range(5):
            time.sleep(1)
            try:
                element = driver.find_element(by=By.XPATH, value="/html/body/aside/div/form/div[2]/div[2]/button[2]")
                element.click()
                break
            except NoSuchElementException:
                pass
        self.driver = driver

    def sort_products(self, sort_option):
        """
        Sorts the products on the page by the specified option.

        :param sort_option: A string representing the option to sort by. Must be one of:
                            - 'position'
                            - 'name'
                            - 'price'
                            - 'new_arrivals'
        """
        assert isinstance(sort_option, str), "sort_option should be a string"
        assert sort_option in ['position', 'name', 'price', 'new_arrivals'], "sort_option should be one of 'position', 'name', 'price', or 'new_arrivals'"

        for _ in range(5):
            time.sleep(3)
            try:
                sorter_dropdown = self.driver.find_element(By.XPATH, "//*[@id='sorter']")
                sorter_dropdown.click()
                time.sleep(3)
                sorter_select = Select(sorter_dropdown)          
                # Select the desired option by visible text
                if sort_option == 'position':
                    logging.info('Sorting by position')
                    sorter_select.select_by_visible_text("Position")
                elif sort_option == 'name':
                    logging.info('Sorting by name')
                    sorter_select.select_by_visible_text("Product Name")
                elif sort_option == 'price':
                    logging.info('Sorting by price')
                    sorter_select.select_by_visible_text("Price")
                elif sort_option == 'new_arrivals':
                    logging.info('Sorting by new arrivals')
                    sorter_select.select_by_visible_text("New Arrivals")
                break
            except ElementClickInterceptedException:
                pass

    def get_products_order_state(self) -> str:
        logging.info('Getting products direction sorting')
        sorter_element = self.driver.find_element(By.CSS_SELECTOR,'a.action:nth-child(3)')
        if sorter_element.get_attribute("data-value") == 'asc':
            return 'desc'
        elif sorter_element.get_attribute("data-value") == 'desc':
            return 'asc'

    def products_direction_switch(self):
        logging.info('Switching products direction sorting')
        sorter_element = self.driver.find_element(By.CSS_SELECTOR,'a.action:nth-child(3)')
        sorter_element.click()

    def get_first_product_name(self) -> str:
        logging.info('Extracting first product name')
        first_product = self.driver.find_element(By.CSS_SELECTOR,'ol.products:nth-child(1) > li:nth-child(1) > div:nth-child(1) > div:nth-child(2) > strong:nth-child(1) > a:nth-child(1)')
        first_product_link = first_product.get_attribute("href")
        first_product_name = test_utils.parse_product_url(first_product_link)
        return first_product_name
    
    
    def get_second_product_name(self) -> str:
        logging.info('Extracting second product name')
        first_product = self.driver.find_element(By.CSS_SELECTOR,'ol.products:nth-child(1) > li:nth-child(2) > div:nth-child(1) > div:nth-child(2) > strong:nth-child(1) > a:nth-child(1)')
        first_product_link = first_product.get_attribute("href")
        first_product_name = test_utils.parse_product_url(first_product_link)
        return first_product_name
 



