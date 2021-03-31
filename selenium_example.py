from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from locators import locator
from csv import reader
from selenium.webdriver.support.ui import Select
import random

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)

driver.get("http://automationpractice.com/")
driver.maximize_window()

with open('data.csv') as csvfile:
    csvreader = reader(csvfile, delimiter=',')
    for row in csvreader:

        assert driver.find_element(*locator["sign_in_link"]).is_displayed()
        driver.find_element(*locator["sign_in_link"]).click()

        driver.find_element(*locator["email_field"]).send_keys(str(random.randint(0,1000000))+row[0])

        driver.find_element(*locator["create_account_button"]).click()

        assert driver.title == "Login - My Store"

        driver.find_element(*locator["gender_radiobutton"]).click()

        driver.find_element(*locator["firstname"]).send_keys(row[1])

        driver.find_element(*locator["lastname"]).send_keys(row[2])

        driver.find_element(*locator["password"]).send_keys(row[3])

        select = Select(driver.find_element(*locator["days_dropdown"]))
        select.select_by_value(row[4])

        select = Select(driver.find_element(*locator["months_dropdown"]))
        select.select_by_value(row[5])

        select = Select(driver.find_element(*locator["years_dropdown"]))
        select.select_by_value(row[6])

        driver.find_element(*locator["newsletter_checkbox"]).click()

        driver.find_element(*locator["optin_checkbox"]).click()

        driver.find_element(*locator["address"]).send_keys(row[7])

        driver.find_element(*locator["city"]).send_keys(row[8])

        select = Select(driver.find_element(*locator["state_dropdown"]))
        select.select_by_visible_text(row[9])

        driver.find_element(*locator["postcode"]).send_keys(row[10])

        driver.find_element(*locator["mobile"]).send_keys(row[11])

        driver.find_element(*locator["register_button"]).click()

        assert driver.title == "My account - My Store"

        driver.find_element(*locator["logout_button"]).click()
  
driver.quit()


























