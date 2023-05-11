from myFunctions.functions import *
from selenium.webdriver import Chrome

# Main variables
# My url has some filters preselect
# So my starting state is US and all but small companies
# Please adjust if needed
URL = 'https://finance.yahoo.com/screener/equity/new'

DELAY = 1
CLASS_FILTER_NAMES = ['Sector', 'Industry']
VALUE_FILTER_NAME = 'Avg Vol (3 month)'
VALUE = 1000000
DRIVER = Chrome()

# Min or Max the scraping window
# DRIVER.maximize_window()
# DRIVER.minimize_window()

# Load YF screener page
load_YF_screener(URL, DRIVER, DELAY)
# Add the filters
add_class_filter(CLASS_FILTER_NAMES, DRIVER, DELAY)
add_value_filter(VALUE_FILTER_NAME, DRIVER, DELAY, VALUE)
# Get the option values for the filters
sectors = get_list_cats(CLASS_FILTER_NAMES, DRIVER, DELAY)
# Loop through them and get the table info
stock_tickers_sectors = loop_filters(sectors, DRIVER, DELAY, VALUE_FILTER_NAME, VALUE)
# Save output as csv
stock_tickers_sectors.to_csv('tickers_yf_test_202305.csv', index=False)
