# Import packages
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


# Main variables
URL = 'https://finance.yahoo.com/screener/unsaved/7a0cd242-0e7e-4051-aa98-af69b52795b2?offset=1&count=100'
DELAY = 3
FILTER_NAMES = ['Exchange', 'Sector']
# Def main functions


def load_YF_screener(url):
    """
    INPUT: Yahoo Finance URL -> str
    Load yf main page and accept the cookie policy.
    """
    DRIVER.get(url)
    WebDriverWait(DRIVER, DELAY).until(
        EC.element_to_be_clickable((By.NAME, 'agree')))
    DRIVER.find_element(By.NAME, 'agree').click()


def add_filter(filter_names):
    """
    INPUT: Filter Names -> list(str)

    Load a filter to the screener menu.
    """
    DRIVER.implicitly_wait(DELAY)
    for filter in filter_names:
        DRIVER.find_element(
            By.XPATH, "//span[text()='Add another filter']").click()
        DRIVER.find_element(By.XPATH, f"//span[text()='{filter}']").click()
        DRIVER.find_element(By.XPATH, "//span[text()='Close']").click()
        DRIVER.find_element(By.XPATH, "//span[text()='Add ']").click()
        DRIVER.find_element(By.XPATH, "//button[@title='Close']").click()


def get_list_cats(filter_names):
    """
    INPUT: Filter names -> list(str)
    OUTPUT: Filter options -> dict 

    Scrape the options under the provided filter names
    and return a dictionary with filter names as keys
    and filter optoions as values.
    """
    filter_options = dict()

    for filter in filter_names:

        DRIVER.find_element(
            By.XPATH, f"//span[text()='{filter}']/ancestor::div[2]//div[@role='button']").click()
        time.sleep(DELAY)
        list_li = DRIVER.find_element(
            By.XPATH, "//input[@type ='checkbox']/ancestor::div[1]").find_elements(By.TAG_NAME, 'li')

        filter_options[filter] = [
            li.get_attribute('innerText') for li in list_li]

        DRIVER.find_element(By.XPATH, "//button[@title='Close']").click()

    # Refresh page - drops the filters
    DRIVER.refresh()
    # Wait
    time.sleep(DELAY)

    return filter_options


def get_page_contents(key, option):
    """
    INPUT: Target filter -> str
    OUTPUT: Scraped info -> df

    Scrape the page contents and returns a dataframe with
    the Ticker, Name and the provided targer filter.
    """
    symbols = [i.get_attribute('innerText') for i in DRIVER.find_elements(
        By.XPATH, "//a[@data-test ='quoteLink']")]
    names = [i.get_attribute('title') for i in DRIVER.find_elements(
        By.XPATH, "//a[@data-test ='quoteLink']")]

    df = pd.DataFrame(
        {'symbol': symbols, 'name': names, key: option}
    )

    return df


def select_filter_option(filter):
    """
    INPUT: Filter Option Name -> str

    Open the fiter menu and select the provided option.
    """
    # Open select tab
    DRIVER.find_element(By.XPATH, "//div//span[text()='Add ']").click()
    # Select sector
    DRIVER.find_element(By.XPATH, f"//label//span[text()='{filter}']").click()
    # Wait
    WebDriverWait(DRIVER, DELAY).until(
        EC.presence_of_element_located((By.XPATH, "//button[@title='Close']")))
    # Close the window
    DRIVER.find_element(
        By.XPATH, "//button[@title='Close']").click()
    # Wait
    time.sleep(DELAY)


def remove_filter_option(option, key):
    """
    INPUT: Filter Option Name -> str, Name of the filter -> str

    Open the fiter menu and deselect the provided option.
    """
    # Close Filter
    DRIVER.find_element(
        By.XPATH, f"//span[text()='{key}']/ancestor::div[2]//div[@role = 'button']").click()
    DRIVER.find_element(By.XPATH, f"//label//span[text()='{option}']").click()
    # Wait
    WebDriverWait(DRIVER, DELAY).until(
        EC.presence_of_element_located((By.XPATH, "//button[@title='Close']")))
    # Close the window
    DRIVER.find_element(
        By.XPATH, "//button[@title='Close']").click()


def remove_filter(key):
    """
    INPUT: Name of the filter -> str

    Drop filter menu.
    """
    # Close Filter
    DRIVER.find_element(
        By.XPATH, f"//button[@title='Remove {key}']").click()
    # Wait
    time.sleep(DELAY)


def click_find_stock():
    """
    Locate and click Find Stock button.
    Waits before and after the click,
    time needed to load the page.
    """
    # Wait
    time.sleep(DELAY)
    # Get stocks
    DRIVER.find_element(
        By.XPATH, "//button[@data-test='find-stock']").click()

    caution_present = len(DRIVER.find_elements(
        By.XPATH, "//span[text()='Screening Criteria has changed.']")) > 0

    # If the table dont show up first try keep clicking find stocks
    while caution_present:

        DRIVER.find_element(
            By.XPATH, "//button[@data-test='find-stock']").click()

        # DRIVER.refresh()

        time.sleep(DELAY**2)

        caution_present = len(DRIVER.find_elements(
            By.XPATH, "//span[text()='Screening Criteria has changed.']")) > 0


def loop_filters(options):
    """
    INPUT: Filter Options -> dict
    OUTPUT: Scraped Info -> df

    Taka a list of filter value and loops over them
    scraping the page contents. The output is a DataFrame
    with all the information from the relevant pages.
    """

    output_df = pd.DataFrame()

    for i, key in enumerate(options.keys()):

        add_filter([key])

        key_df = pd.DataFrame()

        for option in options[key]:

            # Select filter option
            select_filter_option(option)

            # Filter stocks
            click_find_stock()

            # If empty page or error
            # take next element
            try:
                # Scrape
                while DRIVER.find_element(By.XPATH, "//button[@aria-label='Jump to last page']").get_attribute('aria-disabled') == 'false':
                    option_df = get_page_contents(key, option)
                    key_df = pd.concat([key_df, option_df])
                    DRIVER.find_element(
                        By.XPATH, "//button//span[text()='Next']").click()
                    time.sleep(DELAY)

                # Get last page
                option_df = get_page_contents(key, option)
                key_df = pd.concat([key_df, option_df])

                # Refresh and Wait
                DRIVER.refresh()
                time.sleep(DELAY)

                # Remove filter option
                remove_filter_option(option, key)

            except:
                # Remove filter option and continue
                remove_filter_option(option, key)

                continue

        # Remove filter option and continue
        remove_filter(key)

        # First filter df
        if i == 0:
            output_df = key_df
        # Then join next key df
        else:
            output_df = output_df.merge(
                key_df, on=['symbol', 'name'], how='left')

    return output_df


# def select_100_rows():
#     """
#     Click show 100 rows at the bottom of the bage.
#     """
#     DRIVER.find_element(
#         By.XPATH, "//div[@data-test='select-container']").click()
#     DRIVER.find_element(By.XPATH, "//div[@data-value='100']").click()


DRIVER = webdriver.Chrome()
# DRIVER.maximize_window()
# DRIVER.minimize_window()
load_YF_screener(URL)
add_filter(FILTER_NAMES)
options = get_list_cats(FILTER_NAMES)
stock_tickers_sectors = loop_filters(options)
print(stock_tickers_sectors)
stock_tickers_sectors.to_csv('tickers_yf.csv', index=False)
