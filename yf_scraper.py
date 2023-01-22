from myFunctions.functions import *
from selenium.webdriver import Chrome

# Main variables
# My url has some filters preselect
# So my starting state is US and all but small companies
# Please adjust if needed
URL = 'https://finance.yahoo.com/screener/unsaved/7a0cd242-0e7e-4051-aa98-af69b52795b2?offset=1&count=100'

DELAY = 1
FILTER_NAMES = ['Exchange', 'Sector']
DRIVER = Chrome()

# Min or Max the scraping window
# DRIVER.maximize_window()
# DRIVER.minimize_window()

# Load YF screener page
load_YF_screener(URL, DRIVER, DELAY)
# Add the filters
add_filter(FILTER_NAMES, DRIVER, DELAY)
# Get the option values for the filters
options = get_list_cats(FILTER_NAMES, DRIVER, DELAY)
# Loop through them and get the table info
stock_tickers_sectors = loop_filters(options, DRIVER, DELAY)
# Save output as csv
stock_tickers_sectors.to_csv('tickers_yf_test.csv', index=False)
