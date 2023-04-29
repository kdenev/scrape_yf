# Import packages
import time
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# List
from typing import List


# Scraping functions
"""
Driver and delay are inputs for all functions,
apart from get_page_contents. It takes driver only.
"""


def load_YF_screener(url: str, driver: Chrome, delay: int):
    """
    INPUT: Yahoo Finance URL -> str
    Load yf main page and accept the cookie policy.
    """
    driver.get(url)
    WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.NAME, 'agree')))
    driver.find_element(By.NAME, 'agree').click()


def add_filter(filter_names: List[str], driver: Chrome, delay: int):
    """
    INPUT: Filter Names -> list(str)

    Load a filter to the screener menu.
    """
    driver.implicitly_wait(delay)
    for filter in filter_names:
        driver.find_element(
            By.XPATH, "//span[text()='Add another filter']").click()
        driver.find_element(By.XPATH, f"//span[text()='{filter}']").click()
        driver.find_element(By.XPATH, "//span[text()='Close']").click()
        driver.find_element(By.XPATH, "//span[text()='Add ']").click()
        driver.find_element(By.XPATH, "//button[@title='Close']").click()


def get_list_cats(filter_names: List[str], driver: Chrome, delay: int):
    """
    INPUT: Filter names -> list(str)
    OUTPUT: Filter options -> dict 

    Scrape the options under the provided filter names
    and return a dictionary with filter names as keys
    and filter optoions as values.
    """
    filter_options = dict()

    for filter in filter_names:

        driver.find_element(
            By.XPATH, f"//span[text()='{filter}']/ancestor::div[2]//div[@role='button']").click()
        time.sleep(delay)
        list_li = driver.find_element(
            By.XPATH, "//input[@type ='checkbox']/ancestor::div[1]").find_elements(By.TAG_NAME, 'li')

        filter_options[filter] = [
            li.get_attribute('innerText') for li in list_li]

        driver.find_element(By.XPATH, "//button[@title='Close']").click()

    # Refresh page - drops the filters
    driver.refresh()
    # Wait
    time.sleep(delay)

    return filter_options


def get_page_contents(key: str, option: str, driver: Chrome):
    """
    INPUT: Target filter -> str
    OUTPUT: Scraped info -> df

    Scrape the page contents and returns a dataframe with
    the Ticker, Name and the provided targer filter.
    """
    symbols = [i.get_attribute('innerText') for i in driver.find_elements(
        By.XPATH, "//a[@data-test ='quoteLink']")]
    names = [i.get_attribute('title') for i in driver.find_elements(
        By.XPATH, "//a[@data-test ='quoteLink']")]

    df = pd.DataFrame(
        {'symbol': symbols, 'name': names, key: option}
    )

    return df


def select_filter_option(filter: str, driver: Chrome, delay: int):
    """
    INPUT: Filter Option Name -> str

    Open the fiter menu and select the provided option.
    """
    # Open select tab
    driver.find_element(By.XPATH, "//div//span[text()='Add ']").click()
    # Select sector
    driver.find_element(By.XPATH, f"//label//span[text()='{filter}']").click()
    # Wait
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, "//button[@title='Close']")))
    # Close the window
    driver.find_element(
        By.XPATH, "//button[@title='Close']").click()
    # Wait
    time.sleep(delay)


def remove_filter_option(option: str, key: str, driver: Chrome, delay: int):
    """
    INPUT: Filter Option Name -> str, Name of the filter -> str

    Open the fiter menu and deselect the provided option.
    """
    # Close Filter
    driver.find_element(
        By.XPATH, f"//span[text()='{key}']/ancestor::div[2]//div[@role = 'button']").click()
    driver.find_element(By.XPATH, f"//label//span[text()='{option}']").click()
    # Wait
    WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, "//button[@title='Close']")))
    # Close the window
    driver.find_element(
        By.XPATH, "//button[@title='Close']").click()


def remove_filter(key: str, driver: Chrome, delay: int):
    """
    INPUT: Name of the filter -> str

    Drop filter menu.
    """
    # Close Filter
    driver.find_element(
        By.XPATH, f"//button[@title='Remove {key}']").click()
    # Wait
    time.sleep(delay)


def click_find_stock(driver: Chrome, delay: int):
    """
    Locate and click Find Stock button.
    Waits before and after the click,
    time needed to load the page.
    """
    # Wait
    time.sleep(delay)
    # Get stocks
    driver.find_element(
        By.XPATH, "//button[@data-test='find-stock']").click()

    caution_present = len(driver.find_elements(
        By.XPATH, "//span[text()='Screening Criteria has changed.']")) > 0

    # If the table dont show up first try keep clicking find stocks
    while caution_present:

        driver.find_element(
            By.XPATH, "//button[@data-test='find-stock']").click()

        time.sleep(delay)

        caution_present = len(driver.find_elements(
            By.XPATH, "//span[text()='Screening Criteria has changed.']")) > 0


def loop_filters(options: dict, driver: Chrome, delay: int):
    """
    INPUT: Filter Options -> dict
    OUTPUT: Scraped Info -> df

    Taka a list of filter value and loops over them
    scraping the page contents. The output is a DataFrame
    with all the information from the relevant pages.
    """

    output_df = pd.DataFrame()

    for i, key in enumerate(options.keys()):

        add_filter([key], driver, delay)

        key_df = pd.DataFrame()

        for option in options[key]:

            # Select filter option
            select_filter_option(option, driver, delay)

            # Filter stocks
            click_find_stock(driver, delay)

            # If empty page or error
            # take next element
            try:
                # Scrape
                while driver.find_element(By.XPATH, "//button[@aria-label='Jump to last page']").get_attribute('aria-disabled') == 'false':
                    option_df = get_page_contents(key, option, driver)
                    key_df = pd.concat([key_df, option_df])
                    driver.find_element(
                        By.XPATH, "//button//span[text()='Next']").click()
                    time.sleep(delay)

                # Get last page
                option_df = get_page_contents(key, option, driver)
                key_df = pd.concat([key_df, option_df])

                # Refresh and Wait
                driver.refresh()
                time.sleep(delay)

                # Remove filter option
                remove_filter_option(option, key, driver, delay)

            except:
                # Remove filter option and continue
                remove_filter_option(option, key, driver, delay)

                continue

        # Remove filter option and continue
        remove_filter(key, driver, delay)

        # First filter df
        if i == 0:
            output_df = key_df
        # Then join next key df
        else:
            output_df = output_df.merge(
                key_df, on=['symbol', 'name'], how='left')
            
    # Close Chrome
    driver.close()
    return output_df


# def select_100_rows():
#     """
#     Click show 100 rows at the bottom of the bage.
#     """
#     DRIVER.find_element(
#         By.XPATH, "//div[@data-test='select-container']").click()
#     DRIVER.find_element(By.XPATH, "//div[@data-value='100']").click()
