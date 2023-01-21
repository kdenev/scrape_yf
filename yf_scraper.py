import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


URL = 'https://finance.yahoo.com/screener/unsaved/b511142a-77ad-4ab4-a8c1-925bd9d3a123?offset=0&count=100'
DRIVER = webdriver.Chrome()
DELAY = 3
# DRIVER.minimize_window()
DRIVER.maximize_window()


def load_YF_screener(url):
    DRIVER.get(url)
    WebDriverWait(DRIVER, DELAY).until(
        EC.element_to_be_clickable((By.NAME, 'agree')))
    DRIVER.find_element(By.NAME, 'agree').click()


def add_filter(filter_name):
    DRIVER.implicitly_wait(DELAY)
    DRIVER.find_element(
        By.XPATH, "//span[text()='Add another filter']").click()
    DRIVER.find_element(By.XPATH, f"//span[text()='{filter_name}']").click()
    DRIVER.find_element(By.XPATH, "//span[text()='Close']").click()
    DRIVER.find_element(By.XPATH, "//span[text()='Add ']").click()
    DRIVER.find_element(By.XPATH, "//button[@title='Close']").click()

# list_li = driver.find_element(By.XPATH,"//span[text()='Agricultural Inputs']/ancestor::div[1]").find_elements(By.TAG_NAME, 'li')


def get_list_cats():
    DRIVER.find_element(By.XPATH, "//span[text()='Add ']").click()
    DRIVER.implicitly_wait(DELAY)
    list_li = DRIVER.find_element(
        By.XPATH, "//input[@type ='checkbox']/ancestor::div[1]").find_elements(By.TAG_NAME, 'li')
    list_str = list()

    for l in list_li:
        list_str.append(l.get_attribute('innerText'))

    DRIVER.find_element(By.XPATH, "//button[@title='Close']").click()

    return list_str


def get_page_contents(s, i):
    symbols = [i.get_attribute('innerText') for i in DRIVER.find_elements(
        By.XPATH, "//a[@data-test ='quoteLink']")]
    names = [i.get_attribute('title') for i in DRIVER.find_elements(
        By.XPATH, "//a[@data-test ='quoteLink']")]

    df = pd.DataFrame(
        {'symbol': symbols, 'names': names, 'sector': s, 'industry': i}
    )

    return df


def loop_sectors(sectors):
    output_df = pd.DataFrame()
    for s in sectors:

        # Open select tab
        DRIVER.find_element(By.XPATH, "//span[text()='Add ']").click()

        # Select sector
        DRIVER.find_element(By.XPATH, f"//span[text()='{s}']").click()
        # Wait
        WebDriverWait(DRIVER, DELAY).until(
            EC.presence_of_element_located((By.XPATH, "//button[@title='Close']")))
        # Close the window
        DRIVER.find_element(
            By.XPATH, "//button[@title='Close']").click()

        # Wait
        time.sleep(DELAY)
        
        # Get Industires
        industries = get_list_cats()

        for i in industries:
            # Open select tab
            DRIVER.find_element(By.XPATH, "//span[text()='Add ']").click()
            # Select Industry
            DRIVER.find_element(By.XPATH, f"//span[text()='{i}']").click()
            # Wait
            WebDriverWait(DRIVER, DELAY).until(
                EC.presence_of_element_located((By.XPATH, "//button[@title='Close']")))
            # Close the window
            DRIVER.find_element(
                By.XPATH, "//button[@title='Close']").click()
            # Wait
            WebDriverWait(DRIVER, DELAY).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-test='find-stock']")))
            # Wait
            time.sleep(DELAY)
            # Get stocks
            DRIVER.find_element(
                By.XPATH, "//button[@data-test='find-stock']").click()
            # If the table dont show up first try keep clicking find stocks
            while EC.presence_of_element_located((By.XPATH, "//svg[@data-icon='attention']")):
                time.sleep(DELAY)
                DRIVER.find_element(
                    By.XPATH, "//button[@data-test='find-stock']").click()
                if EC.presence_of_element_located((By.XPATH, "//th[text()='Name']")):
                    break
            # Wait
            time.sleep(DELAY)
            # Scrape
            while DRIVER.find_element(By.XPATH, "//button[@aria-label='Jump to last page']").get_attribute('aria-disabled') == 'false':
                df = get_page_contents(s, i)
                output_df = pd.concat([output_df, df])
                DRIVER.find_element(
                    By.XPATH, "//button//span[text()='Next']").click()
                time.sleep(DELAY)

            # Get last page
            df = get_page_contents(s,i)
            output_df = pd.concat([output_df, df])
            ########

            # Close Industry
            DRIVER.find_element(
                By.XPATH, f"//button//span[text()='{i}']").click()

        # Close sector
        DRIVER.find_element(By.XPATH, f"//button//span[text()='{s}']").click()

    return output_df


load_YF_screener(URL)
add_filter('Sector')
sectors = get_list_cats()
print(sectors)
stock_tickers_sectors = loop_sectors(sectors)
print(stock_tickers_sectors)
stock_tickers_sectors.to_csv('tickers_yf.csv', index=False)

# while DRIVER.find_element(By.XPATH, "//button[@aria-label='Jump to last page']").get_attribute('aria-disabled') == 'false':
#     # Get all the symbols
#     DRIVER.find_element(
#         By.XPATH, "//a[@data-test ='quoteLink']").get_attribute('innerText')
#     # Get all the names
#     DRIVER.find_element(
#         By.XPATH, "//a[@data-test ='quoteLink']").get_attribute('title')
#     DRIVER.find_element(By.XPATH, "//button//span[text()='Next']").click()
#     break

# Get all the sectors
# driver.find_element(By.XPATH,"//span[text()='Basic Materials']").click()
# driver.find_element(By.XPATH,"//button[@data-test='find-stock']").click()

# # Get all industries
# driver.find_element(By.XPATH,"//span[text()='Agricultural Inputs']").click()

# driver.find_element(By.XPATH,"//span[text()='Add ']").click()


# cats = driver.find_element(By.XPATH, "//div[@data-test='filter-menu']").find_elements(By.TAG_NAME, 'h2')

# Scrape options
# for c in cats:
#     print(c.get_attribute('innerText'))
#     spans = c.find_element(By.XPATH, '//h2/parent::div[1]/div').find_elements(By.TAG_NAME, 'Span')

#     for s in spans:
#         print(s.get_attribute('innerText'))
