from myFunctions.functions import *
from selenium.webdriver import Chrome

# Main variables
# My url has some filters preselect
# So my starting state is US and all but small companies
# Please adjust if needed
URL = 'https://finance.yahoo.com/screener/unsaved/5153afcc-304f-4656-8438-a91158d94c86'

DELAY = 1
FILTER_NAMES = ['Sector']
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
stock_tickers_sectors.to_csv('tickers_yf_test_202304.csv', index=False)
