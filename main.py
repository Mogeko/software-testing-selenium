from selenium import webdriver
# from webdriver_manager.firefox import GeckoDriverManager
from locators import locator
from searchData import product
from csv import reader
from selenium.webdriver.support.ui import Select
import unittest
import random
import time

class Automation_Test(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Firefox(GeckoDriverManager().install())
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.get("http://automationpractice.com/")
        self.driver.maximize_window()
        with open('accountData.csv') as csvfile:
            self.csvreader = list(reader(csvfile, delimiter=','))

    def tearDown(self):
        self.driver.quit()

    def test_create_account(self):
        for row in self.csvreader:
            assert self.driver.find_element(
                *locator["sign_in_link"]).is_displayed()
            self.driver.find_element(*locator["sign_in_link"]).click()
            self.driver.find_element(
                *locator["email_field"]).send_keys(str(random.randint(0, 1000000))+row[0])
            self.driver.find_element(*locator["create_account_button"]).click()
            assert self.driver.title == "Login - My Store"
            self.driver.find_element(*locator["gender_radiobutton"]).click()
            self.driver.find_element(*locator["firstname"]).send_keys(row[1])
            self.driver.find_element(*locator["lastname"]).send_keys(row[2])
            self.driver.find_element(*locator["password"]).send_keys(row[3])
            select = Select(self.driver.find_element(
                *locator["days_dropdown"]))
            select.select_by_value(row[4])
            select = Select(self.driver.find_element(
                *locator["months_dropdown"]))
            select.select_by_value(row[5])
            select = Select(self.driver.find_element(
                *locator["years_dropdown"]))
            select.select_by_value(row[6])
            self.driver.find_element(*locator["newsletter_checkbox"]).click()
            self.driver.find_element(*locator["optin_checkbox"]).click()
            self.driver.find_element(*locator["address"]).send_keys(row[7])
            self.driver.find_element(*locator["city"]).send_keys(row[8])
            select = Select(self.driver.find_element(
                *locator["state_dropdown"]))
            select.select_by_visible_text(row[9])
            self.driver.find_element(*locator["postcode"]).send_keys(row[10])
            self.driver.find_element(*locator["mobile"]).send_keys(row[11])
            self.driver.find_element(*locator["register_button"]).click()
            assert self.driver.title == "My account - My Store"
            self.driver.find_element(*locator["logout_button"]).click()


    def test_search_product(self):
        for item in product:
            self.driver.find_element(*locator["search"]).clear()
            self.driver.find_element(*locator["search"]).send_keys(item)
            self.driver.find_element(*locator["search_botton"]).click()
            assert self.driver.title == "Search - My Store"
            time.sleep(3)


if __name__ == '__main__':
    unittest.main()
