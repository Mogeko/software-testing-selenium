from selenium import webdriver
# from webdriver_manager.firefox import GeckoDriverManager
from locators import locator
from searchData import product
from csv import reader, writer
from selenium.webdriver.support.ui import Select
import unittest
import random
import time


WEBSITE = "http://automationpractice.com/"


class Automation_Test(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Firefox(GeckoDriverManager().install())
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.get(WEBSITE)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_create_account(self):
        def create_account(row: list):
            account_email   = str(random.randint(0, 1000000))+row[0]
            account_passswd = row[3]
            assert self.driver.find_element(
                *locator["sign_in_link"]).is_displayed()
            self.driver.find_element(*locator["sign_in_link"]).click()
            self.driver.find_element(*locator["email_field"]).send_keys(account_email)
            self.driver.find_element(*locator["create_account_button"]).click()
            assert self.driver.title == "Login - My Store"
            self.driver.find_element(*locator["gender_radiobutton"]).click()
            self.driver.find_element(*locator["firstname"]).send_keys(row[1])
            self.driver.find_element(*locator["lastname"]).send_keys(row[2])
            self.driver.find_element(*locator["password"]).send_keys(account_passswd)
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
            return [account_email, account_passswd]

        with open("registrationData.csv", "r") as csvfile_1:
            with open("loginData.csv", "w", newline="") as csvfile_2:
                writer(csvfile_2).writerows(
                    map(create_account, reader(csvfile_1, delimiter=","))
                )

    def test_search_product(self):
        for item in product:
            self.driver.find_element(*locator["search"]).clear()
            self.driver.find_element(*locator["search"]).send_keys(item)
            self.driver.find_element(*locator["search_botton"]).click()
            assert self.driver.title == "Search - My Store"
            time.sleep(3)

    def test_login_with_correct_credentials(self):
        with open("loginData.csv", "r") as csvfile:
            for row in reader(csvfile, delimiter=","):
                assert self.driver.find_element(
                    *locator["sign_in_link"]).is_displayed()
                self.driver.find_element(*locator["sign_in_link"]).click()
                assert self.driver.title == "Login - My Store"
                self.driver.find_element(*locator["email"]).send_keys(row[0])
                self.driver.find_element(*locator["password"]).send_keys(row[1])
                self.driver.find_element(*locator["login_button"]).click()
                self.driver.find_element(*locator["logout_button"]).click()

    def test_login_with_incorrect_credentials(self):
        for _ in range(3):
            random_email  = str(random.randint(0, 1000000))+"@email.com"
            random_passwd = str(random.randint(100000, 1000000000))
            assert self.driver.find_element(
                *locator["sign_in_link"]).is_displayed()
            self.driver.find_element(*locator["sign_in_link"]).click()
            assert self.driver.title == "Login - My Store"
            self.driver.find_element(*locator["email"]).send_keys(random_email)
            self.driver.find_element(*locator["password"]).send_keys(random_passwd)
            self.driver.find_element(*locator["login_button"]).click()
            self.driver.find_element(*locator["login_error_message"]).text == "Authentication failed."


if __name__ == '__main__':
    unittest.main()
